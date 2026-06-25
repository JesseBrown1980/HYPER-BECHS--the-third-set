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

## Anti-Deflation Addendum - `:4949` also carries the revolver/router

The `:4949` surface must not be treated as "just a dashboard" or a simple HTTP health server.

`MEASURED_FROM_SOURCE` on Liris:

- `fabric-revolver.mjs` describes the actual architecture: fixed chambers rotate `EMPTY -> LOAD -> RUN -> COLLECT -> EJECT -> EMPTY`; billions of backend addresses are tuple space; only N live workers sit in chambers; Omnispindle loads chambers; Omniflywheel routes; the fabric loop fires.
- `/api/fabric-revolver` is a real dashboard route reading `fabric-revolver-runtime-latest.json`, `chambers-latest.json`, or `fabric-revolver-state.json`.
- Local Liris `http://127.0.0.1:4944/api/fabric-revolver` returns HTTP 200 and a real chamber state: chamber 0 `COMPLETE`, pid `BH.REVOLVER.CHAMBER.000`, `rotation=2`, `totalLoads=9`, `lastTickAt=2026-05-26T23:56:28.841Z`.
- Existing Liris reports classify the Liris revolver as `STALE_IDLE`, not absent: `lastTickAt=2026-05-26T23:56:28.841Z`, stale opencode model id, and missing preferred dashboard feed files.
- Prior Liris dashboard docs also recorded the older stale 8-chamber state and wrong Acer handshake route as a known routing problem.

`OPERATOR_OBSERVED` from Acer in the current session:

- After a fresh `:4949` restart, the Node process bound `0.0.0.0:4949` and then consumed about 85% of one core.
- Operator identified this as the Brown-Hilbert PID spinner / fabric-revolver / router path, not an idle bug.

Honest synthesis:

- The revolver/router is real and attached to the `:4949` legacy surface.
- Killing `:4949` kills more than a dashboard; it interrupts the chamber/spinner/router surface, even if persisted state lets it restart.
- From Liris, today's Acer high-CPU spin is `OPERATOR_OBSERVED` and plausible, but forward progress is still `UNVERIFIED_CURRENT` until Acer shows fresh `lastTickAt`, rotation, load/collect/eject counters, or dispatch-log growth.

Host-8 port consequence:

- Split the decision plane into at least two Host-8 responsibilities:
  1. **responder/gateway**: `/health`, `/api/canon-index`, `/api/everything`, `/api/council/query`, `/api/council/verdicts`, `/api/loop/pending`; must stay responsive under worker load.
  2. **revolver/router worker**: Brown-Hilbert PID spinner + chamber rotation + dispatch bridge; must run in a separate thread/process with explicit yield/backpressure and progress counters.
- The port must preserve the revolver's chamber semantics while preventing the old single-threaded Node failure mode where worker activity starves the council/HTTP responder.
- Add acceptance gate C0.1: prove `lastTickAt/rotation/counters` advance while `/health` and `/api/council/query` still return within bounded latency.

## Acer Forward-Progress Addendum - finite burst, not proven revolver progress

`OPERATOR_OBSERVED_ACER` / `ACER_MEASURED` from the follow-up probe:

- `:4949` PID 20812 had accumulated substantial CPU (`573s` reported), but the follow-up sample showed `dCPU=0s over 4s => 0% of one core`.
- Therefore the earlier high CPU was a finite burst, not a permanent infinite loop.
- Acer-side revolver state files were stale: `chambers-latest` and `fabric-revolver-runtime-latest` were May-dated; `fabric-revolver-state.json` was absent.
- Acer e-cohort dispatch files were stale to `2026-06-20`; no today-write was proven in the samples.
- Acer source inspection showed the dashboard `/api/fabric-revolver` is primarily a viewer over feed/state files; the real worker/router surfaces are separate daemons/scripts such as `fabric-revolver.mjs`, `auto-fabric-query-daemon --watch`, and `gnn-dispatch-bridge --watch`.

Corrected read:

