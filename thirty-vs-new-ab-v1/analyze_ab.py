#!/usr/bin/env python3
"""Compare uniform-pass arms of the thirty-vs-new-way cube A/B.

Exact integers and fractions only; no floats enter any emitted value. Each arm
directory must contain ``FIRST-FLOOR-RESULT.hbp`` from the pinned first-floor
module run on an identical source cohort.
"""
from __future__ import annotations

import argparse
import pathlib
from collections import defaultdict
from fractions import Fraction


def load(dirpath: str):
    hbp = pathlib.Path(dirpath) / "FIRST-FLOOR-RESULT.hbp"
    hdr, cubes, merges = {}, {}, defaultdict(list)
    for line in hbp.read_text(encoding="utf-8").splitlines():
        parts = line.split("|")
        tag = parts[0]
        fields = dict(kv.split("=", 1) for kv in parts[1:] if "=" in kv)
        if tag == "FIRSTFLOORHDR":
            hdr = fields
        elif tag == "CUBE":
            cubes[fields["id"]] = fields
        elif tag == "MERGE":
            merges[fields["cube"]].append(
                (int(fields["n"]), int(fields["net_gain"]))
            )
    return hdr, cubes, merges


def frac(numerator: int, denominator: int) -> Fraction:
    return Fraction(numerator, denominator) if denominator else Fraction(0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cohort",
        default="deterministic_selftest_27",
        help="stable cohort identifier emitted in ABCOMPAREHDR",
    )
    parser.add_argument("arm_dirs", nargs="+")
    args = parser.parse_args()
    if len(args.arm_dirs) < 2:
        parser.error("at least two arm directories are required")
    return args


def main() -> int:
    args = parse_args()
    arms = {}
    for arm_dir in args.arm_dirs:
        name = pathlib.Path(arm_dir).name.replace("out-", "")
        arms[name] = load(arm_dir)

    names = list(arms)
    cube_ids = sorted(next(iter(arms.values()))[1])
    for name, (_, cubes, _) in arms.items():
        assert sorted(cubes) == cube_ids, f"cube cohort differs in arm {name}"
        for cube_id in cube_ids:
            assert (
                cubes[cube_id]["source_sha256"]
                == arms[names[0]][1][cube_id]["source_sha256"]
            ), f"SOURCE BYTES DIFFER for {cube_id} in {name} — A/B invalid"

    print(
        "ABCOMPAREHDR|schema=LIRIS-30-VS-NEW-AB-V1|arms="
        + ",".join(names)
        + f"|cohort={args.cohort}|same_source_sha=1|uniform_passes_within_arm=1|json=0"
    )

    cohort = {
        name: {"rules": 0, "gain": 0, "glyphs": 0, "tokens": 0, "held": 0}
        for name in names
    }
    wins = {name: 0 for name in names}

    for cube_id in cube_ids:
        row = [f"ABCUBE|cube={cube_id}"]
        best_name = None
        best_gain = None
        tied = False
        for name in names:
            _, cubes, merges = arms[name]
            cube = cubes[cube_id]
            rules = int(cube["accepted"])
            held = int(cube["held"])
            glyphs = int(cube["cold_glyphs"])
            tokens = int(cube["final_tokens"])
            gain = sum(value for _, value in merges.get(cube_id, []))

            cohort[name]["rules"] += rules
            cohort[name]["gain"] += gain
            cohort[name]["glyphs"] += glyphs
            cohort[name]["tokens"] += tokens
            cohort[name]["held"] += held

            density = frac(gain, glyphs)
            row.append(
                f"{name}_rules={rules}|{name}_held={held}|{name}_gain={gain}"
                f"|{name}_density_gain={density.numerator}/{density.denominator}"
                f"|{name}_final_tokens={tokens}"
            )
            if best_gain is None or gain > best_gain:
                best_name, best_gain, tied = name, gain, False
            elif gain == best_gain:
                tied = True

        if tied:
            row.append("denser_arm=TIE|json=0")
        else:
            assert best_name is not None
            wins[best_name] += 1
            row.append(f"denser_arm={best_name}|json=0")
        print("|".join(row))

    def decades(merge_map):
        buckets = defaultdict(int)
        for cube_rows in merge_map.values():
            for pass_number, value in cube_rows:
                buckets[(pass_number - 1) // 10] += value
        if not buckets:
            return "0"
        return ",".join(
            str(buckets.get(index, 0)) for index in range(max(buckets) + 1)
        )

    print(
        "ABDECADES|"
        + "|".join(
            f"{name}_gain_by_10={decades(arms[name][2])}" for name in names
        )
        + "|json=0"
    )

    summary = []
    for name in names:
        values = cohort[name]
        density = frac(values["gain"], values["glyphs"])
        summary.append(
            f"{name}_rules={values['rules']}|{name}_held={values['held']}"
            f"|{name}_gain={values['gain']}"
            f"|{name}_cohort_density={density.numerator}/{density.denominator}"
        )
    print("ABCOHORT|" + "|".join(summary) + "|json=0")
    print(
        "ABWINS|"
        + "|".join(f"{name}={wins[name]}" for name in names)
        + "|metric=per_cube_net_gain|json=0"
    )

    order = sorted(names, key=lambda name: cohort[name]["gain"], reverse=True)
    print(
        f"ABVERDICT|cohort_gain_ranking={'>'.join(order)}"
        "|claim=SHADOW_MEASURED_AB_ONLY|super_cube_formation=HELD"
        "|live_promotion=HELD|archive_ratio=NOT_CLAIMED|json=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
