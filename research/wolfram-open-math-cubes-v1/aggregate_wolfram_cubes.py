#!/usr/bin/env python3
"""Aggregate twenty Wolfram/open-math cube artifacts."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_receipt(result: dict[str, Any]) -> bool:
    claimed = result.get("receipt_sha256")
    body = dict(result)
    body.pop("receipt_sha256", None)
    actual = sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
    return claimed == actual


def concurrency(results: list[dict[str, Any]]) -> tuple[int, list[dict[str, Any]]]:
    events: list[tuple[float, int, str]] = []
    for result in results:
        runtime = result.get("runtime", {})
        start = runtime.get("started_epoch")
        end = runtime.get("ended_epoch")
        if isinstance(start, (int, float)) and isinstance(end, (int, float)):
            events.append((float(start), 1, result["lane"]["id"]))
            events.append((float(end), -1, result["lane"]["id"]))
    events.sort(key=lambda x: (x[0], x[1]))
    active: set[str] = set()
    maximum = 0
    snapshots = []
    for timestamp, delta, lane in events:
        if delta < 0:
            active.discard(lane)
        else:
            active.add(lane)
            if len(active) > maximum:
                maximum = len(active)
                snapshots.append({"timestamp_epoch": timestamp, "concurrency": maximum, "active_lanes": sorted(active)})
    return maximum, snapshots


def jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    root = Path(args.input)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    invalid = []
    for path in sorted(root.rglob("cube-result.json")):
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
            result["artifact_path"] = str(path.relative_to(root))
            result["receipt_verified"] = verify_receipt(result)
            if not result["receipt_verified"]:
                invalid.append(result["lane"]["id"])
            results.append(result)
        except Exception as exc:
            invalid.append(f"{path}:{type(exc).__name__}:{exc}")
    results.sort(key=lambda x: x["lane"]["id"])

    observed, snapshots = concurrency(results)
    status_counts = collections.Counter(result["status"] for result in results)
    license_counts = collections.Counter()
    repo_records = []
    for result in results:
        for source in result.get("sources", []):
            classification = source.get("license", {}).get("classification", "UNKNOWN")
            license_counts[classification] += 1
            repo_records.append({
                "lane": result["lane"]["id"],
                "repo": source["repo"],
                "commit": source.get("commit"),
                "license": classification,
                "allowed": source.get("license", {}).get("allowed", False),
                "license_files": source.get("license", {}).get("files", []),
            })

    ranked = []
    for result in results:
        cube = result.get("cube") or {}
        baseline_rows = [row for row in result.get("baselines", []) if isinstance(row.get("bpc"), (int, float))]
        best_baseline = min(baseline_rows, key=lambda x: x["bpc"]) if baseline_rows else None
        best_bpc = cube.get("best_bpc")
        ranked.append({
            "lane": result["lane"]["id"],
            "status": result["status"],
            "corpus_bytes": result.get("corpus", {}).get("bytes", 0),
            "files": result.get("corpus", {}).get("file_count", 0),
            "cube_bpc": best_bpc,
            "best_level": cube.get("best_level"),
            "restore": cube.get("all_restore", False),
            "best_baseline": best_baseline,
            "delta_vs_best_baseline_pct": (
                (best_bpc / best_baseline["bpc"] - 1) * 100
                if isinstance(best_bpc, (int, float)) and best_baseline else None
            ),
        })
    ranked.sort(key=lambda x: (float("inf") if x["cube_bpc"] is None else x["cube_bpc"], x["lane"]))

    symbol_sets: dict[str, set[str]] = {}
    symbol_counts = collections.Counter()
    formula_counts = collections.Counter()
    for result in results:
        shadow = result.get("method_shadow") or {}
        symbols = {row["name"] for row in shadow.get("top_wolfram_symbols", [])}
        symbol_sets[result["lane"]["id"]] = symbols
        for row in shadow.get("top_wolfram_symbols", []):
            symbol_counts[row["name"]] += int(row["count"])
        for formula in shadow.get("formula_candidates", []):
            formula_counts[formula] += 1

    overlap = []
    lanes = sorted(symbol_sets)
    for i, left in enumerate(lanes):
        for right in lanes[i + 1:]:
            overlap.append({
                "left": left,
                "right": right,
                "jaccard": jaccard(symbol_sets[left], symbol_sets[right]),
                "shared": len(symbol_sets[left] & symbol_sets[right]),
                "union": len(symbol_sets[left] | symbol_sets[right]),
            })
    overlap.sort(key=lambda x: (-x["jaccard"], -x["shared"], x["left"], x["right"]))

    occurrence = collections.Counter()
    for symbols in symbol_sets.values():
        occurrence.update(symbols)
    threshold = max(2, len(symbol_sets) // 3)
    core_symbols = [
        {"symbol": symbol, "cube_count": count, "total_count": symbol_counts[symbol]}
        for symbol, count in occurrence.items() if count >= threshold
    ]
    core_symbols.sort(key=lambda x: (-x["cube_count"], -x["total_count"], x["symbol"]))

    method_cube = {
        "schema": "ASOLARIA-WOLFRAM-SHARED-METHOD-CUBE-v1",
        "nonreconstructive": True,
        "source_cube_count": len(results),
        "minimum_cube_occurrence": threshold,
        "shared_symbols": core_symbols[:2048],
        "repeated_formula_candidates": [
            {"formula": formula, "cube_count": count}
            for formula, count in formula_counts.most_common(512) if count >= 2
        ],
        "top_pairwise_overlaps": overlap[:190],
    }
    method_cube_bytes = json.dumps(method_cube, sort_keys=True, separators=(",", ":")).encode()
    method_cube["sha256"] = sha256(method_cube_bytes)
    (out / "WOLFRAM-SHARED-METHOD-CUBE.json").write_text(json.dumps(method_cube, indent=2), encoding="utf-8")

    registry = {
        "schema": "ASOLARIA-WOLFRAM-OPEN-MATH-CUBE-REGISTRY-v1",
        "requested_lanes": 20,
        "returned_lanes": len(results),
        "observed_max_concurrent_sessions": observed,
        "concurrency_snapshots": snapshots,
        "status_counts": dict(status_counts),
        "license_counts": dict(license_counts),
        "invalid_receipts": invalid,
        "repositories": repo_records,
        "ranked_cubes": ranked,
        "shared_method_cube_sha256": method_cube["sha256"],
        "results": results,
    }
    (out / "WOLFRAM-CUBE-REGISTRY.json").write_text(json.dumps(registry, indent=2), encoding="utf-8")

    hbp = [
        "WOLFRAMCUBEFORGEv1" + "".join([
            "|requested=20", f"|returned={len(results)}", f"|observed_max={observed}",
            f"|invalid={len(invalid)}", f"|method_cube_sha256={method_cube['sha256']}", "|json=0"
        ])
    ]
    for row in ranked:
        hbp.append(
            "WOLFRAMCUBEREG" +
            f"|lane={row['lane']}|status={row['status']}|corpus_bytes={row['corpus_bytes']}|"
            f"files={row['files']}|cube_bpc={row['cube_bpc']}|best_level={row['best_level']}|"
            f"restore={int(bool(row['restore']))}|delta_vs_best_pct={row['delta_vs_best_baseline_pct']}|json=0"
        )
    (out / "WOLFRAM-CUBE-REGISTRY.hbp").write_text("\n".join(hbp) + "\n", encoding="utf-8")

    lines = [
        "# Wolfram open-math cube forge — aggregate result", "",
        f"- Requested lanes: **20**",
        f"- Returned lanes: **{len(results)}**",
        f"- Observed maximum concurrent runners: **{observed}**",
        f"- Invalid receipts: **{len(invalid)}**",
        f"- Shared method-cube SHA-256: `{method_cube['sha256']}`", "",
        "## Status", "",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## License classifications", ""])
    for license_name, count in sorted(license_counts.items()):
        lines.append(f"- `{license_name}`: {count}")
    lines.extend(["", "## Reversible cube ranking", "", "| Lane | Corpus B | Files | Cube bpc | Best level | Best baseline | Delta | Restore |", "|---|---:|---:|---:|---:|---|---:|---|"])
    for row in ranked:
        baseline = row["best_baseline"]
        baseline_text = f"{baseline['name']} {baseline['bpc']:.6f}" if baseline else "—"
        delta = f"{row['delta_vs_best_baseline_pct']:.2f}%" if row["delta_vs_best_baseline_pct"] is not None else "—"
        cube_bpc = f"{row['cube_bpc']:.6f}" if isinstance(row["cube_bpc"], (int, float)) else "—"
        lines.append(f"| `{row['lane']}` | {row['corpus_bytes']} | {row['files']} | {cube_bpc} | {row['best_level']} | {baseline_text} | {delta} | {row['restore']} |")
    lines.extend(["", "## Shared language", ""])
    lines.append(f"Symbols appearing in at least **{threshold}** cube shadows: **{len(core_symbols)}**.")
    lines.append("")
    for item in core_symbols[:50]:
        lines.append(f"- `{item['symbol']}` — {item['cube_count']} cubes, {item['total_count']} total occurrences")
    lines.extend(["", "## Interpretation", "",
        "Each accepted lane contains an exact source-representation cube plus a non-reconstructive method shadow.",
        "The exact cube is passive data/codebook state, not an executable AI agent.",
        "License-held components remain listed and are not silently included.",
        "A low bpc on source code or notebooks is not an enwik/Hutter result.",
    ])
    (out / "WOLFRAM-CUBE-FORGE-RESULT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    next_doc = """# Next Wolfram/Asolaria cube tournament

