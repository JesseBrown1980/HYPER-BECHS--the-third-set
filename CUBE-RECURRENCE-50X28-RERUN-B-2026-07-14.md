# Cube recurrence 50×28 — fresh rerun B

**Date:** 2026-07-14  
**Repository:** `JesseBrown1980/HYPER-BECHS--the-third-set`  
**Pull request:** `#34`  
**Tested head:** `beb2098f7fdbd3f5eda3dc9947b3e5be8b111a51`  
**Workflow run:** `29325486884` — SUCCESS  
**Receipt-integrity run:** `29325486877` — SUCCESS  
**Aggregate artifact:** `8307874455`  
**Aggregate ZIP SHA-256:** `7bedfbc332470bba8afba14bf3bf56018ac5a88c5dbd2426fc5ee8a220c92094`

## Outcome

```text
requested base-cube containers       50
returned base-cube receipts          50
MEASURED cubes                       49
held cubes                            1
requested perspective rows        1,400
accepted perspective rows         1,372
maximum overlapping runners          20
invalid receipts                       0
```

The held surface remained:

```text
first:30-private-class-copy-wolf-ram-gate
HELD_MISSING_PRIVATE_INPUT
```

The public Wolfram set remained complete at `20/20`. Every eligible cube again returned exactly:

```text
8 reversible representation views
10 black/white Fischer prediction viewpoints
10 exact persistent recurrence passes
= 28 rows
```

All base-cube inverses, all Ring-A inverse views, and all Ring-C byte/model/context gates passed.
Ring-B values remained finite and were retained as predictive measurements rather than mislabeled
archives.

## Ring A — reproduced perspective selection

| Perspective | Wins | Mean complete bpc | Median payload delta | Restore |
|---|---:|---:|---:|---|
| `MIRROR_NIBBLE_SWAP` | **21** | **2.248406** | **−1.494%** | PASS |
| `DBWH_REVERSE_ROTATE_BITS` | **13** | **2.248843** | **−1.401%** | PASS |
| `DBBH_FORWARD_IDENTITY` | **14** | 2.272655 | 0.000% | PASS |
| `DBBH_REVERSE_BYTES` | 1 | 2.319283 | +1.707% | PASS |
| `PI_SLICE_BLOCK_REVERSE` | 0 | 2.405701 | +6.562% | PASS |
| `QPRISM_PRIME_BLOCK` | 0 | 2.472690 | +10.928% | PASS |
| `DBWH_FORWARD_XOR_DELTA` | 0 | 2.709050 | +21.050% | PASS |
| `NESTED_EVEN_ODD` | 0 | 3.288019 | +56.173% | PASS |

Relative to native identity order:

```text
nibble mirror mean gain    1.066996%
bit rotation mean gain     1.047762%
```

Set-specific winners:

```text
first Asolaria/Hutter set
  nibble 16, rotate 9, identity 3, reverse 1

Wolfram set
  identity 11, nibble 5, rotate 4
```

The stable law remains: local reversible byte remaps sometimes help, but the scheduler must choose
per cube. Applying every transformation blindly is worse.

## Ring B — reproduced black/white symmetry and anti-blunder signal

| Predictor | Wins | Mean estimated bpc | Mean accuracy | Mean confident blunders | Mean trust |
|---|---:|---:|---:|---:|---:|
| `BLACK_FORWARD_ORDER_2` | **18** | **4.044052** | 49.9574% | 2,226.00 | 0.156592 |
| `WHITE_REVERSE_ORDER_2` | **11** | **4.044053** | 48.4808% | 2,324.06 | 0.156592 |
| `WHITE_REVERSE_ORDER_1` | **15** | 4.048081 | 29.3292% | 223.37 | **0.160717** |
| `BLACK_FORWARD_ORDER_1` | 5 | 4.048085 | 30.9998% | 220.24 | 0.160716 |
| `BLACK_FORWARD_ORDER_3` | 0 | 4.598760 | 65.3693% | 4,536.12 | 0.090773 |
| `WHITE_REVERSE_ORDER_3` | 0 | 4.598773 | 63.9436% | 4,771.76 | 0.090772 |
| `BLACK_FORWARD_ORDER_4` | 0 | 5.118271 | 73.2004% | 4,957.18 | 0.054747 |
| `WHITE_REVERSE_ORDER_4` | 0 | 5.118282 | 71.8354% | 5,178.31 | 0.054747 |
| `BLACK_FORWARD_ORDER_5` | 0 | 5.522783 | 76.9902% | 4,612.22 | 0.037172 |
| `WHITE_REVERSE_ORDER_5` | 0 | 5.522791 | 75.8524% | 4,822.43 | 0.037171 |

