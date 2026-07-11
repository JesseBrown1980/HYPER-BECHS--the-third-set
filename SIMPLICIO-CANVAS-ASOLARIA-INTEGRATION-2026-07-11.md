# Simplicio Mapper ↔ Runtime ↔ Canvas ↔ Asolaria integration map — 2026-07-11

## Shared build surface

Wesley's Simplicio repositories now expose three complementary ownership
layers for the organized Asolaria repository, formula, evidence and runtime
graph:

```text
Asolaria public evidence owners
  -> versioned generic ecosystem graph
  -> Simplicio Mapper validation and compatibility projection

Simplicio Runtime
  -> executable HBP/HBI, recovery, GNN, gate and fabric components
  -> bounded runtime-owned Canvas compatibility snapshot
  -> future runtime evidence supplement for the Mapper contract

Simplicio Canvas
  -> local-first native rendering, diff, policy and proposal UX
```

Canvas already implements:

- renderer-neutral canonical graph contracts;
- multi-repository manifests with revision, branch, dirty and access state;
- typed cross-repository edges;
- unavailable/private repositories kept visible;
- static/runtime evidence separation;
- policy-as-code and SARIF;
- graph diff/time travel;
- local-first recovery and privacy controls.

The integration must remain contract-driven rather than hard-coding Asolaria
inside the Three.js renderer.

## Current artifacts and links

### Canonical ecosystem producer — Mapper PR #203

