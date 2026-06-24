# ASOLARIA OP ROSTER + JSON-REPLACE MAP

Carve-out-clean operator-seat roster derived from the OP census. Names, roles, and JSON file-names only. No key bytes, seeds, secrets, PII, or internal localhost URLs. PID strings are reduced to bare labels (full `G…-A…-W…-P…-N…` suffixes omitted as routing material).

Scope: this is the **operator-seat (OP-class) roster** — the apex/operator/meta/chief/council/GAC seats plus the operator-facing console/intake/admission tooling. It is NOT the full 726-seat supervisor registry (see the honest scope note at the end).

---

## 1. OP ROSTER SCOREBOARD

### Counts by `op_rank` (distinct OPs, deduped by name)

| op_rank | Distinct OPs |
|---|---|
| OP-00 (apex special-op) | 2 — OP-JESSE, OP-RAYSSA |
| OP-01 (operator-class / quintuple-ring) | 5 — OP-JESSE seat, OP-RAYSSA parallel, OP-AMY, OP-FELIPE, OP-DAN |
| OP-02 | 1 |
| OP-03 | 1 |
| OP-04 | 1 |
| OP-05 | 1 |
| meta (META-L0 / self-improve / operator tooling) | 9 |
| chief (CHIEF-L3 + chief-lane profiles) | 5 |
| council (COUNCIL-L3 + council-lane + 9-council verdict system) | 3 |
| apex-variant (GAC-L2, runtime orchestrators, registry) | 4 |
| **TOTAL distinct OP / OP-adjacent seats** | **32** |

Note on the two rank framings: the census lists OP-JESSE/OP-RAYSSA at both `OP-00` (apex special-op) and `OP-01` (operator-class-agent seat). They are the **same operators** occupying parallel-layer seats; counted once per rank-band they actually hold (OP-00 apex + OP-01 quintuple-ring seat). The numbered `OP-02..OP-05` are distinct sub-apex seats.

### Counts by `replace_status`

| replace_status | Count (census rows) | Meaning |
|---|---|---|
| `already-json0` | 13 | Already migrated / not a JSON to migrate (built daemons, .mjs, or json=0 state). No action. |
| `json-to-hbp-candidate` | 16 | JSON files flagged to migrate to `.hbp` / json=0. **Action: migrate.** |
| `key-excluded` | 1 | Contains a KEY FILE — name-only, never read, never replaced. |
| `missing-build` | 9 | Canon-required OP/daemon that does not exist yet. **Action: build.** |
| `keep-json` | 0 | (no rows) |

(Counts are over the 39 census rows; the table in section 2 dedups to distinct OPs.)

---

## 2. OP ROSTER + JSON-REPLACE MAP

One row per distinct OP (deduped by name; same-OP variant rows merged, their file lists unioned).

