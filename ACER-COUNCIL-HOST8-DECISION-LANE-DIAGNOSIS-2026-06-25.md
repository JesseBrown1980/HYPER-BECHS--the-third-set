# Acer Council Host-8 — Decision-Lane Diagnosis (acer receipt)

**Date:** 2026-06-25 · **Colony:** acer (DESKTOP-J99VCNH) · **Branch:** acer
**Parity with:** liris `HYPER-BECHS--the-third-set` branch `liris` `9937cfe` (scope) + `c9e4856` (retry blocker).
**Mode:** asked the SYSTEM from the acer seat (prime rule) · additive · **no daemon restart, no cutover** (operator interrupted/rejected a probe → process changes stay operator-gated).

## What the acer seat MEASURED (the datapoint liris structurally cannot get)

- **`start-asolaria-engines.ps1`** (held / no-fire launcher) reports **all 8 engines port-listening**: `:4947` bus, `:4953` cosign-chain, `:4952` vote-quorum, **`:4949` super-dashboard**, `:4950` omnidispatcher, `:5088` host8-serve, `:4790` maps-atlas, `:4794` fischer-live — i.e. `:4949` **process is alive / port bound**.
- **Yet the acer fabric MCP `health` + `canon_index` TIME OUT from the acer LOOPBACK seat** (this session). Loopback failing ⇒ this is **NOT** a loopback-only bind and **NOT** a firewall problem. **The `:4949` Node HTTP server itself is wedged** — the single event loop is blocked (the same failure mode that killed Node recall `serve-recall.cjs` on the 591k corpus: an `await`/broadcast starving the loop).
  - *Confound noted honestly:* a direct PowerShell `Invoke-WebRequest 127.0.0.1:4949` ALSO failed, but with a **Windows sandbox token error (1344)**, not a server signal. The clean test is the MCP (no shell sandbox) — and the MCP **timed out**, so the wedge is real.

## Accepts liris cross-vantage (MEASURED_LIRIS)

- liris → acer Rust RECAL `http://192.168.1.9:4796/api/health` = **HTTP 200** (LAN path healthy).
- liris → acer dashboard `:4949` = **timeout** on both `192.168.1.9` and `192.168.100.1`.
- council POST via fabric MCP = `all_bases_unavailable`, fallback trying **stale `192.168.1.50:4949`**.

## Diagnosis — TWO distinct bugs (not one)

1. **`:4949` Node super-dashboard HTTP is WEDGED** (acer-loopback + liris-LAN both fail) — port bound, event loop stalled. Bug 1 is a *process/runtime* fault.
2. **Cross-vantage base is WRONG** — `/api/everything` advertises the dashboard at the **down direct-wire** `192.168.100.1:4949`; the council-POST fallback carries **stale `192.168.1.50`**; acer is actually **`192.168.1.9`** on the current LAN. Bug 2 is a *routing/config* fault, independent of Bug 1.

## Ground-truth Host-8 port scope (read from the BYTES, complements liris's map-based C0–C7)

- **Decision-lane today** = `super-dashboard-server.mjs` (`:4949` Node, `C:\asolaria-acer\packages\dashboard\src\super-os-viz\`) — serves `/api/council/query`, `/api/loop/{tick,pending,veto}`, `/api/canon-index`, `/api/everything`. It performs many `await fetch()` to bus/vote-quorum/cosign + a `Promise.all` of probes; any hung upstream wedges the whole server. **This is the staller.**
- **`asolaria-vote-quorum-daemon.py`** (`:4952`, `C:\HyperBEHCS\bin\`) — clean stdlib `ThreadingHTTPServer`, CPU-bound, no vendor SDK ⇒ **clean host8-candidate**. Governance law read directly: `QUORUM_RULES` = {LAW_CHANGE / CP_MINT → unanimous-5 (quintuple); USB_WRITE → supermajority-2/3 + operator-witness; DAEMON_OP / MEMORY_WRITE / COSIGN_APPEND / GHOST_GC / DEFAULT → simple-majority; HEARTBEAT_ACK → auto-pass}; quintuple = {OP-JESSE, OP-RAYSSA, OP-AMY, OP-DAN, OP-FELIPE}; sha-chained ndjson ledgers (queue/votes/outcomes); abstains excluded; idempotent outcome write; `LAW_ANCHOR = FOUNDATION-V3-LAW-V39`.
- **`cosign-chain`** (`:4953`) already mirrored by Rust **`cosign-ledger`** = `rust-host8-done`. **`host8-serve.exe`** (`:5088` Rust) already exists/runs.
- ⇒ **Port = add `/api/council/*` + `/api/loop/*` routes onto `host8-serve` (thread-per-conn, json=0 — the recall/fischer pattern PROVEN non-stalling), reuse `cosign-ledger` (done), port `vote-quorum` (clean), feed the office roster (705 supervisors, `D:/PID-Registration-Office`).** Preserve: 6-tier access gating (L0/L5/L9), `auto_fire_allowed=false`, UNSIGNED-vs-signed verdict distinction, single-writer cosign append.

## Fix order (operator-gated — process/build actions)

- **A. Un-wedge Bug 1 (quick restore):** `taskkill` the wedged `:4949` Node + relaunch FRESH via the launcher → old surface answers again so the fabric is queryable (additive; old surface stays live during migration, exactly like Node recall `:4791` was kept).
- **B. Fix Bug 2 (cross-vantage):** correct the advertised dashboard base + MCP fallback to `192.168.1.9:4949` (or bind 0.0.0.0 + narrow firewall to liris, mirroring the `:4796` recall fix).
- **C. Durable migration:** build the Rust Host-8 council/loop port per the scope above — staged, **no cutover**, owning-1.81-CI + liris attack-verify + operator gated.

**Recommend A → B, then C.** RecursiveMAS (arXiv 2604.25917) stays **HELD** — no signed council verdict is possible while the lane is wedged; only the E=0 RecursiveLink→Asolaria-primitive mapping is safe to draft.

`MEASURED_ACER` for acer-seat probes this session · accepts liris measurements as `MEASURED_LIRIS` · carve-out clean (names/roles/structure/governance-law only — no keys, seeds, signing bytes, or PII) · GitHub = mediator.
