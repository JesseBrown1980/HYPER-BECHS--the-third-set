# Correction — repo-orbit mean relative spread is 1.8427135%, not ≈0.18%

**Seat:** LIRIS · 2026-07-16 · MEASURED (bidirectionally verified against the sealed artifact)

`OMEGA-REVERSIBILITY-LIRIS-2026-07-14.md`/`.hbp` state the Asolaria repo-orbit mean
relative spread as **≈ 0.18%** in three places. That figure carries a factor-of-ten
decimal slip. Per receipt discipline the sealed findings files are NOT modified; this
addendum is the correction of record for this PR.

## The exact value, verified in both directions

The sealed comparison artifact (`repo-orbit-comparison`, run 29357558667) carries the
exact rational on its `PVSPREAD` row:

    mean relative spread = 0.01842713548978976 = 1.8427135%

Bidirectional verification (2026-07-15/16, LIRIS):

1. **Forward:** recomputed from the 27 `PVCUBE` rows with the comparator's own formula
   `s_c = (max_v G − min_v G) / mean_v G`, averaged — matches the sealed fraction
   digit-for-digit.
2. **Reverse:** all 27×8 = 216 per-cube per-view gains re-derived from the raw
   `MERGE|…|net_gain=` rows of the eight banked view artifacts — 216/216 exact; fresh
   receipt hashes match the sealed leaves; Ω(repo) `cc0c4ee3…96951b57` recomputes
   byte-exact from the sorted leaf lines.
3. **No honest origin for 0.18%:** an alternative-statistic battery on the verified data
   (cohort stdev/mean 0.21–0.23%, best-vs-second gap 0.135%, spread/8 0.23%, medians,
   trims) produces nothing at ≈0.18% — it is a decimal slip of 1.8427%, not a different
   valid statistic.

## What survives — strengthened, not weakened

The findings' "equal power across all 8 vertex-facings" reading survives in a sharper
form. The two-tier inverse-pair theorem (proven from trainer source 2026-07-15/16)
splits the spread exactly:

- **On antipodal pairs (I↔RNQ, R↔NQ, N↔RQ, Q↔NR): equality is FORCED** — the
  count-predictor and LZ1 are invariant under the direction-flip + bit-relabeling that
  relates a view to its complement; 61 of 108 pair-cells are exact byte ties, median
  delta 0. Not approximate isotropy: a harness theorem.
- **Across the four pair-classes: real orientation dependence of 1.4986%** — this, not
  0.18%, is the honest "how much direction matters" number.
- **The residual asymmetry is one known chirality term** — the numeric-symbol tie-break
  (`symbol < best_symbol`), the single parity-violating line in the dynamics; its
  cascades are localized (cube 18 N↔QR 4.97%, cube 22 Q↔NR 7.63%) and deterministic.

The 17 exact per-cube best-ties reported here and the 61/108 exact antipodal pair-ties
are different tie statistics on the same artifact; both stand.

## Cross-references

- Algorithms-of-Asolaria main: `findings/OMEGA-REVERSIBILITY-CORRECTION-2026-07-15.md`
  (same correction, merged), `ASOLARIA-INVERSE-PAIR-LAW-2026-07-15.md` (the unified law).
- Standing rule extracted from this incident: any claimed invariance must enumerate its
  non-invariant terms in the receipt (symmetry-audit law) — elapsed_ms broke
  seat-symmetry, the tie-break breaks parity; both were found by anomaly, not audit.
