<!-- STAGED build packet (workflow-generated draft). NO CUTOVER. Verifier = owning 1.81 CI + liris attack-verify, NOT this packet. auto_fire=false. -->

# BUILD PACKET — Rust Host-8 council/loop port (STAGED, additive, v2 — adversarially hardened)

Tag legend: **[M]** MEASURED-from-source · **[D]** DESIGN-proposed · **[U]** UNVERIFIED (must be proven by the 1.81 owning gate or a parity receipt before any claim).

This v2 folds in **every** real fix from the four adversarial verifier passes (quorum-parity, engine-isolation, cosign/tier-safety, owning-CI-1.81). Each fix carries a `FIX-n` back-reference so liris can map the packet to the review that demanded it.

---

## 1. What + why  **[D over M grounding]**

The acer super-dashboard council/loop runs inside a **single-thread Node event loop on `:4949`** **[M]** (`super-dashboard-server.mjs`, PORT=`SUPER_OS_PORT||4949`). A loop `tick()` or a bus fetch blocks the SAME loop that serves HTTP, so `/api/*` times out during a crank — the wedge memory recorded (`:4949` 85%→0% burst). The Rust target `host8-serve` `:5088` reproduces the SAME disease today: a **serial accept loop** `for stream in listener.incoming() { handle_client(.., &mut gnn, &mut registry) }` **[M]** (`main.rs:154-161`) runs handlers inline, so a crank blocks accept. The proven cure is `recall-serve`'s **thread-per-conn + Arc read-only state + bounded concurrency + keep-alive** core **[M]** (it fixed the identical Node 591k-row stall). This packet ports council/query+verdicts, the GNN→dispatch→veto loop, vote-quorum, the 6-tier transit gate, and the engine-drive crank onto that non-stalling core as **new sibling crates** on a **new port `:5090`** — additive, no cutover; `:4949`/`:4952`/`:4953` and `host8-serve:5088` stay up. The engine cranks on its **own thread** so the responder answers while it cranks, with every spawn gate preserved.

---

## 2. Crate layout + file responsibilities  **[D crate / M sources]**

### Reused as-is — do NOT redefine  **[M]**
- `asolaria-server-cosign-ledger` (`servers/cosign-ledger`) — `CosignChain`, `CosignRow`, `Signature`, `CosignChainErr`, `GENESIS_PREV_SHA16`, wire shape. `#![no_std]`+`alloc`, rust-version **1.75**. host8-serve already path-deps + constructs it.
- `asolaria-server-tier-policy` (`servers/tier-policy`) — `AccessTier`, `policy_for`, `classify_path`, `quintuple_auth_covers`, `TIER_POLICY_TABLE`.
- `asolaria-server-highway` (`servers/highway`) — `check_transit` / `execute_transit`.

### Modified in place (not new) — required by the verifiers
- **`servers/cosign-ledger/src/lib.rs`** — **FIX-A2/A3/Flaw7**: (a) **COPY** (never move) the kernel v0.2 body (`canonical_bytes_of_row`+`sha16_of`+monotonic/chain/kind checks) up from `kernel/core/src/cosign_chain/mod.rs`, keeping it **core+alloc-only** so the no_std crate still checks AND the separate `kernel/Cargo.toml` sub-workspace check stays green; (b) add `CosignChain::resume_from(tail) -> Self` seeding `next_row=last.row+1`, `head_sha16` from the last row — construct via resume, **never `new()`**, in the council; (c) collapse to **ONE append surface** (the `&mut self` method holding both in-memory head + the ndjson write), and **retire/redirect** the module-level `append(&[u8])` + `static APPEND_SEQ_COUNTER` lane so there are not two counters. All `std` fs persistence stays in the **council crate**, never in the no_std ledger.
- **`servers/tier-policy/src/lib.rs`** — **FIX-C2**: add a **distinct `redaction_policy` field** to `TierPolicy`/`TIER_POLICY_TABLE` (it currently collapses the JS `redaction_policy` + `enumeration_policy` into one `EnumerationPolicy`). Carry SECRET=`deny_public_content`, HIDDEN=`fully_redacted_metadata_only`, etc., as a separate column so the canonical crate is the single source of truth (REPO_LAW Invariant 5) and the council does not hold a drifting local map.
- **root `Cargo.toml`** — **FIX-Flaw1 (false-green killer)**: `[workspace].members` is an **explicit list, no globs** **[M]** — add **both** new crates or the gate goes vacuously green having linted zero new lines.

