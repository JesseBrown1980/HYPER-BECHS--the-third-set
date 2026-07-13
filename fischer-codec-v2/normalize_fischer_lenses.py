#!/usr/bin/env python3
"""Normalize independent lens reports after all ten seats have completed.

Each isolated runner cannot know the best peer's log loss. This aggregate pass
recomputes the public Fischer-style CPL and PROCEED/HOLD/BLOCK verdict against
the best of the ten measured lenses before the final receipt is minted.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("root")
    args = p.parse_args()
    paths = sorted(Path(args.root).rglob("lens-*.json"))
    if len(paths) != 10:
        raise SystemExit(f"expected 10 lens reports, found {len(paths)}")
    rows = [(path, json.loads(path.read_text(encoding="utf-8"))) for path in paths]
    best = min(float(row["ideal_bpb"]) for _, row in rows)
    for path, row in rows:
        cpl = round(1000 * max(0.0, float(row["ideal_bpb"]) - best))
        verdict = "BLOCK" if cpl >= 500 else ("HOLD" if cpl >= 150 else "PROCEED")
        row["cpl_vs_best"] = cpl
        row["fischer_verdict"] = verdict
        row["aggregate_best_ideal_bpb"] = best
        path.write_text(json.dumps(row, indent=2), encoding="utf-8")
    print(f"FISCHER_CPL_NORMALIZE|lenses=10|best_ideal_bpb={best:.6f}|status=PASS|json=0")


if __name__ == "__main__":
    main()
