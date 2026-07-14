#!/usr/bin/env python3
"""Compare uniform-pass arms of the thirty-vs-new-way super-cube A/B.

Exact integers and fractions only; no floats enter any emitted value.
Each arm directory must contain FIRST-FLOOR-RESULT.hbp from the pinned
first-floor module run on the identical deterministic 27-cube corpus.
"""
import pathlib
import sys
from collections import defaultdict
from fractions import Fraction


def load(dirpath):
    hbp = pathlib.Path(dirpath) / "FIRST-FLOOR-RESULT.hbp"
    hdr, cubes, merges = {}, {}, defaultdict(list)
    for line in hbp.read_text(encoding="utf-8").splitlines():
        parts = line.split("|")
        tag = parts[0]
        f = dict(kv.split("=", 1) for kv in parts[1:] if "=" in kv)
        if tag == "FIRSTFLOORHDR":
            hdr = f
        elif tag == "CUBE":
            cubes[f["id"]] = f
        elif tag == "MERGE":
            merges[f["cube"]].append((int(f["n"]), int(f["net_gain"])))
    return hdr, cubes, merges


def frac(n, d):
    return Fraction(n, d) if d else Fraction(0)


def main():
    arms = {}
    for arg in sys.argv[1:]:
        name = pathlib.Path(arg).name.replace("out-", "")
        arms[name] = load(arg)
    if len(arms) < 2:
        print("usage: analyze_ab.py <out-arm1> <out-arm2> [...]")
        return 1

    names = list(arms)
    cube_ids = sorted(next(iter(arms.values()))[1])
    for name, (_, cubes, _) in arms.items():
        assert sorted(cubes) == cube_ids, f"cube cohort differs in arm {name}"
        for cid in cube_ids:
            assert cubes[cid]["source_sha256"] == arms[names[0]][1][cid]["source_sha256"], \
                f"SOURCE BYTES DIFFER for {cid} in {name} — A/B invalid"

    print("ABCOMPAREHDR|schema=LIRIS-30-VS-NEW-AB-V1|arms=" + ",".join(names)
          + "|cohort=deterministic_selftest_27|same_source_sha=1|uniform_passes_within_arm=1|json=0")

    cohort = {n: {"rules": 0, "gain": 0, "glyphs": 0, "tokens": 0, "held": 0} for n in names}
    win = {n: 0 for n in names}
    for cid in cube_ids:
        row = [f"ABCUBE|cube={cid}"]
        best, best_gain = None, None
        for n in names:
            _, cubes, merges = arms[n]
            c = cubes[cid]
            rules = int(c["accepted"]); held = int(c["held"])
            glyphs = int(c["cold_glyphs"]); tokens = int(c["final_tokens"])
            gain = sum(v for _, v in merges.get(cid, []))
            cohort[n]["rules"] += rules; cohort[n]["gain"] += gain
            cohort[n]["glyphs"] += glyphs; cohort[n]["tokens"] += tokens
            cohort[n]["held"] += held
            dg = frac(gain, glyphs)
            row.append(f"{n}_rules={rules}|{n}_held={held}|{n}_gain={gain}"
                       f"|{n}_density_gain={dg.numerator}/{dg.denominator}"
                       f"|{n}_final_tokens={tokens}")
            if best_gain is None or gain > best_gain:
                best, best_gain, tied = n, gain, False
            elif gain == best_gain:
                tied = True
        if tied:
            row.append("denser_arm=TIE|json=0")
        else:
            win[best] += 1
            row.append(f"denser_arm={best}|json=0")
        print("|".join(row))

    def decades(merges):
        buckets = defaultdict(int)
        for cube in merges.values():
            for p, v in cube:
                buckets[(p - 1) // 10] += v
        if not buckets:
            return "0"
        return ",".join(str(buckets.get(i, 0)) for i in range(max(buckets) + 1))

    print("ABDECADES|" + "|".join(
        f"{n}_gain_by_10={decades(arms[n][2])}" for n in names) + "|json=0")

    summary = []
    for n in names:
        c = cohort[n]
        dg = frac(c["gain"], c["glyphs"])
        summary.append(f"{n}_rules={c['rules']}|{n}_held={c['held']}|{n}_gain={c['gain']}"
                       f"|{n}_cohort_density={dg.numerator}/{dg.denominator}")
    print("ABCOHORT|" + "|".join(summary) + "|json=0")
    print("ABWINS|" + "|".join(f"{n}={win[n]}" for n in names)
          + "|metric=per_cube_net_gain|json=0")
    order = sorted(names, key=lambda n: cohort[n]["gain"], reverse=True)
    print(f"ABVERDICT|cohort_gain_ranking={'>'.join(order)}"
          "|claim=SHADOW_MEASURED_AB_ONLY|super_cube_formation=HELD"
          "|live_promotion=HELD|json=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
