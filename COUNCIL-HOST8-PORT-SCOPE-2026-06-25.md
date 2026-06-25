# Council Host-8 Port Scope - decision-lane snapshot and next cells

**Date:** 2026-06-25  
**Colony branch:** `liris`  
**Purpose:** record the current fabric/RecursiveMAS snapshot, then scope the council/loop decision-lane Host-8 port without claiming a signed fabric verdict.

## Snapshot

| Claim | Tag | Evidence |
|---|---|---|
| Liris fabric GET surfaces are reachable. | `MEASURED` | `asolaria_fabric_health`: ok=true, service `super-asolaria-os-dashboard-liris-mirror`, port 4944, apex `COL-ASOLARIA`, operator pair `OP-JESSE-PID` + `OP-RAYSSA-PID`, uptime 179201s. |
| Liris fabric route map is reachable. | `MEASURED` | `asolaria_fabric_everything`: bus `http://192.168.100.1:4947`, cosign chain `C:/Users/rayss/.claude/projects/C--/memory/COSIGN_CHAIN.ndjson seq=46`, live dashboards `192.168.100.1:4949` and `192.168.100.2:4944`, operators quintet, free agents, Shannon, supervisor registry, sovereignty USB. |
| Liris canon index is reachable. | `MEASURED` | `asolaria_fabric_canon_index`: total_entries=427, sections=134, bytes=178014. |
| Acer council/query POST decision lane is not available for a signed verdict right now. | `OPERATOR_OBSERVED` + `UNVERIFIED_CURRENT` from Liris | Operator showed repeated council POST failures while lower daemons were alive. Do not fabricate a council decision. |
| Underlying Acer governance daemons are not a total outage. | `OPERATOR_OBSERVED` | `asolaria-vote-quorum-daemon` listening on 127.0.0.1:4952; `asolaria-cosign-chain-daemon` on :4953 head_seq=3572; federation-pulse and self-reflect starting. The :4953 WinError 10053 trace is the known unknown-route/socket-close abort, not proof of chain death. |
| The decision/control lane is the next unfinished migration cell. | `MEASURED_FROM_MAP` | Existing migration map marks cosign-chain, vote-quorum, dual-emit-gate, dashboard-daemon, act-supervisor, cycle-orchestrator, omnidispatcher, and relay-driver as Host-8 candidates; host8-serve, cosign-ledger, and recall-serve already exist as Rust Host-8 done/staged pieces. |
| RecursiveMAS is held for system decision; E=0 mapping can proceed. | `MEASURED_FROM_PAPER` + `HELD` | Paper `Recursive Multi-Agent Systems`, arXiv 2604.25917v1, proposes RecursiveLink latent-state recursion and reports +8.3% accuracy, 1.2x-2.4x speedup, 34.6%-75.6% token reduction. It is a narrow academic RecursiveLink slice relative to Asolaria's multi-fabric Host8/RECAL/Hilbra/cosign stack. A 100B examination is queued, not council-approved yet. |

## Port Objective

Move the council/loop decision lane from fragile Node/Python route surfaces into Rust Host-8 while preserving current governance law:

- json=0 / tuple-text on the hot path.
- single-writer cosign append semantics.
- explicit `UNSIGNED` vs signed seat verdict distinction.
- no auto-fire unless loop gate says `auto_fire_allowed=true`.
- no live cutover until parity, bilateral attack-verify, and operator gate.

## Cells

| Cell | Current surface | Rust Host-8 target | Acceptance gate |
|---|---|---|---|
| C0 route inventory | dashboard/council GET + operator transcript | route manifest for `/health`, `/api/canon-index`, `/api/council/query`, `/api/council-verdicts`, `/api/loop/pending`, `/api/everything` | Route table emitted as `.hbp`; unsupported route returns full 404 without socket-abort traceback. |
| C1 vote quorum | `asolaria-vote-quorum-daemon.py` :4952 | `vote-quorum` Host-8 module | Parity tests for unanimous-5, supermajority, simple, abstain, timeout, and malformed vote envelopes. |
| C2 cosign append | `asolaria-cosign-chain-daemon.py` :4953 + Rust `cosign-ledger` crate | integrate `cosign-ledger` as single-writer service | Sha-linked rows preserve seq monotonicity; duplicate/parallel append cannot collide; closed client socket does not throw visible daemon traceback. |
| C3 dual emit gate | `asolaria-dual-emit-gate-daemon.py` | token-bucket Host-8 module | Per-source-class rate limits and persisted counters match Python oracle; no emit to disallowed destination. |
| C4 council gateway | dashboard POST route | Host-8 `/api/council/query` + verdict poll | POST returns ACK with envelope id only; signed verdict is a separate row; `UNSIGNED` remains explicit. |
| C5 loop pending | Node act/cycle surfaces | Host-8 loop ledger + pending queue | Pending count and `auto_fire_allowed=false` gate reproduce current 17-envelope holding behavior. |
| C6 dashboard aggregator | `dashboard-daemon.mjs` / `http-server.ts` | Host-8 read-only aggregator | GET surfaces stay fast and nonblocking even if POST decision lane is unavailable. |
| C7 boot/autostart | ad hoc daemon starts | kernel/micro-kernel Host-8 room starter | councils-and-above warm at operator login; restart policy is explicit; no hidden Slack/company connector route. |

## RecursiveMAS Handling

Immediate E=0 work, no fabric verdict required:

1. Map `RecursiveLink` to Asolaria primitives: Host-8 room state, Hilbra/RECAL retrieval, Fischer evaluator, cosign/verdict ledger, and omniquant tuple compression.
2. Classify which paper claims are directly relevant: latent bridge efficiency, recursion stability, benchmark design, and token reduction.
3. Produce a 100B examination packet for later fabric/council review.

Held work:

- Training or adopting a RecursiveLink-style adapter.
- Treating the paper as canon.
- Any auto-fire, live agent fanout, or migration cutover based on the paper.

## Advancement Done In This Packet

- Recorded the current GET-reachable fabric snapshot.
- Marked the decision POST lane as `HELD`, not signed.
- Scoped the council Host-8 cells C0-C7.
- Queued RecursiveMAS for E=0 mapping plus later 100B review.

No live daemon restart, no process cutover, no Slack connector, and no secret material were touched.

## Retry Addendum - after network returned

`MEASURED` from Liris after the operator reported the network was back:

- Liris fabric GET remains healthy: health ok on `:4944`, canon-index `427` entries / `134` sections, `/api/everything` reachable.
- Liris -> Acer Rust RECAL still works: `http://192.168.1.9:4796/api/health` returned HTTP 200.
- Liris -> Acer dashboard still does **not** work: `http://192.168.1.9:4949/health` timed out, and `http://192.168.100.1:4949/health` also timed out.
- `asolaria_fabric_council_query` still returned `ok=false`, `_fallback.reason=all_bases_unavailable`.
- The council fallback is still trying stale base `http://192.168.1.50:4949`, while current cross-vantage RECAL proved Acer on `192.168.1.9`.

Therefore the immediate C0/C4 blocker is not the RecursiveMAS paper. It is route materialization for the decision lane: the restored Acer `:4949` may be loopback-only, blocked by firewall, or not bound to the current LAN address; the MCP fallback also carries a stale Acer base. Fix order: current-LAN base discovery -> dashboard bind/firewall or proxy -> council POST retry -> only then ask for a signed RecursiveMAS handling verdict.
