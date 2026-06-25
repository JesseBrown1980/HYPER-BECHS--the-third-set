# LIRIS attack-verify - Cosign Rust stand-up packet

Date: 2026-06-25  
Seat: liris  
Target packet: `COSIGN-RUST-STANDUP-PACKET-2026-06-25.md` from `origin/acer` at `7c26b7daa66b5ab658664baabfa989dde6cca572`  
Packet blob: `40e540f080c69c3901f83e9686a10f45101182a3`  
Federation base checked: `JesseBrown1980/asolaria-federation-1024` `origin/main` at `80f47808f83d44abee551f13f6f253312a6219bd`

## Verdict

`ACCEPT_WITH_BOUNDARIES`.

Liris accepts the cosign packet as the correct staged design direction: additive `cosign-serve` shadow, live Python `:4953` untouched, separate shadow ledger, `py_parity` as the daemon-recipe compatibility layer, and 100% row parity as the cutover gate. This receipt does not claim the service exists, compiles, or has parity yet.

## MEASURED_LIRIS

- Liris fabric health `:4944/health` returned HTTP 200.
- Liris canon index is live: 427 entries / 134 sections.
- Liris direct bus probe `:4947/behcs/health` returned HTTP 200. The fabric bus-health helper still reports fallback because it probes other dashboard bases/routes.
- Liris cannot read Acer's live `C:/asolaria-acer/COSIGN_CHAIN.ndjson`; the fabric cosign-live helper reports `cosign_chain_unreadable` from this seat. Acer's `7/300` row-hash sample is therefore accepted as `MEASURED_ACER`, not independently re-run by Liris.
- Liris-local readable cosign ledgers checked this turn contain legacy rows only: 37/37, 91/91, and 37/37 rows had no `row_hash`, so they cannot prove or disprove the daemon `row_hash` parity recipe.

## Byte checks

- `servers/cosign-ledger/src/lib.rs` is `#![no_std]` and `#![forbid(unsafe_code)]`, uses `alloc`, and currently has `CosignChain::append` returning `Unimplemented`.
- The same crate still has the module-level `APPEND_SEQ_COUNTER` append lane.
- `kernel/core/src/cosign_chain/mod.rs` contains the native pipe-delimited recipe: `row={}|ts={}|prev={}|kind={}|payload={}`. That is materially different from the daemon-style sorted-key JSON recipe described by Acer.
- `origin/main` has no `servers/cosign-serve` crate and no `py_parity` module yet, matching the packet's `STAGED / NOT BUILT / NOT COMPILED` status.
- Liris-local archaeology contains sorted-key JSON cosign material (`canonicalEntryMaterial`-style scripts), so the packet's separation of JSON-daemon parity from the native pipe lane is consistent with visible Liris history.

## Accepted Design Constraints

- Keep the existing no_std native `cosign-ledger` pipe lane untouched.
- Add only pure `alloc`/`sha2` daemon parity logic inside the no_std crate; keep all `std::fs`, socket, mutex, and HTTP work in a new `cosign-serve` bin crate.
- Never write the live Python ledger during staging. Use a separate shadow ledger and read-only replay harnesses.
- Treat CI green and parity green as separate gates: CI can prove build/lint/no-bloat; it does not prove historical row parity unless the parity harness/receipt is run.
- Keep append disabled by default; no HVD/spawn-gate/verdict rows should be reproduced by the shadow appender.

## Boundaries

- `cosign-serve` is `UNVERIFIED`: no code is present on `origin/main` yet.
- `py_parity` is `UNVERIFIED`: no module is present on `origin/main` yet.
- 100% row parity is `UNVERIFIED`: the required Harness A/B receipts do not exist yet.
- Live Acer daemon behavior remains `ACER_OWNED` until Acer publishes reproducible fixtures/receipts or exposes a safe bilateral read surface.
- No cutover, no live ledger write, no signing change, and no engine fire are claimed.

## Liris next checks when code lands

1. Verify `servers/cosign-serve` is an explicit workspace member.
2. Verify `servers/cosign-ledger` remains no_std and does not gain hidden std feature-unification.
3. Run the owning 1.81 CI gate and no-bloat check.
4. Attack Harness A over a published redacted/fixture ledger or Acer-signed parity receipt.
5. Attack Harness B against a path-patched daemon copy; reject any harness that can touch the live ledger.
6. Verify shadow appends are byte-identical to daemon appends for the payload matrix before any T0 discussion.

