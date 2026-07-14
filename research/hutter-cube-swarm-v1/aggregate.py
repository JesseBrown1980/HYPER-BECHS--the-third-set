#!/usr/bin/env python3
"""Aggregate research-cube artifacts and compute observed runner concurrency."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path
from typing import Any

CURRENT_RECORD = 110_793_128
ONE_PERCENT_TARGET = 109_685_196


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_cube(cube: dict[str, Any]) -> bool:
    claimed = cube.get("cube_sha256")
    body = dict(cube)
    body.pop("cube_sha256", None)
    actual = sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
    return claimed == actual


def max_concurrency(cubes: list[dict[str, Any]]) -> tuple[int, list[dict[str, Any]]]:
    events: list[tuple[float, int, str]] = []
    for cube in cubes:
        runtime = cube.get("runtime", {})
        start = runtime.get("started_epoch")
        end = runtime.get("ended_epoch")
        if isinstance(start, (int, float)) and isinstance(end, (int, float)):
            events.append((float(start), 1, cube["lane_id"]))
            events.append((float(end), -1, cube["lane_id"]))
    # At identical timestamps, count an ending before a starting session.
    events.sort(key=lambda x: (x[0], x[1]))
    active: set[str] = set()
    maximum = 0
    snapshots: list[dict[str, Any]] = []
    for timestamp, delta, lane in events:
        if delta < 0:
            active.discard(lane)
        else:
            active.add(lane)
            if len(active) > maximum:
                maximum = len(active)
                snapshots.append({"timestamp_epoch": timestamp, "concurrency": maximum, "active_lanes": sorted(active)})
    return maximum, snapshots


def candidate_score(cube: dict[str, Any]) -> float:
    score = 0.0
    if cube.get("status") in {"MEASURED", "PRIVATE_INPUT_HASHED_AND_TRAINABLE"}:
        score += 20
    training = cube.get("training") or {}
    if training.get("all_restore"):
        score += 30
    if isinstance(training.get("best_bpc"), (int, float)):
        score += max(0.0, 10.0 - float(training["best_bpc"]))
    baselines = cube.get("baselines") or {}
    if baselines.get("status") == "MEASURED" and all(row.get("restore", True) for row in baselines.get("rows", [])):
        score += 10
    score += min(15, len(cube.get("research", {}).get("algorithm_hits", [])) / 4)
    score += min(10, len(cube.get("research", {}).get("formula_candidates", [])) / 8)
    if cube.get("family") in {"hutter-winner", "hutter-official", "hutter-winner-docs"}:
        score += 10
    return round(score, 4)


def esc(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\p").replace("\n", "\\n")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    root = Path(args.input)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    cube_paths = sorted(root.rglob("cube.json"))
    cubes = []
    invalid = []
    for path in cube_paths:
        try:
            cube = json.loads(path.read_text(encoding="utf-8"))
            cube["artifact_path"] = str(path.relative_to(root))
            cube["digest_verified"] = verify_cube(cube)
            if not cube["digest_verified"]:
                invalid.append(cube["lane_id"])
            cubes.append(cube)
        except Exception as exc:
            invalid.append(f"{path}: {type(exc).__name__}: {exc}")

    cubes.sort(key=lambda c: c["lane_id"])
    observed, snapshots = max_concurrency(cubes)
    status_counts = collections.Counter(c.get("status", "UNKNOWN") for c in cubes)
    family_counts = collections.Counter(c.get("family", "unknown") for c in cubes)
    algorithm_counts = collections.Counter()
    formula_counts = collections.Counter()
    people_counts = collections.Counter()
    for cube in cubes:
        for item in cube.get("research", {}).get("algorithm_hits", []):
            algorithm_counts[item["term"]] += item["count"]
        for formula in cube.get("research", {}).get("formula_candidates", []):
            formula_counts[formula] += 1
        for person in cube.get("research", {}).get("people_candidates", []):
            people_counts[person["name"]] += person["count"]

    ranked = sorted(({"lane_id": c["lane_id"], "family": c["family"], "status": c["status"],
                      "score": candidate_score(c), "training": c.get("training"),
                      "cube_sha256": c.get("cube_sha256")} for c in cubes),
                    key=lambda x: (-x["score"], x["lane_id"]))

    registry = {
        "schema": "ASOLARIA-HUTTER-CUBE-SWARM-REGISTRY-v1",
        "requested_sessions": 30,
        "returned_sessions": len(cubes),
        "invalid_cube_digests": invalid,
        "status_counts": dict(status_counts),
        "family_counts": dict(family_counts),
        "observed_max_concurrent_sessions": observed,
        "concurrency_snapshots": snapshots,
        "current_hutter_record_bytes": CURRENT_RECORD,
        "one_percent_target_bytes": ONE_PERCENT_TARGET,
        "top_algorithms": [{"term": term, "count": count} for term, count in algorithm_counts.most_common(100)],
        "top_people_candidates": [{"name": name, "count": count} for name, count in people_counts.most_common(80)],
        "ranked_lanes": ranked,
        "cubes": cubes,
    }
    registry_bytes = json.dumps(registry, indent=2, ensure_ascii=False).encode()
    (out / "CUBE-REGISTRY.json").write_bytes(registry_bytes)

    hbp_rows = [
        "CUBESWARMv1" + "".join([
            f"|requested=30", f"|returned={len(cubes)}", f"|observed_max_concurrent={observed}",
            f"|current_record={CURRENT_RECORD}", f"|one_percent_target={ONE_PERCENT_TARGET}",
            f"|invalid={len(invalid)}", "|json=0"
        ])
    ]
    for cube in cubes:
        hbp_rows.append("CUBEREG" + "".join([
            f"|lane={esc(cube['lane_id'])}", f"|family={esc(cube['family'])}",
            f"|status={esc(cube['status'])}", f"|sha256={esc(cube.get('cube_sha256'))}",
            f"|verified={int(bool(cube.get('digest_verified')))}",
            f"|algorithms={len(cube.get('research', {}).get('algorithm_hits', []))}",
            f"|formulas={len(cube.get('research', {}).get('formula_candidates', []))}",
            f"|training={esc((cube.get('training') or {}).get('status', 'not-run'))}",
            f"|restore={int(bool((cube.get('training') or {}).get('all_restore')))}", "|json=0"
        ]))
    (out / "CUBE-REGISTRY.hbp").write_text("\n".join(hbp_rows) + "\n", encoding="utf-8")

    concurrency = {
        "schema": "CUBE-CONCURRENCY-RECEIPT-v1",
        "requested": 30,
        "observed_max": observed,
        "method": "maximum overlap of runner-reported wall-clock intervals",
        "snapshots": snapshots,
        "intervals": [{"lane": c["lane_id"], "start": c.get("runtime", {}).get("started_at"),
                       "end": c.get("runtime", {}).get("ended_at"),
                       "start_epoch": c.get("runtime", {}).get("started_epoch"),
                       "end_epoch": c.get("runtime", {}).get("ended_epoch"),
                       "runner": c.get("runtime", {}).get("runner_name")} for c in cubes],
    }
    (out / "CONCURRENCY-RECEIPT.json").write_text(json.dumps(concurrency, indent=2), encoding="utf-8")

    graph_nodes = []
    graph_edges = []
    for cube in cubes:
        graph_nodes.append({"id": cube["lane_id"], "type": "cube", "family": cube["family"], "status": cube["status"]})
        for item in cube.get("research", {}).get("algorithm_hits", [])[:25]:
            aid = "algorithm:" + item["term"]
            graph_nodes.append({"id": aid, "type": "algorithm"})
            graph_edges.append({"from": cube["lane_id"], "to": aid, "relation": "mentions", "weight": item["count"]})
    # Deduplicate graph nodes deterministically.
    unique_nodes = {node["id"]: node for node in graph_nodes}
    (out / "SOURCE-GRAPH.json").write_text(json.dumps({"nodes": list(unique_nodes.values()), "edges": graph_edges}, indent=2), encoding="utf-8")

    lines = [
        "# Asolaria / Hutter cube-swarm result", "",
        f"- Requested cube sessions: **30**",
        f"- Returned cube sessions: **{len(cubes)}**",
        f"- Observed maximum simultaneous runner intervals: **{observed}**",
        f"- Invalid cube digests: **{len(invalid)}**",
        f"- Current public Hutter record used by the plan: **{CURRENT_RECORD:,} B**",
        f"- Approximate one-percent target: **{ONE_PERCENT_TARGET:,} B**", "",
        "## Status counts", "",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Highest-ranked research/training lanes", "", "| Lane | Family | Status | Score | Training best |", "|---|---|---|---:|---:|"])
    for item in ranked[:20]:
        training = item.get("training") or {}
        best = training.get("best_bpc", "—")
        lines.append(f"| `{item['lane_id']}` | {item['family']} | `{item['status']}` | {item['score']:.2f} | {best} |")
    lines.extend(["", "## Most frequent algorithm families", ""])
    for term, count in algorithm_counts.most_common(35):
        lines.append(f"- `{term}` — {count}")
    held = [c for c in cubes if c["status"].startswith("HELD")]
    if held:
        lines.extend(["", "## Held lanes", ""])
        for cube in held:
            lines.append(f"- `{cube['lane_id']}` — `{cube['status']}`")
    lines.extend(["", "## Interpretation", "",
        "The concurrency number is an empirical property of this run, not a promise of permanent account capacity.",
        "GitHub may queue jobs differently under other repository, billing, or platform load conditions.",
        "The swarm artifacts are research cubes and reversible mini-cube measurements; they are not a Hutter Prize archive.",
    ])
    (out / "SWARM-RESULT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    tournament = """# Next implementation tournament

