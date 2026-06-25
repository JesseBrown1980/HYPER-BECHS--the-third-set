<!-- STAGED build packet (workflow-generated draft). ADDITIVE shadow service (cosign-serve), NO CUTOVER, NOT BUILT, parity UNVERIFIED. Live py :4953 + its ledger file UNTOUCHED. Verifier = owning 1.81 CI + a 100%-row parity receipt + liris attack-verify, NOT this packet. auto_fire=false. -->

# STAGED BUILD PACKET — additive Rust cosign shadow service (`cosign-serve`)

**Status banner (read first):** STAGED · ADDITIVE · NO CUTOVER · NOT BUILT · NOT COMPILED · PARITY UNVERIFIED. This packet folds in every confirmed fix from four adversarial verifiers (parity-exactness, single-writer-safety, chain-integrity/resume, owning-CI-1.81/safety). Every claim is tagged **MEASURED** (read from the grounding bytes), **DESIGN** (proposed here, unbuilt), or **UNVERIFIED** (needs a live/gate check). Carve-out clean: no signature bytes, keys, signer names, IPs, or PII below.

---

## 1. What + why (one paragraph)

**DESIGN.** Stand up `cosign-serve`, an additive, loopback-only Rust HTTP service that mirrors the live Python cosign-chain daemon (`:4953`, MEASURED parity target) by *reading* the on-disk ledger and, only behind an operator flag, *appending to its own separate shadow ledger* — never the live file. Its reason to exist is to give the federation a no-Node, thread-per-conn cosign reader/optional-appender that can eventually replace `:4953` **without ever cutting over until byte-parity is proven**. Parity IS the cutover gate: until the replay harness recomputes every on-disk daemon `row_hash` and matches it byte-for-byte, and the differential harness shows byte-identical appends versus a path-patched daemon copy, this service is a shadow only. The two "cosign" Rust artifacts on disk use a **different hash recipe** than the daemon (MEASURED: crate/kernel use pipe-delimited `row=|ts=|prev=|kind=|payload=`; daemon uses sorted-keys JSON), so "reuse the crate, don't re-implement" is honored by adding the daemon-parity logic **once, as a new `py_parity` module inside the existing crate**, leaving the native pipe lane untouched — not by re-using the incompatible pipe recipe.

---

## 2. Crate / file layout — reuse `cosign-ledger`, no re-implementation, **capability-split** (folds V4-F1)

**MEASURED critical constraint that reshapes the whole layout:** the existing crate `asolaria-server-cosign-ledger` is `#![no_std]`, `#![forbid(unsafe_code)]`, `extern crate alloc`. Placing any `std::fs::File` / `std::path::Path` / `std::io` signature inside it is a **compile error → `cargo check --workspace` goes RED before fmt/clippy ever run.** The draft's "put `py_parity` (with `resume_from(path)`/`append_row(file)`) inside the crate" therefore fails the owning gate. **DESIGN fix — split by capability, not by file:** pure logic (operates on `&[u8]`/`&str`/`String`, uses `alloc` + `sha2` no-default-features only) stays in the no_std lib; ALL filesystem/socket/mutex code lives in the new std **bin**. Do **NOT** add a `std` feature to `cosign-ledger` — `--workspace` feature-unification would flip it to std for every consumer (`host8-serve`, `highway`), silently breaking the no_std guarantee and the "native lane untouched" promise.

```
C:/asolaria-acer/federation-remake-1024/
  Cargo.toml                                  # workspace: add member "servers/cosign-serve"
  servers/cosign-ledger/                      # EXISTING no_std crate — EXTEND (alloc-only, ZERO std I/O)
    src/lib.rs                                # native lane UNTOUCHED + one line: `pub mod py_parity;`
    src/py_parity/
      mod.rs                                  # consts, RawJson, PyRow, PyChainErr, ResumeState, AppendOut
      json_tok.rs                             # quote/escape-aware STRUCTURAL tokenizer over &[u8]  (no_std)
      canon.rs                                # RECURSIVE canonical_bytes + persisted_line + sha16     (no_std, String out)
      repr.rs                                 # CPython-repr float formatter + ensure_ascii=False escape table (no_std)
      chain.rs                                # PURE compute_append(head,payload) + seq-max folder    (NO I/O)
  servers/cosign-serve/                       # NEW std bin crate asolaria-server-cosign-serve
    Cargo.toml                                # path-dep ../cosign-ledger (mirrors host8-serve/highway)
    src/main.rs                               # bind, thread-per-conn accept, Arc<Shared>, Mutex<Writer>  (ALL std)
    src/resume.rs                             # resume_from(path): per-PHYSICAL-LINE json-skip MAX-scan (std I/O)
    src/store.rs                              # newline-guard + append-under-lock(re-scan→write→fsync→truncate-on-err)
    src/http.rs                               # request line + headers + Content-Length body framing
    src/routes.rs                             # append / head / range / tail / verify / health dispatch
    tests/parity_replay.rs                    # HARNESS A — #[ignore] + env-gated (THE gate); brace-balanced reader
    tests/parity_differential.rs             # HARNESS B — #[ignore]; path-patched daemon copy, temp files
    fixtures/                                 # frozen <2000-line slices of the ledger (read-only)
```