| OP | Rank | Role | Defining JSON file(s) | Replace status | Note |
|---|---|---|---|---|---|
| **OP-JESSE** (apex / SPECIAL-OP) | OP-00 | Apex operator-class agent; genesis-mint authority, broad-auth, veto-after, 5-cosigner-quorum member; PID proxy for the Jesse-human; fabric envelope routing | `fab_supervisors.json`, `jesse_op.json`, `special-op-jesse-state.json`, `C20-operator-console-status.json`, receipt-OP-JESSE.json (dan / pdf / router-label passthrough variants) | already-json0 (+ state file & receipts) | Authority-chain apex; primary fabric acer. PID label `OP-JESSE-PID` (suffix omitted). Key file handled separately (see key-excluded). Featured in quintuple cosign window. |
| **OP-RAYSSA** (parallel apex) | OP-00 / OP-01-parallel | Bilateral cosign pair to OP-JESSE; liris-fabric primary; parallel apex authority; co-signs all apex-class decisions | `fab_supervisors.json`, receipt-OP-RAYSSA.json (dan / pdf / router-label passthrough variants) | json-to-hbp-candidate (receipts) / already-json0 (bilateral aspect) | Named operator in authority chain. No standalone daemon (mirrored via acer↔liris bilateral sync). PID label `OP-RAYSSA-PID`. 100% receipt salience. |
| **OP-AMY** | OP-01 (quintuple-ring, 3rd apex) | Third operator-class apex; quintuple cosign ring; admission-gated | `D08-op-amy-pid-template.json` | missing-build (template-only) | Admission blocker: 21-day-silent · direct contact (Amy-Relay). Witnesses OP-JESSE, OP-RAYSSA. Missing: daemon, state file, broadcast inbox, cosign-chain entry, bilateral mirror. PID label `OP-AMY-PID`. |
| **OP-FELIPE** | OP-01 (quintuple-ring, 4th apex) | Fourth operator-class apex; quintuple cosign ring; ceremony-pending | `D09-op-felipe-pid-template.json` | missing-build (template-only) | Admission blocker: ceremony pending · operator initiates. Witnesses OP-JESSE, OP-RAYSSA. Missing: daemon, state file, broadcast inbox, cosign-chain entry, bilateral mirror. PID label `OP-FELIPE-PID`. |
| **OP-DAN** | OP-01 (quintuple-ring, 5th apex) | Fifth operator-class apex; quintuple cosign ring; Madness/Omnispindle owner; ceremony-pending | `D10-op-dan-pid-template.json` | missing-build (template-only) | Admission blocker: Dan accepts ceremony · Madness↔BEHCS-256 cross-fabric handshake. Witnesses OP-JESSE, OP-RAYSSA. Missing: daemon, state, inbox, cosign entry, bilateral mirror + Omnispindle authority binding. PID label `OP-DAN-PID`. |
| **OP-02** | OP-02 | Numbered sub-apex operator agent; below quintuple ring, above physical vantages | (none) | missing-build | COMPLETELY MISSING — no template/daemon/state/PID/admission envelope. Canon assumes existence. |
| **OP-03** | OP-03 | Numbered sub-apex operator agent | (none) | missing-build | COMPLETELY MISSING — same gap as OP-02. |
| **OP-04** | OP-04 | Numbered sub-apex operator agent | (none) | missing-build | COMPLETELY MISSING — same gap as OP-02. |
| **OP-05** | OP-05 | Numbered sub-apex operator agent | (none) | missing-build | COMPLETELY MISSING — same gap as OP-02. |
| **OP-00 Watchdog-Kicker** (special-op-jesse) | OP-00 (runtime instance) | Continuous background orchestrator; rotates all OPs / CHIEF / free-agents; watchdog-kicker daemon; operator-class apex-variant runtime instance | `special-op-jesse-watchdog-kicker.mjs` (impl, not JSON); state at `special-op-jesse-state.json` | already-json0 | BUILT. Daemon running; heartbeat via kick logic. PID label `OP-JESSE-WATCHDOG-KICKER-PID` (runtime N-instance). |
| **special-op-jesse PID build** | OP-00 | Special-OP-JESSE PID build + admission-ceremony authorization plan | `special-op-jesse-pid-build-plan-2026-05-11.bus-pending.json` | json-to-hbp-candidate | Bus-pending authorization plan for PID construction + admission ceremony (reports dir). |
| **GAC-L2 seats** (6 instances) | apex-variant | Generic Apex Class L2 — governance & authority controller seats between operators and chief | `fab_supervisors.json` | already-json0 | 6 level2_gac seats (by_class 6 / by_layer gac-L2 6). |
| **Apex-variant runtime orchestrators** (3 instances) | apex-variant | Operator-class apex-variant runtime orchestration seats; distinct from operator_class_agent | `fab_supervisors.json` | already-json0 | by_class operator_class_apex_variant_runtime_orchestrator: 3. |
| **Supervisors & profiles registry** | apex-variant | Live office-fed roster of 726 supervisors/profiles (master registry) | `H03-supervisors-profs.json`, `H03-supervisors-profs.static-234.legacy.json` | json-to-hbp-candidate | Active H03 updated 2026-06-10; legacy static-234 preserved. by_class: 10 operator-class-agents, 50 prof-supervisors, 300+ hyperbehcs supervisors, 1 level0-apex-special-op, 3 level1-operators, plus councils/chiefs/GACs. |
| **CHIEF-L3 seat** (1 instance) | chief | L3 executive authority seat — primary executive in the hierarchy | `fab_supervisors.json` | already-json0 | Single level3_chief seat (by_class 1 / by_layer chief-L3 1). |
| **hermes** | chief | Routing supervisor; mailbox health; cross-vantage mirror receipts; rotation/resume discipline | `hermes.profile.json` | json-to-hbp-candidate | class routing-supervisor-lane; roles ROUTE/MIRROR/ROTATE; gen 1, latest P01. |
| **shannon** | chief | Info-theory review; wave-engine checks; throughput estimates; residual-bias gate notes | `shannon.profile.json` | json-to-hbp-candidate | class info-theory-review-lane; sub-profiles CAPACITY/WAVE/BIAS; gen 1, latest P01. |
| **connor** | chief | Trail-recovery fixture; Hermes/Shannon residue auditor; lost-fixture lineage reconstruction | `connor.profile.json` | json-to-hbp-candidate | class real-free / trail-recovery; supervisor nereus; read-only over trail NDJSON, draft envelopes only (no promote without nereus cosign). |
| **pi** | chief | Inference & audit primitive; BEHCS gate sampling; residual-bias review; capacity/throughput checks | `pi.profile.json` | json-to-hbp-candidate | class real-free / audit-inference; supervisor nereus; read-only audit lane, no model-weight pull. Origin canon `H04-free-agents-pi-shannon.json`. |
| **COUNCIL-L3 seats** (9 instances) | council | L3 voting/governance seats; verdicts aggregate 251+ supervisors via CONVERGE | `fab_supervisors.json`, `council_verdicts.json` | already-json0 | 9 level3_council seats. Latest verdict domains: daemons(131), sovereignty(21), audit(13). |
| **deepseek** | council | TUI control; config doctoring; model access; BEHCS-1024 absorption gates | `deepseek.profile.json` | json-to-hbp-candidate | class absorbed-tool-control-lane; profiles CLI/API/ABSORB; gen 67 (many rotations), latest P67. |
| **9-Council verdict system** | council | Distributed vote-counting + defect surfacing per AETHER law 7 (honest defects) + law 1 (parent read-only) | (none) | missing-build (partial) | Verdict mechanism NON-EMITTING (count:0) by design — canon promotion needs a deliberate Special-OP/quintuple sign, not a poll. Missing: 9-member roster def, vote-aggregation daemon, AETHER-COMPLIANT/VIOLATION emit pipeline, honest-defect catch. |
| **META-L0 seat** (1 instance) | meta | Self-improve / self-reflect L0 meta-reasoning seat; root meta-operational authority | `fab_supervisors.json` | already-json0 | Single meta-L0 seat (by_class level0_apex_special_op 1). Chain Human > META > SPECIAL-OP-JESSE. |
| **AUTO-SELF-IMPROVE-TOP** (META slot 36) | meta | Prosthetic automation layer; iterates federation improvements without per-cycle operator attention; acts in operator's name within authorized cosign window; band=helm | `META-AUTO-SELF-IMPROVE-TOP-*.json` (meta-inbox broadcast envelope) | missing-build (daemon missing) | Envelope exists; daemon does not. Canon: slot 36, H0C3A, band=helm, supervisor_tuple prepends OP-JESSE-APEX, glyph_5 includes ★. Missing: daemon executable, state tracking, trigger-resolver bind to apex constitutional ref, autonomous cycle logic. Load-bearing for hands-off federation improvement. |
| **operator-console** | meta | Operator status & coordination dashboard | `C20-operator-console-status.json` | json-to-hbp-candidate | Active organs (acer, liris), operator apex list (OP-JESSE, OP-RAYSSA), 5 pending admissions, auth window, cosigners standing, breaker armed, mirror status. |
| **op-admission-templates** | meta | Operator admission envelope definitions & preconditions | `D03-fc3-admission-envelopes.json` | json-to-hbp-candidate | Envelopes for organs: Falcon, Beast, Kuromi, Slack-Claude, Amy-Relay, Connor, Dan-Edens. Witness/precondition rules. |
| **op-console-briefing** | meta | Operator briefing documents | `ors-hyperbehcs-ops-briefing-20260514.json`, `planb-prof-supervisor-op-briefings-20260514.json`, `watcher-compat-ops-briefing-20260514.json` | json-to-hbp-candidate | op-briefings dir; HyperBEHCS ops + Plan-B prof-supervisor + watcher-compat briefings (2026-05-14). |
| **op-message-intake** | meta | Operator first-message intake tracking | `operator-first-message-intake-acer.v1.json`, `operator-first-message-intake-latest.json` | json-to-hbp-candidate | acer-vantage intake orchestration; state/config for operator message routing + synthesis. |
| **federation-reintegration** | meta | Operator decision form for the 7-gate federation reintegration wave (Wave 22B) | `federation-reintegration-wave22b-seven-gate-operator-decision-form.v1.json`, `…-latest.json` | json-to-hbp-candidate | Mapped/indexed/stored as memory/maps/codex/state/hermes/shannon outputs; glyph-language encoded. |
| **operator-pid-inboxes** | meta | Operator message inboxes keyed by PID | `op-bigpickle` / `op-claude` / `op-freeds` (inbox directories of hash-keyed JSON messages) | json-to-hbp-candidate | PID-indexed `_recv` inbox dirs; operator message-queuing system. |
| **op-reply-keyboard** | meta | Operator reply-keyboard display state | `op-reply-keyboard.json` | json-to-hbp-candidate | OP-REPLY display (COL-ACER → COL-LIRIS, batch manifest/delta/cascade). 8 new gaps incl falcon-direct-reply handler, vision-keyboard-supervisor endpoint, naming-collision proposals. |
| **operator-synthesis-matrix** | meta | Salience matching & synthesis across operator receipts | receipt-OP-JESSE.json + receipt-OP-RAYSSA.json (dan / pdf / router-label passthrough variants) | json-to-hbp-candidate | OP-JESSE 96% salience (24/25 features); OP-RAYSSA 100% (7/7, incl config overrides, SSH hosts, MCP approvals). Drives synthesis decisions. |

