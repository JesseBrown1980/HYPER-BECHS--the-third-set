# E9 Super-Cube A/B — v1

Operator directive (OP-JESSE, 2026-07-14): repeat the thirty-vs-new-way A/B on enwik9 data and
compare the result difference.

## Design

- **Corpus:** enwik9, downloaded in-container and verified against the pinned trilateral receipt
  hash `159b8535…3744bc` before any slicing. 27 contiguous cubes of 37,037 B each are cut from
  offset 500,000,000 — mid-corpus, well beyond the enwik8 prefix, so every byte is E9 data no
  prior test touched. Total floor: 999,999 B (the "1 MB of E9" floor). Every cube sha-pinned in
  an OLDCUBEREF manifest; the module's source-drift gate re-verifies bytes+sha at load.
- **Machinery:** identical pinned first-floor module (corrective head lineage `d47b44bd`); same
  single-language law per cube; no new language system minted.
- **Arms (own cloud container each):** `old-30` (10×3 rule-of-three) vs `new-100` (10×10 —
  pass-axis of 10×10×8). The 800 arm is omitted: the selftest A/B measured new-800 byte-identical
  to new-100 (passes 41–800 = pure HOLDs).
- **Fan-in:** the same exact-arithmetic comparator (`analyze_ab.py`): per-cube density
  (gain/glyphs), per-decade gain curves, denser-arm wins with explicit ties, cohort verdict.
- **Uniform training law:** identical pass count for all 27 cubes inside each arm; no
  size-scaling, no early stopping. (All cubes are equal-sized here by construction, which also
  removes size as a confound entirely.)

## Boundaries

`SHADOW_MEASURED_AB_ONLY`. No super cube formed; live promotion HELD; 27⁴ HELD; and explicitly:
this measures glyph-language floor density on E9 slices — it is NOT a Hutter Prize attempt and
claims no compression record.