### New crate 1 — `asolaria-server-vote-quorum` (lib + optional feature-gated bin)  **[D crate / M logic]**
| file | responsibility | budget |
|---|---|---|
| `src/json.rs` | **FIX-F2**: generic `JsonValue` (Object/Array/Str/Num/Bool/Null) + recursive `canonicalize()` matching python `json.dumps(sort_keys=True, ensure_ascii=False)` separators `", "`/`": "`, keys sorted at **every depth**, UTF-8 passthrough; a minimal parser to read on-disk rows. No serde. | ~320 |
| `src/rules.rs` | `QUORUM_RULES`, `QUINTUPLE`, `AUTHORIZED_CLASSES`, `rule_for`, `is_authorized` (**FIX-F7**: NO time-window gate inside it), window constants as **data only**. | ~240 |
| `src/quorum.rs` | `evaluate_quorum` (**FIX-F1** cross-multiply thresholds, **FIX-F4** internal auth filter, **FIX-F5** unanimous set-superset, abstain-excluded, min-3 floor). | ~220 |
| `src/ledger.rs` | `VoteLedger` behind ONE `Mutex` (**FIX-A4**): `sha16`, `last_row_hash` (**FIX-F5** 2048-tail/last-non-empty/missing-key fallback), `now_iso` (ms), `append_row` (excludes `row_hash` from hash; key is `antecedents`). | ~260 |
| `src/cast.rs` | **FIX-F3**: full cast/submit state machine — `submit` (`VOTE-`+sha16 mint), `cast` (400/404/409 ladder, one-vote-per-pid), `outcome_exists` idempotency, conditional outcome append on `{PASS-UNANIMOUS,PASS-MAJORITY,PASS-SUPERMAJORITY,PASS-AUTO,REJECT}`, nested `tally` outcome row — all under the single `VoteLedger` mutex so read-tail→evaluate→append is atomic. | ~300 |
| `tests/parity.rs` | re-derive `row_hash` over the **on-disk** ledgers (queue/votes/outcomes) by parse→drop `row_hash`→canonicalize→sha16; **FIX-F1** table-test every rule at `total` ∈ 3..7 incl. the `3,3,2` boundary; idempotency + 409 tests. | ~300 |

