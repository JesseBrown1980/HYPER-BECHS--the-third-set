# Fischer Bidirectional Codec v3 — ten-runner black/white prediction bench

**Date:** 2026-07-13  
**Status:** executable independent research bench  
**Scope:** classical deterministic prediction and exact lossless coding; not physical quantum cloning

## The idea being tested

The operator's chess/world-model hypothesis is converted into a lawful codec:

```text
five BLACK Fischers
  predict a byte from already-decoded values on its left
  orders 1, 2, 3, 4 and 5

five WHITE Fischers
  predict the same byte from already-decoded values on its right
  orders 1, 2, 3, 4 and 5

one Shannon consensus mixer
  weights the ten predictions by recent calibrated correctness

one Fischer anti-blunder report
  ranks each expert relative to the best expert and emits
  PROCEED / HOLD / BLOCK-style CPL diagnostics

one exact readback gate
  source SHA-256 must equal restored SHA-256
```

The ten independent GitHub matrix jobs are separate runner environments, not ten physical quantum
clones or ten independently networked machines.

## Why the backward model is decodable

A conventional one-pass left-to-right codec cannot use unknown future bytes. This bench uses a
**deterministic pyramid schedule**:

1. decode coarse anchors from left to right;
2. decode interval midpoints;
3. recursively decode the remaining midpoints;
4. at every midpoint, both the nearest decoded values on the left and on the right already exist.

Therefore the white model uses genuine right-hand source context while remaining causal with respect
to the archive's decoding order. Encoder and decoder construct the same task schedule without storing
that schedule in the payload.

The direct comparison is:

```text
BLACK-PYRAMID
  same pyramid schedule, five left-context experts

BLACK+WHITE-PYRAMID
  same schedule, five left-context plus five right-context experts
```

Their byte difference isolates the value of the white/right-side models. `BLACK-SEQUENTIAL` remains a
control for the cost of the pyramid schedule itself.

## Predictor transform

For task `i`, the Shannon mixer emits one byte prediction `p_i`.

```text
hit_i = 1  when p_i = x_i
hit_i = 0  otherwise, and x_i is appended to the miss stream
```

The archive stores:

```text
metadata
+ losslessly coded hit bitmap
+ losslessly coded miss-byte stream
```

The decoder recreates every model prediction. On a hit it emits the prediction; on a miss it consumes
one byte from the miss stream. Both model state and mixer trust are updated from the recovered byte.

This is a predictive transform followed by zstd or zlib. It does not claim the predictor itself is an
entropy coder.

## Bounded-memory experts

Each Fischer uses a fixed hash table:

```text
context hash -> current best byte + confidence
```

The hash includes:

```text
prime-rooted expert identity
context order
pyramid phase
interval scale
already-decoded context bytes
```

The five black prime roots are:

```text
11, 13, 17, 19, 23
```

The five white prime roots are:

```text
29, 31, 37, 41, 43
```

Prime numbers provide deterministic viewpoint lineage and decorrelated hash seeds. They do not create
information or prove statistical independence.

## Shannon consensus and Fischer CPL

The Shannon mixer accumulates integer trust for experts that correctly predict the observed byte and
reduces trust for misses. The chosen symbol maximizes:

```text
sum_j trust_j * (1 + confidence_j)
```

For reporting, each expert receives a codec prediction-loss score relative to the best expert:

```text
CPL_j = round(1000 * max(0, error_rate_j - best_error_rate))
```

and the existing Fischer-style thresholds:

```text
CPL < 150      PROCEED
150..499       HOLD
>=500          BLOCK
```

This codec CPL is a prediction diagnostic inspired by the public Host-8 Fischer evaluator. It does
not replace the federation kernel's authority/proof/cosign evaluator.

## Test matrix

Ten separate runner jobs execute:

```text
BLACK order 1 through 5
WHITE order 1 through 5
```

The composed runner executes and restore-verifies:

```text
black sequential
black pyramid
white pyramid
black + white pyramid
```

on:

```text
first 150,000 bytes of enwik8
first 1,000,000 bytes of enwik8
```

Same-slice baselines are recorded for zstd, gzip, bzip2, xz and PPMd/7z where available.

## Existing Asolaria guards

The workflow also:

- runs property tests over empty, short, random, boundary and multi-block byte strings;
- checks out the public `asolaria-federation-1024` Fischer evaluator at a pinned revision;
- runs the Fischer evaluator package tests/checks under Rust 1.97;
- records the public kernel's CPL/verdict lineage separately from the codec's prediction CPL.

## Acceptance and evidence rules

The run fails when:

```text
any archive fails byte-identical restoration
any SHA-256 differs
any matrix expert fails to produce its report
archive metadata or stream digests disagree
Fischer evaluator compilation/tests fail
```

It does **not** fail merely because white models produce no compression improvement. A negative or
small white delta is valid evidence.

The operator-reported first-flight target:

```text
black only       3.6304 bpc
black + white    3.0820 bpc
white gain       15.1%
trust split      approximately 50/50
```

is treated as an attack-verify target. It is not promoted until the source, exact corpus slice and
sealed output are reproduced.

## Information-theory boundary

The white experts do not manufacture information. The pyramid schedule exposes already-decoded
right-side source context to a better conditional model:

```text
P(x_i | decoded left, decoded right)
```

A better model can lower the entropy-coded residual. The complete archive, model algorithm, metadata
and decoder must still restore the original bytes exactly.

## Output artifacts

```text
expert-audits/black-o1.json ... black-o5.json
expert-audits/white-o1.json ... white-o5.json
150k/*.fsc3 and JSON reports
1m/*.fsc3 and JSON reports
same-slice-baselines.json
fischer-kernel-cargo-test.log
ten-runner-summary.json
SHA256SUMS
```

Every claim is scoped to the exact source bytes, algorithm version, runner environment and archived
readback result.
