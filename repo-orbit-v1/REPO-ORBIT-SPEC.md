# Repo Orbit v1 — the 8-view orbit on Asolaria's own repos (self-referential)

Operator directive (OP-JESSE, 2026-07-14): "train the cubes on my repos." The cube-training
machinery, until now run on enwik9 (Wikipedia — an ungrounded proxy corpus), is turned on the
system's **own knowledge**: a frozen, sha-pinned corpus built deterministically from Jesse's repos.

## Source (frozen, byte-exact)

- `asolaria-repo-corpus.txt` — 727,827 B, sha256 `cf34464d…ae01`, concatenated in deterministic
  sorted order (sorted repos → sorted files) from five repos:
  Algorithms-of-Asolaria, dbbh-coms-quant-prism, qprism-3d-slice-harness, Q-PRISM-human-organoid,
  Metatagging-data-for-a-Quantum-universe (`.md/.py/.rs/.hbp/.hbi/.json/.toml/.yml/.txt`).
- 27 contiguous sha-pinned cubes of 26,000 B each; source-drift gate re-verifies at load.

**GitHub is the Ω over the seats** (operator framing): this corpus is the *published, trimmed*
projection — GitHub "sees parts of the cubes from itself." Each machine (ACER/LIRIS/RELIC) stores
its files differently, so each seat cuts a *different* corpus from the *same* system and learns a
different catalog; the full local trees dwarf this trim. This run is the LIRIS-seat, GitHub-trim
sector at full orbit depth.

## Experiment

Identical machinery to the enwik9 orbit — 8 vertex views (C₂³ from R/N/Q involutions,
group-gated per input) × 27 cubes × uniform 800 passes — only the corpus changes.

Questions:
1. Does **isotropy at depth** (enwik9 converged to ≈±0.26%) hold on the system's own writing?
2. What is the density vs Wikipedia? (100-pass baseline already measured: repo **0.2943** vs
   enwik9 **0.2640** gain/glyph = **~11% denser** — the system's own structured text is more
   learnable by its own glyph language.)
3. Ω(repo) mints from the eight view digests, extending the Ω lineage.

## Receipts

HBP source of record + HBI exact-row projection + SHA-256 sidecars on every artifact
(`REPO-ORBIT-SOURCE.*` for the frozen source; `REPO-ORBIT-COMPARISON.*` sealed in-CI with the
verdict + Ω). `seal_hbi.sh` is the reusable sealer; every HBP/HBI row ends `json=0`.

## Boundaries

`SHADOW_MEASURED_ISOLATED`; `archive_ratio=NOT_CLAIMED` (ledger-gain, not compression);
super-cube formation / 27⁴ / live promotion HELD; the full-local-tree corpus and the
trilateral per-seat runs are deferred design, not claimed here.