**no-bloat (MEASURED rule, <2000 lines/file):** the lib `py_parity` is split into 5 small files; the bin into 5. Committed `fixtures/` slices must each be **<2000 lines** (MEASURED hazard: the real ledger is 5,419 lines — never commit it whole). **DESIGN.**

**json=0 hot path (DESIGN):** no `serde_json` on append/head/range/tail/verify — the in-crate `json_tok` parses; responses are byte-concatenated. `serde_json` (with `arbitrary_precision`) appears ONLY as a `[dev-dependencies]` cross-check in the harnesses.

**What is reused, untouched (MEASURED):** `CosignChain`, `CosignRow`, `Signature([u8;64])`, `GENESIS_PREV_SHA16`, the v0.1 `Unimplemented` append stub, and the kernel v0.2 pipe-delimited `canonical_bytes_of_row`/`sha16_of` remain the **native federation lane**, byte-for-byte as-is, so their 1.75/1.81 status is unaffected. `py_parity` is a strictly additive sibling module for the heterogeneous JSON-row on-disk shape (which the pipe recipe can never reproduce — MEASURED: whole-row sorted-keys recompute matched only 7/300 sampled rows).

---

## 3. The service draft — real Rust signatures (DRAFT / CI-PENDING)

### 3a. Lib side — pure, no_std (`servers/cosign-ledger/src/py_parity/`)

