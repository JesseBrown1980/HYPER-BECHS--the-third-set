# Measured Asolaria × Hutter 30-cube swarm result — 2026-07-14

## Execution receipt

```text
repository
  JesseBrown1980/HYPER-BECHS--the-third-set

pull request
  #29

clean tested head
  f2982999acdc962ca0dc591abeb510eb2b8a8bfd

workflow
  Hutter deep-research 30-cube swarm

run
  29295933454

conclusion
  SUCCESS

aggregate artifact
  8296812031

artifact SHA-256
  3ff512cf84bb391f8fa87acbdd73e9bdfac07cb6a801a2182a694e0ab486d21e

receipt-integrity run
  29295933457 — SUCCESS
```

The first attempt exposed a nullable-receipt-rendering defect after every cube body had already been
written. That failed attempt was preserved. The defect was corrected, NumPy was added so the uploaded
Asolaria codec could participate in the baseline lanes, and the complete thirty-session run then
finished green.

## Measured parallelism

```text
requested matrix jobs          30
returned cube sessions         30
maximum overlapping runners    20
invalid cube digests             0
MEASURED sessions               29
HELD sessions                    1
```

The twenty-session maximum is calculated from the overlap of runner-reported start/end intervals.
It is the measured GitHub-hosted-runner concurrency for this repository/account at this moment. It is
not an OpenAI Codex-container limit and is not a promise that GitHub will always schedule twenty.
The remaining ten sessions ran in the next queue wave.

## Input coverage

### Public Asolaria material

```text
Algorithms-of-Asolaria and the combined quant atlas
HyperBEHCS / Catalog47 / Hyper60 / OMNIEVENT
Path 1 / Path 2 / Q-PRISM
N-LENS and N-VANTAGE formulas
Fischer / OmniShannon receipts
first-floor glyph-learning branch
public Plan-B IX agent-index archive
public Cube A/B candidate branch
```

### Hutter and compression material

```text
fx2-cmix
fx-cmix
fast-cmix
STARLIT
cmix
fxcm
paq8pxd
official Hutter FAQ/rules
Matt Mahoney compression references
NNCP and ts_zip
Language Modeling Is Compression
MambaByte
CTW and adaptive CTW
ANS / rANS / FSE implementations
PMATIC probability synchronization
statistical-compression thesis
public fx2 action-plan Google documents
```

The two public fx2 Google documents were exportable and were hashed into their research cube. A
Google Drive connector was not exposed to this session, so no private Drive corpus was read.

### Held private input

```text
class-copy exact source     not found in connected public GitHub
private Plan-B corpus       not present at the declared import path
wolf-ram exact source       not identified
```

Lane 30 therefore returned:

```text
HELD_MISSING_PRIVATE_INPUT
```

No unrelated corpus was silently substituted under those names.

## Public Hutter target indexed by the swarm

The current awarded source lane was pinned to:

```text
repository  kaitz/fx2-cmix
commit      04c5806f99b9b0fa8572be8c8063b4324ec405de

compressor executable       441,463 B
self-extracting archive 110,351,665 B
total                   110,793,128 B
```

Approximate one-percent improvement target:

```text
109,685,196 B
0.877481568 bits per enwik9 byte
```

The source archaeology recovered the main current-winner families:

```text
NLP stemmer and language-dependent text preprocessing
reverse dictionary transform and multiple word streams
Wikipedia parsing and article-similarity ordering
large context maps and context switching
PPM and disk-backed/mmap state
match and sparse-match models
LSTM predictors
logistic mixers
APM/SSE calibration
arithmetic/range-style final coding
self-extracting archive construction
```

These are literature/source-code findings. The swarm did not spend the tens of hours required to
rerun the complete fx2 enwik9 archive.

## Reversible cube training

All three training lanes restored their input byte-for-byte at every tested level. Their bpc values
apply to the declared research/code/document corpora—not to enwik9.

### Public Plan-B IX corpus