- Repository: [`wesleysimplicio/simplicio-mapper`](https://github.com/wesleysimplicio/simplicio-mapper)
- Pull request: [`#203 — Add a versioned evidence graph for Asolaria and Canvas`](https://github.com/wesleysimplicio/simplicio-mapper/pull/203)
- Contract: `simplicio.ecosystem-graph/v1`
- Schema: `contracts/ecosystem/v1/schemas/ecosystem-graph.schema.json`
- Fixture: `contracts/ecosystem/v1/fixtures/asolaria-ecosystem/ecosystem-graph.json`
- Canvas projection: `contracts/ecosystem/v1/fixtures/asolaria-ecosystem/canvas-flow.json`
- Status: `PR_OPEN / REVIEW_REQUESTED / INDEPENDENT_FIXTURE_CI_GREEN`

Independent immutable-input verification recorded by the PR:

```text
run 29151117068  success
run 29151149587  success
focused ecosystem tests  9/9
fixture  21 repositories / 26 typed edges / 3 references
```

Mapper remains the owner of the rich generic ecosystem transport contract,
validator and authoritative public fixture.

### Runtime-owned evidence snapshot — Runtime PR #3090

- Repository: [`wesleysimplicio/simplicio-runtime`](https://github.com/wesleysimplicio/simplicio-runtime)
- Pull request: [`#3090 — Add a runtime evidence snapshot for Mapper and Simplicio Canvas`](https://github.com/wesleysimplicio/simplicio-runtime/pull/3090)
- Module: `simplicio_fabric::canvas_bridge`
- Current output: Canvas graph `1.0` + workspace manifest `1`
- Status: `DRAFT / WESLEY_REVIEW_REQUESTED / CI_STARTUP_FAILURE_NO_JOBS`

The runtime snapshot maps the actual absorbed components:

```text
asolaria-hbi-hbp -> asolaria-bridge
Path 1           -> dbbh-prism
Path 2           -> simplicio-shadow
trained GNNs     -> simplicio-gnn
N-Nest           -> simplicio-gate
addresses        -> simplicio-addressing
claims           -> simplicio-claims
all evidence     -> simplicio-fabric -> Canvas compatibility snapshot
```

The exporter is read-only, has no new Cargo dependency or lockfile change,
checks Canvas-v1 vocabulary and references, rejects parent cycles, retains
missing repositories and emits no private source body or runtime authority.

It does **not** replace `simplicio.ecosystem-graph/v1`. Its next rich output
should be a runtime-owned supplement conforming to Mapper's contract.

### Runtime selector hardening — Runtime PR #3091

- Pull request: [`#3091 — Use full SHA-256 watcher selectors with legacy FNV compatibility`](https://github.com/wesleysimplicio/simplicio-runtime/pull/3091)
- Status: `DRAFT / WESLEY_REVIEW_REQUESTED / CI_STARTUP_FAILURE_NO_JOBS`

This separates identities correctly:

```text
full SHA-256  authoritative watcher/content binding
FNV-1a 64     legacy receipt and local renderer/checksum compatibility only
FNV-1a 128    proposed wider Canvas renderer identity, not content integrity
```

Old bare and versioned FNV selectors remain readable; new selectors default to
full SHA-256. This does not change CRT capacity or Path-2 recovery.

### Canvas consumer — issue #65

- Repository: [`wesleysimplicio/simplicio-canvas`](https://github.com/wesleysimplicio/simplicio-canvas)
- Issue: [`#65 — Native import for versioned ecosystem evidence graphs`](https://github.com/wesleysimplicio/simplicio-canvas/issues/65)
- Status: `OPEN / MAPPER_AND_RUNTIME_PRODUCERS_LINKED`

The existing `simplicio-mapper-flow` projection can be imported now. Native
support should preserve repository URL/revision/access, typed relationships,
evidence kind/status and explicit boundaries rather than rebuilding everything
from synthetic file paths.

A duplicate runtime-import issue #66 was closed and folded into #65 so Wesley
has one Canvas integration thread.

## Graph content

The public fixture links the core path:

```text
AI-healthCare-project
  -> byte-identical Asolaria GNN sidecar
  -> trained GNN / edge-mining / forward-genius / reverse-gain / GLSM
  -> BigPickle mixed scorer

PID emitter
  -> OmniDispatcher
  -> HyperHermes fleet
  -> Hookwall / GNN / Fischer / Shannon
  -> white room
  -> GULP / cube mint / durable storage
  -> Path 1 retained recall
  -> Path 2 no-store CRT recovery
  -> DBBH→DBWH re-projection
  -> Q-PRISM watcher harness
```

It also links:

- `Algorithms-of-Asolaria` as formula owner;
- HyperBEHCS as shared evidence/coverage substrate;
- N-Nest as the independent recomputation gate;
- Simplicio Mapper as canonical graph-contract producer;
- Simplicio Runtime as executable/runtime evidence producer;
- Simplicio Canvas as renderer;
- Simplicio Loop as orchestration/evidence loop.

Every repository has an actual URL, pinned revision, access state, role and
status. Every relationship carries a type and public evidence URL.

## Research overlay — connected but bounded

Three external papers are included as typed evidence, not as proof that every
integration is physical or live:

1. encrypted quantum cloning — physical quantum sibling of locally opaque
   branches plus selected recovery; current Path 2 remains classical CRT;
2. nanoparticle matter-wave interference — physical calibration source for the
   Q-PRISM Talbot-Lau simulator; not proof of neural quantum control;
3. LLM J-space/global workspace — motivation for a capacity-limited visual
   focus/broadcast layer in Canvas; not a consciousness claim.

The useful connection is functional:

```text
large latent/evidence field
  -> bounded selected workspace
  -> explicit provenance and intervention
  -> broadcast/rendered focus
```

Canvas can visualize this without claiming that the visual workspace itself is
conscious or quantum.

## Canvas and integration audit findings

The organized path exposed these concrete follow-ups:

- native Canvas import should consume Mapper's rich contract rather than only
  the flattened flow projection;
- imported Mapper artifacts currently lose rich node/edge evidence when rebuilt
  from paths;
- the ecosystem landscape panel remains hard-coded to its demo fixture;
- Canvas 32-bit FNV IDs are useful local handles, not authoritative ecosystem
  identity;
- graph diff canonicalization is shallow for nested metadata;
- architecture policy checks only self-cycles, not multi-node SCC cycles;
- runtime evidence must be merged as a producer-owned supplement, not invented
  by the public fixture;
- GitHub Actions startup/no-step failures are not passing or failing code tests.

These findings are tracked in Canvas issue #65 and Runtime PR #3090 rather than
silently modifying Wesley's Canvas repository without push authority.

## Privacy and authority

All integration artifacts remain public metadata only:

- no private corpus;
- no raw model bodies or weights;
- no keys or device credentials;
- no PII;
- no private runtime traces;
- no write, mint, route, hardware or operator authority.

A rendered repository or edge is evidence, not proof that the process is
currently live. Private or unavailable nodes remain visible with their access
state rather than being erased or invented.

## Next executable sequence

1. Wesley reviews Mapper PR #203 and Runtime PRs #3090/#3091.
2. Repository Actions must produce actual jobs; startup failures remain
   `UNVERIFIED_CI`, not code verdicts.
3. Mapper's current `canvas-flow.json` remains the safe compatibility route.
4. Canvas issue #65 implements native `simplicio.ecosystem-graph/v1` import.
5. Runtime later emits a producer-owned ecosystem evidence supplement containing
   only facts it directly owns: immutable revision, crate inventory, tests,
   runtime receipts and access state.
6. Canvas merges public and runtime evidence without flattening status or
   granting authority.