Directional totals:

```text
black wins     23
white wins     26
black trust    50.000023%
white trust    49.999977%
```

The higher-order experts again achieved greater top-1 accuracy while worsening probability log loss
and multiplying high-confidence mistakes. The Fischer mixer therefore needs calibration and explicit
confident-blunder penalties rather than an accuracy-only selector.

## Ring C — reproduced memory improvement and holdout overfit

All `49 × 10 = 490` recurrence passes restored byte-identically and ended with matching encoder and
decoder model/context state.

```text
cubes improved by epoch 10      49 / 49
mean epoch-1 bpc                3.249609
mean epoch-10 bpc               2.091880
mean per-cube change          −34.186162%
median per-cube change        −29.430007%
mean exact checkpoint          89,230.08 B
```

Set means:

```text
first set recurrence change    −33.798104%
Wolfram recurrence change      −34.748847%
```

The disjoint holdout again moved in the opposite direction:

```text
holdout after epoch 1          2.883070 bpc
holdout after epoch 5          3.034234 bpc   +5.243%
holdout after epoch 10         3.118484 bpc   +8.165%
```

The result is independently stable:

```text
same-object memory improves strongly
continued same-object repetition overfits unseen within-cube material on average
```

White Rooms should promote the validation-optimal checkpoint rather than automatically promoting the
latest epoch.

## Comparison with the preceding receipt-bearing seat

Structural outputs reproduced exactly:

```text
50 returned / 49 measured / 1 held
1,372 accepted perspective rows
Ring-A winner counts 21 / 13 / 14 / 1
Ring-B winner counts and black/white totals
49 / 49 recurrence improvement
holdout degradation direction
all restore/state/digest gates
```

Aggregate numerical movement was tiny:

```text
mean recurrence epoch-1 change     −0.000014 bpc
mean recurrence epoch-10 change    −0.000009 bpc
mean recurrence-change delta       −0.000061 percentage point
```

Five arXiv-derived first-set corpus digests changed while their byte counts remained fixed:

```text
19 Language Modeling Is Compression
20 MambaByte
21 Context Tree Weighting
22 Adaptive CTW
25 PMATIC probability synchronization
```

All twenty Wolfram corpus digests were unchanged. The arXiv movement comes from externally fetched,
mutable metadata/text surfaces. Future archival byte-for-byte aggregate repetitions should pin the
retrieved paper bytes or their normalized text artifacts.

## Independent aggregate verification

```text
returned receipts                         50
measured receipts                         49
held receipts                              1
verified perspective rows              1,372
all base artifacts restored              true
all Ring-A paths restored                 true
all Ring-C paths restored/state-matched   true
all Ring-B estimates finite               true
```

Aggregate artifact file SHA-256 values:

```text
CUBE-RECURRENCE-REGISTRY.json
661215dfeb304e343e516a67adf0b72fe0142f4981752886fa83b3241975d48d

CUBE-RECURRENCE-REGISTRY.hbp
45939a5db87dfbdbc7de21cea8933e1cae3473a80741d74cfd6778997a8e0e2a

CUBE-RECURRENCE-50X28-RESULT.md
b19eb7f2e2fc23094698eda9173eef358905b7d201783d76f0ea4becc0e7759d

PERSPECTIVE-WINNER-MAP.json
9c702f6ccf4a12278caea19a524f2cc98fc010a9499302094c2b8d119d85fe9d

INDEPENDENT-ARTIFACT-VERIFICATION.json
54bbbead2883d16d60c8427b0fecf951e5deee794256b1f6930885411945f745

CONCURRENCY-RECEIPT.json
d7c06a68cd365be78bdba70f5b8743c77c963c7228aa2c74fca9674bfc6c049a
```

## Verdict

The full recurrence floor has now reproduced again on a fresh pull-request seat. The most stable
system laws are:

```text
choose reversible views per cube
black and white prediction are complementary
confidence must be calibrated and blunders penalized
recurrence improves memory
validation is required to stop overfitting
all reconstructive claims require exact readback
```

No enwik/Hutter record, physical quantum result, or total-ledger sub-entropy result is claimed.
