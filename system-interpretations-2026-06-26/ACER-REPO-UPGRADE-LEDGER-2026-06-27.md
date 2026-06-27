# acer repo-upgrade ledger — what's upgraded, what's dirty, what's left (2026-06-27)

Seat: acer (Claude Opus 4.8) · Source: operator's GitHub repo list (the map) + owning-gate sweep (`gh search prs --owner JesseBrown1980`) + this session's migration knowledge. Answers the operator's four questions. Bilateral: liris answered from the mirror; this is the acer owning-seat version + the durable ledger liris recommended.

## TL;DR (the honest answers)
1. **Why so many "old" repos?** ~70 repos, but only **~21 are Asolaria-core.** The rest = **8 upstream forks** (not ours to upgrade) + **~40 pre-2026 personal/client projects** (unrelated to Asolaria) + the **my-history×12** stubs. The Asolaria *old* repos that ARE ours are **preserved strata** (proof history / old execution layer), not trash — per the OLD-vs-NEW law, don't delete/deflate the OLD until Host-8 has parity.
2. **Did I realize the dirty repos?** Honestly — not until I swept it just now. The real dirt is **NOT "old repo exists"**; it's **62 open unreconciled PRs** (≈**40 on Asolaria-core**), led by `what-is-asolaria` (**19**), the private root (**5 drafts**, incl. the structural main-adoption #6), `Algorithms-of-Asolaria` (5), `Asolaria-ASI-On-Metal-Fabric` (3), and **2 DIRTY** federation PRs (#7/#10). Ironically I'd been *adding* Host-8 PRs without reconciling the backlog.
3. **What still needs upgrading?** (a) reconcile the ~40 core open PRs (merge-good / close-superseded / rebase-DIRTY); (b) the root structural main-adoption (#6, no-common-ancestor); (c) Host-8 runtime gaps — `:4947` bus, remaining `:4949` routes/UI, Hilbra `:4790` refresh, the remaining 47-daemon-map ports; (d) decide retire-vs-port for stub/strata lanes.
4. **Considered + updated where needed?** The classification below covers **all** repos. Doctrine + root README + recall reindex + 2 Host-8 upgrades (dashboard #12, DSpark scheduler #13) are **done**. The PR backlog + structural + runtime gaps are **pending** (the work-list below). Not every repo is byte-audited; not every old runtime has a Host-8 replacement yet.

## Classification (all repos)

### A · Host-8 kernel — CURRENT (upgrades land here)
- **asolaria-federation-1024** (Rust) — the live Host-8 kernel. Merged this session: dashboard-serve `:4949` (#12 `36ceca8`), council confidence-schedule (#13 `1fb9bd1`). **Dirty:** PR **#7** (hookwall-rs) + **#10** (cosign-shadow) both `DIRTY` → rebase or close. **Gaps:** `:4947` bus, `:4949` routes/UI, more daemons.

### B · Receipts / coordination
- **HYPER-BECHS--the-third-set** — bilateral receipts (this doc). Healthy.

### C · Doctrine / explanatory (doctrine README propagated)
- **what-is-asolaria...** — ⚠️ **19 open PRs** (the single dirtiest repo; a findings backlog) → triage merge/close. **Algorithms-of-Asolaria** (5), **Asolaria-ASI-On-Metal-Fabric-and-matrix** (3), **ASOLARIA-AS-NEURAL-NETWORK** (1), **35-TB-google-AI-Ultra-migration** (1), **Asolaria-gac-working** (1 draft), **Omni-Asolaria-ASI-OS-Matrix-Fabric**, **Hilbra**, **NOT-WEDGED-SYSTEM-RULE**. Doctrine landed; the open PRs need reconciliation.

### D · OLD-system strata — PRESERVE (proof history; don't delete/deflate)
- **bigpickle-rebuild** (the BUILD-and-upgrade suite + 100B/BigPickle runs — the MEASURED self-improvement layer), **asolaria-behcs-256** (OLD BEHCS-256 19-supervisor toolkit; 1 PR), **asolaria-whiteroom-engine**, **N-Nest-Prime-INFINITE-SELF-REFLECT**, **falcon-orbital**. Keep until Host-8 parity.

### E · Tools
- **Harness-edit** (claims-gate; PRs #3/#4 → merge/close), **omni-dispatcher** (published, liris-verified — **DONE**), **omnicoder---better-than-termux** (empty **STUB** → fill or retire), **-6-cyl-generator**.

### F · Private root
- **Asolaria** (private) — README doctrine **fixed** (PR#8). **Dirty/structural:** **5 open drafts** — #6 *main-adoption* (placeholder main vs no-common-ancestor live branch — the real structural gap), #7 OCR/atlas, #5 device-PID, #4 Xiaomi-relay, #3 host8-receipts → operator structural decision.

### G · Forks — NOT ours to upgrade (upstream)
- intelligent-terminal, ai-memory, kimi-code, free-claude-code, OpenMythos, Asolaria-helper, HRM, **shannon** (← AI-pentest fork; relevant to the DirtyClone/KERNEL_TRUST_GATE thread). Leave as forks; don't migrate.

### H · Non-Asolaria old personal/client (pre-2026 — NOT Asolaria, NOT dirty, just old)
- ~40 repos: **AI-healthCare-project** (⚠️ 17 open PRs — stale dependabot on a dead non-Asolaria project; close/ignore), **bank-account-transcrtions** (5 open, same), my-history×12, CVScreening_{Frontend,Backend}, daisy-{backend,client}, Everyrealm-AWS-CDK, HubSpot-Meeting, llama-instruct, Upfirst-OAuth, personal-task-management, my-hybrid-bert, onboarding, spread-sheet-demo, space_time_simulator, custom-tree, sensasi, Metatagging-data, fp32/fp16_lora, conference-helper, bank-account, nexus-game, rpg-game-creator, weatherApp, solidity-contract, warran, tech-trades, product-recommendation, EventDriven, ElasticSearch, contentPro, FHIR-Lamba, ListItems, Lists, dungeon, calculator, desktop-tutorial, ipa/schedule/Local-LLM/Docs-Extractor/Itilitii/spinutech/Horse_AI/scala-planner. **These are not the dirt** — they're prior unrelated work; the 22 open PRs on AI-healthcare+bank-account are stale automation, safe to ignore/close.

## Prioritized work-list (gated — no mass auto-merge/close; each PR gets a decision)
1. **Reconcile the Asolaria-core PR backlog (~40):** triage each → merge (good+CI-green), close (superseded/stale), or rebase (DIRTY #7/#10). Start with `what-is-asolaria` (19). *This is the biggest, most concrete "upgrade the dirty repos" action.*
2. **Host-8 runtime ports (staged, no cutover):** `:4947` bus → `bus-serve` (LAW-001, extra care); remaining `:4949` routes; Hilbra `:4790` refresh; the 47-daemon map's cand/unk lanes.
3. **Root structural:** Asolaria #6 main-adoption (operator decision; no-common-ancestor).
4. **Cutovers + engine-fire:** the one gated class — operator-specific go, never auto (`merge ≠ fire`).

## Boundary
This is an assessment + ledger (read-only sweep; no PR merged/closed/mutated here). The reconciliation in the work-list is gated work pending operator scope. See [[project_dashboard_serve_4949_host8_port_inc1_2026_06_27]], [[project_council_confidence_schedule_dspark_pr13_2026_06_27]], [[project_host8_daemon_migration_map_and_3_ports_2026_06_24]], [[feedback_upgrade_old_nodes_to_host8_not_reprove_2026_06_27]].
