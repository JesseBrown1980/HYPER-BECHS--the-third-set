# Cube recurrence 50×28 — measured CI receipt

**Date:** 2026-07-14  
**Repository:** `JesseBrown1980/HYPER-BECHS--the-third-set`  
**Pull request:** `#33`  
**Tested head:** `348b5512bdd20e059f1f9eb914305355b2efcbcd`  
**Workflow run:** `29306380531` — SUCCESS  
**Receipt-integrity run:** `29306380528` — SUCCESS  
**Aggregate artifact:** `8300509907`  
**Aggregate ZIP SHA-256:** `6ca4d352e3ad9afd57ef74be9da409025792fce93d18fa1cd24b63616699c8c5`

## Outcome

```text
requested base-cube containers       50
returned base-cube receipts          50
MEASURED cubes                       49
held cubes                            1
requested perspective rows        1,400
returned perspective rows         1,372
maximum overlapping runners          20
invalid receipts                       0
```

The one held surface was:

```text
first:30-private-class-copy-wolf-ram-gate
HELD_MISSING_PRIVATE_INPUT
```

The separate twenty-lane public Wolfram set was fully measured. The held lane is the original first-set
private-input gate, not a failure of the public Wolfram source family.

Every measured cube produced exactly:

```text
8 reversible representation perspectives
10 Fischer prediction perspectives
10 exact persistent recurrence passes
= 28 rows per cube
```

Thus:

```text
49 × 28 = 1,372 accepted rows
```

## First-flight defects and correction

The first flight was preserved as failed development evidence. Its exact gates exposed two deterministic
implementation defects:

```text
1. ASCII-heavy catalogs could allocate learned token IDs below 256.
   Transformed raw bytes could then collide with learned glyph IDs during inverse expansion.

2. The license classifier required a literal "MIT License" title.
   Canonical MIT grants without that heading were incorrectly held.
```

The corrected runner:

```text
reserves IDs 0..255 permanently for raw bytes
starts every learned glyph at ID 256
recognizes MIT by its operative permission and warranty clauses
keeps UNKNOWN sources held
```

The correction did not waive any restore or license gate. It repaired the representation namespace and
license parser, then reran all fifty containers.

# Ring A — eight exact views of every cube

One fixed source-trained glyph catalog was reused from eight reversible perspectives. All 392 measured
Ring-A paths (`49 × 8`) restored the original bytes and SHA-256.

| Perspective | Cubes | Wins | Mean complete bpc | Median payload delta vs identity | Restore |
|---|---:|---:|---:|---:|---|
| `MIRROR_NIBBLE_SWAP` | 49 | **20** | **2.248461** | **−1.494%** | PASS |
| `DBWH_REVERSE_ROTATE_BITS` | 49 | **14** | **2.248793** | **−1.401%** | PASS |
| `DBBH_FORWARD_IDENTITY` | 49 | **14** | 2.272857 | 0.000% | PASS |
| `DBBH_REVERSE_BYTES` | 49 | 1 | 2.319304 | +1.707% | PASS |
| `PI_SLICE_BLOCK_REVERSE` | 49 | 0 | 2.405651 | +6.562% | PASS |
| `QPRISM_PRIME_BLOCK` | 49 | 0 | 2.472188 | +10.928% | PASS |
| `DBWH_FORWARD_XOR_DELTA` | 49 | 0 | 2.709091 | +21.050% | PASS |
| `NESTED_EVEN_ODD` | 49 | 0 | 3.288292 | +56.173% | PASS |

Against the identity view's mean complete rate:

```text
nibble mirror improvement   1.073354%
bit-rotation improvement    1.058783%
```

The result is not “every alternate view helps.” Two simple byte-local bijections helped on average;
block permutations, XOR delta under this fixed catalog, and even/odd nesting generally hurt. The next
scheduler should learn a per-cube view selector rather than apply every transform blindly.

Set-specific winners also differed:

```text
first set:
  nibble 15, rotate 10, identity 3, reverse 1

Wolfram set:
  identity 11, nibble 5, rotate 4
```

The public Wolfram languages were therefore more likely to prefer their native source order, while the
first Asolaria/Hutter set more often benefited from a local reversible remapping.

# Ring B — ten Fischer viewpoints

Five black forward and five white reverse adaptive context models measured each cube. These rows are
predictive log-loss measurements, not complete compressed archives.

| Perspective | Wins | Mean estimated bpc | Mean accuracy | Mean high-confidence blunders | Mean trust |
|---|---:|---:|---:|---:|---:|
| `BLACK_FORWARD_ORDER_2` | **18** | **4.044056** | 49.9575% | 2,226.02 | 0.156592 |
| `WHITE_REVERSE_ORDER_2` | **11** | **4.044057** | 48.4808% | 2,323.98 | 0.156592 |
| `WHITE_REVERSE_ORDER_1` | **15** | 4.048090 | 29.3292% | 223.37 | **0.160716** |
| `BLACK_FORWARD_ORDER_1` | 5 | 4.048094 | 30.9998% | 220.22 | 0.160715 |
| `BLACK_FORWARD_ORDER_3` | 0 | 4.598761 | 65.3693% | 4,536.02 | 0.090773 |
| `WHITE_REVERSE_ORDER_3` | 0 | 4.598775 | 63.9437% | 4,771.65 | 0.090772 |
| `BLACK_FORWARD_ORDER_4` | 0 | 5.118272 | 73.2004% | 4,957.16 | 0.054748 |
| `WHITE_REVERSE_ORDER_4` | 0 | 5.118283 | 71.8354% | 5,178.29 | 0.054747 |
| `BLACK_FORWARD_ORDER_5` | 0 | 5.522783 | 76.9903% | 4,612.20 | 0.037172 |
| `WHITE_REVERSE_ORDER_5` | 0 | 5.522791 | 75.8524% | 4,822.41 | 0.037172 |

