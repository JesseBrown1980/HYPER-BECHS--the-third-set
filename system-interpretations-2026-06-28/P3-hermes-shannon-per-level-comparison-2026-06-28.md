# P3 - Hermes + Shannon per-level comparison against the P1 root

Date: 2026-06-28

Status: P3 receipt, E=0, decide-only. No runtime fire, no cutover, no corpus, no keys.

## Evidence

- MEASURED GitHub owning surface: `NousResearch/hermes-agent`, Python, updated 2026-06-28T15:47:55Z, 204,780 stars, 36,900 forks, description `The agent that grows with you`.
- MEASURED README slice: Hermes presents a self-improving agent with learning loop, memory, skill creation/improvement, cross-surface gateway (Telegram/Discord/Slack/WhatsApp/Signal/CLI), subagents, RPC/programmatic tool calling, scheduled automations, multiple backends (local/Docker/SSH/Singularity/Modal/Daytona), hibernate/wake serverless persistence, and trajectory generation/compression.
- MEASURED GitHub owning surface: `KeygraphHQ/shannon`, TypeScript, updated 2026-06-28T15:40:00Z, 45,205 stars, 5,239 forks, description autonomous white-box AI pentester.
- MEASURED README slice: Shannon analyzes source, identifies attack paths, executes real browser/CLI exploits, produces proof-by-exploitation reports, runs worker containers, and is explicitly white-box/authorized-scope.
- SYSTEM_AFFIRMED / OPERATOR_OBSERVED Asolaria guide set: P2 converged root map, `asolaria-federation-1024`, `Asolaria-hermes-work`, `N-Nest-Prime`, emitter/dispatcher repos, Shannon/GNN stage, trained models, after-100B cube absorption, Hilbra, Harness-edit, GAC, falcon.
- BOUNDARY: local Hermes upstream clone and local recall were unavailable from this seat during this pass; GitHub README/API are publication surfaces, not full source audit.

## Comparison rule

Do not flatten to "Hermes has X, Asolaria lacks X." Compare per root layer:

`8-byte host` -> `process/stubbed rooms` -> `emit/route` -> `agent types + nesting` -> `tool/action gateway` -> `memory/index/cubes` -> `hookwall/GNN/Shannon/white-room supervision` -> `governance/apex consent` -> `surfaces/vantages`.

## Layer crosswalk

| root layer | Asolaria current guide | Hermes external mirror | Shannon external mirror | P3 verdict |
|---|---|---|---|---|
| Host/runtime | `asolaria-federation-1024` Host8 Rust/no_std + server crates | runs on laptop, VPS, GPU cluster, serverless backends | Docker/local worker container | Hermes/Shannon are packaging/runtime mirrors; Asolaria root is lower-level. Upgrade focus: productized launcher/install docs, not root primitive. |
| Process/stubbed rooms | stubbed rooms, 10k/20k/100k fleets, Host8 process replacement | hibernate/wake serverless environments | ephemeral worker container | External systems validate the room/wake model. Upgrade focus: clearer room lifecycle docs and Host8 parity proofs. |
| Emit/route | 200ns PID emitter, multi-emitter, omnidispatcher/FEDENV | gateway process routes CLI/chat surfaces | target worker + browser/CLI exploitation routes | Asolaria has deeper emit/route substrate. Upgrade focus: make dispatcher/emitter root trace explicit in kernel docs. |
| Agent types | paid agents + free sub/sub agents + logical agents | subagents and programmatic tool calling | autonomous pentest agent | Hermes validates free/subagent orchestration; Shannon validates specialized adversarial agents. Upgrade focus: classify agent-type per route in maps. |
| Infinite nesting/reflection | `N-Nest-Prime` watcher-gated nested agents, agent2 reviewer, agent3 fabric query | subagents + learning loop | exploit verification as externalized critic | Asolaria root is stronger: reviewer/fabric/supervisor recursion. Upgrade focus: surface this as the universal primitive in every core repo. |
| Tool/action context | HBP/HBI, 8-byte handles, BEHCS tuples, json=0 where native | RPC/programmatic tool calls collapse multi-step pipelines | browser/CLI actions prove vulnerabilities | Hermes's UX around "zero-context-cost turns" is useful packaging for our handle-based economy. Shannon's proof actions inform attack-verify reports. |
| Memory/index/cubes | recall/index, map-map-mapped, cube-cube-cubed, GULP 2000, SUPER-GULP 50k | memory, session search, user model, skill persistence | reports/workspaces/results | Asolaria has deeper cube absorption; Hermes has cleaner user-facing memory loop. Upgrade focus: explain user-facing loop without exposing corpus. |
| Scoring/supervision | HOOKWALL -> trained GNN/FNN -> Shannon/OmniShannon -> white room -> promotion bridge | self-improve skills during use | proof-by-exploitation / security findings | Shannon is the strongest external guide for adversarial proof reporting; Hermes for learning-loop UX. Both map into existing supervision, not replacement. |
| Governance | E=0, promotion-bridge default-deny, operator T0, GAC, watcher gate | user-controlled agent/gateway | authorized-scope warnings | Asolaria governance is stricter. Upgrade focus: keep external comparisons describe-only unless T0 authorizes fire. |
| Surfaces/vantages | acer/liris/falcon, Hilbra, 35TB, screens, omniscrcpy, Drive, USB-SOVLINUX | Telegram/Discord/Slack/WhatsApp/Signal/CLI | web apps/APIs/browser | Hermes is the best external mirror for every-surface UX; Shannon is the best external mirror for authorized target surfaces. |