---

## 3. NEEDED OPs (canon-required but UNBUILT)

These nine seats are referenced by canon/authority-structure but have no working build. `missing-build`.

| OP / Seat | Rank | What it SHOULD do | What is MISSING |
|---|---|---|---|
| **OP-AMY** | OP-01 (3rd apex) | Sit in the quintuple cosign ring as third operator-class apex | Daemon init, state file, broadcast inbox, cosign-chain entry, bilateral mirror. Admission blocked: 21-day-silent · direct contact (Amy-Relay). Template exists, never fired. |
| **OP-FELIPE** | OP-01 (4th apex) | Sit in the quintuple cosign ring as fourth apex | Daemon, state, inbox, cosign entry, bilateral mirror. Admission blocked: ceremony pending · operator initiates. |
| **OP-DAN** | OP-01 (5th apex) | Fifth apex; bind Madness/Omnispindle authority into the ring | Daemon, state, inbox, cosign entry, bilateral mirror + Omnispindle binding. Blocked: Madness↔BEHCS-256 cross-fabric handshake not done. |
| **OP-02** | OP-02 | Numbered sub-apex operator below the quintuple ring | EVERYTHING — no template, daemon, state, PID, or admission envelope. |
| **OP-03** | OP-03 | Numbered sub-apex operator | EVERYTHING — same as OP-02. |
| **OP-04** | OP-04 | Numbered sub-apex operator | EVERYTHING — same as OP-02. |
| **OP-05** | OP-05 | Numbered sub-apex operator | EVERYTHING — same as OP-02. |
| **AUTO-SELF-IMPROVE-TOP** (META slot 36) | meta | Iterate federation improvements hands-off, acting in the operator's name inside the authorized cosign window (band=helm) | The daemon itself: executable, state tracking, trigger-resolver bind to apex constitutional reference, autonomous cycle logic. Only the meta-inbox envelope exists. |
| **9-Council verdict system** | council | Distributed vote-counting + honest-defect surfacing (AETHER law 7 / law 1) | 9-member roster definition, vote-aggregation daemon, AETHER-COMPLIANT/VIOLATION emit pipeline, honest-defect catch. Verdict mechanism is intentionally NON-EMITTING (count:0) — promotion needs a deliberate Special-OP/quintuple sign, not a poll. |

