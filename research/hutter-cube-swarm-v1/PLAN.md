# Hutter / Asolaria deep-research cube swarm — plan

**Date:** 2026-07-14  
**Mode:** public-repository research and reversible cube-candidate training  
**Authority:** research branch only; no live-catalog, private-drive, hardware, or production promotion

## Objective

Run a broad parallel research-and-training pass from the current Asolaria state rather than treating
one codec, one quant, or one paper as the answer. The swarm combines:

```text
Algorithms of Asolaria
+ the combined quant atlas
+ Fischer / OmniShannon / white-room / glyph-floor work
+ public Plan-B index material
+ Path 1 / Path 2 / Q-PRISM evidence
+ current Hutter Prize winners and source code
+ older PAQ/cmix/CTW/PPM/ANS foundations
+ newer neural/byte-model/online-learning papers
+ exact reversible cube-candidate training
+ same-slice lossless baselines
```

Every lane must return a source-pinned research cube containing:

```text
source identity and commit/digest
people/authors
algorithm and formula vocabulary
implementation surfaces
measured or reported benchmark numbers
Asolaria cross-links
claim boundaries
training-corpus digest
reversible-cube result where applicable
```

## Current Hutter target

The latest public awarded record identified in the source sweep is `fx2-cmix`:

```text
compressor executable       441,463 B
self-extracting archive 110,351,665 B
total                   110,793,128 B
```

A prize-qualifying one-percent improvement must total no more than approximately:

```text
109,685,196 B
0.877481568 bits per enwik9 byte
```

The Hutter FAQ requires the compressed file plus decompressor/model and insists that ideas be combined
with current state-of-the-art compressors. Referential heads, external retained bodies, uncharged
private catalogs, and non-restoring sketches do not qualify as a prize archive.

## Phases

### Phase 0 — intake and boundaries

1. Pin public GitHub sources and current commits.
2. Index the public Plan-B entries already present under `asolaria-behcs-256/data/agent-index`.
3. Search for class-copy material in the checked-out repository.
4. If private Plan-B/class-copy files are absent, emit a `HELD_MISSING_PRIVATE_INPUT` receipt rather
   than pretending they were read.
5. Preserve the uploaded Asolaria codec rule: no compression claim without byte-identical restore.

### Phase 1 — thirty parallel cube sessions

Thirty GitHub-hosted runner jobs are requested through one dynamic matrix. The workflow deliberately
requests `max-parallel: 30` and keeps each lane alive long enough to measure actual overlap. The
aggregate job computes the maximum concurrent interval from runner timestamps. That measured value,
not the requested number, is the account/repository concurrency evidence.

The lanes are divided into:

```text
8 Asolaria architecture/evidence lanes
8 Hutter winner/source-code lanes
10 paper/method/recent-work lanes
4 reversible-training/benchmark/input-gate lanes
```

### Phase 2 — deterministic aggregation

The aggregate job downloads every cube artifact, verifies its source/corpus hashes, preserves failed
or held lanes, builds one registry, computes measured concurrency, and ranks candidate mechanisms by:

```text
exactness / restore evidence
incremental compression potential
model/catalog cost
implementation maturity
memory and runtime feasibility
compatibility with Fischer, glyph floors, Path 1/2, and OmniShannon
novelty versus already-known PAQ/cmix practice
```

### Phase 3 — candidate implementation tournament

The first swarm does research, source archaeology, light compilation, reversible mini-cube training,
and same-slice baselines. It does not spend 50–70 hours on thirty full enwik9 jobs.

The aggregate result will propose a smaller implementation tournament. Expected candidates include:

```text
Fischer anti-blunder logistic/context mixer
blockwise lawful right-context bridge
online reverse dictionary transform
glyph/BPE language before prediction
article similarity reordering
large disk-backed PPM
SSE/APM probability calibration
match and sparse-match models
byte-level Mamba/SSM prior
arithmetic/range or rANS backend
per-block selector choosing the smallest complete archive
```

Every candidate then competes on identical 1 MB, 10 MB, 100 MB, and finally enwik9 lanes with model,
catalog, executable, archive, RAM, disk, time, and restore all charged.

## Private-source status

The GitHub connector is active. A Google Drive connector is **not exposed to this session**, so
private Drive files cannot be read by this workflow. Public Google documents may be fetched through
an export URL if their permissions allow it.

The exact meanings and locations of `class-copy` and `wolf ram` were not found in the connected public
GitHub search. The intake lane records this as ambiguity/missing input and leaves deterministic import
paths for a later connected or committed source. It does not substitute unrelated material under
those names.

## Safety and honesty gates

```text
lossless result       requires byte-identical restore and SHA equality
referential result    must charge/identify retained body
learned result        must charge model/catalog/checkpoint or deterministic replay
external source       must carry URL + commit/digest + license/attribution where known
paper-derived claim   remains literature-derived until code reproduces it
reported benchmark    is never relabeled as locally measured
failed lane           is retained, not silently omitted
```

## Outputs

```text
lane-XX/cube.json
lane-XX/cube.hbp
lane-XX/SUMMARY.md
lane-XX/source-manifest.json
lane-XX/runtime.json

aggregate/SWARM-RESULT.md
aggregate/CUBE-REGISTRY.json
aggregate/CUBE-REGISTRY.hbp
aggregate/CONCURRENCY-RECEIPT.json
aggregate/SOURCE-GRAPH.json
aggregate/NEXT-TOURNAMENT.md
```
