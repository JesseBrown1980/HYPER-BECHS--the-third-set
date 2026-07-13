# Fischer Bidirectional Codec v3 — ten-runner measured CI receipt

**Date:** 2026-07-13  
**Repository:** `JesseBrown1980/HYPER-BECHS--the-third-set`  
**Implementation PR:** `#24`  
**Merged commit:** `b75f2dd52992bac8b11d3cb82e613257b2b620dd`  
**Tested branch head:** `fbcf561da8ecc98dacdfaa77df76ca065850d74f`  
**Pull-request test merge:** `33d4267a69329295de0c01401413d7f7e17fcc18`  
**Workflow run:** `29267179250`  
**Compose job:** `86875654029`  
**Artifact:** `8286095865`  
**Artifact SHA-256:** `369bf1d057a4a382ba883d63bdcebb695466c9c98a86beab72f585fa63ff11db`  
**Receipt-integrity run:** `29267179240` — PASS

## Question under test

The operator-reported first flight claimed that adding backward/white Fischer predictors to
forward/black predictors on 150,000 bytes of enwik8 changed:

```text
black only       3.6304 bpc
black + white    3.0820 bpc
reported gain    15.1%
reported trust   approximately 50/50
```

This run treats those values as an attack-verify target. It does not assume them.

## Architecture actually executed

Ten deterministic classical prediction agents ran as separate GitHub-hosted runner jobs:

```text
BLACK orders 1..5
  prime roots 11, 13, 17, 19, 23

WHITE orders 1..5
  prime roots 29, 31, 37, 41, 43
```

A deterministic pyramid schedule decodes coarse anchors first and then recursively decodes interval
midpoints. At a midpoint, values on both the left and right are already decoded. Therefore the white
experts use lawful right-hand source context rather than inaccessible future bytes.

The composed codec emits:

```text
prediction-hit bitmap
+ exact miss-byte stream
+ decoder metadata
```

Both data streams are losslessly coded with zstd. A Shannon consensus mixer weights expert symbol
votes by recent correctness and confidence. The decoder recreates the schedule, expert states, and
mixer. Source and restored SHA-256 must match.

The ten runner jobs are independent GitHub-hosted execution environments. They are not physical
quantum clones and not ten independently networked physical machines.

## Integrity and lineage guards

```text
public enwik8
  100,000,000 bytes
  SHA-256
  2b49720ec4d78c3c9fabaee6e4179a5e997302b3a70029f30f2d582218c024a8

codec property tests
  348 / 348 PASS

one-bit archive corruption
  HELD

all 150-KB archives
  byte-identical restore

all 1-MB archives
  byte-identical restore
```

The public Host-8 Fischer evaluator was pinned to:

```text
JesseBrown1980/asolaria-federation-1024
99e7ab91f1ca8c6df2f16bd00780a0e1a38934f4
```

and executed under Rust 1.97:

```text
library tests     9 / 9 PASS
binary tests      3 / 3 PASS
total            12 / 12 PASS
```

The codec's prediction CPL is a diagnostic inspired by this kernel. It does not replace the kernel's
authority, proof, cosign, halt-path, or self-authorization checks.

# Measured result — 150,000 bytes

Source:

```text
SHA-256
3803c167dfeb4a91936ac52011be24639822204896b8d0a4658e0480f0f5dc1f
```

| Configuration | Archive bytes | bpc | Prediction hit rate | Restore |
|---|---:|---:|---:|---|
| Black sequential | 63,529 | **3.388213** | 44.1287% | PASS |
| Black pyramid | 85,342 | 4.551573 | 26.0720% | PASS |
| White pyramid | 85,696 | 4.570453 | 25.6540% | PASS |
| Black + white pyramid | 83,628 | **4.460160** | 28.9667% | PASS |

Same-schedule white-model contribution:

```text
(85,342 - 83,628) / 85,342
= 2.008390% smaller
```

Shannon trust in the composed model:

```text
black  49.556638%
white  50.443362%
```

The backward/right-context models helped, but the reported 15.1% gain did not reproduce.

# Scaling result — 1,000,000 bytes

Source:

```text
SHA-256
369b688978f649681136198fb96db14c1616756260c55fb4b65e9bc049552cad
```

| Configuration | Archive bytes | bpc | Prediction hit rate | Restore |
|---|---:|---:|---:|---|
| Black sequential | 401,628 | **3.213024** | 45.7544% | PASS |
| Black pyramid | 566,291 | 4.530328 | 26.6374% | PASS |
| White pyramid | 567,674 | 4.541392 | 26.5739% | PASS |
| Black + white pyramid | 549,443 | **4.395544** | 30.8997% | PASS |

