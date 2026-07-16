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
separates the invariant mathematical core from the implementation's one known
non-invariant term:

- **Permutation-equivariant core:** for antipodal pairs
  `I↔RNQ`, `R↔NQ`, `N↔RQ`, `Q↔NR`, the count-predictor and LZ1 gain are invariant under
  the direction-flip plus bit relabeling that relates a view to its complement.
  Equality is forced for that core.
- **Complete measured pipeline:** the numeric-symbol tie-break
  (`symbol < best_symbol`) is not invariant under arbitrary symbol relabeling.
  Consequently, 61 of 108 pair-cells are exact byte ties and the median pair delta is
  0, while the remaining deterministic residuals are the measured chirality term.
- **Across the four pair-classes:** real orientation dependence is **1.4986%**. This,
  not 0.18%, is the honest independent-direction signal after the antipodal pairing is
  factored out.
- **Localized residuals:** the largest measured cascades are cube 18 `N↔QR` at 4.97%
  and cube 22 `Q↔NR` at 7.63%.

The 17 exact per-cube best-ties reported in the sealed findings and the 61/108 exact
antipodal pair-ties are different tie statistics on the same artifact; both stand.

## Symmetry-audit law for Ω-GNN admission

A group-law gate can prove transform-level involution, commutation, and restore while
an implementation detail still breaks learning-level symmetry. Therefore any claimed
invariance must enumerate:

    invariant core
    + every known non-invariant term
    + measured residual under those terms

The Ω-GNN admission contract should hard-gate the algebra and separately receipt this
symmetry audit. `elapsed_ms` previously broke seat symmetry; the numeric-symbol
tie-break breaks parity. Both were discovered by anomaly rather than by an explicit
audit, which is why this law is now required.

## Cross-references

- Algorithms-of-Asolaria main: `findings/OMEGA-REVERSIBILITY-CORRECTION-2026-07-15.md`
  (same correction, merged), `ASOLARIA-INVERSE-PAIR-LAW-2026-07-15.md` (the unified law).
- Standing rule extracted from this incident: any claimed invariance must enumerate its
  non-invariant terms in the receipt.