- The Brown-Hilbert PID spinner / fabric-revolver / dispatch router are real architecture and must not be deflated away.
- Today's measured Acer `:4949` burst is not enough to claim live revolver forward progress.
- The next diagnostic is a true progress probe: sample `lastTickAt`, `rotation`, load/collect/eject counters, and dispatch-log sizes twice while also measuring `/health` and `/api/council/query` latency.

Operator supplied old Acer desktop notes as archaeology leads, especially `SLICES.txt`, `Sub milisecond loop.txt`, `Full system.txt`, `ASK THE FABRIC.txt`, and `REMEMBER the old systems builds the new.txt`. These exact files are not present on the Liris filesystem in this session, so their contents remain Acer-side evidence/leads until copied or rehydrated here.

## Hilbert Intersection / PTP Collision Geometry Addendum

`MEASURED_LIRIS_SOURCE`:

- `C:/Users/rayss/Asolaria/tools/cube/hilbert-intersection-engine.js` exists locally and declares itself `REAL 6^4 intersection cube`.
- The same engine shape is mirrored under `C:/Users/rayss/Asolaria/engines/hilbert-intersection-engine.js`.
- The source computes `6 x 6 x 6 x 6 = 1,296` Brown-Hilbert cube intersection points over layer, protocol, surface, and dimension axes.
- `C:/Users/rayss/Asolaria/brown-hilbert/08-2026-04-10-cube-multiplication.md` records `6^4 = 1,296 intersection points`.
- `C:/Users/rayss/Asolaria/ASOLARIA-OS-MASTER.md` lists `hilbert-intersection-engine` among live components.

`OPERATOR_OBSERVED_ACER` from the old Acer desktop notes read on Acer:

- The Hilbert intersection engine is not "just a hash"; it is the Brown-Hilbert collision geometry.
- The axes are cubes of primes; rule-of-3 digital-root plus primes / primes^2 / primes^3 form the PTP non-colliding lanes.

Host-8 consequence:

- C0.1 must preserve the Brown-Hilbert PID spinner as geometry, not collapse it into a hash lookup.
- Add follow-on gate C0.2: prove the Host-8 worker can walk the same `6^4` intersection geometry and preserve PTP lane separation while the responder remains nonblocking.

## Acer Rust RECAL Peer Rebuild Addendum

`OPERATOR_OBSERVED_ACER` from the live `recall-serve` log:

```text
RECALLSERVE|building inverted index from C:\asolaria-acer\recall-atlas\data/ASOLARIA-ACER-RECALL.hbi ...|json=0
RECALLSERVE|ok=true|engine=rust-inverted|colony=acer|bind=0.0.0.0:4796|rows=591286|terms=2614638|postings=23930053|skipped=0|built_ms=55155|key=true|peers=1|max_conn=256|json=0
```

`MEASURED_LIRIS` follow-up over the LAN:

- `http://192.168.1.9:4796/api/health` returned HTTP 200 from `asolaria.recall.rust.v1`.
- Acer health reports `bind=0.0.0.0`, `port=4796`, `rows=591286`, `terms=2614638`, `postings=23930053`, `built_ms=55155`, `key_configured=true`, and `peers=[{name:liris, base:http://192.168.1.10:4791}]`.
- Liris -> Acer public search `q=brown-hilbert` returned HTTP 200, `candidate_count=49`, and real Acer rows.
- Liris local RECAL `http://127.0.0.1:4791/api/health` remains HTTP 200 with `rows=10644`, `key_configured=true`, and peer `acer`.
- Liris local search `q=atlas` returned HTTP 200 with a real Liris atlas row.

Honest read:

- `peers=1` and peer identity `liris` are now measured from the Acer Rust engine's own health surface.
- The route is live from Liris to Acer and the local Liris RECAL remains live.
- A persistent socket or active session should not be claimed unless the engine exposes a live-connection counter; the current measured claim is configured peer plus successful cross-vantage search.
- Data-plane RECAL is healthy and durable while the decision-plane/council Host-8 work remains the active migration cell.
