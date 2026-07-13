# FISCHER-CODEC-v2 — five black, five white, Shannon consensus, exact restore

**Date:** 2026-07-13  
**Status:** executable independent reference codec and attack-verify bench  
**Scope:** classical deterministic lossless coding; no physical quantum cloning

## Lineage

This experiment translates Jesse Brown's chess-language architecture into a decoder-valid codec:

```text
BLACK Fischer
  predicts from already decoded left context — plays toward the future

WHITE Fischer
  predicts from already decoded right context — plays toward the past

Shannon / OmniShannon
  combines calibrated probabilities and accounts every emitted bit

Bobby Fischer gate
  compares candidate lines block by block and preserves the lower-cost legal move

white room
  keeps winning blocks and compacts losing candidate receipts; nothing is silently deleted

readback
  byte-identical restore + encoder/decoder model-state equality, or HOLD
```

The existing Host-8 Fischer evaluator remains the governance lineage: it emits CPL, verdict, best
alternative, candidate count, proof/center/king-safety axes, and HBP receipts. This codec does not
pretend the governance evaluator itself is a text probability model. It applies the same
anti-blunder principle to competing legal coding lines.

The existing Shannon/GNN stage remains the architectural pipeline:

```text
Hookwall -> GNN ensemble -> Shannon/OmniShannon -> white rooms -> GULP -> exact recovery
```

The first codec flight uses deterministic context experts because a standalone decoder must reproduce
every probability exactly. Trained GNN weights are not silently consulted. A later GNN mixer is legal
only when the exact weights, feature transform, version digest, and decoder implementation are
packaged or pre-shared and charged.

## The ten independent model lanes

```text
BLACK orders 1,2,3,4,5
WHITE orders 1,2,3,4,5
```

Each expert is a fixed-memory hashed binary context model. Context collisions are explicit model
sharing, not hidden source loss. Tables are bounded and deterministic.

Every GitHub expert audit runs in a separate container and emits:

```text
actor PID
direction
context order
ideal log loss
bit accuracy
high-confidence blunder count
model table bytes
occupied slots
```

The combined codec reruns all ten models in one deterministic decoder path.

## The decoder-availability rule

A probability is legal only when the decoder possesses the same conditioning information at that
exact step.

### Conventional black path

Symbols are coded left-to-right. All five BLACK contexts are decoder-known.

### Legal black+white path

A pyramid schedule first codes anchor positions. Interior symbols are then coded only after their
left and right anchors are known. Thus WHITE context is real decoder side information, not a future
oracle.

### Future oracle audit

A separate audit deliberately allows WHITE models to inspect the true unencoded future. It measures
an upper-bound-looking number but is tagged:

```text
ORACLE_NOT_CODEC
```

It cannot be called compression unless the future context or a sufficient model of it is included in
the archive or already retained and charged.

This distinction directly tests the supplied first-flight claim. A large oracle gain and a small
valid-codec gain mean the apparent improvement came mainly from unavailable future bytes.

## Shannon consensus

Each expert predicts a binary probability for every bit. A contextual mixer keeps deterministic
trust by:

```text
bit plane
pyramid stage
left byte class
right byte class
recent calibrated correctness
```

Probabilities are combined in log-odds space. Trust is updated only after the true decoded bit becomes
known, so encoder and decoder evolve identically.

The receipt reports:

```text
BLACK trust share
WHITE trust share
per-expert ideal bits/bit
centipawn-like loss versus the best expert
blunder count
final model-state SHA-256
```

## Fischer tournament

For each independent block the encoder evaluates two legal candidate lines from their own persistent
states:

```text
candidate 0  five BLACK experts, sequential order
candidate 1  five BLACK + five WHITE experts, decoder-valid pyramid order
```

The smaller payload is selected. The decoder reads that move, reconstructs the block, then replays the
recovered bytes through the unselected candidate state. Therefore both candidate civilizations remain
synchronized without transmitting the losing payload.

This realizes:

```text
recognize the blunder
play the better continuation
preserve the losing line as a compact receipt
```

The archive counts:

```text
selected payload
block move byte
raw length
payload length
range-coder flush
file header
```

The report also preserves the full always-BLACK and always-BLACK+WHITE candidate byte totals.

## Exactness gate

A run passes only when:

```text
SHA256(decoded) = SHA256(input)
encoder BLACK state SHA = decoder BLACK state SHA
encoder BLACK+WHITE state SHA = decoder BLACK+WHITE state SHA
archive framing consumed exactly
```

The historical Asolaria codec v0.1 established the same non-negotiable principle: a compression
number is valid only after byte-identical restore.

## Omni integration

The workflow produces reference events for:

```text
RUN_OPENED
10 x EXPERT_AUDITED
FISCHER_CANDIDATES_PLAYED
SHANNON_CONSENSUS
FISCHER_MOVE_SELECTED
WHITE_ROOM_KEEP_COMPACT
FINAL_READBACK
RUN_CLOSED
```

Events are stamped through the merged Catalog47/HyperBEHCS-60D reference contract with actor PID,
run/trace/span identity, UTC/HLC time, event hash, and Merkle root. The live `omni-dispatcher` daemon
is not claimed to have routed these GitHub jobs; the workflow is a reference dispatcher over ten
isolated containers.

## Bench matrix

The first immutable run uses the first 150,000 bytes of public enwik8 to match the supplied Claude
flight scale. It measures:

```text
stride 2
stride 4
stride 8
```

For each stride:

```text
always-BLACK candidate bpc
always-BLACK+WHITE candidate bpc
valid WHITE gain or penalty
block moves selected by Fischer
final tournament bpc
BLACK/WHITE trust split
exact restore
state equality
```

It also measures same-slice:

```text
gzip -9
bzip2 -9
xz -6
zstd -19
```

and the future-oracle audit.

## Claim classes

```text
MEASURED_CODEC
  self-contained archive, exact restore, exact state synchronization

MEASURED_CONDITIONAL
  requires declared retained/pre-shared state, with that state counted elsewhere

ORACLE_NOT_CODEC
  uses target future bytes unavailable to the decoder

REFERENCE_PIPELINE
  Catalog47/Hyper60 events and dispatcher roles executed in CI, not the live daemon

GNN_HELD
  trained mixer weights not in the standalone decoder package
```

## Questions the run answers

1. Does a decoder-valid WHITE path improve the same coding schedule?
2. Does the Fischer tournament ever select the BLACK+WHITE move?
3. Is the supplied 15.1% improvement reproducible without future leakage?
4. Does the Shannon mixer naturally split trust between black and white experts?
5. How far is the valid first flight from standard same-slice compressors?
6. Does every path restore byte-identically?

No outcome is predeclared. Negative and held results remain first-class white-room evidence.
