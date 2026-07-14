# E9 Super-Cube A/B — v1

Operator directive (OP-JESSE, 2026-07-14): repeat the thirty-vs-new-way A/B on enwik9 data,
measure the literal 800-pass arm when the real corpus remains unsaturated, and compare all three
uniform schedules.

## Design

- **Corpus:** enwik9, downloaded in-container and verified against the pinned trilateral receipt
  hash `159b8535…3744bc` before any slicing. Twenty-seven contiguous cubes of 37,037 B each are cut
  from offset 500,000,000 — mid-corpus, well beyond the enwik8 prefix, so every byte is E9 data no
  prior test touched. Total floor: 999,999 B. Every cube is SHA-pinned in an `OLDCUBEREF` manifest;
  the module's source-drift gate re-verifies bytes and SHA at load.
- **Machinery:** identical pinned first-floor module (corrective head lineage `d47b44bd`); the same
  single-language law is used per cube; no super-cube or new language system is minted.
- **Arms (one cloud container each):**
  - `old-30`: 10×3 rule-of-three schedule;
  - `new-100`: 10×10 schedule;
  - `new-800`: 10×80 schedule, launched after the real E9 100-pass curve showed no saturation.
- **Fan-in:** exact-integer comparator (`analyze_ab.py`) reporting per-cube net ledger gain,
  per-decade gain curves, arm wins, holds, and cohort ranking.
- **Uniform training law:** the same pass count is applied to all 27 equal-sized cubes within an arm;
  no per-cube early stopping is allowed in this A/B. Pass count is therefore the only moving variable.

## Measured scope

The per-pass admission rule charges the current two-byte token ledger and six bytes per accepted rule.
Consequently, `ledger_gain/raw` measures recovery from the expanded BEHCS token ledger. It is not a
serialized archive ratio. Any archive claim requires a packed catalog, packed or entropy-coded token
stream, framing, an independent decoder, and exact source-SHA restoration.

The density curve and the separate 50-container holdout curve optimize different objectives:

```text
density curve
  asks whether another same-body merge pays the declared token/catalog ledger

holdout curve
  asks whether the resulting state generalizes to disjoint material
```

A production uniform pass count must therefore be chosen at a validation-optimal checkpoint rather
than automatically at the density-maximal endpoint.

## Boundaries

`SHADOW_MEASURED_AB_ONLY`. No super cube formed; live promotion HELD; 27⁴ HELD; archive ratio
`NOT_CLAIMED`; no Hutter Prize or compression-record claim. This experiment measures exact
single-language floor density on SHA-pinned E9 slices.
