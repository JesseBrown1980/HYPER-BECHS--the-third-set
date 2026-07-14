# E9-Wide Orbit v1 — the full wiki, sampled end to end

Operator directive (OP-JESSE, 2026-07-14): "Test it on the E9 wiki NOW."

All prior orbit measurements sampled one contiguous 1 MB neighborhood (offset 500 MB). This
experiment draws the 27 sha-pinned cubes **evenly across the entire gigabyte** — one cube every
37 MB from offset 500,000 to the corpus tail — and runs the identical full-depth orbit:
**8 vertex views × 27 cubes × uniform 800 passes**, group gates hard-asserted per view,
round-trips byte-exact, every restore gated.

Only the sampling changes (local neighborhood → whole corpus). Tensors, schedule, views,
comparator, and gates are byte-identical to the mid-corpus orbit, so the two verdicts compare
directly:

- Does **isotropy at depth** (orbit convergence to ~±0.26%) hold across the whole wiki?
- Does the per-cube winner texture change with corpus position (head vs middle vs tail)?
- Ω(epoch 1, wide) mints from the eight wide-view digests and can be compared against the
  mid-corpus Ω lineage.

Boundaries: `SHADOW_MEASURED_ISOLATED`; super-cube formation, 27⁴, live promotion HELD;
`archive_ratio=NOT_CLAIMED`.