```rust
// mod.rs — recipes MEASURED-from-source; signatures DESIGN
pub const GENESIS_PREV: &str = "0000000000000000";                 // 16 ASCII zeros (MEASURED)
pub const APPENDED_BY_DAEMON: &str =
    "ASOLARIA-COSIGN-CHAIN-SINGLE-WRITER-DAEMON-PID-2026-05-23";    // injected if absent (MEASURED)
pub const LAW_ANCHOR: &str =
    "ASOLARIA-FOUNDATION-V3-LAW-V39-LOAD-DIVISION-PID-2026-05-23";  // /health only (MEASURED)

/// A JSON value kept STRUCTURALLY (not flattened) so the canonicalizer can recurse.
/// Scalars keep their EXACT on-disk token verbatim (no f64 round-trip on replay).
pub enum RawJson {
    Object(alloc::vec::Vec<(alloc::string::String, RawJson)>), // insertion order; duplicate keys collapsed last-wins on parse
    Array(alloc::vec::Vec<RawJson>),                            // element order PRESERVED
    Scalar(alloc::string::String),                             // raw token: number / "string" / true / false / null
}

pub struct PyRow { /* top-level Object members + a key index */ }
impl PyRow {
    pub fn parse_line(bytes: &[u8]) -> Result<Self, PyChainErr>;  // via json_tok (quote/escape-aware)
    pub fn get(&self, key: &str) -> Option<&RawJson>;
    pub fn contains(&self, key: &str) -> bool;
    pub fn seq_if_integer(&self) -> Option<u64>;                  // Some ONLY for an integer token (MEASURED: isinstance int)
}

#[non_exhaustive]
pub enum PyChainErr { Parse, NonInteger, ChainBroken, Io }

// ---- canon.rs : the parity core ----
/// sha256(utf8) -> lowercase hex -> first 16 chars. == daemon sha16. (MEASURED)
pub fn sha16(s: &str) -> alloc::string::String;

/// HASH BASE. Drop top-level "row_hash"; then emit the object RECURSIVELY with keys
/// re-sorted by code point AT EVERY DEPTH; arrays keep element order; nested objects
/// re-sorted too; each leaf scalar emitted as its RAW token. Separators ", " between
/// members and ": " after keys, NO pad after '{'/'[' or before '}'/']'. NO trailing '\n'.
/// MUST equal Python json.dumps(row_without_row_hash, sort_keys=True, ensure_ascii=False). (MEASURED)
pub fn canonical_bytes(row: &PyRow) -> alloc::string::String;

/// PERSISTED LINE. INSERTION order, INCLUDE row_hash, same ", "/": " spacing, single trailing '\n'.
/// (MEASURED — distinct from canonical_bytes; the #1 parity trap.)
pub fn persisted_line(row: &PyRow) -> alloc::string::String;

// ---- chain.rs : PURE, no I/O ----
pub struct ResumeState { pub head_seq: u64, pub head_hash: alloc::string::String } // head_hash VERBATIM width
pub struct AppendOut   { pub seq: u64, pub row_hash: alloc::string::String, pub antecedent_prev: alloc::string::String }

/// Fold one parsed line into a running (max_seq, max_hash). Counts ONLY integer seq tokens;
/// strict `>` (FIRST-max-wins on duplicate seqs); a parsed row missing row_hash contributes
/// GENESIS_PREV; head_hash taken VERBATIM (may be 16- or 64-hex). (MEASURED daemon chain_head)
pub fn fold_seq_max(acc: &mut ResumeState, line: &PyRow);

/// PURE append computation (no clock, no I/O). The bin injects `now` for ts-default.
/// Steps in daemon order (MEASURED):
///   seq = head.head_seq + 1
///   antecedents: absent -> [head.head_hash];
///                present & is LIST & head.head_hash not in it -> PREPEND head.head_hash;
///                present & (already in list  OR  NOT a list, e.g. bare string) -> LEAVE UNTOUCHED  // 3-way
///   ts absent      -> now (caller passes "%Y-%m-%dT%H:%M:%S.000Z", UTC, literal .000)
///   appended_by_daemon absent -> APPENDED_BY_DAEMON
///   insertion order after payload: seq, antecedents, ts, appended_by_daemon, row_hash(LAST)
///   row_hash = sha16(canonical_bytes(row))
/// Returns the finished PyRow (for persisted_line) + AppendOut.
pub fn compute_append(head: &ResumeState, payload: PyRow, now: &str) -> (PyRow, AppendOut);

// ---- repr.rs : APPEND-path number/string normalization (MEASURED requirement) ----
/// CPython float.__repr__-EXACT. Shortest round-trip; exponent when exp10 < -4 or >= 16;
/// exponent as e[+-]NN (>=2 digits, signed); "1.0" not "1"; "-0.0"; preserve incoming
/// int-vs-float token distinction (1 -> 1, 1.0 -> 1.0). NEVER Rust `format!("{}",f64)`.
pub fn py_number(token: &str) -> alloc::string::String;
/// Python json.dumps(ensure_ascii=False) escape table (see §3c). For NEW values only.
pub fn py_escape_string(s: &str) -> alloc::string::String;
```

### 3b. Bin side — std (`servers/cosign-serve/src/`)

```rust
// main.rs — DESIGN
struct Writer { shadow: std::fs::File, head: ResumeState, shadow_path: std::path::PathBuf }
struct Shared {
    writer:      std::sync::Mutex<Writer>,        // single in-process append writer (shadow file only)
    live_path:   std::path::PathBuf,              // LIVE ledger — READ-ONLY, never opened for write
    append_live: bool,                            // ALWAYS false; live appends are categorically refused
}

fn main() -> std::io::Result<()> {
    // 1) resume.rs::resume_from(&shadow_path) -> ResumeState  (per-physical-line MAX-scan, mirrors daemon)
    // 2) store.rs::ensure_clean_tail(&shadow_path)?           (newline-guard, V3-F1)
    // 3) open shadow in append mode -> Writer behind Mutex
    // 4) TcpListener::bind("127.0.0.1:5091")?; for stream -> thread::spawn(move || handle(Arc::clone(&shared), stream))
    //    handle() ONLY ever receives Arc<Shared>; it NEVER constructs a Writer or opens an append fd.
}
```

**Routes (DESIGN; parity status MEASURED):**

