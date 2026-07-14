# Thirty vs New-Way Super-Cube A/B — v1

## Authorization and purpose

Operator directive (OP-JESSE, 2026-07-14, voice): build two super-cube candidates from the same
27 base cubes, trained on the exact same data with the same language machinery, differing ONLY in
the number of uniform training passes — the old way (30, the rule-of-three schedule) versus the
new way — run side-by-side in cloud containers, not on local hardware, and measure which floor
comes out denser. "Every cube gets exactly the same amount of passes no matter what" — the
uniform training law applies inside each arm.

## Design

- **Corpus:** the deterministic public selftest 27-cube corpus (identical bytes in every arm,
  asserted by source sha per cube in the comparator). No private data leaves any seat.
- **Machinery:** the pinned first-floor module from the trilaterally sealed corrective head
  `d47b44bd` (digest `067afd92…55ac` lineage). No new language system is minted for this test;
  every arm uses the identical glyph-language implementation.
- **Arms (each in its own cloud container via the CI matrix):**
  - `old-30` — 10 passes × 3 cycles = 30 uniform passes per cube (the measured first floor).
  - `new-100` — 10 passes × 10 cycles = 100 uniform passes per cube (the pass-axis equivalent of
    the proposed 10×10×8 geometry: 10 languages × 10 passes; the full geometry with 10 fresh
    languages and 8 PID views awaits the 10×10×8 harness and will rerun this A/B when it lands).
  - `new-800` — 10 passes × 80 cycles = 800 uniform passes per cube (the literal operator number,
    as a saturation bound).
- **Fan-in:** a compare job downloads all arms and runs `analyze_ab.py` (exact integers/fractions
  only): per-cube rules learned, holds, net gain, density = gain/glyphs, per-decade gain curves,
  cohort totals, per-cube denser-arm wins, and a ranking verdict.

## What this test isolates

Only the PASS variable moves. Language freshness (Axis A) and the 8 PID views (Axis C) are held
constant at the first-floor implementation, so any density difference is attributable to pass
count alone. This is deliberately the clean first cut; the geometry variables get their own A/B
against the same baseline when the 10×10×8 harness exists.

## Boundaries

- No super cube is formed; the arms produce floor-density evidence only.
- `SHADOW_MEASURED_AB_ONLY`; live promotion HELD; 27⁴ HELD; no record claims.
- Uniform training law honored inside each arm: identical pass count for all 27 cubes.
