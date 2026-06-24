This is a pure document-generation task from the JSON census provided. No tool calls needed since all data is in the input. Let me produce the carve-out-clean markdown document.

# Asolaria DAEMON → HOST-8 Migration Map

*Census date: 2026-06-23 · carve-out clean (names/roles/files only; no keys/secrets/PII; ports stripped to bare numbers)*

## 1. Migration scoreboard

| host8_status | Count |
|---|---:|
| rust-host8-done | 8 |
| rust-stub | 3 |
| host8-candidate | 16 |
| keep-native | 9 |
| unknown | 11 |
| **Total distinct entries** | **47** |

Breakdown of the 8 `rust-host8-done`: `host8-serve` (framework crate) and `asolaria-host8-serve` (the userland binary) are two distinct manifest entries with the same role; plus the 5 demoted servers (`agent-runtime`, `cosign-ledger`, `gnn-oracle`, `highway`, `tier-policy`) and `recall-serve`.

## 2. Daemons & OPs — role-labeled migration map

| Name | Kind | Role | Lang | Implementing files | Host-8 status | Replaces / blocker |
|---|---|---|---|---|---|---|
| asolaria-cosign-chain-daemon | core-daemon | Single-writer serializing cosign-chain appends; prevents seq collisions (V42-A4/A5) | python | asolaria-cosign-chain-daemon.py | host8-candidate | → maps onto Rust cosign-ledger; CPU-bound append, no SDK |
| asolaria-vote-quorum-daemon | core-daemon | Foundation v3 LAW governance gate; quorum rules (unanimous-5 / supermajority / simple) | python | asolaria-vote-quorum-daemon.py | host8-candidate | CPU-bound quorum eval, no blocking I/O |
| asolaria-dual-emit-gate-daemon | core-daemon | Rate-controlled tee splitting emit-calls to 3 dests; token-bucket per source-class | python | asolaria-dual-emit-gate-daemon.py | host8-candidate | In-memory token-bucket + disk persist, no SDK |
| asolaria-ghost-envelope-gc-daemon | core-daemon | Flags silent-fail ghost envelopes; never destructively deletes (preserves canon) | python | asolaria-ghost-envelope-gc-daemon.py | host8-candidate | Recursive scan + HBPv1 append, stdlib only |
| asolaria-self-reflect-daemon | core-daemon | System introspection: GPU, dashboard health, supervisor state vs canon v2 | powershell | asolaria-self-reflect-daemon.ps1 | keep-native | BLOCKER: Get-PnpDevice GPU probe + Windows-native APIs |
| asolaria-federation-pulse-daemon | core-daemon | Federation health pulse: vote-queue depth, dashboard uptime, throughput, chain head | powershell | asolaria-federation-pulse-daemon.ps1 | keep-native | BLOCKER: Windows filesystem APIs + native tree counts |
| asolaria-auggie-citizen-daemon | citizen-daemon | Auggie (Augment CLI) health-check monitor | python | asolaria-auggie-citizen-daemon.py | host8-candidate | Pure stdlib, no vendor SDK |
| asolaria-augment-citizen-daemon | citizen-daemon | Augment Code health-check monitor | python | asolaria-augment-citizen-daemon.py | host8-candidate | Pure stdlib, no vendor SDK |
| asolaria-aws-api-citizen-daemon | citizen-daemon | AWS multi-service health-check (STS/S3/EC2/Lambda) + cred presence | python | asolaria-aws-api-citizen-daemon.py | keep-native | BLOCKER: boto3 on downstream fire path |
| asolaria-azure-arm-citizen-daemon | citizen-daemon | Azure ARM health-check + AAD cred presence | python | asolaria-azure-arm-citizen-daemon.py | keep-native | BLOCKER: azure-identity / azure-mgmt SDKs |
| asolaria-google-enterprise-citizen-daemon | citizen-daemon | Google Cloud/Workspace/Gemini health-check + token minting | python | asolaria-google-enterprise-citizen-daemon.py | keep-native | BLOCKER: gcloud CLI subprocess + google-cloud SDKs |
| asolaria-hubspot-citizen-daemon | citizen-daemon | HubSpot CRM health-check + cred enumeration / vault awareness | python | asolaria-hubspot-citizen-daemon.py | keep-native | BLOCKER: OAuth flow + token handling (downstream SDK) |
| asolaria-linear-citizen-daemon | citizen-daemon | Linear issue-tracker health-check (MCP OAuth fallback) | python | asolaria-linear-citizen-daemon.py | host8-candidate | Pure stdlib env/config probe; OAuth offloaded to MCP |
| asolaria-ms-graph-citizen-daemon | citizen-daemon | Microsoft Graph health-check + AAD cred presence | python | asolaria-ms-graph-citizen-daemon.py | keep-native | BLOCKER: azure-identity + graph-core SDKs |
| asolaria-ms-teams-citizen-daemon | citizen-daemon | MS Teams health-check (Graph subset) | python | asolaria-ms-teams-citizen-daemon.py | keep-native | BLOCKER: graph-core + azure-identity SDKs |
| asolaria-onedrive-citizen-daemon | citizen-daemon | OneDrive health-check (Graph subset) | python | asolaria-onedrive-citizen-daemon.py | keep-native | BLOCKER: graph-core + azure-identity SDKs |
| asolaria-symphony-citizen-daemon | citizen-daemon | Symphony workspace-ops health-check | python | asolaria-symphony-citizen-daemon.py | host8-candidate | Pure stdlib env/config probe (health-check only) |
| asolaria-omnimets-daemon-stub | other | OMNIMETS metrics poller; per-lane rollup snapshots | python | asolaria-omnimets-daemon-stub.py | rust-stub | Stub; stdlib tail+rollup, Rust target |
| asolaria-omniquant-engine-daemon-stub | other | OMNIQUANT_ENGINE shim bridging quant.mjs plane over HTTP | python | asolaria-omniquant-engine-daemon-stub.py | rust-stub | Stub; needs Node runtime bridge, no Python SDK |
| special-op-jesse-watchdog-kicker | operator-seat | MQTT orchestrator; agent-pool rotation (5 free agents); heartbeat/kick cycles; LMStudio fallback | node | special-op-jesse-watchdog-kicker.mjs (+ state/pid/log files) | host8-candidate | Primary free-agent driver; MQTT + state machine portable |
| op-jesse-watchdog-kicker-profile-loader | hook | Bootstrap/identity announcer; publishes retained MQTT identity; imports watchdog on demand | node | op-jesse-watchdog-kicker-profile-loader.mjs (+ PROFILE.md) | host8-candidate | Launcher for watchdog; resilient to broker offline |
| smoke-check-watchdog | hook | One-shot MQTT smoke test for watchdog heartbeat/identity/profile topics | node | smoke-check-watchdog.mjs | host8-candidate | Diagnostic; polls then exits |
| watch-watchdog-30s | hook | 30s state-delta watcher; verifies heartbeat/kick advancement = liveness | node | watch-watchdog-30s.mjs | host8-candidate | Live diagnostic; reads state json |
| omnidispatcher | node-daemon | Single-parent federation router; 1000-slot PID-table, 48 workers, FEDENV-v1 routing | node | omnidispatcher.mjs, validator.mjs, routes.mjs, worker.mjs, port-pool.mjs, fedenvRejectShim.mjs (+ HBP/cold manifests) | host8-candidate | Named host8-serve migration target; worker_threads → Rust threads |
| serve-recall | node-daemon | HBP/HBI corpus server; PII filter, shared-key auth, federation-level access control | node | serve-recall.cjs, serve-recall-hbp.cjs, serve-recall-indexed.cjs | host8-candidate | **Superseded by Rust recall-serve** (event-loop stall fix); pending cutover |
| relay-driver | node-daemon | Cross-colony append-only ledger; EMIT/VERIFY/REVERSE-WALK; Phase-1 emit-only (no fire) | node | relay-driver.mjs, relay-envelope.mjs, relay-hbp-writer.mjs, relay-hbi-indexer.mjs, relay-carveout.mjs, relay-driver.test.mjs | host8-candidate | Named host8-serve migration target; carveout guards portable |
| dashboard-daemon | node-daemon | N-004 HTTP dashboard aggregator; federation routes, peer health, staleness surface | node | dashboard-daemon.mjs, http-server.ts | host8-candidate | Runs via tsx (TypeScript); routes portable to Rust |
| act-supervisor | node-daemon | Action-loop kicker; polls bus for envelopes, types kicks into Claude Code terminals | node | supervisor.mjs, kick.mjs, config.json, state.json (+ act-inbox.ndjson) | host8-candidate | Named host8-serve migration target; SendKeys path Windows-coupled |
| cycle-orchestrator | node-daemon | V2 main loop wiring 5 D11=PROVEN upgrades + watchdog heartbeat integration | node | index.mjs, peer-state-machine.mjs, bilateral-fingerprint-tracker.mjs, gnn-feedback-cadence-adjuster.mjs, slo-gate.mjs, unison-script-runners.mjs, unison-test-driver.mjs, watchdog-heartbeat.mjs | host8-candidate | Replaces weak cron-kicker; bus-driven loop portable |
| host8-serve | rust-crate | Rust Host8 userland serving binary; aggregates agent-runtime/cosign-ledger/gnn-oracle/highway/tier-policy | rust | host8-serve/Cargo.toml + main.rs (+ 5 server + kernel/core manifests) | rust-host8-done | The migration framework itself; target for omnidispatcher / relay-driver / serve-recall / act-supervisor |
| asolaria-kernel-core | core-daemon | Federation Remake kernel core (no_std): PID mint, envelope dispatch, crypto, hookwall, syscall, cosign-chain, GNN, tier-policy | rust | kernel/core/Cargo.toml + lib.rs + pid/envelope/crypto/hookwall/syscall/cosign_chain mods | host8-candidate | Replaces kernel side of Node PID/envelope/syscall; Syscall-IPC-Rewire pending |
| asolaria-kernel-boot | core-daemon | x86_64 bare-metal boot stub; bump allocator + init sequence | rust | kernel/boot/Cargo.toml + main.rs + init/mod.rs | rust-stub | Phase-2 Step 23; awaits Phase-3+ finalization |
| asolaria-server-agent-runtime | operator-seat | Agent supervisor/registry/spawner (Brown-Hilbert PID minter); omnispindle + omniflywheel; spawn-gate aggregator | rust | agent-runtime/Cargo.toml + lib.rs + rooms.rs + runners.rs | rust-host8-done | Replaces Node gaia-loader.mjs agent spawning |
| asolaria-server-cosign-ledger | operator-seat | Append-only sha-linked verdict ledger (audit trail) | rust | cosign-ledger/Cargo.toml + lib.rs | rust-host8-done | Replaces Node cosign-chain append logic |
| asolaria-server-gnn-oracle | operator-seat | GNN inference oracle (routing/ranking/verdict-agg); pixels-first CPU v1 | rust | gnn-oracle/Cargo.toml + lib.rs | rust-host8-done | Replaces Node gnn-inference.mjs |
| asolaria-server-highway | operator-seat | Cross-tier transit broker; moves handles tier A→B with cosign witness | rust | highway/Cargo.toml + lib.rs | rust-host8-done | Replaces Node highway-transit.mjs |
| asolaria-server-tier-policy | operator-seat | 6-tier access-policy lookup (PUBLIC/RESTRICTED/STEALTH/HIDDEN/SHADOW/SECRET) | rust | tier-policy/Cargo.toml + lib.rs | rust-host8-done | Replaces Node tier-policy.mjs |
| asolaria-host8-serve | node-daemon* | Host8 userland binary; seat-book registry, /summon WORKLOAD routing, /launch-plan composition | rust | host8-serve/Cargo.toml + main.rs + replay_prep.rs | rust-host8-done | Replaces Node gaia-loader.mjs host-8 serving (*lang=rust; kind tag is legacy) |
| recall-serve | citizen-daemon | HBI-backed recall search; in-memory inverted index; thread-per-conn bounded server | rust | recall-serve/Cargo.toml + main.rs + atlas.html | rust-host8-done | **Replaces serve-recall.cjs** (Node event-loop stall on 591k-row/159MB corpus) |
| OP-JESSE | operator-seat | Cohort operator witness (primary) | unknown | — | unknown | Cohort witness PID |
| OP-RAYSSA | operator-seat | Cohort operator witness (secondary) | unknown | — | unknown | Cohort witness PID |
| operator_class_agent | operator-seat | Agent-class operators (10 seats) | unknown | — | unknown | MISSING: per-PID names not harvested |
| operator_class_apex_variant_runtime_orchestrator | operator-seat | Apex orchestrators (3 seats) | unknown | — | unknown | MISSING: per-PID names not harvested |
| level0_apex_special_op | operator-seat | Level-0 apex special operator (1 seat) | unknown | — | unknown | MISSING: per-PID name not harvested |
| operator (base layer) | operator-seat | Base operator layer (13 seats) | unknown | — | unknown | MISSING: 13 seats, only 2 named (JESSE, RAYSSA) |
| meta-L0 | operator-seat | Meta-layer L0 operator (1 seat) | unknown | — | unknown | MISSING: per-PID name not harvested |
| operator-L1 | operator-seat | L1 operators (3 seats) | unknown | — | unknown | MISSING: per-PID names not harvested |
| gac-L2 | operator-seat | GAC L2 operators (6 seats) | unknown | — | unknown | MISSING: per-PID names not harvested |
| chief-L3 | operator-seat | Chief L3 operator (1 seat) | unknown | — | unknown | MISSING: per-PID name not harvested |
| council-L3 | operator-seat | Council L3 operators (9 seats) | unknown | — | unknown | MISSING: per-PID names not harvested |