| route | parity | behavior |
|---|---|---|
| `POST /api/cosign/append` | **py-parity** (writes the **shadow** file only) | body = row dict w/o seq/row_hash → `{ok,seq,row_hash,antecedent_prev}`. Disabled by default; operator flag. |
| `GET /api/cosign/head` | **py-parity** | re-scan per request (see §5) → `{ok,seq,row_hash,ts}` |
| `GET /api/cosign/range?from=N&to=M` | **py-parity** | inclusive, defaults from=1 to=999999, **full scan** → `{ok,from,to,count,rows}` |
| `GET /health` | **py-parity** | `{ok,service,port,head_seq,head_row_hash,anchor_pid,law_anchor,ts}` |
| `GET /api/cosign/tail?n=N` | **additive** | last-N via full scan (NOT O(1) offset — see §5) |
| `GET /api/cosign/verify?from=&to=` | **additive** | recompute row_hash + seq-monotonic + **antecedent-link** check → `{ok,checked,mismatches:[{seq,disk,recomputed}],broken_links:[...]}` (covers `/api/cosign-integrity` intent; also flags non-list/orphan antecedents per V3-F6) |

**Body framing (MEASURED, mirror daemon `_read_body`/`_send`):** read exactly Content-Length bytes; parse fail → 400 `{ok:false,error:"parse"}`; append exception → 500 `{ok:false,error:"append-failed"}`; unknown route → 404 `{ok:false,error:"unknown route",path}`; responses `Content-Type: application/json` with explicit Content-Length. Loopback bind only — never `0.0.0.0`.

### 3c. The two append-path normalization specs (MEASURED, were under-specified in the draft)

**Float — CPython `repr` (V1-F7):** raw-token passthrough is correct for **replay** (disk tokens were already Python-normalized) but **WRONG for append** — the daemon does `json.loads(body)`→Python number→`json.dumps`, so `0.1000`/`1.50`/`1e2` normalize to `0.1`/`1.5`/`100.0`. `repr.py_number` must implement: shortest round-trip; switch to exponent for decimal exp `< -4` or `>= 16`; exponent `e[+-]NN` (≥2 digits, signed); `1.0` not `1`; `-0.0`; and **preserve the incoming int-vs-float distinction** (`1`→`1`, `1.0`→`1.0`). Rust `format!("{}",f64)` diverges (`1e16`→`10000000000000000`, `1e-5`→`0.00001`, `e16` vs `e+16`).

**String — `ensure_ascii=False` table (V1-F8):** `"`→`\"`, `\`→`\\`, U+0008→`\b`, U+0009→`\t`, U+000A→`\n`, U+000C→`\f`, U+000D→`\r`, all other C0 (U+0000–U+001F)→`\u00xx` **lowercase** hex; everything else **raw** (incl. U+007F, all non-ASCII; `/` NOT escaped; U+2028/U+2029 NOT escaped).

**Top-level + nested key sort (MEASURED clean, with the recursion caveat from V1-F1):** Python sorts `str` by code point; Rust `str` Ord sorts by UTF-8 bytes; these **agree for valid UTF-8** provided you sort the **decoded** key, not the quoted/escaped form — and you must do it at **every depth** (the single change that turns V1-F1 from red to green). `sha16`, the `", "`/`": "` separators with no bracket padding, the row_hash-only exclusion set, the genesis constant, and the insertion-order persisted line are all MEASURED-clean.

**Windows trap (MEASURED, own memory):** write bytes via `write_all` only — never a text-mode wrapper; enforce **LF not CRLF**, **no BOM**, and keep the `\n` out of the hashed bytes (`canonical_bytes` has no trailing newline; only `persisted_line` does).

---

## 4. The EXACT parity harness — **THE gate** (DESIGN; corpus MEASURED)

### Harness A — read-only replay over the LIVE ledger (`tests/parity_replay.rs`)

`#[ignore]` + env-gated on `ASOLARIA_COSIGN_NDJSON=` (V4-F2: a plain `#[test]` opening an absolute path outside the repo panics on the CI runner; and CI runs no `--all-targets`, so it never executes the harness — green CI ≠ parity-verified). **Read-only**: the live `C:/asolaria-acer/COSIGN_CHAIN.ndjson` is never written by any harness.

