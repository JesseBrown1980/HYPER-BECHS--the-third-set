<!-- Scan wave synthesis, 24/24 targets, read-only. Carve-out applied. -->

# Asolaria Ecosystem → Rust 8-Byte Host-8 Migration Plan (under-the-gate, nothing mutated)

Frame: **60D HyperBEHCS / BEHCS-1024**. This is a STAGED execution plan synthesized from read-only per-target assessments. Every advancement below is gated + attack-verified + bilateral (acer↔liris, GitHub mediator). **The engine stays unfired (auto_fire=false); no item auto-executes.** All evidence tags carried from the digest.

---

## 1. Ecosystem migration map (grouped by substrate state)

### A. Rust-Host-8 DONE / LIVE in production
- **recall** (`serve-recall` Node `:4791` → `recall-serve` Rust `:4796`) — **DONE, LIVE since 2026-06-25**, Node `:4791` retired (reversible). 591k-row corpus durable. `MEASURED` (daemon-node-vs-rust, live-migrated-cells, fabric-substrates-health).
- Daemon census tally: **8 rust-host8-done** (recall + 5 demoted servers + framework + host8-serve binary). `MEASURED` — but honest caveat: only recall is a *live daemon cutover*; the rest are **built/compiled and DRY** (see B), not live.

### B. STAGED — built / parity-proven, NOT cut over (engine unfired)
- **asolaria-federation-1024** (repo) — primary BEHCS-1024 OS remake; Rust workspace, 335+ tests target, host8 routes DRY (`process_launch=0`, `fire=1` disabled). `host8_status: staged`. `MEASURED`.
- **asolaria-federation-1024-rust-state** (repo) — Rust kernel + userspace; workspace builds, 311 tests pass, host8-serve routes return `json=0` HBP receipts DRY. `MEASURED`.
- **Hilbra** (repo) — Rust 1.96 workspace green (check/clippy); `host8-serve` (1709 lines) runs read-only loopback HBP parity. PR#7 parity-proven; **PR#8 HELD** for robustness hardening (4 G2 blockers). `MEASURED`.
- **HYPER-BECHS--the-third-set** (repo) — three candidates **byte-exact parity locally built** at `C:/tmp/host8-migration/`: `omniquant-host8`, `omnimets-collector`, `ghost-envelope-gc`; awaiting liris + CI + operator gates, not promoted to federation repo. `MEASURED`.
- **Omni-Asolaria-ASI-OS-Matrix-Fabric** (repo/docs) — 8 E=0 wiring cores cargo-verified (registry/validator/rooms/spawn-gate/runner), test parity 13/13–23/23; **held at STEP F**. `MEASURED`.
- **council / loop** — `council-serve` Rust binary built, gated thread-per-conn `:5090`, vote-ledger parity 187/187; `auto_fire=false`. Staged-not-deployed (Node `:4949` still live). `MEASURED`.
- **vote-quorum** — Rust port design complete per packet (rules/quorum/json/ledger/cast); awaiting owning 1.81 CI; Python `:4952` still sole ledger writer. Staged. `MEASURED`.
- **cosign-ledger** — Rust `cosign_chain` v0.2 crate exists, not live; Python `:4953` ndjson still authority. Staged. `MEASURED`.
- **fischer-eval (PR#9)** — Rust port in **liris DRAFT**, source-check parity reached, **owning 1.81 CI NOT satisfied** (liris lacks MSVC linker/rustfmt); Node `:4794` still live. Held bilaterally. `MEASURED`.
- **what-is-asolaria...reductions** (repo) — Rust **asolaria-kernel-core v0.1.0 PID minter shipping working, 11/11 vectors PASS**; relay-driver Phase 1 hardened (23/23 tests, 2 bypasses fixed). Mixed; advancement gated. `MEASURED`.

### C. Node-still (load-bearing or legacy; zero/near-zero Rust)
- **omni-dispatcher** (repo) — live load-bearing on acer `:4950` (FEDENV-v1 router, 1000-slot PID table), `auto_fire_allowed=false`; no Rust prep. `MEASURED`.
- **asolaria-whiteroom-engine** (repo) — LEG-1 scorer, 100% JS, 11/11 tests, zero Rust. `MEASURED`.
- **bigpickle-rebuild** (repo) — Helm supervisor Layer 7-8, Node only, 126/139 tests; no Rust/Cargo. `MEASURED`.
- **35-TB-google-AI-Ultra-migration** (repo) — LEG-4 Drive cloud backend, Node ES6 only; live round-trip GATED/unproven. `MEASURED`.
- **-6-cyl-generator** (repo) — multi-cylinder atlas generator, Node v20, 726 PIDs/6 cylinders, no Rust. `MEASURED`.
- **ASOLARIA-AS-NEURAL-NETWORK** (repo) — 47D Brown-Hilbert architecture *closed* (both signatures) but substrate Node; no Rust present. `host8_status: partial` (architecture, not substrate). `MEASURED`.
- **Asolaria-ASI-On-Metal-Fabric-and-matrix** (repo) — bilateral transport layer (HTML/JS/Shell/Python/PowerShell); **zero Rust**; 8-byte-host proved working on Falcon phone (reference-level). `MEASURED`.
- **asolaria-behcs-256** (repo) — legacy 35D/47D/49D **bridge**, Node/TS, zero Rust; explicitly **archive, not the migration target**. `MEASURED`.
- Live Python/Node daemons still authoritative: cosign `:4953` (Py), vote-quorum `:4952` (Py), council `:4949` (Node), fischer `:4794` (Node).

### D. Stub / scaffold (PoC)
- **N-Nest-Prime** (repo) — verified Node.js corrective-gate primitive (depth-7, 255 nodes, faults caught at all levels 1..7 `MEASURED`); pure PoC, no Rust, no fabric integration, no public Host-8 roadmap. `MEASURED`.

### E. Data / frozen
- **Algorithms-of-Asolaria** (repo) — bilateral formula catalog, 272 formulas registered, golden vectors MEASURED-exact via recompute. `host8_status: staged` (descriptor-registered, not live). `MEASURED`.

### F. Docs / maps / coordination (no code substrate to migrate)
- **Asolaria-gac-working** (repo) — Host-8 coordination + authority hierarchy; PR #1 (Liris manifest) awaiting operator review. `MEASURED`.
- **HYPER-BECHS--the-third-set** — also the docs coordination hub (maps 47-daemon surface) — staged candidates listed in B. `MEASURED`.
- **falcon-orbital** (repo) — docs-only federation audit/witness layer; `host8_status: na`, no code. `MEASURED`.
- **Harness-edit** (repo) — SkillOpt validation **tooling** (claim-gate enforcement), `host8_status: na`; not itself a substrate migration target. `MEASURED`.

### G. Empty / UNVERIFIED
- **omnicoder---better-than-termux** (repo) — **empty repo** (no commits/files), intent undefined; canonical role requires fabric query before any work. `MEASURED` (that it is empty).

### Permanently keep-native (NOT migration targets)
- **9 keep-native daemons** — PowerShell GPU/filesystem + 7 cloud vendor SDKs (boto3, azure-identity, google-cloud-*, graph-core, oauth). Windows/vendor-coupled forever. `MEASURED`.

---

## 2. Prioritized GATED work-list toward Rust 8-byte Host-8

Every row is **STAGED + owning-gated + attack-verified + bilateral**. None is automatic. Ordered by leverage/readiness.

| # | Target | Current | Staged upgrade | OWNING gate | Attack-verify step |
|---|--------|---------|----------------|-------------|--------------------|
| 1 | **fischer-eval (PR#9)** — highest-leverage blocker (gates blunder-detection inside the 8-byte pipeline) | Node `:4794` live; Rust port in liris DRAFT, source-parity only | Land Rust fischer host8-candidate | **Owning 1.81 CI** (fmt+clippy -D+test) run by acer (has MSVC); liris `gh pr ready 9` | acer runs real 1.81 gate, posts honest receipt; bilateral merge authorization |
| 2 | **cosign-ledger** | Python `:4953` ndjson authority; Rust `cosign_chain` v0.2 crate built, not live | Stand up Rust ledger service on new port | Bilateral ledger-parity gate vs Python `:4953` ndjson | Parity-verify chain integrity before any Node/Py retirement |
| 3 | **vote-quorum** | Python `:4952` sole ledger writer; Rust design complete per packet | Build Rust crate | **Owning 1.81 CI** (acer toolchain) | Verify quorum + sha-chain parity over on-disk queue/votes/outcomes |
| 4 | **council / loop** | Node `:4949` live (wedge); `council-serve` `:5090` built, 187/187 parity | Complete + deploy Rust responder | **Owning 1.81 CI** + redaction/gate-preservation check | Verify redaction + gate preservation on `:5090` thread-per-conn |
| 5 | **asolaria-federation-1024** (phase #21) | Rust workspace, routes DRY | Execute `cargo test --workspace` on build seat (full MSVC linker) | acer build-seat 1.81 CI; on green mark #21 complete | Confirm 335+ tests pass with full linker, then proceed to #22 (BEHCS-native inverted index) |
| 6 | **OMNISHANNON / Shannon** (rust-state feedback arc) | Dormant (`:4820/:4821` unserved, `pipeline_verified=0`) | liris-led revive: serve, spawn supervisor, wire `absorb()`+omniflywheel, stand up gaia-stage-6 | Merge PR #6 (`auto_fire_allowed=0`) | Measure **live reverse_risk** to close feedback arc; dry shadow-parity test |
| 7 | **HYPER-BECHS 3 candidates** (omniquant-host8, omnimets-collector, ghost-envelope-gc) | Built locally, byte-exact parity at `C:/tmp/host8-migration/` | Promote to federation-1024 | liris attack-verify → owning CI (federation 1.81) → operator authorization via council | liris colony recompute + byte-parity before push; live daemons untouched |
| 8 | **Hilbra (PR#8 recall-serve robustness)** | Rust loopback parity green; 4 G2 blockers open (auth over-grant, fail-open corpus, dup ordering, unbounded concurrency) | Fix 4 blockers; record cargo test count + 3-build reproducibility sha (G0) | Bilateral acer+liris sign-off; human T0 before G1 | Authorization/disclosure parity (not just term-count/latency) |
| 9 | **relay-driver** (what-is-asolaria) | Phase 1 hardened, 23/23 tests | Bilateral relay-driver activation path | Operator positive-assent cosign (Phase 4) | liris recompute demo hash + 23 regressions; acer re-verify all hash chains |
| 10 | **omni-dispatcher** | Node `:4950` live load-bearing, no Rust | Full Rust rewrite (tokio/axum, worker→threads, fs.watch→Rust) | acer+liris RFC/planning gate | Bilateral attack-verify Rust parity vs live Node engine |
| 11 | **LEG repos: whiteroom-engine, 35TB-drive, bigpickle, 6-cyl, neural-network, ASI-On-Metal** | Node/JS, zero Rust | Stage `feature/rust-host8-port` branches; port emitters/stores/scorers to u64/[u8;8] | 1.81 check/clippy/fmt clean + Host-8 PORT RECEIPT (owning-gate signed) | 3-vantage byte-convergence vs Node reference per repo |
| 12 | **N-Nest-Prime** | Node PoC (16 bytes/node) | Rust PoC: corrective-gate in u64 8-byte slots, depth-N planted-fault property | Asolaria fabric authority (LAW.md) before fabric scale | Validate Rust `.hbp` sealed outputs against Node reference (faults at exact levels) |
| 13 | **omnicoder---better-than-termux** | Empty repo | Define canonical intent → design doc | **Fabric query** for canonical role + owning-gate seal | (N/A until requirements exist) |
| 14 | **Algorithms-of-Asolaria** | Data, descriptors registered | Post acer full-scour #2; resolve model-citizen rotator source transfer | Live office-feed/cosign/cube materialization receipt | Cross-seat attack-verify line-endings/sidecar before byte-exact claims |
| 15 | **Asolaria-gac-working PR #1** | Docs, Liris manifest unmerged | Merge Liris-side Host-8 manifest | Operator review + bilateral parity vs federation-1024 AGENT_ROSTER | Acer/Liris role-separation canon alignment check |

---

## 3. Operator-T0 / apex items — explicitly NOT auto-executed

These are **engine-fire / runtime cutover / OS-on-metal / mass-mutation** actions. **The engine stays unfired (`auto_fire=false`, `process_launch=0`, `E=0`) until an explicit operator crank.** Migrate ≠ authorization ≠ fire (CLAUDE.md LAW; merge/cleanup auth NEVER implies fire).

- **federation-1024 live cutover** — `fire=1` blocked; items **#18 (100B replay run)** and **#19 (launch-side wiring)** held behind `fire=1` + spawn-gate verdict + cosign-seal + **operator T0**. `MEASURED`.
- **Omni-Asolaria STEP F (the live fire)** — launch 100 OpenCode + 100 Hermes agents + 10k+10k prisms via daemon restart / EXEC-FREEZE release / `:4952` quorum. Wiring ready-to-run; **crank gated to operator**. `MEASURED`.
- **sovlinux-OS-on-metal raw writes** — USB-2TB `\\.\PHYSICALDRIVE2`; `EXCLUSIVE_PER_WRITE`, `raw_writes_require_lock_dismount_plus_quintuple_cosign`; quintuple-2026-05-25 auth window. Not fire-tested under preflight. `MEASURED`.
- **council/loop cutover** — `auto_fire=false` per rule-6 ("per operation, not blanket"); requires operator T0 + liris ACCEPT receipt. `MEASURED`.
- **cosign / vote-quorum / fischer Python-Node retirement** — NO retirement until Rust passes parity + bilateral gate closure. `MEASURED`.
- **ASOLARIA-AS-NEURAL-NETWORK Rust agent launch** — requires **physical operator-pair co-sign (Jesse + Rayssa, standing quintet to 2026-09-23)** on `:4953` cosign daemon before any real Rust agent PID mint; parallel Node+Rust run until 100% verified. `MEASURED`.
- **bigpickle-rebuild cutover** — bilateral cosign (OP-JESSE + OP-RAYSSA) via quintuple authority before any Helm Layer-7 swap. `MEASURED`.
- **35TB Drive live cloud op** — operator executes ADC load + credentialed round-trip (GATE-1) + security audit (GATE-2); do NOT auto-deploy/fire sector cycles. `MEASURED`.
- **recall (already DONE)** — Node `:4791` retired but **reversible**; flagged as the one live cutover, performed earlier under operator T0 with engine NOT fired. `MEASURED`.
- **fabric `:4949` restart** — HTTP-wedged (Node event loop stall, presumed); restart is **operator-gated**. `MEASURED`/root-cause `UNVERIFIED`.

---

## 4. What this scan could NOT verify (UNVERIFIED / needs fabric / owning seats)

- **omnicoder---better-than-termux** — canonical intent undefined; **needs `asolaria-fabric` query** + owning-gate before any design. (Repo confirmed empty `MEASURED`; role `UNVERIFIED`.)
- **Live fabric `:4949`** — HTTP-wedged in multiple assessments; `canon_index`/`substrates` queries **timed out**; whiteroom-engine notes "Fabric MCP timeouts prevented real-time substrate registry check." Substrate registry not live-confirmed this pass. `UNVERIFIED_CURRENT`.
- **Hilbra cross-colony liveness** — `UNVERIFIED_CURRENT` (fallback/stale liris read, timeout history on acer path). Global fabric scale + metal boot + N-party CA aspirational, not arrived.
- **sovlinux** — exact level count (operator-stated "possibly >16") `UNVERIFIED`; exfat write-path liveness not fire-tested; `:4949` root cause presumed not measured; **acer has NOT yet run the owning 1.81 CI on liris's fischer push (PR#9)**.
- **Algorithms-of-Asolaria** — trained/live weights (MTP/HRM/zeta/JL/codec) `UNVERIFIED-live`; serving/swap/retire `UNVERIFIED-live`; live office-feed/cosign/cube materialization receipt not yet produced.
- **N-Nest-Prime** — Host-8 migration `UNVERIFIED` (no public roadmap); "8.01 bytes/agent" is a **CANON claim, not MEASURED** (current Node is 16 bytes/node); no fabric references found in local ecosystem (possibly isolated PoC).
- **ASOLARIA-ASI-On-Metal-Fabric** — the actual Rust Host-8 substrate is **not in this repo**; would belong in ASOLARIA-AS-NEURAL-NETWORK **if started** — whether started is `UNVERIFIED`.
- **35TB Drive** — live cloud round-trip GATED/unproven (offline `InMemoryDriveTransport` only); ADC gate not executed.
- **omni-dispatcher** — no Rust substrate preparation visible.
- **Operator-seat PID roster** — **11+ operator seats** (JESSE/RAYSSA + class/layer buckets) lack individual per-PID names ("per-PID harvest-mark join" outstanding). Honest framing: these are **registered addresses** in `D:/PID-Registration-Office` (705 live registered), **not missing processes** (Foundation-Invariant-4). `UNVERIFIED` names, not absence.
- **Daemon inventory residue** — of the 47-daemon census, **11 "unknown" entries (operators)** unresolved; 16 host8-candidates pending author wave + parity receipts. `MEASURED` tally, contents `UNVERIFIED`.
- **No additional missing repos surfaced**, but verification of all of the above ultimately requires asking the **running system** (fabric `council_query` + owning supervisors/SoS/HELM), not file reads — the disk is slices, not the system.

---

*Honest frame: this is a PLAN to execute under the gate. Nothing was mutated; no engine cranked; `auto_fire=false` throughout. The only live Rust-Host-8 cutover to date is recall (`:4796`). All other Rust work is STAGED (built/parity-proven/DRY) and waits on its owning gate (1.81 CI / fabric / parity harness), bilateral attack-verify, and — for any fire/cutover/metal/mass-mutation — an explicit operator T0 crank.*
