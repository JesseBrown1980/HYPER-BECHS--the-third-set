# Pyramid Views v1 — the calculated mechanics of the six pyramids, tested in isolation

Operator directive (OP-JESSE, 2026-07-14): test the new pyramid/dimensional-aspect idea
separately and in isolation; derive the calculated mechanics of the four pyramids beyond the
black/white pair that complete the cube.

## Calculated mechanics (v2 — generators corrected)

A cube decomposes into six face-pyramids (apex at center) = **3 axes × side/anti-side**. Each
axis maps to a measured, exactly invertible transform of the data. **v2 correction:** the
GENESIS/RECENTER cross-seat review caught that v1's `E` (even/odd nesting) is NOT an involution
(it has a distinct inverse), so v1's C₂³ group claim was unproven — v1's eight views remain valid
labeled bijections and their measured baseline stands, but not as a group. The corrected
generators are the **three scales of reversal**, each a genuine involution, all mutually
commuting:

| Axis (scale) | Transform | Measured anchor |
|---|---|---|
| Stream | `R` reverse byte order | Fischer black/white (trilateral, trust ~50/50) |
| Byte | `N` swap the two nibbles per byte | Ring A top perspective (21 wins) |
| Nibble | `Q` reverse bits within each nibble | Ring A bit-level perspective lineage |

Their full composition `RNQ` is **complete bit-order reversal of the entire message** (the total
black↔white flip). The group axioms are NOT assumed: `--group-gates` verifies squares,
commutators, distinctness, and the RNQ-total-reversal property **on the actual sha-pinned
inputs** and emits `GROUP-GATES.hbp`; CI fails unless `C2^3_CONFIRMED_ON_INPUTS`. If confirmed,
the 8 views `{I,R,N,NR,Q,QR,NQ,NQR}` are the algebraic binary cube — 8 vertex labels matching
the 8 DBBH–DBWH pairs. Boundary kept per the review: this is the sign/encoding vertex group,
NOT the cube's 24/48-element spatial symmetry suite, which belongs to the isotropy gates of the
GENESIS/RECENTER contract (G7, 24 proper rotations) in a later rung.

### Adopted divergence taxonomy (from GENESIS/RECENTER CONTRACT v1)

```text
LANGUAGE DIVERGENCE      permitted   (measured here: catalogs may differ per view)
DECODED-LAW DIVERGENCE   not permitted (v2 conjugacy gate: g⁻¹Φg(gU) = Φ(U) — needs propagation harness)
IDENTITY DIVERGENCE      never permitted (restore gates, enforced every pass)
```

### v1 baseline result (100 passes, E-generation views — preserved as measured)

Views diverge decisively (mean relative spread ≈ 0.425): nibble-mirror swept 27/27 cubes and
out-learned the native encoding (217,662 vs 211,182 B, +3.1%); adjacency-preserving views
(n,r,i,nr ≈ 211–218k) vs adjacency-destroying interleave views (≈ 142–144k, −32%) — orientations
that destroy byte adjacency impair pair-based language learning. Pre-registered prediction
half-confirmed: divergence yes, but corpus-wide (one sweeping winner), not cube-specific.

The level axis ("up and down the pyramids" — Q-prism quant-down/readback) is real but not
size-preserving; it is explicitly **DEFERRED to v2**, not dropped, to keep v1 isolated and
single-variable.

## Experiment

- **Isolation:** own branch, own containers, no changes to any sealed lane; the pending 10×10×8
  contract and first-floor evidence are untouched.
- **Cohort:** the same 27 sha-pinned E9 cubes as the E9 A/B (offset 500,000,000, 37,037 B each),
  enwik9 verified against the pinned receipt hash before slicing.
- **Views:** each cube transformed through all 8 vertex views; every transform round-trip
  (`inverse(view(x)) == x`) asserted byte-exact before training; native and view SHA-256 recorded
  in `views-map.hbp` — all 8 views of a cube share one native sha (the "same quantum key").
- **Training:** each view mints its own fresh language in its own cloud container — uniform
  10×10 = 100 passes for every cube in every view (uniform training law; 100 chosen as the
  comparative tier from the E9 A/B, not as a "full" claim).
- **Fan-in (`compare_views.py`, exact arithmetic):** per-cube gain per view, per-cube winning
  view, cohort ranking, and the pre-registered divergence metric: relative spread of gains
  across views per cube.

## Pre-registered question and prediction

**Question:** do the 8 orientation-languages learn DIFFERENT structure on the same bytes
(pyramid sections are genuinely distinct dimensional aspects) or the same structure relabeled
(orientations redundant)?

**Prediction (falsifiable, registered before the run):** views diverge per cube — Ring A's
winner diversity (nibble 21 / rotation 13 / identity 14) predicts cube-specific view preference.
If mean relative spread ≈ 0 and one view wins everywhere, the dimensional-aspect model is
weakened and the formation stack should not multiply by orientation count.

## Boundaries

`SHADOW_MEASURED_ISOLATED`. No super cube formed; 27⁴ HELD; level axis DEFERRED_V2; live
promotion HELD; `archive_ratio=NOT_CLAIMED`; no Hutter/record claim. This measures whether
orientation is a real training dimension — nothing more.
