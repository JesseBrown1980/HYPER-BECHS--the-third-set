# Fischer bidirectional ten-seat codec — experiment specification

**Date:** 2026-07-13  
**Status:** executable independent reference experiment  
**Input:** first 150,000 bytes of public enwik8  
**Scope:** classical deterministic context models; not physical quantum cloning

## Lineage and separation of roles

The public `asolaria-federation-1024/servers/fischer-eval` crate is an anti-blunder evaluator. It
assigns CPL, verdicts, best alternatives, proof/authority axes, G4 state, voxel coordinates and HBP
receipts. It is not itself a compression model.

This experiment reuses that evaluator's philosophy in a new predictive codec:

```text
Fischer
  each model records log loss, extreme-confidence mistakes, CPL versus the best peer,
  and a PROCEED / HOLD / BLOCK verdict

OmniShannon
  deterministic recent-agreement weights combine the active model probabilities

White room
  optional joint left/right bridge contexts are rebuilt from already-decoded evidence

DBWH readback
  every archive must decode byte-identically or the run is held
```

The workflow separately executes the real public Rust Fischer evaluator and guards the twelve
canonical OmniShannon finding types. Those checks establish lineage; they do not relabel the
predictive Python code as the original runtime.

## Ten independent seats

Ten GitHub Actions matrix jobs inspect the exact same sealed object:

```text
BLACK / forward-context models
  orders 1,2,3,4,5
  primes 11,13,17,19,23

WHITE / backward-context models
  orders 1,2,3,4,5
  primes 29,31,37,41,43
```

Each job has its own process, memory and model table. These are classical independent executions,
not quantum states or physical clones.

## Why the white context is legal

A normal left-to-right decoder cannot condition byte `x_i` on unknown future bytes. This codec uses
a deterministic pyramid schedule:

```text
1. decode sparse anchors;
2. decode interval midpoints;
3. recurse into the left and right subintervals;
4. at each midpoint, the listed left and right context bytes have already been decoded.
```

Thus the white expert predicts:

```text
P(x_i | already-decoded right context)
```

rather than receiving hidden source bytes. Encoder and decoder generate the same task order and the
same model state.

The schedule has a real price: anchors and coarse levels initially have weak context. The white-model
benefit must exceed that price before the full bidirectional codec can beat an ordinary forward
left-to-right codec.

## Model families

### `black`

Five forward hashed-context models, orders 1–5.

### `white`

Five right-context hashed models, orders 1–5.

### `both`

The ten black/white models mixed by one integer-only adaptive Shannon consensus.

### `omni`

The ten black/white models plus five joint bridge experts. A bridge interleaves already-known left
and right bytes. It represents deterministic white-room synthesis, not newly created source
information.

All model tables are bounded-memory arrays. Prime values seed independent context hashes and provide
readable model lineage; they do not supply information by themselves.

## Runs and controlled hypotheses

Six exact codec configurations run on separate GitHub Actions workers:

```text
black-seq
black-pyr32
white-pyr32
both-pyr32
omni-pyr32
both-pyr64
```

The primary hypotheses are:

```text
H1: both-pyr32 < black-pyr32
    right-context models add predictive value under the same legal schedule

H2: both-pyr32 < black-seq
    the predictive gain exceeds the end-to-end pyramid scheduling price

H3: omni-pyr32 < both-pyr32
    joint left/right white-room contexts add useful predictive structure
```

Each hypothesis can pass or fail independently. No result is forced.

## Same-slice baselines

The aggregate job measures on the identical 150-KB bytes:

```text
gzip -9
bzip2 -9
xz -6
zstd -19
Asolaria codec v0.1
```

The v0.1 lane is the exact predecessor: adaptive order-2 byte context plus carryless range coding,
counted only when decompression restores every byte.

## Fischer and Shannon measurements

Every model reports:

```text
ideal binary log loss
bit-prediction accuracy
number of predictions assigning <10% probability to the true bit
model-table slots touched
prime and actor PID
CPL versus the best of all ten seats
PROCEED / HOLD / BLOCK verdict
```

The aggregate codec reports:

```text
archive bytes and bpc
ideal mixer bpb
black / white / bridge trust shares
encoding and decoding time
input/archive/output SHA-256
byte-identical restore
```

The trust percentages are adaptive model weights. Approximately equal black/white trust is not by
itself evidence of compression gain; actual archive bytes decide.

## Omni event integration

The final aggregate emits Catalog47/HyperBEHCS-60D `OMNIEVENTv1` rows for:

```text
run open
10 independent lens results
6 exact codec results
OmniShannon consensus
white-room synthesis
final readback
run close
```

Every event carries actor PID, UTC/HLC ordering, 47 semantic coordinates, a separate 60×10-bit
selector, prior-event hash and full event hash. Full rows, compact portals and 3D observer shadows are
sealed in the workflow artifact.

## Boundaries

This experiment does not claim:

```text
physical quantum cloning
information creation by reflection
live trained GNN inference
live OmniDispatcher or HyperHermes daemon routing
compression SOTA
Hutter Prize qualification
```

A backward or bridge model may reduce code length because it supplies a better probability model
from lawfully available context. It does not add Shannon information to the source. The only accepted
compression result is the complete archive size with a byte-identical decoder.