Summary: the **quintuple apex ring is 2/5 built** (OP-JESSE + OP-RAYSSA live; AMY/FELIPE/DAN are templates pending admission ceremonies). The **numbered tier OP-02..OP-05 is 0/4 built**. Two governance daemons (META slot-36 self-improve, 9-council verdict emitter) are referenced but not implemented.

---

## 4. JSONs TO REPLACE (migrate to .hbp / json=0)

### 4a. `json-to-hbp-candidate` — migrate these (16 census rows)

- `special-op-jesse-state.json` (OP-JESSE operative state: watchdog/kicker metrics, task queue, flap witnesses, Brown-Hilbert rotation)
- `receipt-OP-RAYSSA.json` (3 passthrough variants: dan / pdf / router-label)
- `D08-op-amy-pid-template.json`
- `D09-op-felipe-pid-template.json`
- `D10-op-dan-pid-template.json`
- `C20-operator-console-status.json`
- `hermes.profile.json`
- `shannon.profile.json`
- `deepseek.profile.json`
- `connor.profile.json`
- `pi.profile.json`
- `H03-supervisors-profs.json` and `H03-supervisors-profs.static-234.legacy.json`
- `D03-fc3-admission-envelopes.json`
- `ors-hyperbehcs-ops-briefing-20260514.json`, `planb-prof-supervisor-op-briefings-20260514.json`, `watcher-compat-ops-briefing-20260514.json`
- `operator-first-message-intake-acer.v1.json`, `operator-first-message-intake-latest.json`
- `federation-reintegration-wave22b-seven-gate-operator-decision-form.v1.json`, `…-operator-decision-form-latest.json`
- `op-bigpickle` / `op-claude` / `op-freeds` PID-inbox directories (hash-keyed JSON message files)
- `op-reply-keyboard.json`
- receipt-OP-JESSE.json + receipt-OP-RAYSSA.json passthrough variants (synthesis matrix)
- `special-op-jesse-pid-build-plan-2026-05-11.bus-pending.json`