Procedure:
1. Stream with the **brace-balanced, quote/escape-aware** tokenizer (V3-F4: a brace counter that ignores in-string `{`/`}` and backslash escapes will desync record boundaries). NOT `split('\n')` — MEASURED hazard: ~63 multi-line pretty records, 1,682 indented fragment lines, 113 `}` lines.
2. Classify each record:
   - **daemon-recipe rows** (16-hex `row_hash`, `antecedents`) → **ASSERT** `sha16(canonical_bytes(row_without_row_hash)) == on-disk row_hash` byte-exact, using the **recursive** canonicalizer (V1-F1: the flat top-level recipe matched 3,210/3,316 — it fails exactly the 106 rows carrying an unsorted nested object; recursion is what makes those green).
   - **legacy / ceremonial rows** (no `row_hash`; `prev_sha`; 64-hex sorted-keys-compact; amend rows) → **SKIP-not-fail**, but **count and bucket** in the receipt (never pass by skipping everything).
3. Re-emit **raw on-disk scalar tokens** on replay → float-repr and string-escape drift cannot cause false mismatches; any mismatch is a real sort/separator/exclusion bug.
4. Receipt: `{daemon_rows_checked, daemon_rows_matched, mismatches[], legacy_skipped_by_bucket}`. **Parity = matched == checked AND mismatches == [].** Until this prints all-green over the full live file, parity is **UNVERIFIED** (the prior 7/300 is the exact failure mode this converts to all-green or to a precise list).

### Harness B — live differential, path-patched daemon vs rust shadow (`tests/parity_differential.rs`, `#[ignore]`)

**SAFETY fix (V4-F3):** the daemon **hardcodes** `COSIGN = Path("C:/asolaria-acer/COSIGN_CHAIN.ndjson")` (MEASURED) — running the *unmodified real* daemon in the harness would append to the **live audit chain**. B must launch a **path-patched copy** of the daemon (or one only after an env/arg path override is confirmed to exist), and **assert both temp paths != the live path before any POST**. Until that copy exists this is an UNVERIFIED prerequisite, not a runnable step.

Procedure:
1. Copy a frozen fixture to `F_py` and `F_rust` (identical bytes → identical MAX-scan head).
2. Launch the **path-patched py daemon** → `F_py` on a temp port; launch `cosign-serve` → `F_rust` (shadow) on `:5091`.
3. For each payload, **inject a fixed `ts`** (both keep a present ts — ts only defaults if absent) to remove `now_iso()` nondeterminism; do NOT inject `appended_by_daemon` (test both inject the identical ANCHOR).
4. POST the same payload to both. Assert returned `{seq,row_hash,antecedent_prev}` equal **and** the newly appended last lines of `F_py`/`F_rust` are **byte-identical**.
5. Payload matrix: (a) minimal `{event,i}`; (b) full daemon schema with **float** `confidence`/`cp` (the float-repr gate, V1-F7); (c) payload already carrying `antecedents` **as a list** (prepend + "skip if present"); (d) payload with `antecedents` **as a bare string** (the 3-way "leave untouched", V1-F6); (e) payload already carrying `ts` (no-override); (f) a **nested object** value (the recursive-sort gate, V1-F1); (g) non-ASCII field (`ensure_ascii=False`, V1-F8); (h) two sequential appends (head advances correctly on both).
6. **Frozen-clock unit test (V1-F9):** a no-`ts` payload with both clocks pinned, asserting Rust emits exactly `YYYY-MM-DDTHH:MM:SS.000Z` in UTC (the `.000Z` default path is otherwise never exercised because every B payload injects ts).

---

## 5. Shared-file hazard handling — separate shadow ledger + read-only replay (folds V2-F1/F6, V3-F1/F2/F3, cross-cutting portalocker)

**MEASURED ground truth:** the daemon re-derives the head with a full-file **MAX-scan inside its lock on EVERY append** (it never caches a head between appends); it takes **no portalocker** (relies on the in-process `threading.Lock` + the `:4953` bind as the de-facto single-writer guard); and the ledger has **many** concurrent writers (`append-cosign-*.mjs`, `emit-cosign-{204,207,213}.py`, `build-cosign-envelope.py`, `s3d-write-lineage-cosign-row.mjs`, the live daemon). seq is **not monotonic in file position** (MEASURED: out-of-order race-appends are the entire reason MAX-scan exists).

