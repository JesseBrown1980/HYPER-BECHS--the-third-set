# Simplicio Canvas ↔ Asolaria integration map — 2026-07-11

## Shared build surface

Wesley's `simplicio-canvas` is a strong visualization target for the organized
Asolaria repository, formula, evidence and runtime graph. It already implements:

- renderer-neutral canonical graph contracts;
- multi-repository manifests with revision, branch, dirty and access state;
- typed cross-repository edges;
- unavailable/private repositories kept visible;
- static/runtime evidence separation;
- policy-as-code and SARIF;
- graph diff/time travel;
- local-first recovery and privacy controls.

The correct integration is not to hard-code Asolaria into the Three.js renderer.
It is:

```text
Asolaria public repository/evidence ledger
  -> versioned generic ecosystem graph
  -> Simplicio Mapper validation and compatibility projection
  -> Simplicio Canvas native renderer
```

## Current artifacts and links

### Producer contract — proposed

- Repository: [`wesleysimplicio/simplicio-mapper`](https://github.com/wesleysimplicio/simplicio-mapper)
- Pull request: [`#203 — Add a versioned evidence graph for Asolaria and Canvas`](https://github.com/wesleysimplicio/simplicio-mapper/pull/203)
- Contract: `simplicio.ecosystem-graph/v1`
- Fixture: `contracts/ecosystem/v1/fixtures/asolaria-ecosystem/ecosystem-graph.json`
- Current Canvas projection: `contracts/ecosystem/v1/fixtures/asolaria-ecosystem/canvas-flow.json`
- Status: `PR_OPEN / AUDITED`; fresh GitHub execution is blocked by the repository's no-step Actions condition, not promoted to green.

### Canvas consumer — issue open

- Repository: [`wesleysimplicio/simplicio-canvas`](https://github.com/wesleysimplicio/simplicio-canvas)
- Issue: [`#65 — Native import for versioned ecosystem evidence graphs`](https://github.com/wesleysimplicio/simplicio-canvas/issues/65)
- Status: the existing `simplicio-mapper-flow` projection can be imported now; native rich contract support remains open.

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
- Simplicio Mapper as artifact producer;
- Simplicio Canvas as renderer;
- Simplicio Loop and Runtime as orchestration/runtime evidence surfaces.

Every repository has an actual URL, pinned revision, access state, role and status.
Every relationship carries a type and public evidence URL.

## Research overlay

Three external papers are included as typed evidence, not as proof that every
integration is already physical or live:

1. encrypted quantum cloning — quantum sibling of locally insufficient branches
   plus selected recovery; current Path 2 remains classical CRT;
2. nanoparticle matter-wave interference — calibration source for the Q-PRISM
   Talbot-Lau simulator; not proof of neural quantum control;
3. LLM global workspace — motivation for a capacity-limited visual evidence focus
   layer in Canvas; not a consciousness claim.

## Canvas audit findings

The current Canvas repository is mature and evidence-focused, but this integration
exposed several follow-ups:

- imported Mapper artifacts are rebuilt from paths, losing rich node/edge evidence;
- the ecosystem landscape panel remains hard-coded to its demo fixture;
- graph IDs and recovery checksums are compact 32-bit FNV values, useful as local
  handles but not authoritative ecosystem identity;
- one recovery path writes edge type `calls` while the canonical type is `call`;
- readiness prose and compatibility fixtures describe different capture counts
  without naming the layer/version difference;
- fresh GitHub Actions runs currently fail or skip before steps execute, so current
  CI cannot be treated as an independent green seat.

These findings are attached to Canvas issue #65 rather than silently modifying
Wesley's repository without push authority.

## Privacy and authority

The integration is public metadata only:

- no private corpus;
- no raw model bodies or weights;
- no keys or device credentials;
- no PII;
- no private runtime traces;
- no write, mint, route, hardware or operator authority.

A rendered repository or edge is an evidence surface, not proof that the process
is currently live. Private or unavailable nodes remain visible with their access
state rather than being erased or invented.

## Next executable step

After Mapper PR #203 has healthy independent checks and review, Canvas issue #65
can implement the native parser. Until then, the committed `canvas-flow.json`
projection is the safe compatibility path for opening the Asolaria core graph in
Canvas today.