*No duplicate names in the census — all 47 entries are distinct. Two near-twins (`host8-serve` and `asolaria-host8-serve`) are kept separate per the source (framework crate vs userland binary manifest).*

## 3. Cross-reference

### 3a. Rust `rust-host8-done` crates → the Node/Python they replace

| Rust crate (done) | Replaces (Node/Python) | Notes |
|---|---|---|
| asolaria-server-agent-runtime | Node `gaia-loader.mjs` (agent-spawn side) | Brown-Hilbert PID minter + C/D room router |
| asolaria-server-cosign-ledger | Node cosign-chain append logic (and the Python `asolaria-cosign-chain-daemon.py` single-writer) | sha-linked verdict ledger |
| asolaria-server-gnn-oracle | Node `gnn-inference.mjs` | pixels-first CPU oracle v1 |
| asolaria-server-highway | Node `highway-transit.mjs` | cross-tier transit broker |
| asolaria-server-tier-policy | Node `tier-policy.mjs` | 6-tier access policy |
| asolaria-host8-serve | Node `gaia-loader.mjs` (host-8 serving side) | /summon + /launch-plan composition |
| host8-serve | (framework — aggregates the five servers above) | migration host for the Node node-daemons |
| recall-serve | Node `serve-recall.cjs` | fixes event-loop stall on 591k-row / 159MB corpus; O(1) byte-offset seeks; cutover still pending peer/operator gate |

