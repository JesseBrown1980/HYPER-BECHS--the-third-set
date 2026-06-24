# BOOT-AUTOSTART & SUPERVISED-RESTART SPEC — councils-and-above ready the moment the operator sits

**Requirement (operator, 2026-06-24):** during/after the daemon→Host-8 migration, **every** OP / daemon / Host-8 process must **start automatically at system boot** — from the **kernel / micro-kernel 8-byte stubbed-room host** — and **restart itself when it dies**, so that **the councils and everything above them are already running and ready** at any moment the operator sits down. Zero cold-start at the operator's chair.

## The rule

| # | Requirement |
|---|---|
| 1 | **Boot-resident:** the 8-byte stubbed-room host (kernel + micro-kernels) launches at Windows startup and brings up all registered Host-8 processes. |
| 2 | **Warm-on-arrival:** councils-and-above (OP-00 Special-OP-Jesses, OP-01 OP-Jesse, OP-Rayssa, OP 02–05, GAC, Chief, the 9-seat Council, prof-supervisors) are already live before the operator interacts — no per-seat cold start (portal-per-level: one warm seat services unlimited room spawns). |
| 3 | **Supervised restart:** each Host-8 process is watched; if it dies it is restarted (the Special-OP-Jesse watchdog-kicker pattern, itself a Host-8 process — `kill-0` liveness, never-restart-others-it-doesn't-own). |
| 4 | **Backend-shelless (Foundation Invariant 4):** rotation is function-call inside the long-running host — NOT a fresh process per agent. Only the real daemons are OS processes; the 726 logical seats rotate inside the host. |
| 5 | **json=0 at boot:** boot manifest + heartbeats are `.hbp` tuple-text, not JSON (hot-path law). |

## Mechanism (wire, don't re-invent)

- **Startup hook already exists:** `C:\HyperBEHCS\Install-HyperBEHCS-Startup.ps1` (+ `Start-/Status-/Stop-HyperBEHCS.ps1`, `HyperBEHCS.psm1`). The Host-8 boot supervisor registers here.
- **Boot manifest (to build):** an append-only `.hbp` registry of every Host-8 process to launch at boot — name · binary · port/room · restart-policy · owning-seat. Each migrated crate (recall-serve, omniscrcpy, omniquant-host8, omnimets-collector, ghost-envelope-gc, host8-serve framework, …) gets a row.
- **Restart supervisor (to build/port):** a Host-8 process (port the Special-OP-Jesse watchdog-kicker) that `kill-0`-sweeps the manifest at a cadence and restarts dead Host-8 processes. Honors halt invariants (`no_destructive_irreversible`, `atomic_state_writes`, `DISABLE_not_DELETE`, `never_restart_other_daemons_it_doesnt_own`).
- **Per-migration hook:** as each daemon is ported to Host-8 (see `ASOLARIA-DAEMON-HOST8-MIGRATION-MAP.md`), **add it to the boot manifest + the restart supervisor** — this is part of "done," not a follow-up.

## Status (honest)

- **EXISTS:** the HyperBEHCS startup PS1 lifecycle; the watchdog-kicker pattern (Node today, Host-8 port in staging); the SessionStart/PreCompact hooks (canon-load, snapshot-on-compact).
- **TO BUILD:** the unified Host-8 **boot manifest** (`.hbp`) + the **Host-8 restart supervisor** (promote the watchdog-kicker port) + registration of each migrated crate. None of this fires/cuts-over live daemons until proven + operator-gated.

## Acceptance

> Cold-boot the machine → wait → query the fabric: councils-and-above respond with no cold-start, every Host-8 process in the manifest is `kill-0`-live, and killing any one of them sees it restarted within one supervisor cadence. All boot/heartbeat artifacts are `.hbp` json=0.

*acer-colony spec. Boot-wiring is operator-gated (no auto-fire / T0 until proven + cosigned).*