### New crate 2 — `asolaria-server-council` (bin)  **[D]**
| file | responsibility | budget |
|---|---|---|
| `src/main.rs` | arg/env, `TcpListener::bind(127.0.0.1:5090)`, **thread-per-conn** accept, `MAX_CONN` 503 fast-close, spawn engine thread + cosign-writer thread, build `Arc<CouncilState>`. **FIX-Flaw3**: `fn main()` returns `()` (NOT `-> !`). | ~250 |
| `src/http.rs` | keep-alive loop (`set_read_timeout(30s)`, `MAX_REQS_PER_CONN`), header parse, `respond()` (**FIX-Flaw5** `write_all` + read-to-completion; never bare `.read()/.write()`). | ~240 |
| `src/hbp.rs` | `hbp_escape` + `hbp_line(kind,&[(k,v)]) -> "…|json=0\n"`. | ~120 |
| `src/routes.rs` | route `match path`; **json=0 lane** for council/loop; **FIX-F6** authority lane exempt from json=0 (emits real `application/json` or proxies Node). | ~340 |
| `src/redact.rs` | **FIX-C1/C4**: every outbound body passes through tier gate — classify each item, apply `redaction_policy`, emit `proof_sha16`, assert `content_dumped=false`. | ~240 |
| `src/bus.rs` | std-net HTTP/1.1 client to `BUS_URL=http://127.0.0.1:4947` (3s timeout, 502 fallback like `proxyBus()`); **FIX-Flaw5** `write_all`/read-loop. | ~260 |
| `src/cosign_writer.rs` | **FIX-Flaw C/A1**: dedicated **single cosign-writer thread** owning the one `CosignChain` (resume_from disk), fed by an append channel; lock scope = in-memory head only, never across the ndjson write; `catch_unwind` + explicit `PoisonError` recovery. | ~220 |
| `src/loop_engine.rs` | C0.1 engine-drive thread + resolve-only `tick`/`pending`/`veto`; **FIX-A/B/E** consumer-side gate. | ~420 |
| `src/canon_index.rs` | memory-dir scan; **FIX-C4** filenames+counts only, each orphan through `classify_path`. | ~150 |
| `src/tier.rs` | wraps tier-policy + highway; `auth_covers` real time check (**FIX-C3** fail-closed); UNSIGNED-vs-SIGNED split. | ~280 |
| `tests/*.rs` | json=0 body tests (no `{`/`}`) for council/loop lane; **FIX-B** grep test asserting every `engine_tx.send` site is the verified-operator path; gate tests `process_launch=0`/`auto_fire_allowed=false`; **FIX-C1** SECRET/HIDDEN-payload-not-echoed; **FIX-C3** transit-to-Secret-DENIED-today. | ~320 |

All files < 2000 lines (no-bloat headroom; host8-serve `main.rs` at **1958** **[M]** is **untouched** — only 42-line headroom, confirming new-crate-not-inline is correct). **[M no-bloat clean]**

---

## 3. vote-quorum Rust port — DRAFT module  **[D / CI-PENDING — not built, not gate-run]**