```text
corpus bytes     650,963
corpus SHA-256   71e298720b7642170b139987e54f630e0c7395508678b91abe9a62baf9806881

best cube
  2 learned levels
  catalog             2,074 B
  payload           196,943 B
  total             199,017 B
  bpc              2.4458164289
  restore                 PASS
```

Same-corpus exact baselines:

```text
bzip2-9             2.045978 bpc
xz-6                2.171650 bpc
zstd-19             2.227371 bpc
glyph cube          2.445816 bpc
gzip-9              2.824099 bpc
Asolaria codec v0.1 3.098105 bpc
```

The cube beat gzip and codec v0.1, but not bzip2, xz, or zstd.

### Hutter-method source/docs corpus

```text
corpus bytes       1,000,000
corpus SHA-256     6d829297aaa1a153599acb9d71aedc8a42d18802eed8aea09ec4423e39a89481

best cube
  1 learned level
  catalog             1,044 B
  payload           139,611 B
  total             140,655 B
  bpc                  1.125240
  restore                  PASS
```

Same-corpus exact baselines:

```text
xz-6                0.973216 bpc
zstd-19             1.006968 bpc
glyph cube          1.125240 bpc
bzip2-9             1.285928 bpc
gzip-9              1.870248 bpc
Asolaria codec v0.1 2.704896 bpc
```

The low values reflect highly repetitive source code and documentation. They are not Hutter Prize
numbers. The learned cube was reversible but remained behind xz and zstd.

### Combined Asolaria + Hutter research corpus

```text
corpus bytes       1,000,000
corpus SHA-256     4a04737c38944e1939bd8a05684391fec854a5da88d9a4c37ee2e24d07ff438b

best cube
  1 learned level
  catalog             1,044 B
  payload           264,041 B
  total             265,085 B
  bpc                  2.120680
  restore                  PASS
```

Same-corpus exact baselines:

```text
xz-6                1.858752 bpc
zstd-19             1.916280 bpc
bzip2-9             2.020336 bpc
glyph cube          2.120680 bpc
gzip-9              2.280168 bpc
Asolaria codec v0.1 3.191584 bpc
```

Again, the cube was exact and useful as a learned language artifact, but not the strongest standalone
codec on its own training corpus.

## Main design conclusion

The source sweep does not support “one larger quant” as the shortest route to the prize. The strongest
combined architecture is a tournament of complementary organs:

```text
reversible article / word / glyph transform
-> black sequential prediction
-> lawful blockwise white/right-context bridge
-> PAQ/cmix-style context maps and match models
-> Fischer high-confidence blunder penalty
-> logistic mixer plus SSE/APM calibration
-> large disk-backed PPM or selective long-memory model
-> arithmetic/range or rANS backend
-> per-block selector choosing the smallest complete archive
-> byte-identical restore and whole-archive ledger
```

Asolaria contributes orchestration, reversible level languages, anti-blunder gating, persistent
catalogs, storage-backed memory, multiple prediction vantages, provenance, and exact readback. The
Hutter lineage contributes mature text transforms, calibrated probability mixing, match/PPM models,
article ordering, and prize-compliant archive accounting.

## Next implementation tournament

Twelve implementation lanes are specified in `NEXT-TOURNAMENT.md`:

```text
1  Fischer-v4 anti-blunder mixer
2  lawful blockwise black/white bridge
3  FX2 reverse-dictionary/NLP transform port
4  reversible article-ordering experiment
5  disk-backed large PPM
6  PAQ/FXCM context tournament
7  CTW/adaptive-CTW lane
8  small MambaByte/SSM prior
9  PMATIC cross-platform probability synchronization
10 arithmetic/range versus rANS/FSE
11 glyph-first prediction
12 per-block smallest-complete-archive selector
```

A candidate advances from 1 MB to 10 MB to enwik8 only with exact restore and a smaller complete
archive. Only the strongest complete candidates proceed to enwik9.

## Boundary

This run establishes a source-pinned research map, three exact research cubes, one empirical runner
concurrency result, and a concrete implementation tournament. It does not establish a new enwik9
record, a prize submission, or access to absent private files.