**DESIGN resolution — never write the live file:**

1. **Separate shadow ledger.** When append is enabled, `cosign-serve` writes to its **own** `COSIGN_CHAIN.shadow.ndjson`, seeded once by a read-only copy of the live file. The service categorically refuses to open the live file for write (`append_live` is hardwired `false`). This **eliminates** the two-writer race against `:4953` for the live ledger. The draft's "in-process Mutex = identical scope to the py Lock" claim was **FALSE** (V2-F1/V3-F2): py re-scans disk under lock; a cached head does not. Even on the sole-writer shadow file we **re-scan the head under the writer lock on every append** to mirror the daemon exactly (optionally short-circuited by a size/mtime stat-guard).
2. **Read-only parity replay on the live file.** Harness A and all `/head`/`/range`/`/verify` reads against the live file are **read-only**, **per-request re-scans** that mirror the daemon's per-physical-line `json.loads` + skip-on-exception (V3-F3). **Drop the recall-serve O(1) byte-offset claim** for this file — it is invalid here because the file is live-mutated and seq≠file-position; reads are full scans, exactly as the daemon does. A cached boot-time head would go stale the moment `:4953` appends (V3-F3), so it is not used for live reads.
3. **`resume_from` mirrors the daemon, NOT brace-balanced (V1-F2/V3-F5).** The runtime resume uses **per-physical-line** parse-and-skip so a multi-line pretty row never changes head selection; integer-only seq; strict `>` first-max-wins; `head_hash` stored **verbatim** (may be 64-hex). The brace-balanced reader is reserved for the Harness-A replay corpus only.
4. **Newline guard before first append (V3-F1).** `store.rs::ensure_clean_tail` stats the shadow file: if the last byte is not `\n` or the trailing record does not parse, fail-closed (or write a leading `\n` and quarantine the fragment) — never O_APPEND blind onto a torn line (which would glue records and fork the chain).
5. **Torn-write + durability + poison (V2-F3/F4, V3-F6).** Under the lock: capture file length → `write_all(persisted_line)` → `flush()` + `sync_data()` (fsync is parity-neutral: identical bytes) → only then advance the in-memory head. On any write error, **truncate back to the captured length** and return `Err` (never leave a partial line). Treat `Mutex` poison as **fatal / fail-closed**; never recover-and-reuse a stale cached head.
6. **Read torn-tail tolerance (V2-F6/V3-F3).** Reads drop an incomplete/unbalanced trailing record and decode lossily (the daemon opens with `errors="ignore"`), so a reader mid-`:4953`-write returns the prior consistent max, not a half-line.
7. **Residuals, stated not solved.** HTTP-retry double-append (V2-F5) is a real vector the mutex does NOT close — shared with `:4953` (no idempotency key); flag in the receipt. **Rust-only portalocker is a trap (V3 cross-cutting):** advisory locks only exclude other advisory-lock takers, and the daemon takes none — so enabling Rust append against any **shared** file would require a coordinated patch to the daemon too (a future **DAEMON_OP**). With the separate-shadow design this is moot; it becomes relevant only if a future cutover ever points Rust at the real file, at which point the full protocol is **LOCK_EX → re-scan-under-lock → assign seq → write → flush+fsync → release** on **both** sides. **UNVERIFIED / DAEMON_OP.**

---

## 6. The exact owning 1.81 CI gate (MEASURED steps; one discrepancy flagged)

```
rustup toolchain 1.81
cargo fmt --all -- --check
cargo check --workspace          # now covers servers/cosign-serve automatically
cargo clippy --workspace -- -D warnings   # NOTE: no --all-targets => harnesses are NOT built/linted by CI
no-bloat: every changed file < 2000 lines
```

- **V4-F1 is what this gate enforces:** the capability split (§2) is the only layout that lets `cargo check --workspace` reach green — std I/O in the no_std crate red-lines `check` before fmt/clippy run.
- **`clippy -D` risk (UNVERIFIED):** hand-rolled HTTP framing + many `String` allocations may trip `or_fun_call`, `needless_return`, `format!`-in-loop. Cannot be judged from a non-building design — fmt/clippy-clean is **UNVERIFIED** until it compiles.
- **CI never runs either harness** (no `--all-targets`): passing CI ≠ parity-verified. Harness A/B are local/manual gates only.
- **Toolchain discrepancy — UNVERIFIED, resolve before any green claim:** manifests pin `rust-version = "1.75"` (`[workspace.package]`, MEASURED) but CLAUDE.md cites the **1.81** CI owning gate. Per the claims-gate, re-read the EXACT GitHub required-checks job/toolchain (`gh pr checks` / `gh run view`) before calling this `green`/`mergeable`. A local single-crate `cargo test -p asolaria-server-cosign-serve` is **SCOPED evidence only**.