```rust
// crate: asolaria-server-vote-quorum  —  DRAFT, CI-PENDING (1.81 owning gate is the verifier)
// edition = "2021", rust-version = "1.75"   (FIX-Flaw6: match the other six server crates, NOT 1.81)
// deps: sha2 = { workspace = true }          (no serde — FIX-F2 controls canonical bytes; FIX-Flaw2 avoids MSRV-drift lints)
#![allow(clippy::doc_lazy_continuation)]      // FIX-Flaw4: 1.81-known lint; do NOT add manual_div_ceil (unknown on 1.81 -> -D warnings hard error, FIX-Flaw2)

// ---------- rules.rs : exact parity with python QUORUM_RULES ----------  [M]
pub enum Rule { Unanimous5, Supermajority23, SimpleMajority, AutoPass }
pub enum Pool { Quintuple, Authorized, Any }
pub struct QuorumRule { pub rule: Rule, pub pool: Pool, pub operator_witness_required: bool }

pub const QUINTUPLE: [&str; 5] = ["OP-JESSE","OP-RAYSSA","OP-AMY","OP-DAN","OP-FELIPE"]; // [M] governance handles
pub const AUTHORIZED_CLASSES: [&str; 4] = ["Special-OP","OP","Asolaria-PID","Profile"];   // [M]

pub fn rule_for(class: &str) -> QuorumRule { // [M] QUORUM_RULES.get(class, DEFAULT)
    use Rule::*; use Pool::*;
    match class {
        "LAW_CHANGE" | "CP_MINT" => QuorumRule{ rule:Unanimous5,     pool:Quintuple,  operator_witness_required:false },
        "USB_WRITE"             => QuorumRule{ rule:Supermajority23, pool:Authorized, operator_witness_required:true  },
        "HEARTBEAT_ACK"         => QuorumRule{ rule:AutoPass,        pool:Any,        operator_witness_required:false },
        // DAEMON_OP | MEMORY_WRITE | COSIGN_APPEND | GHOST_GC | DEFAULT (and unknown):
        _                       => QuorumRule{ rule:SimpleMajority,  pool:Authorized, operator_witness_required:false },
    }
}

// FIX-F7: is_authorized does NOT consult LAW_WINDOW_END / OP_WINDOW_END (python L118-123 doesn't).
pub fn is_authorized(voter_pid: &str, pool: &Pool) -> bool { // [M]
    match pool {
        Pool::Quintuple  => QUINTUPLE.contains(&voter_pid),
        Pool::Authorized => QUINTUPLE.contains(&voter_pid)
            || AUTHORIZED_CLASSES.iter().any(|c|
                 voter_pid.starts_with(&alloc::format!("AGT-{c}")) || voter_pid.starts_with(c)),
        Pool::Any        => true,
    }
}

// ---------- quorum.rs : evaluate_quorum (auth filter INTERNAL) ----------
pub enum Outcome { PassAuto, PassUnanimous, PassSupermajority, PassMajority, Reject, Pending }
pub struct QuorumStatus {
    pub vote_id: String, pub decision_class: String,
    pub yes: u32, pub no: u32, pub abstain: u32, pub total_decisive: u32,
    pub outcome: Outcome,
}

// FIX-F4: caller passes the FULL votes_for(vote_id) set; the filter runs HERE, never outside.
pub fn evaluate_quorum(votes_for_id: &[Vote], vote_id: &str, class: &str) -> QuorumStatus {
    let spec = rule_for(class);
    let mut yes=0u32; let mut no=0u32; let mut abstain=0u32;
    let mut yes_voters: Vec<&str> = Vec::new();
    for v in votes_for_id {
        if !is_authorized(&v.voter_pid, &spec.pool) { continue; } // FIX-F4 internal filter
        match v.vote.as_str() {
            "YES"     => { yes+=1; yes_voters.push(&v.voter_pid); }
            "NO"      => { no+=1; }
            "ABSTAIN" => { abstain+=1; }          // FIX: abstains EXCLUDED from total [M]
            _ => {}
        }
    }
    let total = yes + no; // total_decisive [M]
    let outcome = match spec.rule {
        Rule::AutoPass => Outcome::PassAuto, // [M] immediate
        Rule::Unanimous5 => {
            // FIX-F5: SET-superset on YES voter PIDs, not yes>=5
            let covers = QUINTUPLE.iter().all(|q| yes_voters.contains(q));
            if covers && no == 0 { Outcome::PassUnanimous }
            else if no > 0      { Outcome::Reject }
            else                { Outcome::Pending }
        }
        // FIX-F1: integer cross-multiply (python uses TRUE division). total>=3 hard floor [M].
        Rule::Supermajority23 => {
            if total>=3 && 3*yes >= 2*total { Outcome::PassSupermajority }   // yes >= 2/3·total
            else if total>=3 && 3*no  >  total { Outcome::Reject }           // no  > 1/3·total
            else { Outcome::Pending }
        }
        Rule::SimpleMajority => {
            if total>=3 && 2*yes >  total { Outcome::PassMajority }          // yes > total/2
            else if total>=3 && 2*no >= total { Outcome::Reject }            // no  >= total/2
            else { Outcome::Pending }
        }
    };
    QuorumStatus{ vote_id:vote_id.into(), decision_class:class.into(), yes,no,abstain,total_decisive:total, outcome }
}
// FAILING-CASE PROOF (FIX-F1): total=5,yes=3,no=2,supermajority -> 3*3=9>=10? NO; 3*2=6>5? YES => REJECT
// (naive u32 `3 >= 10/3 == 3` would have falsely PASSED a yes-minority).

// ---------- json.rs : FIX-F2 recursive canonicalizer (python parity, EXCLUDES row_hash) ----------
pub enum JsonValue { Null, Bool(bool), Num(String), Str(String), Arr(Vec<JsonValue>), Obj(Vec<(String,JsonValue)>) }
pub fn canonicalize(v: &JsonValue, out: &mut String) {
    match v {
        JsonValue::Null    => out.push_str("null"),
        JsonValue::Bool(b) => out.push_str(if *b {"true"} else {"false"}),
        JsonValue::Num(n)  => out.push_str(n),
        JsonValue::Str(s)  => { out.push('"'); json_escape(s, out); out.push('"'); } // ensure_ascii=False UTF-8 passthrough
        JsonValue::Arr(a)  => { out.push('['); for (i,e) in a.iter().enumerate() { if i>0 {out.push_str(", ");} canonicalize(e,out);} out.push(']'); }
        JsonValue::Obj(o)  => {
            let mut keys: Vec<&(String,JsonValue)> = o.iter().collect();
            keys.sort_by(|a,b| a.0.cmp(&b.0)); // sort_keys=True at EVERY depth (FIX-F2 recursive)
            out.push('{');
            for (i,(k,val)) in keys.iter().enumerate() {
                if i>0 { out.push_str(", "); }                 // python separator ", "
                out.push('"'); json_escape(k,out); out.push_str("\": "); // python ": "
                canonicalize(val,out);
            }
            out.push('}');
        }
    }
}
// hash base: build the row WITHOUT a `row_hash` member, WITH `antecedents` + `ts` present, then canonicalize. [M L81-84]

// ---------- ledger.rs : sha-chain (FIX-A4 single Mutex<VoteLedger>; FIX-F5 tail read) ----------
pub fn sha16(s: &str) -> String { /* sha256(s).hexdigest()[..16] = first 8 bytes -> 16 lowercase hex */ } // [M]
pub fn last_row_hash(path: &Path) -> String { // FIX-F5: read min(2048,end) tail bytes,
    // .splitlines(), take LAST NON-EMPTY line, json.loads(..).get("row_hash", "0000000000000000")
}
pub fn now_iso() -> String { /* "%Y-%m-%dT%H:%M:%S.%fZ"[..23] + "Z"  ==  millisecond ISO  [M] (NEW rows only) */ }
// append_row: prev=last_row_hash; row.antecedents=prev (key literally "antecedents" — NOT prev/prev_sha16, FIX-F5);
//             row.ts=now_iso; base=canonicalize(row WITHOUT row_hash); row.row_hash=sha16(base); write FULL line via write_all.

// ---------- cast.rs : FIX-F3 + FIX-A4 (whole RMW atomic under ONE VoteLedger mutex) ----------
// submit -> vote_id = "VOTE-" + sha16(decision_pid + now_iso())              [M L219]
// cast   -> 400 bad vote | 404 unknown vote_id | 409 voter already cast       [M L231-239]
//           append VOTES; re-evaluate; if outcome in {PASS-*,REJECT} AND !outcome_exists(vote_id):
//           append OUTCOME row with nested tally {yes,no,abstain,total_decisive}.  [M L247-251]
// outcome_exists scan is INSIDE the same mutex (FIX-A4) so concurrent casts can't double-write.
```

