# P4 — Falcon USB presence receipt (ACER-MEASURED, read-only)

Date: 2026-06-28 · **acer** owning seat · **docs-first / E=0.** Read-only `acer-via-USB` measurement.
Pairs with the liris verification receipt (`a14929d`) — supplies the one fact only acer can see
(acer's USB bus), so the Falcon attach can move `OPERATOR_OBSERVED` → cross-vantage `SYSTEM_AFFIRMED`.

## What was measured (read-only ADB; no control, no start, no spawn)
| probe | result | tag |
|---|---|---|
| device attached | **1, state=`device`** (USB-connected to acer) | MEASURED (acer-via-USB) |
| model | Galaxy **S24 FE** (`SM-S721U1`) — matches `SUBSTRATE-FALCON-S24FE` | MEASURED |
| `com.termux` packages present | **3** (termux + :api + :hub) — the legacy human-terminal path **is installed** | MEASURED |
| node processes | **0** | MEASURED |
| `:8789` (hex `2255`) listening | **0** (not serving) | MEASURED |

## What it confirms
- **omnicoder = STUBBED on falcon** (node=0, `:8789` down) — the dashboard-map row was inference; it is
  now **acer-measured**. The device-native AI host is **not running** (build target, honestly held).
- **Termux is present** — i.e. the legacy human-terminal path it is meant to **replace** is what's on the
  device today. The omnicoder reframe (`d964720`) is the forward target, not the current device state.

## Boundaries held (carve-out + hard holds)
- **Read-only only:** no ADB control, no service start, no spawn, no execution, no OS/firmware action.
- **Serial · verified-boot fingerprint · person↔device binding · auth-file path = held LOCAL** (carve-out;
  not in this receipt). Published: device **model** + **presence state** only (public-coordination form).
- Starting the stubbed surface = device control = `E≠0` = **owning-seat (falcon) / operator T0** — not done here.

## Cross-refs
- omnicoder front door (AI-native reframe): `omnicoder---better-than-termux` main `5095fb1` (README `d964720`).
- liris verification receipt: HYPER-BECHS `a14929d` (sha `ceac06ef…`).
- Council question fired (device-native host realization, held/pending): `council-q-1782673473669-3oz3uz`.
