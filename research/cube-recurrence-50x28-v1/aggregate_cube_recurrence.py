#!/usr/bin/env python3
"""Aggregate fifty base cubes and their 8+10+10 perspective rows."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import statistics
from pathlib import Path
from typing import Any


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_receipt(result: dict[str, Any]) -> bool:
    claimed = result.get("receipt_sha256")
    body = dict(result)
    body.pop("receipt_sha256", None)
    body.pop("artifact_path", None)
    body.pop("receipt_verified", None)
    actual = sha256(json.dumps(
        body, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode())
    return claimed == actual


def observed_concurrency(results: list[dict[str, Any]]) -> tuple[int, list[dict[str, Any]]]:
    events: list[tuple[float, int, str]] = []
    for result in results:
        runtime = result.get("runtime", {})
        start = runtime.get("started_epoch")
        end = runtime.get("ended_epoch")
        if isinstance(start, (int, float)) and isinstance(end, (int, float)):
            key = f"{result['source_set']}:{result['lane_id']}"
            events.append((float(start), 1, key))
            events.append((float(end), -1, key))
    # end events before start events at the same timestamp
    events.sort(key=lambda x: (x[0], x[1]))
    active: set[str] = set()
    maximum = 0
    snapshots = []
    for timestamp, delta, key in events:
        if delta < 0:
            active.discard(key)
        else:
            active.add(key)
            if len(active) > maximum:
                maximum = len(active)
                snapshots.append({
                    "timestamp_epoch": timestamp,
                    "concurrency": maximum,
                    "active_lanes": sorted(active),
                })
    return maximum, snapshots


def mean(values: list[float]) -> float | None:
    return statistics.fmean(values) if values else None


def median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def group_rows(results: list[dict[str, Any]], ring: str) -> dict[str, list[tuple[dict[str, Any], dict[str, Any]]]]:
    groups: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = collections.defaultdict(list)
    for result in results:
        for row in result.get("perspectives", []):
            if row.get("ring") == ring:
                groups[row["perspective"]].append((result, row))
    return groups


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    root = Path(args.input)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    invalid: list[str] = []
    for path in sorted(root.rglob("perspective-result.json")):
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
            result["artifact_path"] = str(path.relative_to(root))
            result["receipt_verified"] = verify_receipt(result)
            if not result["receipt_verified"]:
                invalid.append(f"{result['source_set']}:{result['lane_id']}")
            results.append(result)
        except Exception as exc:
            invalid.append(f"{path}:{type(exc).__name__}:{exc}")
    results.sort(key=lambda x: (x["source_set"], x["lane_id"]))

    maximum, snapshots = observed_concurrency(results)
    status_counts = collections.Counter(result["status"] for result in results)
    set_counts = collections.Counter(result["source_set"] for result in results)
    measured = [result for result in results if result["status"] == "MEASURED"]
    held = [result for result in results if result["status"] != "MEASURED"]
    total_passes = sum(len(result.get("perspectives", [])) for result in results)
    expected_passes = len(measured) * 28

    # Ring A
    ring_a_groups = group_rows(measured, "A_REPRESENTATION")
    ring_a_summary = []
    ring_a_wins = collections.Counter()
    lane_winners = []
    for result in measured:
        rows = [row for row in result["perspectives"] if row["ring"] == "A_REPRESENTATION"]
        winner = min(rows, key=lambda row: row["standalone_bpc"])
        ring_a_wins[winner["perspective"]] += 1
        lane_winners.append({
            "set": result["source_set"],
            "lane": result["lane_id"],
            "ring_a_winner": winner["perspective"],
            "ring_a_bpc": winner["standalone_bpc"],
        })
    for name, items in ring_a_groups.items():
        rows = [row for _, row in items]
        ring_a_summary.append({
            "perspective": name,
            "cubes": len(rows),
            "wins": ring_a_wins[name],
            "mean_payload_bpc": mean([float(row["payload_bpc"]) for row in rows]),
            "mean_standalone_bpc": mean([float(row["standalone_bpc"]) for row in rows]),
            "median_delta_vs_base_payload_pct": median(
                [float(row["delta_vs_base_payload_pct"]) for row in rows]
            ),
            "all_restore": all(row.get("restore") for row in rows),
        })
    ring_a_summary.sort(key=lambda x: (
        float("inf") if x["mean_standalone_bpc"] is None else x["mean_standalone_bpc"],
        x["perspective"],
    ))

    # Ring B
    ring_b_groups = group_rows(measured, "B_FISCHER_PREDICTOR")
    ring_b_summary = []
    ring_b_wins = collections.Counter()
    for result in measured:
        rows = [row for row in result["perspectives"] if row["ring"] == "B_FISCHER_PREDICTOR"]
        winner = min(rows, key=lambda row: row["estimated_bpc"])
        ring_b_wins[winner["perspective"]] += 1
        for lane_row in lane_winners:
            if lane_row["set"] == result["source_set"] and lane_row["lane"] == result["lane_id"]:
                lane_row["ring_b_winner"] = winner["perspective"]
                lane_row["ring_b_bpc"] = winner["estimated_bpc"]
                break
    for name, items in ring_b_groups.items():
        rows = [row for _, row in items]
        ring_b_summary.append({
            "perspective": name,
            "cubes": len(rows),
            "wins": ring_b_wins[name],
            "mean_estimated_bpc": mean([float(row["estimated_bpc"]) for row in rows]),
            "mean_top1_accuracy": mean([float(row["top1_accuracy"]) for row in rows]),
            "mean_blunders": mean([float(row["high_confidence_blunders"]) for row in rows]),
            "mean_trust": mean([float(row["omnishannon_trust"]) for row in rows]),
        })
    ring_b_summary.sort(key=lambda x: (
        float("inf") if x["mean_estimated_bpc"] is None else x["mean_estimated_bpc"],
        x["perspective"],
    ))

    # Ring C
    recurrence_rows = []
    holdout_epoch_values: dict[int, list[float]] = collections.defaultdict(list)
    recurrence_improved = 0
    for result in measured:
        recurrence = result.get("recurrence") or {}
        first = recurrence.get("first_bpc")
        last = recurrence.get("last_bpc")
        change = recurrence.get("change_pct")
        if isinstance(change, (int, float)) and change < 0:
            recurrence_improved += 1
        row = {
            "set": result["source_set"],
            "lane": result["lane_id"],
            "first_bpc": first,
            "last_bpc": last,
            "change_pct": change,
            "checkpoint_bytes": recurrence.get("model_zlib_checkpoint_bytes"),
            "nondefault_cells": recurrence.get("model_nondefault_cells"),
        }
        recurrence_rows.append(row)
        for holdout in recurrence.get("holdouts", []):
            if isinstance(holdout.get("bpc"), (int, float)):
                holdout_epoch_values[int(holdout["epoch"])].append(float(holdout["bpc"]))
        for lane_row in lane_winners:
            if lane_row["set"] == result["source_set"] and lane_row["lane"] == result["lane_id"]:
                lane_row["recurrence_change_pct"] = change
                lane_row["recurrence_first_bpc"] = first
                lane_row["recurrence_last_bpc"] = last
                break
    recurrence_summary = {
        "cubes": len(recurrence_rows),
        "improved_cubes": recurrence_improved,
        "mean_first_bpc": mean([float(row["first_bpc"]) for row in recurrence_rows
                                if isinstance(row.get("first_bpc"), (int, float))]),
        "mean_last_bpc": mean([float(row["last_bpc"]) for row in recurrence_rows
                               if isinstance(row.get("last_bpc"), (int, float))]),
        "mean_change_pct": mean([float(row["change_pct"]) for row in recurrence_rows
                                 if isinstance(row.get("change_pct"), (int, float))]),
        "median_change_pct": median([float(row["change_pct"]) for row in recurrence_rows
                                     if isinstance(row.get("change_pct"), (int, float))]),
        "mean_checkpoint_bytes": mean([float(row["checkpoint_bytes"]) for row in recurrence_rows
                                       if isinstance(row.get("checkpoint_bytes"), (int, float))]),
        "holdout_mean_bpc_by_epoch": {
            str(epoch): mean(values) for epoch, values in sorted(holdout_epoch_values.items())
        },
        "rows": recurrence_rows,
    }

    # Base cube and set summaries
    base_rank = []
    set_summary = {}
    for source_set in sorted(set_counts):
        subset = [result for result in measured if result["source_set"] == source_set]
        base_bpcs = [float(result["base_cube"]["bpc"]) for result in subset if result.get("base_cube")]
        changes = [float(result["recurrence"]["change_pct"]) for result in subset
                   if result.get("recurrence") and isinstance(result["recurrence"].get("change_pct"), (int, float))]
        set_summary[source_set] = {
            "returned": set_counts[source_set],
            "measured": len(subset),
            "mean_base_bpc": mean(base_bpcs),
            "median_base_bpc": median(base_bpcs),
            "mean_recurrence_change_pct": mean(changes),
            "median_recurrence_change_pct": median(changes),
        }
    for result in measured:
        base = result.get("base_cube")
        if base:
            base_rank.append({
                "set": result["source_set"],
                "lane": result["lane_id"],
                "corpus_bytes": result["corpus"]["bytes"],
                "base_bpc": base["bpc"],
                "rules": base["rules"],
                "receipt_sha256": result["receipt_sha256"],
            })
    base_rank.sort(key=lambda x: (x["base_bpc"], x["set"], x["lane"]))

    winner_map = {
        "schema": "ASOLARIA-CUBE-PERSPECTIVE-WINNER-MAP-v1",
        "lane_winners": sorted(lane_winners, key=lambda x: (x["set"], x["lane"])),
        "ring_a_global": ring_a_summary,
        "ring_b_global": ring_b_summary,
        "recurrence_global": recurrence_summary,
    }
    (out / "PERSPECTIVE-WINNER-MAP.json").write_text(
        json.dumps(winner_map, indent=2), encoding="utf-8"
    )

    registry = {
        "schema": "ASOLARIA-CUBE-RECURRENCE-50X28-REGISTRY-v1",
        "requested_cubes": 50,
        "returned_cubes": len(results),
        "measured_cubes": len(measured),
        "held_cubes": len(held),
        "requested_perspective_passes": 1400,
        "expected_passes_from_measured_cubes": expected_passes,
        "returned_perspective_passes": total_passes,
        "observed_max_concurrent_sessions": maximum,
        "concurrency_snapshots": snapshots,
        "invalid_receipts": invalid,
        "status_counts": dict(status_counts),
        "set_counts": dict(set_counts),
        "set_summary": set_summary,
        "ring_a": ring_a_summary,
        "ring_b": ring_b_summary,
        "recurrence": recurrence_summary,
        "base_cube_ranking": base_rank,
        "held": [{
            "set": result["source_set"],
            "lane": result["lane_id"],
            "status": result["status"],
            "errors": result.get("errors", []),
        } for result in held],
        "results": results,
    }
    (out / "CUBE-RECURRENCE-REGISTRY.json").write_text(
        json.dumps(registry, indent=2), encoding="utf-8"
    )

    hbp = [
        "CUBERECURRENCE50X28v1"
        f"|requested_cubes=50|returned_cubes={len(results)}|measured_cubes={len(measured)}"
        f"|held_cubes={len(held)}|requested_passes=1400|returned_passes={total_passes}"
        f"|observed_max_concurrent={maximum}|invalid_receipts={len(invalid)}|json=0"
    ]
    for row in ring_a_summary:
        hbp.append(
            "RINGA"
            f"|perspective={row['perspective']}|cubes={row['cubes']}|wins={row['wins']}"
            f"|mean_bpc={row['mean_standalone_bpc']}|median_delta_pct={row['median_delta_vs_base_payload_pct']}"
            f"|all_restore={int(row['all_restore'])}|json=0"
        )
    for row in ring_b_summary:
        hbp.append(
            "RINGB"
            f"|perspective={row['perspective']}|cubes={row['cubes']}|wins={row['wins']}"
            f"|mean_estimated_bpc={row['mean_estimated_bpc']}|mean_accuracy={row['mean_top1_accuracy']}"
            f"|mean_blunders={row['mean_blunders']}|mean_trust={row['mean_trust']}|json=0"
        )
    hbp.append(
        "RINGC"
        f"|cubes={recurrence_summary['cubes']}|improved={recurrence_summary['improved_cubes']}"
        f"|mean_first_bpc={recurrence_summary['mean_first_bpc']}"
        f"|mean_last_bpc={recurrence_summary['mean_last_bpc']}"
        f"|mean_change_pct={recurrence_summary['mean_change_pct']}"
        f"|median_change_pct={recurrence_summary['median_change_pct']}|json=0"
    )
    (out / "CUBE-RECURRENCE-REGISTRY.hbp").write_text(
        "\n".join(hbp) + "\n", encoding="utf-8"
    )

    concurrency_receipt = {
        "schema": "CUBE-RECURRENCE-CONCURRENCY-v1",
        "requested_jobs": 50,
        "max_parallel_requested": 20,
        "observed_max": maximum,
        "method": "maximum overlap of runner-reported start/end intervals",
        "snapshots": snapshots,
        "intervals": [{
            "set": result["source_set"],
            "lane": result["lane_id"],
            "start": result["runtime"].get("started_at"),
            "end": result["runtime"].get("ended_at"),
            "runner": result["runtime"].get("runner_name"),
        } for result in results],
    }
    (out / "CONCURRENCY-RECEIPT.json").write_text(
        json.dumps(concurrency_receipt, indent=2), encoding="utf-8"
    )

    lines = [
        "# Cube recurrence 50×28 — aggregate result",
        "",
        f"- Requested base cubes: **50**",
        f"- Returned base cubes: **{len(results)}**",
        f"- Measured base cubes: **{len(measured)}**",
        f"- Held base cubes: **{len(held)}**",
        f"- Requested perspective rows: **1,400**",
        f"- Returned perspective rows: **{total_passes}**",
        f"- Observed maximum concurrent containers: **{maximum}**",
        f"- Invalid receipts: **{len(invalid)}**",
        "",
        "## Source sets",
        "",
    ]
    for source_set, stats in set_summary.items():
        lines.extend([
            f"### `{source_set}`",
            "",
            f"- Returned: {stats['returned']}",
            f"- Measured: {stats['measured']}",
            f"- Mean base-cube bpc: {stats['mean_base_bpc']:.6f}" if stats["mean_base_bpc"] is not None else "- Mean base-cube bpc: —",
            f"- Mean recurrence change: {stats['mean_recurrence_change_pct']:.3f}%" if stats["mean_recurrence_change_pct"] is not None else "- Mean recurrence change: —",
            "",
        ])
    lines.extend([
        "## Ring A — global reversible-view ranking",
        "",
        "| Perspective | Cubes | Wins | Mean standalone bpc | Median Δ payload | Restore |",
        "|---|---:|---:|---:|---:|---|",
    ])
    for row in ring_a_summary:
        lines.append(
            f"| `{row['perspective']}` | {row['cubes']} | {row['wins']} | "
            f"{row['mean_standalone_bpc']:.6f} | {row['median_delta_vs_base_payload_pct']:.3f}% | "
            f"{row['all_restore']} |"
        )
    lines.extend([
        "",
        "## Ring B — global Fischer ranking",
        "",
        "| Perspective | Wins | Mean est. bpc | Mean accuracy | Mean blunders | Mean trust |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for row in ring_b_summary:
        lines.append(
            f"| `{row['perspective']}` | {row['wins']} | {row['mean_estimated_bpc']:.6f} | "
            f"{row['mean_top1_accuracy']:.4%} | {row['mean_blunders']:.2f} | "
            f"{row['mean_trust']:.6f} |"
        )
    lines.extend([
        "",
        "## Ring C — recurrence",
        "",
        f"- Cubes measured: **{recurrence_summary['cubes']}**",
        f"- Cubes whose epoch-10 payload beat epoch 1: **{recurrence_summary['improved_cubes']}**",
        f"- Mean epoch-1 bpc: **{recurrence_summary['mean_first_bpc']:.6f}**" if recurrence_summary["mean_first_bpc"] is not None else "- Mean epoch-1 bpc: —",
        f"- Mean epoch-10 bpc: **{recurrence_summary['mean_last_bpc']:.6f}**" if recurrence_summary["mean_last_bpc"] is not None else "- Mean epoch-10 bpc: —",
        f"- Mean change: **{recurrence_summary['mean_change_pct']:.3f}%**" if recurrence_summary["mean_change_pct"] is not None else "- Mean change: —",
        f"- Median change: **{recurrence_summary['median_change_pct']:.3f}%**" if recurrence_summary["median_change_pct"] is not None else "- Median change: —",
        "",
        "## Best base cubes",
        "",
        "| Set | Lane | Corpus B | Base bpc | Rules |",
        "|---|---|---:|---:|---:|",
    ])
    for row in base_rank[:20]:
        lines.append(
            f"| {row['set']} | `{row['lane']}` | {row['corpus_bytes']} | "
            f"{row['base_bpc']:.6f} | {row['rules']} |"
        )
    if held:
        lines.extend(["", "## Held lanes", ""])
        for result in held:
            lines.append(
                f"- `{result['source_set']}:{result['lane_id']}` — `{result['status']}`"
            )
    lines.extend([
        "",
        "## Boundary",
        "",
        "Ring A and Ring C are exact reconstructive paths and are accepted only after byte-identical readback.",
        "Ring B reports predictive log loss and trust; it is not relabeled as a standalone compressed archive.",
        "One shared base catalog is reused across the eight Ring-A views, while standalone bpc also charges it.",
        "The fifty containers each execute twenty-eight passes; the workflow does not request fourteen hundred separate runners.",
        "",
    ])
    (out / "CUBE-RECURRENCE-50X28-RESULT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    tournament = """# Next cube tournament