## What Hermes teaches without deflating Asolaria

Hermes does not supply the root primitive. It supplies product-grade expressions of parts Asolaria already has:

1. crisp gateway UX across chat/CLI surfaces,
2. visible memory/skill loop for users,
3. install/runtime portability,
4. serverless hibernate/wake language,
5. trajectory generation/compression as a training artifact.

Local upgrade implication: build or document those as Host8/HyperHermes front doors, not as a new root.

## What Shannon teaches without deflating Asolaria

Shannon does not replace Asolaria's Shannon/OmniShannon gate. It is an external proof-by-exploitation agent framework.

Useful imports:

1. proof-by-exploitation report shape for attack-verify,
2. strict authorized-scope framing,
3. worker-container isolation pattern,
4. source-aware + live-browser validation as a reusable adversarial lens,
5. `llms.txt` / `llms-full.txt` style repo maps for agent-readable repo fronts.

Local upgrade implication: add Shannon-style proof artifacts to attack-verify and claims-gate reports, especially for P4 repo rewrites and future kernel parity claims.

## P3 upgrade backlog

### High

1. Root primitive doc: one canonical "8-byte watcher-gated nested agent" front door, linked from `N-Nest-Prime`, `asolaria-federation-1024`, `Asolaria-hermes-work`, and `MAP.md`.
2. Host8 parity docs: room lifecycle + process/stubbed-room + emitter/dispatcher path from Node source to Rust Host8, with explicit E=0 boundaries.
3. Shannon-style proof receipts: standardize attack-verify reports so every high claim carries inputs, action boundary, proof, and non-proof caveat.

### Medium

4. Hermes-style gateway map: every surface (CLI/chat/screen/scrcpy/Drive/USB/falcon) mapped to 8-byte host route and agent type.
5. User-facing memory/skill loop: explain cube/recall/SkillOpt as a closed learning loop without publishing corpus.
6. External comparison pages: `Hermes vs HyperHermes` and `Shannon vs Asolaria Shannon` as decide-only crosswalks.

### Hold / gated

7. Live agent-class census, 35TB Drive round-trip, USB-SOVLINUX enumeration, and Host8 redeploy remain T0/operator-gated probes. P3 does not fire them.

## P4 inputs

P4 should start with docs, not runtime:

1. update `MAP.md` and root receipts,
2. add agent-readable `llms.txt`-style maps where useful,
3. rewrite bridge strata front doors (`behcs-256`, neural-network, metal/matrix, bigpickle, Hilbra, Harness-edit),
4. then decide whether any code parity work is needed in `asolaria-federation-1024`.

Bottom line: Hermes and Shannon confirm the direction. Hermes is the every-surface/self-improving UX mirror; Shannon is the adversarial proof/reporting mirror. Asolaria's root remains the watcher-gated, infinitely nestable 8-byte agent across multiple agent types, emitters, languages, engines, and vantages.