**SHARED-FILE rule (FIX-A1):** the Rust vote-quorum lib **either** fully proxies writes to the live python daemon `:4952` and **never opens** `queue/votes/outcomes.ndjson`, **or** the python daemon is stopped and Rust becomes the sole writer — **never both processes writing one sha-chain.** During staging: **proxy** (Node owns the file; Rust is read/eval only). DRAFT / CI-PENDING.

---

## 4. Council/loop responder route map (thread-per-conn, json=0)  **[M shapes / D core]**

Server core = `recall-serve` pattern **[M]**: `const MAX_CONN=256; const MAX_REQS_PER_CONN=100_000;` Arc read-only state, `thread::spawn` per conn, `AtomicUsize` gate with **503 fast-close**, keep-alive loop `set_read_timeout(30s)`. `fn main()` returns `()` (**FIX-Flaw3**). All net I/O via `write_all` + read-to-completion (**FIX-Flaw5** `unused_io_amount` is deny-by-default).

| path | source | lane | redaction (FIX-C1) |
|---|---|---|---|
| `/health` | new **[D]** | json=0 | n/a |
| `/api/council/query` (POST) | mjs:3171 **[M]** | json=0 | advisory only; HBP-then-JSON to `:4947` |
| `/api/council/verdicts` | mjs:3198 **[M]** | json=0 | **classify+redact each verdict** before echo; assert `content_dumped=false` |
| `/api/loop/tick` | E06 **[M→D]** | json=0 | **resolve-only**: `auto_fire:[]`, `process_launch:0` always |
| `/api/loop/pending` | mjs:3089 **[M]** | json=0 | **redact each envelope** (no raw SECRET/HIDDEN dump) |
| `/api/loop/veto` (POST) | mjs:3110 **[M]** | json=0 | SIGNED → cosign-or-abort (FIX-B2) |
| `/api/canon-index` | mjs:3366 **[M]** | json=0 | **filenames+counts only**, each orphan through `classify_path` (FIX-C4) |
| `/api/council/authority*` | mjs:3210 **[M]** | **application/json** (FIX-F6, exempt from json=0 test law) | proxied to `:4952` during staging, or in-process emitting python-exact shapes |