---

## 7. The cutover gate — all PENDING

Cutover stays **operator-gated** and is blocked until **every** item below is satisfied, in order:

1. **PENDING — Harness A all-green:** `daemon_rows_matched == daemon_rows_checked` and `mismatches == []` over the **full live** `COSIGN_CHAIN.ndjson`, with the recursive canonicalizer (must convert the prior 7/300 and the 106 nested-object rows to green).
2. **PENDING — Harness B byte-clean:** byte-identical appends across the full payload matrix (a–h) vs the **path-patched** daemon copy, plus the frozen-clock `.000Z` unit test.
3. **PENDING — owning 1.81 CI green:** fmt + `check --workspace` + `clippy --workspace -D warnings` + no-bloat on the EXACT GitHub toolchain (after resolving 1.75-vs-1.81), read from required checks — not a local run.
4. **PENDING — parity receipt** emitted (100% daemon-row match + bucketed legacy skips + residuals list).
5. **PENDING — liris attack-verify** of the receipt + diff on the EXACT owning gate (bilateral; GitHub is the mediator; HOLD if peer is mid-push).
6. **PENDING — operator T0 authorization** for any cutover. **Merge/cleanup authorization NEVER implies fire or T0.** If append is ever pointed at a shared file, the DAEMON_OP portalocker coordination (§5.7) is an additional prerequisite.

---

## 8. HONEST status

- **STAGED · ADDITIVE · NO CUTOVER · NOT BUILT · NOT COMPILED.** This is a design packet; no crate has been compiled, no parity demonstrated. (DESIGN)
- **Parity UNVERIFIED.** Three on-disk hash recipes diverge (MEASURED); the daemon recipe is reproducible only with the **recursive** canonicalizer + CPython float-repr + the exact escape table — none yet built/run. (UNVERIFIED)
- **`:4953` daemon + `.hbp` mirror untouched.** The live daemon, the `.mjs` mirror (frozen at 190 rows, refuses to re-run), the `:4949` dashboard routes, and the `HOST8GATE cosign_touched=0` invariant all stay exactly as-is. The shadow service runs on its own loopback port (`:5091` proposed, fallback `:5092`, **UNVERIFIED** — no live bind probe) and never writes the live ledger. (MEASURED constraints / DESIGN service)
- **Engine not fired.** No reference to `spawn_gate`, `sys_hookwall_post`, `compose_verdict_row`/HVD, `process_launch`, or `auto_fire`; `auto_fire=false` untouched; this cranks no `E`. (MEASURED-clean on the fire axis)
- **No unauthorized signing.** ed25519 signing is deferred (v0.3) on both sides; the parity append is a truncated-sha256 hash-chain link, not a crypto signature. Append is **OFF by default**, operator-flag-gated, and only ever targets the separate shadow ledger. (MEASURED / DESIGN)
- **Chain-semantic caveat (V4):** a free-standing appender can write seal-shaped audit rows decoupled from any `spawn_gate`/E=0 verdict, degrading the chain's "every row = a real gated fire" meaning. Keep append disabled; if ever enabled, restrict to non-verdict `kind`s and **never** reproduce HVD verdict rows. (DESIGN safety boundary)
- **Carve-out clean:** no signature bytes, keys, signer names, serials, IPs, or PII in this packet.

**Relevant absolute paths:** `C:/asolaria-acer/federation-remake-1024/servers/cosign-ledger/` (extend, no_std lib), `C:/asolaria-acer/federation-remake-1024/servers/cosign-serve/` (new std bin), `C:/asolaria-acer/federation-remake-1024/Cargo.toml` (workspace member add), `C:/asolaria-acer/COSIGN_CHAIN.ndjson` (read-only parity target/fixture source), `C:/HyperBEHCS/bin/asolaria-cosign-chain-daemon.py` (parity recipe source / path-patched py-shadow).