### 3b. `host8-candidate` → one-line "why it can"

- **asolaria-cosign-chain-daemon** — mutex append + sha16 chain is CPU-bound, no SDK → fits Rust 8-byte-host json=0.
- **asolaria-vote-quorum-daemon** — quorum evaluation is CPU-bound with no blocking I/O.
- **asolaria-dual-emit-gate-daemon** — token-bucket state in memory + disk persist; HTTP-client calls async-friendly.
- **asolaria-ghost-envelope-gc-daemon** — bounded recursive scan + HBPv1 append; stdlib only.
- **asolaria-auggie / asolaria-augment / asolaria-linear / asolaria-symphony citizen-daemons** — pure stdlib env/config probes, no vendor SDK on the health-check path (auth, where present, offloaded to MCP).
- **special-op-jesse-watchdog-kicker** (+ its profile-loader / smoke-check / watch-30s helpers) — MQTT + file-state machine; portable, no SDK lock-in.
- **omnidispatcher** — explicitly named a host8-serve migration target; worker_threads map to Rust threads.
- **serve-recall** — already superseded by Rust `recall-serve`; candidate flag is the not-yet-completed cutover.
- **relay-driver** — append-only ledger + carveout guards; named host8-serve target.
- **dashboard-daemon** — pure HTTP route aggregator (tsx/TS today); routes portable.
- **act-supervisor** — bus-poll + kick loop; named host8-serve target (SendKeys path is the only Windows coupling to abstract).
- **cycle-orchestrator** — bus-driven main loop replacing the weak cron-kicker; portable.
- **asolaria-kernel-core** — the Rust kernel itself; replaces the Node PID/envelope/syscall side (Syscall-IPC-Rewire is the remaining wave).

