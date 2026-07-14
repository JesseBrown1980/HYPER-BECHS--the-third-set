#!/usr/bin/env python3
"""Compare the 8 vertex-view languages trained on the same native cubes.

Exact integers/fractions only. Asserts every view maps back to the same native
source SHA per cube (the shared quantum key), then measures whether the
orientation languages diverge (different dimensional aspects) or collapse
(redundant relabelings).
"""
import pathlib
import sys
from collections import defaultdict
from fractions import Fraction


def parse_hbp(path):
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        parts = line.split("|")
        yield parts[0], dict(kv.split("=", 1) for kv in parts[1:] if "=" in kv)


def load_result(dirpath):
    cubes, merges = {}, defaultdict(int)
    for tag, f in parse_hbp(pathlib.Path(dirpath) / "FIRST-FLOOR-RESULT.hbp"):
        if tag == "CUBE":
            cubes[f["id"]] = f
        elif tag == "MERGE":
            merges[f["cube"]] += int(f["net_gain"])
    return cubes, merges


def main() -> int:
    argv = sys.argv[1:]
    maps, dirs = [], []
    while argv:
        a = argv.pop(0)
        if a == "--map":
            maps.append(argv.pop(0))
        else:
            dirs.append(a)
    views = {}
    for d in dirs:
        name = pathlib.Path(d).name.replace("out-", "")
        views[name] = load_result(d)

    native = {}   # cube file -> native sha
    view_sha = defaultdict(dict)
    for m in maps:
        for tag, f in parse_hbp(m):
            if tag != "PVMAP":
                continue
            cube, v = f["cube"], f["view"]
            if cube in native:
                assert native[cube] == f["native_sha256"], \
                    f"NATIVE SHA DIVERGES for {cube} — views not on same universe"
            native[cube] = f["native_sha256"]
            view_sha[v][cube] = f["view_sha256"]

    names = sorted(views)
    cube_ids = sorted(next(iter(views.values()))[0])
    for v in names:
        cubes, _ = views[v]
        assert sorted(cubes) == cube_ids, f"cube set differs in view {v}"
        for cid in cube_ids:
            fname = f"LX-{cid.split('-LX-')[1]}.md"
            assert cubes[cid]["source_sha256"] == view_sha[v][fname], \
                f"view {v} trained on unexpected bytes for {cid}"

    print("PVCOMPAREHDR|schema=LIRIS-PYRAMID-VIEWS-COMPARE-V1|views=" + ",".join(names)
          + f"|cubes={len(cube_ids)}|shared_native_sha=1|uniform_passes=1|json=0")

    wins = {v: 0 for v in names}
    spreads = []
    cohort = {v: 0 for v in names}
    for cid in cube_ids:
        gains = {}
        for v in names:
            _, merges = views[v]
            gains[v] = merges.get(cid, 0)
            cohort[v] += gains[v]
        best = max(gains.values())
        worst = min(gains.values())
        winners = [v for v, g in gains.items() if g == best]
        if len(winners) == 1:
            wins[winners[0]] += 1
        mean_num = sum(gains.values())
        spread = Fraction((best - worst) * len(names), mean_num) if mean_num else Fraction(0)
        spreads.append(spread)
        print(f"PVCUBE|cube={cid}|" + "|".join(f"{v}_gain={gains[v]}" for v in names)
              + f"|best={'TIE' if len(winners) > 1 else winners[0]}"
              + f"|spread={spread.numerator}/{spread.denominator}|json=0")

    mean_spread = sum(spreads, Fraction(0)) / len(spreads)
    print("PVCOHORT|" + "|".join(f"{v}_gain={cohort[v]}" for v in names) + "|json=0")
    print("PVWINS|" + "|".join(f"{v}={wins[v]}" for v in names) + "|metric=per_cube_net_gain|json=0")
    order = sorted(names, key=lambda v: cohort[v], reverse=True)
    print(f"PVSPREAD|mean_relative_spread={mean_spread.numerator}/{mean_spread.denominator}"
          "|interpretation=0_means_views_redundant_larger_means_dimensional_aspects_diverge|json=0")
    print(f"PVVERDICT|cohort_ranking={'>'.join(order)}"
          "|claim=SHADOW_MEASURED_ISOLATED|super_cube_formation=HELD"
          "|level_axis=DEFERRED_V2|live_promotion=HELD|archive_ratio=NOT_CLAIMED|json=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