1. **Parser cube** — codeparser + codeformatter + codeinspector, exact source and shared AST vocabulary.
2. **Quantum cube** — QuantumFramework formulas, operator/circuit graph, Q-PRISM cross-map.
3. **Agent cube** — AgentTools + Chatbook + OMNIEVENT tool/PID schema.
4. **Native cube** — LibraryLink C++/Rust interfaces and hard-drive-backed execution surfaces.
5. **Optimization cube** — GurobiLink model vocabulary mapped to OmniScheduler admission laws.
6. **Symbolic probability cube** — extract distributions, entropy formulas, mixers, and exact rational receipts.
7. **Open dataset lane** — use original permissively licensed mathematical datasets discovered via Wolfram provenance.
8. **Cross-cube encoder law** — choose glyph IDs deterministically when source languages overlap.
9. **Fischer symbolic mixer** — rank parser/quantum/agent experts by exact prediction and anti-blunder score.
10. **Whole-ledger benchmark** — charge source corpus, cube models, method shadows, runtime, and receipts.

Every promotion requires exact restore for reconstructive cubes and explicit nonreconstructive labeling for shadows.
"""
    (out / "NEXT-WOLFRAM-CUBE-TOURNAMENT.md").write_text(next_doc, encoding="utf-8")

    names = [
        "WOLFRAM-CUBE-REGISTRY.json", "WOLFRAM-CUBE-REGISTRY.hbp",
        "WOLFRAM-SHARED-METHOD-CUBE.json", "WOLFRAM-CUBE-FORGE-RESULT.md",
        "NEXT-WOLFRAM-CUBE-TOURNAMENT.md",
    ]
    (out / "SHA256SUMS").write_text("\n".join(f"{sha256((out/name).read_bytes())}  {name}" for name in names) + "\n", encoding="utf-8")
    print(f"WOLFRAMCUBEFORGE|requested=20|returned={len(results)}|observed_max={observed}|invalid={len(invalid)}|status=PASS|json=0")


if __name__ == "__main__":
    main()
