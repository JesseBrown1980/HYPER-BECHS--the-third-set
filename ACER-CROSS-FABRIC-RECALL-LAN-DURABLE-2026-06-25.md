# Acer Cross-Fabric RECALL — LAN-Exposed + Durable (acer receipt)

**Date:** 2026-06-25 · **Colony:** acer (DESKTOP-J99VCNH) · **Branch:** acer
**Complements:** liris receipt `HYPER-BECHS--the-third-set` branch `liris` `44edf58` (liris-measured the path; this records the acer-owned operational change).
**Mode:** operator-authorized admin · additive · **no Node cutover**.

## Problem (MEASURED)
Liris→acer recall failed/intermittent because: acer **Node** `:4791` (`serve-recall.cjs`) **event-loop-stalls on search** over the 591,286-row corpus (health answers, search = 8.006 s timeout, intermittently blocks all routes), and the fast acer **Rust** `recall-serve.exe` was **loopback-only** (`127.0.0.1:4796`). Keys were already in place (Special-OP OP-JESSE/OP-RAYSSA L9; `key_configured=true`) — pure transport/engine-exposure, not keys.

## What acer did (this session)
1. Relaunched Rust `recall-serve.exe` (`…\asolaria-federation-1024\target\release`) bound **`0.0.0.0:4796`** via `C:\asolaria-acer\recall-atlas\acer-rust-recall-lan-4796.bat` (env `ASOLARIA_RECALL_BIND=0.0.0.0 PORT=4796 ASOLARIA_RECALL_DIR=…\recall-atlas\data`; key auto from `%USERPROFILE%\.asolaria\recall.key`). 591,286 rows · `HILBRA-IDX-BEHCS-TUPLE-TEXT-V1` · `json_hot_path=false`. Index build ~54 s one-time per (re)launch.
2. **Narrow firewall**: rule `Asolaria-Recall-4796-In-Liris` = inbound TCP 4796 from **`192.168.1.10/32` only** (liris), not the whole LAN.
3. **Durable**: relaunched DETACHED (`start /min`, survives session) + **autostart** Task Scheduler `Asolaria-Rust-Recall-4796` (`/sc onlogon`, user context so the key file resolves) = Ready.
4. **Node `:4791` left untouched** — old surface preserved; retire/swap stays operator-gated.

## MEASURED (acer-side)
- **Soak 15/15, 0 fail** (health + rotating search incl. heavy `falcon` 14k-candidate term), latency **1.4–22.8 ms**, no stall.
- `:4796` health `ok=true bind=0.0.0.0 rows=591286`; LAN `192.168.1.9:4796` health+search 200 (~2.3 ms); Node `:4791` still 200 post-change.

## Bilateral — cross-fabric recall LIVE both ways
- **acer → liris**: `http://192.168.1.10:4791` (liris Node, 10,644 rows) — health + search ~5 ms (acer-measured).
- **liris → acer**: `http://192.168.1.9:4796` (acer Rust, 591,286 rows) — health + search, liris-confirmed (3–45 ms), durable post-detach (liris `44edf58`).
- Network: acer LAN `192.168.1.9` (+`.16`), liris `192.168.1.10` (Ethernet; `.4` stale). Tailscale down + direct-wire down → LAN is the working transport. L0 public PII-free (no key); L5/L9 HMAC key-off-wire.

## Net / next
- **Recommended peer target**: liris→acer recall = `http://192.168.1.9:4796` (Rust); acer→liris = `http://192.168.1.10:4791`.
- **Operator-gated**: repoint the live peer map + any Node `:4791` retirement (additive-until-parity).
- **Revert path**: `taskkill /F /IM recall-serve.exe` + `schtasks /delete /tn Asolaria-Rust-Recall-4796` (+ optionally delete the firewall rule).

`MEASURED_ACER` for acer probes/ops this session · accepts liris's measurements as `MEASURED_LIRIS` · no cutover · GitHub = mediator.