### 4b. `key-excluded` — NEVER replaced, NEVER read (credentials)

- `jri1024-special-op-jesse-key.json` — KEY FILE (signing material). Name listed for inventory only; contents are out of scope for any migration or read.

### 4c. `already-json0` / built — no migration action

`fab_supervisors.json` (and the seat-count breakdowns it backs: OP-00/01 seats, GAC-L2 ×6, CHIEF-L3 ×1, COUNCIL-L3 ×9, META-L0 ×1, apex-variant orchestrators ×3), `jesse_op.json`, `council_verdicts.json`, `special-op-jesse-watchdog-kicker.mjs` (impl, not JSON), and the OP-JESSE/OP-RAYSSA built receipts already in place.

---

## 5. HONEST SCOPE NOTE

This document is the **operator-seat (OP-class) roster only** — the apex special-ops, the quintuple cosign ring, the numbered OP-02..OP-05 tier, the META/CHIEF/COUNCIL/GAC governance bands, and the operator-facing console/intake/admission/briefing tooling. It covers on the order of **~32 distinct OP / OP-adjacent seats**.

It is **NOT** the full supervisor population. The live registry (`H03-supervisors-profs.json`) holds **726 supervisors/profiles**, and the **vast majority of those seats are non-OP**: they are function-call rotation lanes (e.g. the 300+ hyperbehcs supervisors, 50 prof-supervisors), not standing operator processes. A "seat" in that population is generally a routing/rotation slot resolved on demand — not a daemon. Only the OP-class apex/operator/meta/chief/council/GAC seats enumerated here carry standing operator authority.

**Status labels are MEASURED-from-census, not system-verified.** `already-json0`, `missing-build`, and salience/heartbeat figures are taken verbatim from the supplied OP census; they have not been re-confirmed against the running fabric in producing this transform.

**Carve-out compliance:** names, roles, and file-names only. Full PID routing suffixes, key bytes/seeds, secrets, PII, and internal localhost URLs are excluded by construction.