## Admission gate

Every candidate must package the complete decoder/model/catalog and restore the exact same source SHA.
Candidates compete first on 1 MB, then 10 MB, then full enwik8. Only candidates that beat the current
best complete archive advance to enwik9.

## Proposed parallel candidates

1. **Fischer-v4 anti-blunder mixer** — logistic context mixer, SSE/APM, confidence-blunder penalty.
2. **Blockwise black/white bridge** — lawful right-context at block boundaries rather than per-byte pyramid.
3. **FX2 transform port** — reverse dictionary, stemmer word classes, four word streams, wiki parsing.
4. **Article-order experiment** — embeddings/cheap lexical vectors, one-dimensional ordering, reversible permutation.
5. **Disk-backed large PPM** — mmap/cold-store policy with measured RAM, disk writes, and SSD boundary.
6. **PAQ/FXCM context tournament** — state tables, match/sparse-match, bracket/template/table contexts.
7. **CTW/ACTW lane** — exact Bayesian tree mixture and nonstationary weighting.
8. **MambaByte lane** — small deterministic byte SSM trained online or transmitted as charged model state.
9. **PMATIC probability-sync lane** — test cross-CPU probability mismatch tolerance for neural/Fischer predictors.
10. **Entropy backend lane** — arithmetic/range versus rANS/FSE with identical probability traces.
11. **Glyph-first lane** — reversible BPE/cube language before prediction; catalog charged.
12. **Per-block selector** — choose the smallest fully decodable archive among black-only, black+white, PPM, CTW, and glyph modes.

## Prize gate

A Hutter submission exists only when:

```text
archive + decompressor/model <= 109,685,196 bytes
exact enwik9 SHA restored
runtime, RAM, disk, CPU, source-license, and publication rules satisfied
```
"""
    (out / "NEXT-TOURNAMENT.md").write_text(tournament, encoding="utf-8")

    hashes = []
    for name in ["CUBE-REGISTRY.json", "CUBE-REGISTRY.hbp", "CONCURRENCY-RECEIPT.json", "SOURCE-GRAPH.json", "SWARM-RESULT.md", "NEXT-TOURNAMENT.md"]:
        hashes.append(f"{sha256((out / name).read_bytes())}  {name}")
    (out / "SHA256SUMS").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    print(f"CUBESWARM|requested=30|returned={len(cubes)}|observed_max_concurrent={observed}|invalid={len(invalid)}|json=0")


if __name__ == "__main__":
    main()
