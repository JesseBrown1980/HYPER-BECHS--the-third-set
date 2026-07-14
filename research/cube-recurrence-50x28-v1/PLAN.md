# Cube recurrence 50×28 — plan

**Date:** 2026-07-14  
**Mode:** fifty source-pinned cube languages, twenty-eight deterministic perspectives each  
**Total requested perspective passes:** `50 × (8 + 10 + 10) = 1,400`  
**Authority:** research branch only; no live-catalog or production promotion

## Correction being implemented

The earlier runs forged each base cube once. That is only the first floor. The next required run is:

```text
Wolfram open-math set       20 cubes
first Asolaria/Hutter set   30 cubes
                           --------
base cube languages         50

for every eligible cube:
  8 reversible geometric/representation views
  10 Fischer prediction viewpoints
  10 persistent recurrence passes
```

The private-input lane from the first set remains a real lane. If its declared source is still absent,
it returns `HELD_MISSING_PRIVATE_INPUT`; it is not replaced by unrelated bytes.

## Ring A — eight reversible DBBH/DBWH perspectives

One source-trained BPE/glyph catalog is held fixed. The same cube language is then applied to eight
invertible views of the exact same corpus:

```text
1  DBBH_FORWARD_IDENTITY       canonical source order
2  DBBH_REVERSE_BYTES          whole-stream reversal
3  DBWH_FORWARD_XOR_DELTA      predecessor-XOR residual
4  DBWH_REVERSE_ROTATE_BITS    reversible bit rotation
5  MIRROR_NIBBLE_SWAP          high/low nibble exchange
6  PI_SLICE_BLOCK_REVERSE      reversible 256-byte block-order mirror
7  NESTED_EVEN_ODD             even-index bytes followed by odd-index bytes
8  QPRISM_PRIME_BLOCK          prime-seeded reversible block permutation
```

For every view:

```text
source -> transform -> fixed glyph catalog -> zstd token payload
       -> token decode -> glyph expansion -> inverse transform -> source
```

The pass is accepted only if the final byte stream and SHA-256 equal the original source. Catalog
bytes are reported both as a shared one-time cost and as a standalone charged cost.

## Ring B — ten Fischer viewpoints

Five black models read left-to-right and five white models read right-to-left:

```text
BLACK orders 1,2,3,4,5
WHITE orders 1,2,3,4,5
```

Each adaptive context model reports:

```text
predictive log loss / estimated bpc
top-1 accuracy
context count
high-confidence blunders
prime-rooted actor PID
normalized OmniShannon trust
```

These ten rows are predictive measurements, not standalone compressed archives. They test which
perspective sees the cube most clearly and how confidence should be penalized by the Fischer kernel.

## Ring C — ten exact persistent recurrence passes

An adaptive order-2 range-code prior is carried through ten encounters with a deterministic training
slice from the cube. Every pass is decoded from an independent clone of the pre-pass state and must
finish with:

```text
byte-identical restore
matching encoder/decoder model state
matching context state
```

At recurrence passes `1`, `5`, and `10`, the current prior is also evaluated on a disjoint holdout
slice without changing the persistent training state. This separates:

```text
same-object memory
from
unseen-within-cube transfer
```

Dense, sparse-estimate, and compressed-checkpoint state costs are reported.

## Base cube

Before the twenty-eight perspectives, each eligible source trains one exact one-level BPE/glyph cube
with 128 merge rules. The model/catalog and token payload are retained as the lane's base artifact.
That base language is what Ring A reuses from eight directions.

## Source sets

### Set 1 — first Asolaria/Hutter swarm

The thirty source definitions come from:

```text
research/hutter-cube-swarm-v1/sources.json
```

This includes Asolaria formulas/quants, HyperBEHCS, Path 1/2, Fischer, Plan B public material,
Cube A/B, Hutter winners, cmix/PAQ foundations, papers, public Google documents, and the private-input
gate.

### Set 2 — Wolfram open-math forge

The twenty source definitions come from:

```text
research/wolfram-open-math-cubes-v1/sources.json
```

Only repositories that pass the existing per-repository license gate enter a reconstructive cube.

## Runner topology

The workflow requests fifty matrix jobs with:

```text
max-parallel: 20
```

because twenty simultaneous GitHub runners were measured in both preceding swarms. Every job remains
alive for at least two minutes so the aggregate can compute observed overlap rather than infer it from
queue order.

The workflow uses fifty containers, not fourteen hundred containers. Each cube container performs its
own twenty-eight perspective passes. This keeps the experiment economically runnable while still
producing fourteen hundred independently stamped perspective rows.

## Required outputs

Per cube:

```text
base-cube.model.json
base-cube.payload.zst
perspective-result.json
perspective-result.hbp
SUMMARY.md
source-receipt.json
runtime.json
SHA256SUMS
```

Aggregate:

```text
CUBE-RECURRENCE-REGISTRY.json
CUBE-RECURRENCE-REGISTRY.hbp
CUBE-RECURRENCE-50X28-RESULT.md
CONCURRENCY-RECEIPT.json
PERSPECTIVE-WINNER-MAP.json
NEXT-CUBE-TOURNAMENT.md
SHA256SUMS
```

## Acceptance gates

```text
base cube restores exactly
all eight reversible views restore exactly
all ten predictor rows are finite and source-stamped
all ten recurrence passes restore and state-match
holdout evaluations restore and state-match
all receipts verify
all nonempty eligible lanes produce exactly 28 perspective rows
missing/private source remains HELD
```

The supplied Asolaria codec's central rule remains binding: no size or learning claim survives without
byte-identical decompression. The previous false v0 result is preserved as the reason for that gate.