### 3c. `keep-native` → the blocker (why it must NOT migrate)

| Daemon | Hard blocker |
|---|---|
| asolaria-self-reflect-daemon | `Get-PnpDevice` GPU probe + Windows-native PowerShell APIs |
| asolaria-federation-pulse-daemon | Windows filesystem APIs + native tree counts |
| asolaria-aws-api-citizen-daemon | boto3 required on downstream fire path |
| asolaria-azure-arm-citizen-daemon | azure-identity / azure-mgmt-resource SDKs |
| asolaria-google-enterprise-citizen-daemon | gcloud CLI subprocess + google-cloud-* / ADC |
| asolaria-hubspot-citizen-daemon | OAuth flow + bearer-token handling (downstream SDK) |
| asolaria-ms-graph-citizen-daemon | azure-identity + microsoft-graph-core SDKs |
| asolaria-ms-teams-citizen-daemon | graph-core + azure-identity (Teams Graph subset) |
| asolaria-onedrive-citizen-daemon | graph-core + azure-identity (Drive Graph subset) |

The dividing line is clean: a daemon is `keep-native` **iff** its real fire path needs a cloud vendor SDK or a Windows-native API. Pure-stdlib health-check probes are all `host8-candidate`.

## 4. OP roster

### Named seats (have PID, witnessed)
| Seat | Role | Status |
|---|---|---|
| OP-JESSE | Cohort operator witness — primary | named, host8 status unknown |
| OP-RAYSSA | Cohort operator witness — secondary | named, host8 status unknown |