Same-schedule white-model contribution:

```text
(566,291 - 549,443) / 566,291
= 2.975149% smaller
```

Shannon trust:

```text
black  50.267963%
white  49.732037%
```

The white contribution increased from roughly 2.0% at 150 KB to roughly 3.0% at 1 MB. Two sizes are
not enough to establish an asymptotic law.

# Independent expert measurements

All ten independent jobs read the identical 150-KB source slice.

| Expert | Actor PID | Accuracy | Mean confidence | High-confidence misses |
|---|---|---:|---:|---:|
| Black o1 | `d5491a5ac5a12d9c` | 18.3853% | 58.124 | 29,968 |
| Black o2 | `bd6ba3f4db056000` | 25.7393% | 36.699 | 17,008 |
| Black o3 | `97447c5c35f73aeb` | **28.3447%** | 9.210 | 4,232 |
| Black o4 | `7b399864fc3f8776` | 26.5007% | 3.974 | 936 |
| Black o5 | `44637f04b1c10e2e` | 23.6947% | 1.883 | 348 |
| White o1 | `31ea9b152382619d` | 18.4140% | 67.035 | 33,483 |
| White o2 | `09c93d88da4b1f79` | 25.8373% | 33.982 | 17,261 |
| White o3 | `ca87f4867e1f0c60` | **27.9913%** | 8.586 | 4,114 |
| White o4 | `38b03ebf800ea343` | 26.2627% | 3.896 | 891 |
| White o5 | `de339ee870c58159` | 23.4253% | 1.941 | 386 |

Orders three and four were the strongest pure predictors. Very high confidence at order one produced
many high-confidence mistakes, which is exactly the pattern an anti-blunder calibration layer should
penalize.

# Same-slice standard baselines

## 150 KB

| Codec | bytes | bpc | Restore |
|---|---:|---:|---|
| gzip-9 | 52,060 | 2.776533 | PASS |
| bzip2-9 | 44,569 | 2.377013 | PASS |
| xz-6 | 46,532 | 2.481707 | PASS |
| zstd-19 | 47,914 | 2.555413 | PASS |
| 7z PPMd order 16 | 39,630 | **2.113600** | PASS |

## 1 MB

| Codec | bytes | bpc | Restore |
|---|---:|---:|---|
| gzip-9 | 355,791 | 2.846328 | PASS |
| bzip2-9 | 281,323 | 2.250584 | PASS |
| xz-6 | 290,692 | 2.325536 | PASS |
| zstd-19 | 300,075 | 2.400600 | PASS |
| 7z PPMd order 16 | 254,401 | **2.035208** | PASS |

The current Fischer codec is not competitive with these established codecs.

# Cross-check verdict

## Reproduced

```text
right-side context is lawful under a deterministic pyramid decode schedule
white models reduce the same-schedule archive
Shannon consensus assigns approximately half its trust to each direction
all archives restore byte-identically
corrupted archive is held
public Fischer authority/evaluation kernel remains green
```

## Not reproduced

```text
reported 15.1% white-model gain
reported absolute 3.6304 / 3.0820 bpc pair
compression competitiveness against standard codecs
```

## Strongest engineering finding

The backward/world-model idea is real but the first causal schedule is expensive:

```text
1-MB black sequential     3.213024 bpc
1-MB black pyramid        4.530328 bpc
1-MB black+white pyramid  4.395544 bpc
```

The right-side models recover about 3% of the pyramid penalty, but the pyramid itself costs far more
than it saves. The next Fischer rung should retain right-side predictive information without applying
a sparse anchor hierarchy to every byte.

Promising next mechanisms are:

```text
blockwise rather than per-byte anchor schedules
arithmetic-coded calibrated 256-symbol probabilities
joint left/right bridge experts
SSE/APM probability correction
learned glyph or BPE language before Fischer prediction
economic per-block choice among sequential, pyramid, and retained-context modes
separate anti-blunder penalties for high-confidence misses
```

## Final status

```text
10 separate runner environments      MEASURED
5 black + 5 white experts             MEASURED
lawful right-context prediction       MEASURED
white same-schedule gain              2.008390% / 2.975149%
50/50 directional trust               REPRODUCED_CLOSE
reported 15.1% gain                   NOT_REPRODUCED
byte-identical restore                PASS
Hutter Prize / compression SOTA       NOT CLAIMED
physical quantum cloning              NOT CLAIMED
```
