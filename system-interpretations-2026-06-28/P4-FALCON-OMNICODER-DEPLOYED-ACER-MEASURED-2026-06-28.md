# P4 — Falcon omnicoder DEPLOYED + RUNNING (ACER-MEASURED)

Date: 2026-06-28 · **acer** owning USB lane · **fulfills liris handoff packet** `b6aaef8893647bff…`
(`BUILD_DEPLOY_VERIFY_OMNICODER_NATIVE_HOST`, `execute=false`). This is the live-device half liris could
not produce (no NDK linker). Tag: **MEASURED** (acer-via-USB), serial/fingerprint held LOCAL.

## Claim (MEASURED)
The omnicoder — the AI-native 8-byte host process that **replaces Termux** — is **cross-compiled, deployed
over USB, and RUNNING as falcon's own device runtime**, serving its loopback `:8789`, read back from acer.
It is **not** a node app inside Termux and **not** a human terminal; no front-end.

## Build (acer, WSL/Ubuntu lane)
- Source: the blueprint-port host (`omnicoder-host`, Rust std + sha2), carrying the host8-serve laws:
  8-byte PID = `sha16` (sha256-first-16, gaia-loader parity), HBP line protocol, `process_launch=0`,
  execution-gated; plus the operator frame **port.port.port** + **cube cube cubed** + the N-Nest trio.
- Target: `aarch64-unknown-linux-musl`, **static**, `rust-lld` self-contained (no NDK needed).
- Artifact: `ELF 64-bit LSB executable, ARM aarch64, statically linked, stripped`, 433816 bytes.
- **artifact sha256 = `ffe52c0e8ff19a323fa32daac44977acdb44bae0495dd9fba20b62ad462d0801`**

## Deploy + run (acer-via-USB, read-only-then-run; OP-JESSE T0 for falcon upgrade)
- `adb push` → `/data/local/tmp/omnicoder-host` (userspace, reversible — **no OS/firmware flash, no root**).
- started detached `( … & )` → reparented to init (PPID 1, survives the adb shell).
- device cpu abi: `arm64-v8a`.

## MEASURED evidence (acer reading falcon over `adb forward 18789→8789`)
```
OMNIPROC|device=falcon|host_pid8=bf5108845fac9771|host_handle8=afcc775370f78fb3|os_pid=26370|bind=127.0.0.1:8789
OMNIAUTH|helper_packet_authority=1|execution_authority=0|process_launch=0|spawn=gated|killable=1|observable=1|watcher_gated=1
OMNIAGENTS|hosted=24  (roles work/review-predict/ask-fabric, every watcher gate=PASS)
OMNIPORTNEST|port_port_port=8789.55915.54527|one_process=1|logical=1
OMNICUBE|cube=012633ac71bafde8|cube2=4329aa8f49b89077|cube3=ea891c4ab10d0108|aot_distill=1
device socket: 0100007F:2255 state 0A (LISTEN)   [:2255 = hex 8789]
```
**Execution-gate proof** — POST `/api/packet` with a `command` field:
```
OMNIPACKET|...|accepted=1|executed=0|execution_authority=0|held=1|note=command_or_code_present-HELD_execution_gated-helper_only|process_launch=0
```
The host accepts work and HELDs any command/code — it never fires. Governed autonomy, MEASURED.

## State transition
- `falcon-omnicoder`: **STUBBED → RUNNING** (acer-measured). Supersedes the earlier presence receipt
  (omnicoder stubbed, node=0). Termux still present on device; the omnicoder now runs **beside/over** it as
  the AI-native runtime (the replacement target is live; Termux removal is a later, separate step).

## Boundaries held
- **No OS/firmware flash, no root** — userspace binary in `/data/local/tmp`, reversible
  (`pkill -f omnicoder-host` + `rm`).
- **execution_authority=false** compiled in; command/code HELD; spawn/scale/fire remain operator-gated.
- **Serial · fingerprint · person↔device binding · auth path = held LOCAL** (not in this receipt).
- killable · observable · watcher-gated.

## Cross-refs
- omnicoder repo: AI-native README `d964720` (main); liris source branch `f861dcb`; acer deployed source +
  build recipe → acer branch (this work).
- liris handoff packet: `b6aaef8893647bffa597afd7f6aef60cdbf710af6b360eb888405cd690481b42` (execute=false).
- council question (device-native host realization, was held): `council-q-1782673473669-3oz3uz` — now
  ANSWERED by construction (the realization = cross-compiled static aarch64 host8 in /data/local/tmp).
