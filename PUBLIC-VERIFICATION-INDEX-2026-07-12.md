# Asolaria public verification index — 2026-07-12

## Purpose

This file is the branch-aware public entry point for artifacts that external search tools have
repeatedly misclassified as missing. A search-engine miss is a discovery failure, not an absence
proof. Verify a claim in this order:

```text
1. resolve the repository directly by owner/name;
2. read repository metadata and visibility;
3. use the repository's declared default branch;
4. follow branch-qualified links for colony-local maps;
5. fetch the exact path;
6. inspect its workflow/receipt where one exists;
7. record NOT FOUND only after the direct path and branch checks fail.
```

Code-search indexes are eventually consistent and can omit newly created, small, branch-local, or
not-yet-indexed repositories and files. The direct repository/contents API is authoritative for
public-file existence.

## HyperBEHCS — public substrate and map home

Repository:
[`JesseBrown1980/HYPER-BECHS--the-third-set`](https://github.com/JesseBrown1980/HYPER-BECHS--the-third-set)

Visibility: **public**. Default branch: `main`.

The shared `main` branch owns doctrine, cross-repository coverage, verification indexes and shared
receipts. The detailed Acer substrate and daemon maps are colony-local and live on the `acer`
branch:

- [HyperBEHCS fourth-generation substrate map — Acer branch](https://github.com/JesseBrown1980/HYPER-BECHS--the-third-set/blob/acer/ASOLARIA-HYPERBEHCS-SUBSTRATE-MAP.md)
- [Daemon → Host-8 migration map — Acer branch](https://github.com/JesseBrown1980/HYPER-BECHS--the-third-set/blob/acer/ASOLARIA-DAEMON-HOST8-MIGRATION-MAP.md)
- [Trilateral reality/evidence doctrine — main](https://github.com/JesseBrown1980/HYPER-BECHS--the-third-set/blob/main/TRILATERAL-REALITY-EVIDENCE-DOCTRINE-2026-07-11.md)
- [45-merge repository coverage ledger — main](https://github.com/JesseBrown1980/HYPER-BECHS--the-third-set/blob/main/ASOLARIA-TRILATERAL-REPOSITORY-COVERAGE-2026-07-11.md)
- [Measured Path-2/storage substrate record — main](https://github.com/JesseBrown1980/HYPER-BECHS--the-third-set/blob/main/MEASURED-PATH2-STORAGE-SUBSTRATE-2026-07-11.md)

The substrate map states the lineage:

```text
Old Index -> BEHCS-256 -> BEHCS-1024 -> HyperBEHCS
```

and maps HyperBEHCS as the binary/hash/hex/crypto tuple-indexing substrate, omniquant-fronted, with
HBP/HBI/SHA/HEX hot paths, spindle waves, portal-per-level routing, storage layout and Host-8
migration surfaces.

## Public Rust recovery repositories

### Path 1 — retained-store recall

Repository:
[`JesseBrown1980/dbbh-coms-quant-prism`](https://github.com/JesseBrown1980/dbbh-coms-quant-prism)

Public artifacts:

- [README](https://github.com/JesseBrown1980/dbbh-coms-quant-prism/blob/main/README.md)
- [Rust source](https://github.com/JesseBrown1980/dbbh-coms-quant-prism/blob/main/src/lib.rs)
- [Rust 1.97 workflow](https://github.com/JesseBrown1980/dbbh-coms-quant-prism/blob/main/.github/workflows/rust-1.97-independent-verification.yml)
- [Independent verification receipt](https://github.com/JesseBrown1980/dbbh-coms-quant-prism/blob/main/verification/INDEPENDENT-VERIFICATION-2026-07-11.hbp)

Public verification state:

```text
workflow asserts exact test count = 19
Claude Fable 5 operator-supplied third seat = 19/19 under rustc 1.97
GPT-directed GitHub Actions = enumeration success, all tests success, artifact upload success
```

### Path 2 — no-store jointly injective recovery

Repository:
[`JesseBrown1980/path2-two-shadow-recovery`](https://github.com/JesseBrown1980/path2-two-shadow-recovery)

Public artifacts:

- [README](https://github.com/JesseBrown1980/path2-two-shadow-recovery/blob/main/README.md)
- [Rust source](https://github.com/JesseBrown1980/path2-two-shadow-recovery/blob/main/src/lib.rs)
- [Rust 1.97 workflow](https://github.com/JesseBrown1980/path2-two-shadow-recovery/blob/main/.github/workflows/rust-1.97-independent-verification.yml)
- [Independent verification receipt](https://github.com/JesseBrown1980/path2-two-shadow-recovery/blob/main/verification/INDEPENDENT-VERIFICATION-2026-07-11.hbp)
- [Watcher-gate tests](https://github.com/JesseBrown1980/path2-two-shadow-recovery/blob/main/tests/watcher_gate.rs)
- [Multi-cylinder tests](https://github.com/JesseBrown1980/path2-two-shadow-recovery/blob/main/tests/multicylinder_qprism.rs)

Public verification state:

```text
workflow asserts exact test count = 30
Claude Fable 5 operator-supplied third seat = 30/30 under rustc 1.97
GPT-directed GitHub Actions = enumeration success, all tests success, artifact upload success
```

### Q-PRISM 3D slice harness

Repository:
[`JesseBrown1980/qprism-3d-slice-harness`](https://github.com/JesseBrown1980/qprism-3d-slice-harness)

This public crate carries the exact classical representation/watcher harness, the 60D/N-D selector
surface and its own Rust 1.97 workflow. It must not be inferred absent from a global code-search miss.

## Public quant and Brown-Hilbert benchmark sources

Both files are public in
[`JesseBrown1980/ASOLARIA-AS-NEURAL-NETWORK`](https://github.com/JesseBrown1980/ASOLARIA-AS-NEURAL-NETWORK):

### Eight-stage quant head/tail benchmark

- [tools/behcs/quant-huge-message-benchmark.mjs](https://github.com/JesseBrown1980/ASOLARIA-AS-NEURAL-NETWORK/blob/main/tools/behcs/quant-huge-message-benchmark.mjs)

The source contains the eight named stages and calibration rows:

```text
JL + Turbo + Polar + Zeta + Triple + Quadruple + JS-histogram + von-Mangoldt
1 MB    -> 3.1 KB tuple; 62x SHA gain
64 MB   -> 3.1 KB tuple; 4,774x SHA gain
256 MB  -> 10,239x SHA; 637x write; 210x compare; 8.1x e2e
1,024 MB-> 66,158x SHA; 2,881x write; 1,781x compare; 6.8x e2e
2,048 MB-> 79,303x SHA; 4,662x write; 1,698x compare; 7.2x e2e; 1,928 MB/s ingest
```

The source itself marks these as Acer calibration rows, distinguishes them from shipped fabric
bindings and keeps semantic fidelity `UNSWEPT` pending the required sweep.

### Brown-Hilbert expansion stress source

- [tools/behcs/brown-hilbert-expansion-stress.mjs](https://github.com/JesseBrown1980/ASOLARIA-AS-NEURAL-NETWORK/blob/main/tools/behcs/brown-hilbert-expansion-stress.mjs)

The public source emits `BHXSTRESSVERDICT`, tests BigInt coordinate arithmetic, mod-3/mod-6
invariants and decimal digest samples, and explicitly scopes the claim as:

```text
address-coordinate-invariants-tested-NOT-enumeration
```

The checked-in default exponent list reaches `1,000,000`; the CLI accepts a custom
`--exponents=` list, including `10,000,000`. A run-specific 10-million receipt should be cited
separately from the existence of the public executable source.

## Public throughput and 111-test receipts

The previously reported “unlocatable” Acer and Liris throughput receipts are public in
`ASOLARIA-AS-NEURAL-NETWORK/docs/`:

- [LIRIS-SPAWN-THROUGHPUT-READBACK-2026-06-11.hbp](https://github.com/JesseBrown1980/ASOLARIA-AS-NEURAL-NETWORK/blob/main/docs/LIRIS-SPAWN-THROUGHPUT-READBACK-2026-06-11.hbp)
- [ACER-SPAWN-THROUGHPUT-READBACK-2026-06-11.hbp](https://github.com/JesseBrown1980/ASOLARIA-AS-NEURAL-NETWORK/blob/main/docs/ACER-SPAWN-THROUGHPUT-READBACK-2026-06-11.hbp)

The Liris receipt publicly records:

```text
pyramid_after_pull = 111of111_PASS
A = 534,136,675 ops/sec
B = 72,775,013 ops/sec
C = 75,926,339 ops/sec
typed = 187,821,997 ops/sec
prior 5.47M/1.73M provenance values retired unless source machine/method are sealed
```

The Acer receipt publicly records:

```text
blob_level_sidecars = ALL_OK
pyramid_at_pull = 111of111_PASS
A = 872,292,078 ops/sec
B = 60,554,516 ops/sec
C = 59,502,860 ops/sec
typed = 137,291,559 ops/sec
```

This proves the receipt rows are public. It does not, by itself, identify every one of the 111 tests
or prove a separately claimed exact sidecar count unless the corresponding suite manifest is also
cited.

## Public whole-system suite

- [FABRIC-FULL-SUITE-TEST-2026-06-16.md](https://github.com/JesseBrown1980/what-is-asolaria---how-do-we-get-reductions-in-everything/blob/main/FABRIC-FULL-SUITE-TEST-2026-06-16.md)

This public receipt reports:

```text
14 PASS / 0 FAIL / 0 PARTIAL
compression suite: 393/393, 0 fail
16 levels
GNN inference
HBI and SHA sidecars
cubes and tensor-collapse
MCP and WebMCP
```

It is a different suite from the 111/111 bilateral contract pyramid; the two counts must not be
collapsed into one benchmark.

## Standard-corpus boundary

A current connected-repository search returned no public matches for:

```text
enwik8
enwik9
Hutter
```

Therefore no public standard-corpus result is claimed here. The existing compression/reduction
receipts target Asolaria's own rosters, indexes, tuple packets, cubes and runtime corpora.

A future enwik8/enwik9 benchmark would be relevant only for a declared **lossless reversible codec**.
It would not validate referential lookup, semantic distillation, approximate quant routing or a
10-byte content-address cube as if those were ordinary Hutter-Prize compression submissions.

## Corrected inventory verdict

The following “not public/not found” conclusions are now false under direct repository/path checks:

```text
HyperBEHCS repository and shared map home absent                 FALSE
Path-1 Rust repository absent                                   FALSE
Path-2 Rust repository absent                                   FALSE
Rust 1.97 exact 19/30 test-count workflows absent               FALSE
independent Path-1/Path-2 verification receipts absent          FALSE
eight-stage quant benchmark source absent                       FALSE
Brown-Hilbert expansion-stress source absent                    FALSE
Liris spawn-throughput receipt absent                           FALSE
Acer 111/111 and sidecar-ALL_OK receipt absent                  FALSE
```

The narrower remaining boundaries are:

```text
exact separate 74-sidecar manifest/count     not established by the two receipts cited above
sealed 10-million-exponent run receipt       not identified here; executable source supports it
public enwik8/enwik9/Hutter result            no match found
physical/live claims                         remain per-seat and per-receipt
```

## Why external inventories missed these files

The recurring causes are:

1. relying on global search before resolving the exact owner/repository;
2. treating a code-search miss as a repository 404;
3. failing to inspect the second repository page/current repository inventory;
4. assuming every file lives on `main` when colony-local maps live on `acer` or `liris`;
5. not following the HyperBEHCS cross-repository coverage ledger;
6. indexing lag after new repositories and verification PRs were published;
7. conflating “tool could not surface it” with “file is not public.”

Use this file as the public discovery root for future receipt audits.