- **FIX-C1**: NO handler returned raw bus/inbox/jsonl bodies in v2 — `redact.rs` runs every outbound council/loop body through the tier gate; a SECRET/HIDDEN payload injected into the inbox is **not echoed** (asserted by test). SECRET=`deny_public_content`, HIDDEN=`fully_redacted_metadata_only`; emit `proof_sha16` only.
- **FIX-F6**: the authority lane cannot be both json=0 AND drop-in `:4952`-compatible; it is **exempted** from the "body never contains `{`/`}`" test law and either proxies Node or emits the exact python key-sets (`{ok,pending,count}`, `{ok,rules,quintuple,authorized_classes,law_window_end,op_window_end}`, `{ok,decision,status,cast_votes}`).
- **FIX-D**: handlers that talk to the engine use `engine_tx.try_send(..)`; on `Full` they return an immediate `COUNCILBUSY|reason=engine_busy|json=0` line — a responder thread **never blocks on `send()`**.

---

## 5. Engine-drive own-thread (C0.1) — GATE preserved  **[M gates / D thread model]**

```rust
const AUTO_FIRE_MAX_RISK: f32 = 0.35;  // [M] E01:41  (PLAN flag only, never an actual fire)
struct SpawnerPidEmit { operator_pid: String, vote_id: Option<String>, fire: bool } // [D]

fn engine_drive_thread(st: Arc<CouncilState>, rx: Receiver<SpawnerPidEmit>) {
    // FIX-B: BLOCKS on rx ONLY. It never polls pending-dispatches / veto_expires_at.
    //        NO thread anywhere converts veto-expiry into an emit (no autoFireExpired analog).
    for emit in rx.iter() {
        // FIX-A (gate lives in the CONSUMER, not the channel): authorize HERE so it
        //        does not matter which Arc-holder sent. Until launch-wave-#19 wires this,
        //        EXTRACT hard-refuses fire=true.
        let authorized = emit.fire
            && is_authorized(&emit.operator_pid, &Pool::Authorized)        // [M]
            && emit.vote_id.as_deref()
                  .map(|vid| ledger_outcome_is_pass(&st, vid)).unwrap_or(false); // PASS in on-disk ledger
        if emit.fire && !authorized {
            log_rejected_emit(&st, &emit);   // refuse + audit row
            continue;
        }
        // crank pipeline (E=0 by default): GULP(load seats RO) -> QUANT(tuple60d/sha16) ->
        //   FLYWHEEL(spawn_gate ring: PROCEED iff fwd>=720 & rev<=280) ->
        //   EXTRACT(opencode ONLY if `authorized`) -> REGISTER -> PLACE(rename-before-load) -> GC.
        // FIX-B2: before any materialization, append a cosign WITNESS row (sign-or-abort, FIX-B1).
    }
}
```

