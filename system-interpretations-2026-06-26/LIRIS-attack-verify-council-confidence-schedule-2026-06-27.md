# Liris attack-verify - council confidence-scheduled verify

Seat: liris / Rayssa Codex seat
Date: 2026-06-27
Scope: attack-verify of Acer PR #13 (`acer/council-confidence-schedule`) in `JesseBrown1980/asolaria-federation-1024`.

## Verdict: ACCEPT

`MEASURED_GITHUB`:

- PR: https://github.com/JesseBrown1980/asolaria-federation-1024/pull/13
- PR state: `OPEN`, non-draft
- Merge state: `BLOCKED` (normal protected-branch/review gate; not a source/CI failure)
- Branch: `acer/council-confidence-schedule`
- Commit: `1a545d049426d2a56cc50479893774866bfeea90`
- Base merge point: `4011673f44be4ac907335a8ea7410ce94cd2bcd0`
- Diff scope: `servers/council-serve/src/{http.rs,main.rs,routes.rs,schedule.rs}`
- GitHub checks on PR #13: `5/5 success` (`cargo check (workspace)`, node lint/type-check, schema sanity, cosign-chain integrity, no-bloat)

## Source-shape verification

`MEASURED_SOURCE` from checked-out branch bytes:

- Adds pure scheduler module `schedule.rs` with `expected_acceptance()` and `confidence_schedule()`.
- Scheduler ranks by expected acceptance, respects verify budget and threshold, and always sets `fire=false`.
- Adds `GET /api/loop/schedule` only; `POST /api/loop/schedule` is tested as `404`.
- Route reads `ASOLARIA_LOOP_LEDGER` when explicitly configured; unset ledger reports `source=loop_ledger_unwired` rather than faking a clean schedule.
- Output is HBP/json=0 text rows (`COUNCILSCHEDULE`, `COUNCILSCHED`), not hot-path JSON.
- Static scan found no production write route, process launch, `fire=true`, `auto_fire=true`, or `cutover=true` in touched production code.

## Boundary

`BOUNDARY`: Liris local Rust execution is blocked by this seat's Windows toolchain state (`rustfmt`/`clippy` components missing and MSVC `link.exe` missing); the build gate is therefore the owning GitHub CI, which is green on PR #13. No runtime cutover was verified or performed. This PR computes verify intent only; wiring the live loop ledger and letting the schedule gate actual fire are separate operator-gated follow-ups.

## Interpretation

This is the correct first Host-8 application of the DSpark lesson: confidence-scheduled verify is now represented as a staged, read-only planning route in `council-serve`, not as an old-Node crank edit and not as an automatic firing path. PR #13 is accepted for merge subject to normal operator/protected-branch gates; cutover remains separate.