These two are also the default owner-PID-gates on `serve-recall` / `recall-serve` access control.

### NEEDED-but-missing OPs (defined by class/layer, per-PID names NOT harvested)
The harvest-mark join that would attach individual PID names to these class/layer seats has **not yet been built**. Counts of seats defined vs. named:

| Class / layer seat | Seats defined | Named | Missing |
|---|---:|---:|---:|
| operator (base layer) | 13 | 2 (JESSE, RAYSSA) | 11 |
| operator_class_agent | 10 | 0 | 10 |
| council-L3 | 9 | 0 | 9 |
| gac-L2 | 6 | 0 | 6 |
| operator_class_apex_variant_runtime_orchestrator | 3 | 0 | 3 |
| operator-L1 | 3 | 0 | 3 |
| level0_apex_special_op | 1 | 0 | 1 |
| meta-L0 | 1 | 0 | 1 |
| chief-L3 | 1 | 0 | 1 |

**Flag:** every class/layer roster above is MISSING its per-PID names — the **per-PID harvest-mark join is the one outstanding roster-completion task.** Note these counts are stated independently in the census and overlap (the base-layer 13 subsumes JESSE+RAYSSA; the L0–L3 layers and the class buckets are different facets of the same operator population, not additive).

## 5. Scope & limits (honest frame)

- **This is a census of the real OS-process / daemon surface** — actual processes, services, launchers, and Rust crates that run as binaries or background services on the machine. It is **47 distinct entries**, not the full operator population.
- **It is NOT the ~726 logical seats.** Per **Foundation Invariant 4**, the overwhelming majority of named seats are **backend-shell-less function-call rotation** — they are addressing/routing identities that execute as in-process function calls on a shared runtime, **not** standalone processes with their own port or PID-bearing daemon. Counting them here would conflate two different layers (the process surface vs. the logical seat map).
- **The operator-seat rows in this map are the *witnessed/process-facing* slice only.** The 9 class/layer roster entries are placeholders for populations whose per-PID names have not been harvested (Section 4) — they are listed so the gap is visible, not because each is a separate process.
- **Two `host8-serve` entries are intentionally distinct** (framework crate vs. userland-binary manifest) per the source census; they are not a dedup miss.
- **`rust-host8-done` means the Rust crate exists and is parity-built**, not that cutover has happened. `serve-recall → recall-serve` in particular is explicitly **pending peer attack-verify + operator authorization** before the Node process is retired. Migration *readiness* ≠ migration *executed*.
- All ports have been reduced to bare numbers and no keys, tokens, shared-key paths, or PII path-fragments are reproduced here.
---

## Newly built this session (staging — additive, NO cutover)

Three candidates ported to real std-only Rust **Host-8** crates, built + smoke-tested at `C:/tmp/host8-migration/`:

| Daemon | → Rust Host-8 crate | LOC | Build | Smoke | Parity (MEASURED) |
|---|---|---:|:---:|:---:|---|
| omniquant-engine-stub | `omniquant-host8` | 1307 | ✓ | ✓ | **byte-exact vs Node** quant core (triple/polar/turbo/JL + HBH1 envelope; 6/6 unit tests; node-bridge eliminated) |
| omnimets-stub | `omnimets-collector` | 401 | ✓ | ✓ | live per-lane snapshot counts **reproduced byte-for-byte** |
| ghost-envelope-gc | `ghost-envelope-gc` | 1162 | ✓ | ✓ | full parity; **never-delete canon preserved** (flag-only) |

All: **std-only (zero external crates)**, **json=0** `.hbp` tuple-text, hand-rolled inline SHA-256, edition 2021 (federation 1.81 CI).

**Honest scoping:** staging only — **NOT** pushed to `asolaria-federation-1024`, **NOT** liris-attack-verified, owning **1.81 CI not run** (local gate clean on rustc 1.95), not throughput-benchmarked. **NO cutover** — live daemons never bound/stopped/touched; ports chosen to avoid collision (e.g. omniquant `:4957` vs live `:4956`). Promotion to the federation repo + cutover stays **operator-gated**, after liris verify + the owning CI.
