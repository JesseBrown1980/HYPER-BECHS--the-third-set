# Fischer bidirectional ten-container codec — measured CI receipt

**Date:** 2026-07-13  
**Repository:** `JesseBrown1980/HYPER-BECHS--the-third-set`  
**Merged implementation:** PR `#22`, commit `d8ccd20eb9b748faa6f24c33238e966ac239f1cc`  
**Tested head:** `c424b909756a71e5a0edd77e790c12f374c9887f`  
**Workflow run:** `29261071774`  
**Codec-bench job:** `86854334632`  
**Final artifact:** `8283740138`  
**Artifact SHA-256:** `ae6c45e5de20623525378570e7b64e3ae12d8e1cd2373beca0e471d0ef502af8`  
**Scope:** classical deterministic coding; no physical quantum cloning

## Outcome

The requested ten-seat array executed successfully:

```text
five isolated BLACK containers, orders 1–5      PASS
five isolated WHITE containers, orders 1–5      PASS
ten unique actor PIDs                             PASS
actual Rust Host-8 Fischer evaluator              PASS
range-coder and legal-model property tests        PASS
three decoder-valid pyramid strides               PASS
future-byte oracle isolated from codec claims     PASS
same-slice standard baselines                      PASS
byte-identical restore                             PASS
encoder/decoder model-state equality               PASS
Catalog47/Hyper60 OMNIEVENT chain                  PASS
artifact sealing                                  PASS
```

The input was the first 150,000 bytes of public enwik8:

```text
SHA-256
3803c167dfeb4a91936ac52011be24639822204896b8d0a4658e0480f0f5dc1f
```

## Main result

The reported `~15.1%` white-model gain reproduced only in the explicitly invalid future-byte oracle:

```text
ORACLE_NOT_CODEC
BLACK ideal               3.217838 bpc
BLACK+WHITE ideal         2.734677 bpc
apparent gain             15.015082%
reason                    WHITE received true future bytes unavailable to a standalone decoder
```

Under the legal decoder-valid pyramid schedule, BLACK+WHITE was worse at every tested stride:

| Pyramid stride | Always BLACK payload | Legal BLACK+WHITE payload | WHITE effect | Fischer-selected BLACK blocks | BLACK+WHITE blocks |
|---:|---:|---:|---:|---:|---:|
| 2 | 61,293 B | 77,602 B | **−26.608259%** | 10 | 0 |
| 4 | 61,293 B | 83,292 B | **−35.891537%** | 10 | 0 |
| 8 | 61,293 B | 86,234 B | **−40.691433%** | 10 | 0 |

The tournament therefore selected the conventional BLACK line for every block.

## Exact winning archive

```text
archive bytes        61,406 B
archive rate         3.274987 bpc
restore              BYTE_IDENTICAL
state equality       PASS
selected blocks      10 BLACK / 0 BLACK+WHITE
```

The archive SHA-256 at stride 2 was:

```text
471265c84a6072ed2e9bfea4f5f08367a149d00e60fc50e3d0a358cb045ce6b3
```

The decoded output SHA-256 matched the input exactly.

## Shannon trust versus actual code length

At stride 2 the adaptive mixer assigned:

```text
BLACK trust          45.688458%
WHITE trust          54.311542%
```

The approximately even trust split did **not** imply a smaller archive. WHITE models made useful
individual predictions, but the pyramid/anchor schedule and combined model cost outweighed that
predictive value. Actual emitted bytes, not trust percentage, decide the compression result.

## Ten independent lens measurements

