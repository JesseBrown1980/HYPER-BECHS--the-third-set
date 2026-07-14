#!/usr/bin/env python3
"""Authoritative aggregate wrapper for the 50×28 recurrence run.

GitHub matrix jobs can fail in an upload/post-run surface after producing a complete
artifact. The aggregate must therefore be the final authority rather than blindly
inheriting every matrix job conclusion. This wrapper independently verifies every
returned measured cube from its model/payload and receipt, checks all 28 perspective
rows, then invokes the original aggregate. A missing or invalid artifact still makes
the aggregate fail.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import zstandard as zstd

import aggregate_cube_recurrence as aggregate


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expand(tokens: list[int], start_id: int, rules: list[list[int]]) -> list[int]:
    out: list[int] = []
    stack = list(reversed(tokens))
    limit = start_id + len(rules)
    while stack:
        token = int(stack.pop())
        if start_id <= token < limit:
            left, right = rules[token - start_id]
            stack.append(int(right))
            stack.append(int(left))
        else:
            out.append(token)
    return out


def verify_base_artifact(directory: Path, result: dict[str, Any]) -> dict[str, Any]:
    model_path = directory / "base-cube.model.json"
    payload_path = directory / "base-cube.payload.zst"
    if not model_path.exists() or not payload_path.exists():
        raise AssertionError(f"missing base artifact: {directory}")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    payload = payload_path.read_bytes()
    if sha256(payload) != model["payload_sha256"]:
        raise AssertionError(f"payload digest mismatch: {directory}")
    token_count = int(model["token_count"])
    raw = zstd.ZstdDecompressor().decompress(payload, max_output_size=token_count * 2)
    if len(raw) != token_count * 2:
        raise AssertionError(f"token length mismatch: {directory}")
    tokens = [int(x) for x in np.frombuffer(raw, dtype=">u2")]
    restored_tokens = expand(tokens, int(model["start_id"]), model["rules"])
    if any(token > 255 for token in restored_tokens):
        raise AssertionError(f"non-byte token after expansion: {directory}")
    restored = bytes(restored_tokens)
    expected_len = int(model["source_bytes"])
    expected_sha = model["source_sha256"]
    if len(restored) != expected_len or sha256(restored) != expected_sha:
        raise AssertionError(f"base source restore mismatch: {directory}")
    if result["corpus"]["bytes"] != expected_len or result["corpus"]["sha256"] != expected_sha:
        raise AssertionError(f"result/model source mismatch: {directory}")
    return {
        "directory": str(directory),
        "bytes": expected_len,
        "sha256": expected_sha,
        "token_count": token_count,
        "rules": len(model["rules"]),
        "restore": True,
    }


def verify_result(path: Path) -> dict[str, Any]:
    result = json.loads(path.read_text(encoding="utf-8"))
    status = result["status"]
    directory = path.parent
    if status == "MEASURED":
        rows = result["perspectives"]
        if len(rows) != 28:
            raise AssertionError(f"expected 28 perspectives: {path}")
        ring_a = [row for row in rows if row["ring"] == "A_REPRESENTATION"]
        ring_b = [row for row in rows if row["ring"] == "B_FISCHER_PREDICTOR"]
        ring_c = [row for row in rows if row["ring"] == "C_PERSISTENT_RECURRENCE"]
        if (len(ring_a), len(ring_b), len(ring_c)) != (8, 10, 10):
            raise AssertionError(f"8+10+10 mismatch: {path}")
        if not all(row.get("restore") for row in ring_a):
            raise AssertionError(f"Ring-A restore failure: {path}")
        if not all(row.get("restore") and row.get("state_match") for row in ring_c):
            raise AssertionError(f"Ring-C restore/state failure: {path}")
        if not all(math.isfinite(float(row["estimated_bpc"])) for row in ring_b):
            raise AssertionError(f"Ring-B non-finite estimate: {path}")
        recurrence = result.get("recurrence") or {}
        if not recurrence.get("all_restore") or not recurrence.get("all_state_match"):
            raise AssertionError(f"recurrence summary gate failed: {path}")
        base = verify_base_artifact(directory, result)
        return {
            "set": result["source_set"],
            "lane": result["lane_id"],
            "status": status,
            "perspectives": 28,
            "base": base,
            "ring_a_restore": True,
            "ring_c_restore_state": True,
            "predictors_finite": True,
        }
    if not status.startswith("HELD"):
        raise AssertionError(f"unexpected non-measured status: {path}: {status}")
    if result.get("perspectives"):
        raise AssertionError(f"held lane emitted perspective rows: {path}")
    return {
        "set": result["source_set"],
        "lane": result["lane_id"],
        "status": status,
        "perspectives": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(args.input)
    output = Path(args.output)

    paths = sorted(root.rglob("perspective-result.json"))
    if len(paths) != 50:
        raise AssertionError(f"expected 50 returned result files, found {len(paths)}")
    verified = [verify_result(path) for path in paths]
    measured = sum(row["status"] == "MEASURED" for row in verified)
    held = len(verified) - measured
    if measured < 49:
        raise AssertionError(f"expected at least 49 measured cubes, got {measured}")
    if sum(row["perspectives"] for row in verified) != measured * 28:
        raise AssertionError("perspective total mismatch")

    # Invoke the original deterministic aggregate with the same CLI arguments.
    aggregate.main()

    receipt = {
        "schema": "ASOLARIA-CUBE-RECURRENCE-INDEPENDENT-VERIFY-v1",
        "returned": len(verified),
        "measured": measured,
        "held": held,
        "verified_perspective_rows": measured * 28,
        "all_base_artifacts_restored": True,
        "all_ring_a_restored": True,
        "all_ring_c_restored_and_state_matched": True,
        "all_ring_b_estimates_finite": True,
        "rows": verified,
    }
    output.mkdir(parents=True, exist_ok=True)
    receipt_path = output / "INDEPENDENT-ARTIFACT-VERIFICATION.json"
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    sums_path = output / "SHA256SUMS"
    with sums_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{sha256(receipt_path.read_bytes())}  {receipt_path.name}\n")
    print(
        f"CUBERECURRENCEINDEPENDENT|returned={len(verified)}|measured={measured}|"
        f"held={held}|passes={measured*28}|base_restore=1|status=PASS|json=0"
    )


if __name__ == "__main__":
    main()