## Admission

A mechanism advances only when it restores exactly, improves the complete charged ledger, or supplies
independent predictive/integrity value that a downstream mixer can exploit.

## Candidate lanes

1. Train a view-specific catalog only for Ring-A transforms that win repeatedly.
2. Build a per-cube selector that chooses identity, delta, block mirror, or prime permutation.
3. Replace predictor estimates with a lawful arithmetic-coded black/white mixture.
4. Add Fischer confidence-blunder penalties and SSE/APM calibration.
5. Distill the ten predictor rows into a small shared expert cube.
6. Compare same-object recurrence with disjoint-cube transfer.
7. Persist only sparse/checkpoint state when its amortized gain is positive.
8. Cross-apply Wolfram catalogs to first-set cubes and first-set catalogs to Wolfram cubes.
9. Route parser, quantum, agent, native, and optimization cube families to specialized experts.
10. Advance the smallest complete archives to 10 MB, enwik8, and then enwik9.
"""
    (out / "NEXT-CUBE-TOURNAMENT.md").write_text(tournament, encoding="utf-8")

    names = [
        "CUBE-RECURRENCE-REGISTRY.json",
        "CUBE-RECURRENCE-REGISTRY.hbp",
        "CUBE-RECURRENCE-50X28-RESULT.md",
        "CONCURRENCY-RECEIPT.json",
        "PERSPECTIVE-WINNER-MAP.json",
        "NEXT-CUBE-TOURNAMENT.md",
    ]
    (out / "SHA256SUMS").write_text(
        "\n".join(f"{sha256((out / name).read_bytes())}  {name}" for name in names)
        + "\n",
        encoding="utf-8",
    )
    print(
        f"CUBERECURRENCEAGG|requested_cubes=50|returned_cubes={len(results)}|"
        f"measured_cubes={len(measured)}|returned_passes={total_passes}|"
        f"observed_max={maximum}|invalid={len(invalid)}|status=PASS|json=0"
    )


if __name__ == "__main__":
    main()
