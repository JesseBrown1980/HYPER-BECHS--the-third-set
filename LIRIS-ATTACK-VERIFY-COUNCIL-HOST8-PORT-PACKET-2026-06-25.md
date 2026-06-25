# LIRIS attack-verify - Council/Loop Host-8 port packet

Date: 2026-06-25  
Seat: liris  
Target packet: `COUNCIL-HOST8-PORT-PACKET-2026-06-25.md` from `origin/acer` at `c21b9337a6f8f4dbd2df79996123434006e5d207`  
Packet blob: `62f8e0347d1276c3d27cf04790dc108c4d4fdb3d`  
Federation base checked: `JesseBrown1980/asolaria-federation-1024` `origin/main` at `80f47808f83d44abee551f13f6f253312a6219bd`

## Verdict

`ACCEPT_WITH_BOUNDARIES`.

The packet is a real staged design packet, not a cutover claim. It correctly states `STAGED`, `NO CUTOVER`, `NOT BUILT`, `auto_fire=false`, and verifier ownership by the 1.81 CI gate plus Liris attack-verify. Liris accepts the packet as the correct next design target for C0.1 council/loop migration.

## MEASURED_LIRIS

- Liris fabric health `:4944/health` returned HTTP 200 during this check.
- Liris canon index is live: 427 entries / 134 sections.
- Liris bus `/behcs/health` returned HTTP 200. The `/health` path on `:4947` returns a route 404, so `/health` is a wrong-route probe, not proof the bus is dead.
- Liris `:4950` and `:4952` were not listening on this seat during this check. Any live omnidispatcher or vote-quorum runtime claim remains Acer-owned or future parity evidence.
- GitHub owning gate confirms PR #8 recall merged at `eaa97fe482eff29b1cfb5480d0fe28b84391eb7f`, and PR #9 Fischer merged at `80f47808f83d44abee551f13f6f253312a6219bd`.
- PR #8 and PR #9 each have five green checks: workspace cargo check, node lint/type check, ndjson/json schema, cosign sha-link, and no-bloat.

## Byte checks

- Root workspace `Cargo.toml` on `origin/main` explicitly lists workspace members and now includes both `servers/fischer-eval` and `tools/recall-serve`.
- `servers/host8-serve/src/main.rs` is 1958 lines and handles `listener.incoming()` inline with mutable `gnn` and `registry`; the packet's serial-responder risk is grounded.
- `tools/recall-serve/src/main.rs` carries the target nonblocking pattern: `MAX_CONN=256`, keep-alive request loop, `set_read_timeout`, and `thread::spawn` per accepted connection.
- `servers/cosign-ledger/src/lib.rs` is still the no_std userspace v0.1/stub surface: `CosignChain::append` returns `Unimplemented`, durable ndjson writing is not implemented, and the module-level `APPEND_SEQ_COUNTER` lane still exists.
- `kernel/core/src/cosign_chain/mod.rs` contains the fuller canonical row bytes / sha16 / monotonic chain body the packet wants copied into the userspace cosign-ledger crate.
- `servers/tier-policy/src/lib.rs` currently has `EnumerationPolicy` only; a distinct `redaction_policy` field is a real design gap.
- `servers/council` and `servers/vote-quorum` are not present on `origin/main` yet, matching the packet's `DRAFT / CI-PENDING` status.

## Correction

One packet warning should be softened before implementation: the statement that `#![allow(clippy::manual_div_ceil)]` is a guaranteed 1.81 hard error is not supported by the current owning gate. `origin/main` contains that allow in `kernel/core/src/lib.rs` and `servers/agent-runtime/src/lib.rs`, while PR #9's 1.81 CI passed. Treat this as a caution against unverified lint drift, not a blocker by itself.

## Boundaries

- No council/loop Rust code was built or cut over by this receipt.
- No engine was fired.
- `:4949`, `:4952`, and `:4953` live Acer runtime claims remain Acer-owned unless separately re-measured from Acer or exposed through live fabric.
- Single-writer, redaction, vote-quorum row-hash parity, sign-or-abort, engine-thread isolation, and `:5090` responder behavior remain `UNVERIFIED` until code lands and the 1.81 CI plus parity harness proves them.

## Liris next checks when code lands

1. Verify the two new crates are explicit root workspace members.
2. Run the exact 1.81 CI workflow, including the separate kernel sub-workspace.
3. Verify Python vote-quorum row-hash parity on real ledgers before accepting any writer change.
4. Verify only one writer owns each ledger during staging.
5. Inject SECRET/HIDDEN payloads and prove outbound council/loop routes emit proof hashes/redacted metadata only.
6. Grep every engine send/fire path and prove consumer-side authorization plus quorum-PASS gates are enforced.