Directional totals:

```text
black wins    23
white wins    26
black trust   50.000023%
white trust   49.999977%
```

The black and white mean losses were effectively symmetric. The useful finding is not that one
direction dominates; it is that cube families choose different directions and context orders.

The higher-order experts also demonstrate the Fischer anti-blunder problem sharply: top-1 accuracy
rose with order, yet probability log loss worsened and high-confidence misses multiplied. A production
mixer must score calibrated probability and punish confident wrong patterns; raw accuracy alone is not
an admission metric.

# Ring C — ten exact recurrence passes

All 490 reconstructive recurrence passes (`49 × 10`) restored byte-identically and finished with
matching encoder/decoder model and context state.

```text
cubes improved by epoch 10     49 / 49
mean epoch-1 bpc               3.249614
mean epoch-10 bpc              2.091863
mean per-cube change          −34.186810%
median per-cube change        −29.430007%
mean exact checkpoint          89,229.78 B
```

Set summaries:

```text
first set mean change         −33.799198%
Wolfram set mean change       −34.748847%
```

Largest same-object reductions included:

```text
NNCP / ts_zip material                    −71.0312%
fx2 action-plan documents                 −64.3282%
statistical-compression thesis            −59.0367%
Wolfram FunctionCompile template          −56.0941%
Algorithms-of-Asolaria quant atlas        −48.9172%
```

## The decisive holdout result

The disjoint within-cube holdout moved in the opposite direction on average:

```text
holdout mean after epoch 1     2.883068 bpc
holdout mean after epoch 5     3.034234 bpc   +5.243%
holdout mean after epoch 10    3.118488 bpc   +8.166%
```

Therefore the ten-pass recurrence measured two things at once:

```text
same-object memory             strongly improves
unseen within-cube transfer    degrades on average after continued repetition
```

This is an overfitting signal, not a failure of recurrence. White Rooms should checkpoint model state,
measure a disjoint holdout, and retain the epoch that minimizes the complete validation ledger rather
than always accepting the latest state.

# Base-cube floor

All 49 measured base cubes independently restored. Leading source-language cubes were:

| Set | Cube | Corpus bytes | Base bpc |
|---|---|---:|---:|
| first | `05-glyph-first-floor` | 605,224 | **0.574372** |
| Wolfram | `06-wolfram-agenttools` | 827,336 | **0.709119** |
| Wolfram | `18-wolfram-librarylink-rust` | 922,507 | **0.906157** |
| Wolfram | `03-wolfram-codeparser` | 998,375 | **1.035731** |
| Wolfram | `20-wolfram-asolaria-white-room-bridge` | 998,375 | **1.035731** |
| Wolfram | `16-wolfram-quantum-framework` | 772,796 | **1.041579** |
| first | `28-train-hutter-methods-cube` | 1,000,000 | **1.122504** |
| first | `23-ans-rans` | 1,000,000 | **1.164728** |

These numbers describe each declared source/code/document corpus. They are not enwik8/enwik9 or
Hutter Prize rates.

# Independent verification

The aggregate includes a second artifact-level verifier. It checked all fifty receipts and, for every
measured lane:

```text
base payload digest
base token count and rule count
independent base-cube inverse
all eight Ring-A restores
all ten Ring-C byte/state gates
all ten finite predictor results
```

Result:

```text
returned       50
measured       49
held            1
perspectives 1372
base restore    PASS
status          PASS
```

Aggregate file digests:

```text
CUBE-RECURRENCE-REGISTRY.json
452bc3cf3a2503005a449cf5874c9c22aa79e82819ae00d9895a0c1489c733a7

CUBE-RECURRENCE-REGISTRY.hbp
ff2808116fdb356a3eec52072fd6bb5bde199d70fcb26644f10ef53962ef308f

CUBE-RECURRENCE-50X28-RESULT.md
f11ba1e2ee9f0d27bef969085e6c47644b5a3ce3bad504c09f0b418d62cb7042

PERSPECTIVE-WINNER-MAP.json
95c748b921f1bf3bf80e8ab24177279a497f959cb07dd7a4d4f80652105adab1

INDEPENDENT-ARTIFACT-VERIFICATION.json
21a67a8e41dc7d24f60c1bb91598856d43404627079b750ad817367569696783
```

# Verdict

The requested recurrence floor is measured:

```text
both cube sets included                     YES
fifty base-cube containers returned         YES
8 representation perspectives per cube      YES
10 Fischer perspectives per cube            YES
10 exact recurrence passes per cube          YES
all eligible exact views restored            YES
all eligible recurrence passes state-match   YES
predictor rows finite and source-stamped      YES
maximum simultaneous runners                 20
```

Because the private-input gate remains empty, the accepted total is 49 cubes and 1,372 rows rather
than 50 cubes and 1,400 rows. The public Wolfram set itself is complete at 20/20.

The source-code restore rule remains binding: a compact result is accepted only when its decoder
reproduces the original bytes exactly. Ring B is intentionally excluded from archive claims because it
reports predictor quality rather than a complete decodable bitstream.

No enwik/Hutter record, physical quantum result, or total-ledger sub-entropy result is claimed.