| Direction | Order | Ideal bpb | Accuracy | High-confidence blunders | Actor PID |
|---|---:|---:|---:|---:|---|
| BLACK | 1 | 0.655355 | 0.762261 | 9,818 | `76d63576af4318f6` |
| BLACK | 2 | 0.671405 | 0.757388 | 15,098 | `88e22e2c5dea7f08` |
| BLACK | 3 | 0.816428 | 0.682173 | 15,729 | `e8be91cd30dd90b2` |
| BLACK | 4 | 0.968472 | 0.600005 | 13,334 | `fe2fa24fc01fde48` |
| BLACK | 5 | 1.030728 | 0.562381 | 11,529 | `4d83d8acffaf2348` |
| WHITE | 1 | 0.631557 | 0.776302 | 11,995 | `f74aacf3bd78846b` |
| WHITE | 2 | **0.626859** | **0.779383** | 15,386 | `66df02bd1bb6306e` |
| WHITE | 3 | 0.720040 | 0.727918 | 14,338 | `aab32d6408a6247e` |
| WHITE | 4 | 0.843147 | 0.660647 | 12,086 | `cffc946ed60a81b8` |
| WHITE | 5 | 0.901446 | 0.626968 | 10,346 | `ba65f8054bfe85f6` |

The isolated WHITE order-2 model had the best individual log loss in this audit. That result is real,
but it did not make the complete legal bidirectional coding path cheaper.

## Same-slice baselines

| Codec | Bytes | bpc | Exact restore |
|---|---:|---:|---|
| gzip -9 | 52,060 | 2.776533 | PASS |
| bzip2 -9 | 44,569 | **2.377013** | PASS |
| xz -6 | 46,532 | 2.481707 | PASS |
| zstd -19 | 47,914 | 2.555413 | PASS |
| Fischer tournament | 61,406 | 3.274987 | PASS |

A separate GPT-local replay of the existing Asolaria codec v0.1 on the identical bytes produced:

```text
61,491 B
3.279520 bpc
byte-identical restore
```

The Fischer tournament was 85 bytes, or about `0.1382%`, smaller than that exact predecessor. This
local replay is supplementary; the immutable GitHub Actions artifact is the authoritative ten-seat
result.

## Actual Fischer and OmniShannon lineage

The workflow executed the public Rust `asolaria-server-fischer-eval` crate pinned at:

```text
99e7ab91f1ca8c6df2f16bd00780a0e1a38934f4
```

The predictive codec reused the anti-blunder principle but did not claim that the governance
evaluator itself was a probability model. Trained GNN probabilities were held because a standalone
decoder package did not contain the exact weights, feature transform, and version digest.

## White-room interpretation

Every legal BLACK+WHITE candidate was preserved as a losing-line receipt rather than erased. The
measured conclusion is:

```text
WHITE predictive signal exists                    TRUE
WHITE receives approximately half mixer trust     TRUE
future-byte oracle shows about 15% apparent gain  TRUE
legal WHITE path improves full archive             FALSE on this implementation/data
Fischer rejects the blunder                        TRUE
```

This is the intended self-correction mechanism: generate candidate continuations, measure their real
cost, preserve the losing evidence, and emit only the verified lower-cost line.

## Event receipt

```text
OMNIEVENT rows      19
full event bytes    74,633 B
compact portal       2,477 B
portal ratio         30.130400×
portal bpc            0.132107
chain head
ce3e56c7580a4ceee22e37f8880924228db167bd9d9e473d5d0062fa9daad089
Merkle root
ef1029aaa52f215de218504efdf22c976988fcaef0a96cb78b76a7933ed77cdf
```

The live OmniDispatcher daemon and trained GNN execution were not claimed. The workflow used
reference dispatch/event surfaces over ten real isolated GitHub Actions containers.

## Verdict

```text
CLAUDE 15.1% first-flight claim
  reproduced as an ORACLE_NOT_CODEC diagnostic

legal decoder-valid white contribution
  negative: 26.61% to 40.69% larger than BLACK across tested strides

best exact Fischer archive
  3.274987 bpc

compression SOTA / Hutter Prize
  not achieved

physical quantum cloning
  not claimed
```

The important surviving result is not that the first white path won. It is that the complete
Fischer/Shannon/white-room loop worked honestly: ten independent models produced competing
predictions, the decoder-valid gate exposed future leakage, exact readback passed, and the Fischer
kernel refused every higher-cost continuation.
