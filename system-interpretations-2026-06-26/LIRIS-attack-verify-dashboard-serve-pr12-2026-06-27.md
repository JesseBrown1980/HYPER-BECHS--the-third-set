# Liris attack-verify - dashboard-serve PR #12

Seat: liris / Rayssa Codex seat
Date: 2026-06-27
Target: `JesseBrown1980/asolaria-federation-1024` PR #12

PR: https://github.com/JesseBrown1980/asolaria-federation-1024/pull/12

## Verdict

`ACCEPT_WITH_FIX`.

PR #12 is a real Host-8 increment for the Acer `:4949` dashboard, not a re-proof of the old Node system. The scope and CI are clean, but one staged/no-cutover safety defect must be fixed before merge or any cutover.

## Owning gate checks

`MEASURED_GITHUB`:

- PR head: `d0fc461f0db55b9f40b37c0aa664b21ba646cd5c`.
- Changed files: `Cargo.toml` plus new `servers/dashboard-serve` crate only.
- GitHub CI: 5/5 passing, including `cargo check (workspace)` on the owning CI gate.
- PR comment posted: https://github.com/JesseBrown1980/asolaria-federation-1024/pull/12#issuecomment-4819705147

## Source-shape verification

`MEASURED_BYTES` from the PR checkout:

- New crate is stdlib-only.
- Hot path defaults to HBP / `json=0`; JSON is only explicit cold opt-in (`?format=json` / `cold=json`).
- Increment-1 serves `/health`, `/api/canon-index`, `/`, and `/super-os`.
- Runtime code has no process spawn and no filesystem write path; writes in the crate are HTTP socket writes, and temp-file writes are test-only.
- Tests reject POST/fire paths.

## Required fix

`ISSUE_FOUND`:

`servers/dashboard-serve/src/main.rs:17` sets:

```rust
const DEFAULT_BIND: &str = "0.0.0.0:4949";
```

This conflicts with the stated staged/no-cutover boundary. A default all-interface bind on the live dashboard port can accidentally collide with or replace the live Node `:4949` dashboard when launched without `ASOLARIA_DASH_BIND`.

Expected fix: use a shadow-safe default such as `127.0.0.1:14949`, or fail closed unless `ASOLARIA_DASH_BIND` is explicitly set for a cutover. Existing staged Host-8 precedent (`council-serve`) defaults to loopback (`127.0.0.1:5090`).

## Boundary

Liris cannot independently reproduce Acer-local live `:4949` parity or Acer memory-dir counts from this seat. Acer's parity proof (`665/46/619`, live Node diff) remains `ACER_MEASURED`; Liris independently verified the GitHub PR bytes and owning CI only.

Formal GitHub review could not use `request changes` because both seats publish through the same GitHub account identity; the verdict was posted as a PR comment instead.
