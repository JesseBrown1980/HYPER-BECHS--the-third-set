# LIRIS HyperHermes PTC dispatch absorb — PR #23 (2026-06-28)

Seat: Liris/Rayssa · Repo: `JesseBrown1980/asolaria-federation-1024`

## Verdict

`MERGED_STAGED_NO_EXECUTION`

## Claim

HyperHermes absorb #1 landed in the Host-8 council kernel: Programmatic Tool Calling as a staged planner. It collapses a declared N-step tool chain into one planned inference turn while keeping only the final result in context.

## Evidence

- `MEASURED_GITHUB`: PR #23 `Add staged PTC dispatch planner`
  - URL: https://github.com/JesseBrown1980/asolaria-federation-1024/pull/23
  - Head before merge: `ec38606bd58f48846a7e0013cdc379014c436acb`
  - Merge commit: `7bd7373b4a0a451733a64b91aa749693a38c7644`
  - PR CI: 5/5 green.
  - Post-merge main CI: 5/5 green on `7bd7373b4a0a451733a64b91aa749693a38c7644`.

## What landed

- New `servers/council-serve/src/ptc_dispatch.rs`.
- New route: `GET /api/ptc/run`.
- Reads `ASOLARIA_PTC_LEDGER` when wired; otherwise reports staged/unwired.
- Validates an allow-listed declarative pipeline (`recall_search`, `fabric_health`, `canon_index`, `mcp_health`, `lane_health`, `branch_freshness`, `recovery_plan`, `summarize`, `select`, `render_hbp`).
- Reports raw tool turns, planned PTC turns, saved turns, total bytes, final bytes, and saved context bytes.

## Safety

- Plans only: no tool calls, sockets, shell, mutation, restart, merge, rebase, cutover, or engine fire.
- `execute=false` on route and row output.
- Unknown operations become legacy rows and block `executable=true`.
- Duplicate IDs, invalid IDs, and missing/future refs fail closed as `status=invalid`.
- Present-but-malformed `from` / `bytes` fields fail closed into legacy rows and block execution.

## Boundary

This is a staged Host-8 planning module. Live ledger producers and real execution remain a later, separately gated step.