**Invariant, rewritten precisely (FIX-E):** `process_launch` / `os_process_spawn` / `auto_fire_allowed` are **0 / 0 / false on every HTTP-served path and on every emit lacking a verified `operator_pid` + a quorum-PASS `vote_id`.** They are relaxed **only** inside EXTRACT, **only** after the consumer-side authorization passes. An authorized fire increments a **separate, audited spawn counter** with its own cosign row — not a blanket `=0` that EXTRACT would silently violate.

- `loop_tick` is **resolve-only** (diverges from Node E06's `autoFireExpired()`): `{inferred, staged, pending_total, auto_fire:[], process_launch:0}`. **[M→D]**
- `reviewed_prediction` risk gate (`risk=min(1,max(0.02,(write?0.65:0.12)+(broadcast?0.05:0)-(obs?0.08:0)))`, regexes) **[M]** — `auto_fire_allowed=risk<=0.35` is an **inert display flag, never read at any `engine_tx.send` site** (FIX-B; enforced by a grep test over the crate).
- **FIX-C / FIX-Flaw-C(2)**: the engine thread does **not** share a `Mutex<CosignChain>` with responders. It sends sign requests to the **dedicated `cosign_writer.rs` thread** (single owner, `resume_from` disk). Lock scope = in-memory head update only, never across the ndjson write; the crank body is wrapped in `catch_unwind` and `PoisonError` is handled explicitly — a panicking crank cannot poison the signing lane server-wide.
- **FIX-D**: even the legitimate operator emit path uses `try_send`, so no path can wedge a connection.

---

## 6. Exact owning 1.81 CI gate  **[M gate from `.github/workflows/ci.yml`]**

Run from the federation-1024 workspace root with the **pinned 1.81** toolchain (default local is 1.95 — **never** claim green from it, the PR#9 banned move):

```bash
cargo +1.81 fmt --all -- --check                                  # FIX-Flaw8: run +1.81 fmt --all first, 1.95 reflows differ
cargo +1.81 check --workspace --all-features                      # FIX-Flaw1: only sees [workspace].members — both new crates MUST be listed
cargo +1.81 check --manifest-path kernel/Cargo.toml --workspace   # FIX-Flaw7: distinct kernel sub-workspace — keep cosign body COPIED, not moved
cargo +1.81 clippy --workspace --all-features -- -D warnings
# no-bloat: awk '$1 > 2000' over every *.rs  (2000 passes, 2001 fails) — every new file budgeted < 420
```

MSRV / lint pitfalls pre-empted:
- **FIX-Flaw1 (false-green killer):** add `servers/council` + `servers/vote-quorum` to root `members`; a non-member dep builds with `cap-lints=allow` and `fmt --all` skips it → the gate would pass having checked zero new lines.
- **FIX-Flaw2 (toolchain skew, demonstrated):** an `#![allow(clippy::manual_div_ceil)]` is an **unknown lint on 1.81** → `unknown_lints` → `-D warnings` **hard error** (`agent-runtime` is 1.81-clippy-red for exactly this). Only use `#![allow(...)]` for lints that **exist in 1.81** (e.g. `doc_lazy_continuation`, **FIX-Flaw4**).
- **FIX-Flaw3:** `fn main()` returns `()`, not `-> !`.
- **FIX-Flaw5:** hand-rolled net I/O uses `write_all` + read-to-completion loops — bare `.read()/.write()` trips `clippy::unused_io_amount` (correctness, deny-by-default).
- **FIX-Flaw6:** new crates `rust-version = "1.75"` (match the six existing server crates; nothing here needs a feature past 1.75).
- **FIX-Flaw7:** lifted cosign body stays **core+alloc-only** in the no_std crate; **COPY** (leave kernel building); all `std` fs persistence in the council crate.
- **no-bloat is CLEAN** [M]: host8-serve `main.rs` (1958) untouched; landing as new crates (not inline edits) is the right call.

---

## 7. Bilateral hand-off — what liris attack-verifies (all [U] until gate/receipt proves)

1. **canonical_json byte-parity (FIX-F2)** — does the recursive canonicalizer (separators `", "`/`": "`, sort at every depth, `row_hash` omitted, `antecedents` key) reproduce every on-disk `row_hash` over queue/votes/outcomes? The `tests/parity.rs` receipt is the proof. **[U]**
2. **threshold cross-multiply (FIX-F1)** — confirm the `3,3,2`-style boundary cases at `total` 3..7 match python's float division (no integer-division false-pass). **[U]**
3. **single-writer-per-ledger (FIX-A1)** — confirm Rust never opens the vote-quorum ndjson while python `:4952` is up (proxy), and that only one process persists `COSIGN_CHAIN.ndjson`. **[U]**
4. **consumer-side fire gate (FIX-A/E)** — confirm no `engine_tx.send` call site can fire without `is_authorized(operator_pid)` + a quorum-PASS `vote_id`; confirm the grep test covers every send site; confirm EXTRACT hard-refuses fire until launch-wave-#19 wires it. **[U]**
5. **no expiry→emit (FIX-B)** — confirm nothing converts `veto_expires_at` into an emit and `auto_fire_allowed` is read nowhere at a send site. **[U]**
6. **cosign sign-or-abort (FIX-B1/B2)** — confirm SIGNED actions (tier transit, veto resolution, fire=1) **abort** when cosign append ≠ Ok, and are **hard-disabled** until the v0.2 body is lifted; `loop_veto` and fire append a witness row before mutating. **[U]**
7. **cosign-writer isolation (FIX-C/Flaw-C2)** — confirm the dedicated writer thread + `catch_unwind`/`PoisonError` handling means a panicking crank can't kill the signing lane, and no lock is held across the ndjson write. **[U]**
8. **resume-from-disk + single append surface (FIX-A2/A3)** — confirm the council constructs via `resume_from` (not `new()`), and the module-level `append(&[u8])`+`APPEND_SEQ_COUNTER` lane is retired so there are not two counters. **[U]**
9. **redaction wiring (FIX-C1/C2/C4)** — confirm a SECRET/HIDDEN payload in the inbox is not echoed through verdicts/pending; confirm `redaction_policy` is the canonical crate field, not a drifting council-local map; confirm canon-index returns filenames+counts only. **[U]**
10. **auth_covers fail-closed (FIX-C3)** — confirm transit to Secret/Hidden is **DENIED today** (window expired) and a missing/garbled/clock-error window **denies**, never allows. **[U]**
11. **owning-CI prerequisites (FIX-Flaw1/2/6/7)** — confirm workspace membership, 1.75 MSRV, no 1.81-unknown lints, kernel sub-workspace still green, on the **exact 1.81 job** (not a default-toolchain run). **[U]**
12. **tick divergence (resolve-only)** — flagged as intentional per gate-(4), NOT a regression. **[D]**

---

## 8. HONEST STATUS

**STAGED · NO CUTOVER · NOT BUILT.** This is a DRAFT build packet, not a compiled artifact — the **1.81 owning CI gate + liris attack-verify are the only verifiers**; nothing here is claimed green, mergeable, or live. Node `:4949` (super-dashboard) / `:4952` (vote-quorum daemon, still sole ledger writer) / `:4953` (cosign) are **untouched and running**; `host8-serve:5088` is **untouched** (`main.rs` 1958 lines, not edited). The new council responder `:5090` is **additive**. The **engine is NOT fired**: `process_launch=0`, `auto_fire_allowed=false`, `os_process_spawn=0`, EXTRACT hard-refuses `fire=true` until the consumer-side gate (launch-wave-#19, operator-T0) is wired. SIGNED verdicts are **hard-disabled** until the cosign v0.2 append body is lifted into the crate. Tags: route shapes, quorum law, sha-chain logic, thread-per-conn pattern, gate invariants, no-bloat headroom = **MEASURED**; crate split, `:5090` bind, resolve-only tick, all verifier fixes = **DESIGN**; build/parity/CI-green/redaction-enforcement/single-writer-topology = **UNVERIFIED** pending the 1.81 gate + liris. No PII, no secrets, no host serials in this packet.