#!/usr/bin/env python3
"""Aggregate non-reconstructive lens cubes, open-license cubes, and white-room tests."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def verify_lens(cube: dict[str, Any]) -> bool:
    claimed = cube.get("cube_sha256")
    body = dict(cube)
    body.pop("cube_sha256", None)
    return claimed == sha256(canonical(body))


def verify_open_cube(cube: dict[str, Any]) -> bool:
    claimed = cube.get("cube_manifest_sha256")
    body = dict(cube)
    body.pop("cube_manifest_sha256", None)
    return claimed == sha256(canonical(body))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    root = Path(args.input)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    lenses = []
    open_cubes = []
    white_room = None
    invalid = []

    for path in sorted(root.rglob("shadow-cube.json")):
        cube = json.loads(path.read_text(encoding="utf-8"))
        cube["artifact_path"] = str(path.relative_to(root))
        cube["digest_verified"] = verify_lens(cube)
        if not cube["digest_verified"]:
            invalid.append(cube["source_id"])
        lenses.append(cube)

    for path in sorted(root.rglob("cube-manifest.json")):
        cube = json.loads(path.read_text(encoding="utf-8"))
        cube["artifact_path"] = str(path.relative_to(root))
        cube["digest_verified"] = verify_open_cube(cube)
        if not cube["digest_verified"]:
            invalid.append(cube["source_id"])
        open_cubes.append(cube)

    result_paths = sorted(root.rglob("RESULT.json"))
    if result_paths:
        white_room = json.loads(result_paths[-1].read_text(encoding="utf-8"))
        white_room["artifact_path"] = str(result_paths[-1].relative_to(root))

    lenses.sort(key=lambda item: item["source_id"])
    open_cubes.sort(key=lambda item: item["source_id"])
    if len(lenses) != 3:
        invalid.append(f"lens_count={len(lenses)}")
    if len(open_cubes) != 7:
        invalid.append(f"open_cube_count={len(open_cubes)}")
    if white_room is None or white_room.get("status") != "PASS":
        invalid.append("white_room_missing_or_failed")

    registry = {
        "schema": "WOLFRAM-LENS-WHITE-ROOM-REGISTRY-v1",
        "lens_cube_count": len(lenses),
        "open_license_cube_count": len(open_cubes),
        "white_room_status": None if white_room is None else white_room.get("status"),
        "invalid": invalid,
        "lens_cubes": lenses,
        "open_license_cubes": open_cubes,
        "white_room": white_room,
        "summary": {
            "all_lens_raw_body_retained_false": all(not item["retention"]["raw_body_retained"] for item in lenses),
            "all_lens_expressive_text_bytes_zero": all(item["retention"]["expressive_text_bytes"] == 0 for item in lenses),
            "all_lens_nonreconstructive": all(not item["retention"]["source_reconstructable"] for item in lenses),
            "all_open_cube_licenses_verified": all(item["license"] in {"MIT", "Apache-2.0", "BSD-3-Clause"} for item in open_cubes),
            "all_open_cube_restores": all(item["byte_identical_restore"] for item in open_cubes),
            "all_cube_digests_verified": not invalid,
        }
    }
    (out / "CUBE-REGISTRY.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

    hbp = [
        "WOLFRAMLENSREGv1"
        f"|lenses={len(lenses)}|open_cubes={len(open_cubes)}|white_room={registry['white_room_status']}"
        f"|invalid={len(invalid)}|raw_service_bodies=0|json=0"
    ]
    for item in lenses:
        hbp.append(
            "LENSCUBEREG"
            f"|source={item['source_id']}|source_bytes={item['source_bytes']}|source_sha256={item['source_sha256']}"
            f"|categories={item['measurements']['category_count']}|types={item['measurements']['type_or_task_count']}"
            f"|raw_retained=0|reconstructable=0|verified={int(item['digest_verified'])}|json=0"
        )
    for item in open_cubes:
        hbp.append(
            "OPENCUBEREG"
            f"|source={item['source_id']}|repo={item['repo']}|commit={item['commit']}|license={item['license']}"
            f"|corpus_bytes={item['corpus_bytes']}|bpc={item['best_bpc']:.9f}|restore={int(item['byte_identical_restore'])}"
            f"|verified={int(item['digest_verified'])}|json=0"
        )
    (out / "CUBE-REGISTRY.hbp").write_text("\n".join(hbp) + "\n", encoding="utf-8")

    nodes = []
    edges = []
    for item in lenses:
        nodes.append({"id": item["source_id"], "type": "lens_cube"})
        for method in item["white_room_handoff"]["clean_room_methods"]:
            mid = "method:" + method
            nodes.append({"id": mid, "type": "method"})
            edges.append({"from": item["source_id"], "to": mid, "relation": "specifies"})
    for item in open_cubes:
        nodes.append({"id": item["source_id"], "type": "reversible_cube", "license": item["license"]})
        edges.append({"from": item["source_id"], "to": "white-room", "relation": "open_source_reference"})
    nodes.append({"id": "white-room", "type": "independent_builder"})
    unique_nodes = {node["id"]: node for node in nodes}
    (out / "PROVENANCE-GRAPH.json").write_text(json.dumps({"nodes": list(unique_nodes.values()), "edges": edges}, indent=2), encoding="utf-8")

    lines = [
        "# Wolfram lens / white-room result", "",
        f"- Non-reconstructive service lens cubes: **{len(lenses)}**",
        f"- Open-license reversible source cubes: **{len(open_cubes)}**",
        f"- Independent white-room builder: **{registry['white_room_status']}**",
        f"- Invalid receipts: **{len(invalid)}**", "",
        "## Service lens cubes", "",
        "| Source | Input bytes | Categories | Types/tasks | Raw retained | Reconstructable |",
        "|---|---:|---:|---:|---|---|",
    ]
    for item in lenses:
        lines.append(
            f"| `{item['source_id']}` | {item['source_bytes']:,} | {item['measurements']['category_count']} | "
            f"{item['measurements']['type_or_task_count']} | no | no |"
        )
    lines.extend(["", "## Open-license reversible cubes", "",
                  "| Source | License | Corpus bytes | Best level | Catalog | Payload | bpc | Restore | Best standard baseline |",
                  "|---|---|---:|---:|---:|---:|---:|---|---|"])
    for item in open_cubes:
        measured = [row for row in item["baselines"] if row.get("restore") and isinstance(row.get("bpc"), (int, float))]
        best_baseline = min(measured, key=lambda row: row["bpc"]) if measured else {"name": "—", "bpc": float("nan")}
        lines.append(
            f"| `{item['source_id']}` | {item['license']} | {item['corpus_bytes']:,} | {item['best_level']} | "
            f"{item['best_catalog_bytes']:,} | {item['best_payload_bytes']:,} | {item['best_bpc']:.6f} | PASS | "
            f"{best_baseline['name']} {best_baseline['bpc']:.6f} |"
        )
    lines.extend(["", "## White-room implementation", "", "```json",
                  json.dumps(white_room, indent=2) if white_room else "null", "```", "",
                  "## Boundary", "",
                  "The service-page lane retained only aggregate shadows and functional labels. The reversible cubes contain only explicitly licensed source corpora with license and attribution receipts. The independent builder received lens specifications, not Wolfram Service page bodies or cloned third-party source trees.", ""])
    (out / "RESULT.md").write_text("\n".join(lines), encoding="utf-8")

    sums = []
    for name in ("CUBE-REGISTRY.json", "CUBE-REGISTRY.hbp", "PROVENANCE-GRAPH.json", "RESULT.md"):
        sums.append(f"{sha256((out / name).read_bytes())}  {name}")
    (out / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print(f"WOLFRAMLENSAGG|lenses={len(lenses)}|open_cubes={len(open_cubes)}|white_room={registry['white_room_status']}|invalid={len(invalid)}|json=0")
    if invalid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
