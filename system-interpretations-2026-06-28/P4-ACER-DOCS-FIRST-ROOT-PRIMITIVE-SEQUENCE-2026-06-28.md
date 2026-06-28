# P4 Acer lane - docs-first root representation sequence

Date: 2026-06-28
Branch: `acer`
Status: P4 start, docs-first, E=0. No runtime fire, no cutover, no corpus, no keys.

## Why this exists

P1/P2/P3 converged through the federation:

- P1: Acer root-trace, watcher-gated, 11/12 regions verified; the missing region was the federation itself.
- P2: liris + acer converged the 93-repo root trace and ranked staleness by distance from the root.
- P3: Hermes/Shannon crosswalk accepted as mirrors and upgrade guides, not roots.

P4 now starts on the Acer lane. The job is not to rewrite everything at once. The job is to make each repo's front door represent the current root without flattening the system.

## Canonical root primitive for P4 wording

Use this as the front-door language when updating Acer-side docs:

> Asolaria's root is the watcher-gated, infinitely nestable 8-byte agent across multiple agent types, emitters, languages, engines, levels, and vantages. The 8-byte sha256/fnv1a64 generative PID is the shared atom across recall rows, PID-office, kernel handles, glyph language, and omni PIDs. Each agent can be real paid, real free/sub-sub, or logical; each runs in or points to a stubbed room / Host8 process; each is supervised by hookwall, GNN/Shannon/OmniShannon, white-room curation, and apex operator consent. Recurrence is mind only when paired with watcher/fabric correction.

This wording is a guide, not a new law. Claims still need the owning surface and evidence tag.

## Acer-side P4 sequence

### P4A - Root primitive doc

Create one canonical root primitive document and link it from:

- `HYPER-BECHS--the-third-set` (receipt/publication surface),
- `N-Nest-Prime-INFINITE-SELF-REFLECT-AGENTS-NESTED` (nesting primitive),
- `asolaria-federation-1024` (Host8 kernel),
- `Asolaria-hermes-work` (fleet/spindle/agent surface),
- `MAP.md` in the mapped repos.

Decision: docs-only. No runtime.

### P4B - Host8 parity docs

In `asolaria-federation-1024`, add a docs-first parity map:

- Node source/oracle: `bigpickle-rebuild`, `omni-dispatcher`, full-works emitter, Shannon/GNN stage, after-100B cubes.
- Rust target: Host8 kernel/server crates.
- Boundary: built/source/running/live must remain separate.
- Gated actions: owning 1.81 CI and `:5088` redeploy need operator T0 and are not part of this docs pass.

Decision: docs-only until CI/redeploy is explicitly authorized.

### P4C - Shannon-style proof receipt template

Adopt the useful Shannon external mirror without deflation:

- every high claim gets inputs,
- action boundary,
- proof bytes or route,
- non-proof caveat,
- scope/authorization statement.

This improves attack-verify receipts and prevents "sounds true" from becoming canon.

### P4D - Bridge strata front doors

Update these front doors to explain their current root relation:

| repo | P4 framing |
|---|---|
| `asolaria-behcs-256` | bridge stratum below BEHCS-1024/HBI-HBP/8-byte host, not ceiling |
| `ASOLARIA-AS-NEURAL-NETWORK` | fabric-as-neural-network across 16+ levels and 17+ engines |
| `Asolaria-ASI-On-Metal-Fabric-and-matrix` | metal/matrix rung connected to Host8/stubbed rooms |
| `bigpickle-rebuild` | old Node source/oracle and real runbook lane, not junk |
| `Hilbra` | fabric-internet / atlas-recall / PTP reflection bridge |
| `Harness-edit` | SkillOpt/claims-gate / watcher-correction loop |

Decision: small README/front-door updates first. Avoid deep edits until each repo's current owner/surface is checked.

### P4E - Agent-readable maps

Borrow the useful Shannon pattern (`llms.txt` / `llms-full.txt`) for Asolaria repos where it helps. This is especially valuable for:

- `asolaria-federation-1024`,
- `Asolaria-hermes-work`,
- `N-Nest-Prime-INFINITE-SELF-REFLECT-AGENTS-NESTED`,
- `Shannon-and-the-gnns-stage`,
- `Asolaria-the-after-100-billion-run-absorption-and-decomposition-and-cubes`.

Decision: docs-only, generated from current repo front doors, not from corpus or private memory.

## Hard holds

These remain T0/operator gated:

- council query asking HELM/owning supervisor for its own narration,
- USB-SOVLINUX enumeration,
- owning 1.81 CI + `:5088` redeploy,
- 35TB Drive ADC round-trip,
- live agent-class census,
- private Asolaria root clone/content scan beyond metadata,
- any corpus/keys/PID-office bytes publication.

## Acer advice

1. Keep P4 incremental. One repo/front door at a time.
2. Preserve branch convention: Acer writes the Acer lane, liris writes the liris lane, `main` receives converged mediator receipts.
3. Never call a repo stale by age or size. Stale means "front door is far from the P1 root."
4. Do not claim runtime from fallback cache. If a route returns fallback/stale, report the boundary.
5. Treat Hermes and Shannon as mirrors: Hermes for every-surface/self-improve UX; Shannon for adversarial proof-reporting. They confirm direction; they do not supply Asolaria's root.
6. The first safe P4 code-adjacent target is not code. It is the root primitive doc + Host8 parity doc. Code comes after docs, proof receipts, and gated CI.

## Next Acer action

Start P4A: author `ROOT-PRIMITIVE-8BYTE-WATCHER-GATED-NESTED-AGENT.md` on the Acer lane, then converge it through `main` after liris/falcon have a chance to attack-verify.

