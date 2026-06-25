# Liris OMNI / Host-8 Migration Crosswalk

**Date:** 2026-06-25  
**Branch:** `liris`  
**Purpose:** keep the Liris side aligned with Acer's OMNI / Host-8 canon without collapsing Acer, Liris, fabric, RECAL, and GitHub into one evidence bucket.

## Evidence Tags

- `MEASURED_LIRIS`: observed from this Liris seat during this update.
- `MEASURED_ACER`: carried from the Acer branch as a published Acer-side receipt.
- `CANON`: architecture/census statement from published map or fabric/canon surface.
- `OPERATOR_OBSERVED`: operator-sourced scope that must not be deflated.
- `UNVERIFIED`: not remeasured on this Liris seat.

## Liris-Measured Current State

- `MEASURED_LIRIS`: Wi-Fi is repaired and connected to `Desktop_F7624603_5G`, 5 GHz, 100 percent signal, 433.3 Mbps link.
- `MEASURED_LIRIS`: Wi-Fi internet path is repaired. The radio/association was healthy, but Windows had duplicate manual default routes to `192.168.1.1` through both Ethernet and Wi-Fi at metric `0`. Active-store route priority was corrected to Wi-Fi metric `5`, Ethernet fallback metric `75`; normal unforced `8.8.8.8` ping then passed 2/2 at 6 ms and `google.com` DNS/IPv6 ping passed 2/2 at 5 ms.
- `MEASURED_LIRIS`: fabric mirror health answers as `super-asolaria-os-dashboard-liris-mirror` on port `4944`.
- `MEASURED_LIRIS`: fabric health is fresh on Liris `:4944`; bus/manifest/sister/substrate auxiliary reads may return fallback/cached rows and must be tagged as fallback unless the route itself reports fresh.
- `MEASURED_LIRIS`: `/api/everything` names the bilateral bus, Acer dashboard, Liris mirror, operator quintet, sovereignty USB route, hidden/section-Q routes, hookwall coverage, free agents, Pi supervisor, Shannon engines, supervisor/prof registry, device registry, and federation health.
- `MEASURED_LIRIS`: local Fischer remains live at `127.0.0.1:4794` with `FISCHER-LIVE|ok=1|json=0`.
- `MEASURED_LIRIS`: PR #9 Fischer Host-8 branch is mergeable and GitHub CI is green on head `9f05a33`; no live cutover was performed.
- `MEASURED_LIRIS` + `OPERATOR_OBSERVED`: `http://127.0.0.1:4791/` is the local **Asolaria Recall + Atlas** surface: "liris measured recall surface beside the live atlas server." The operator identifies this as **RECAL Atlas** / Hilbra-local recall-atlas communication. This is part of the built Hilbra / Atlas family, not evidence that Hilbra is missing or unbuilt. Public L0 searches for Slack/QDD/Brian/email did not expose email-like strings.
- `MEASURED_LIRIS`: RECAL L9 alias probe on `:4791` shows indexed surfaces for `brown hilbert` (50), `hilbert` (50), `atlas` (9), `registration` (16), `registration office` (8), `office` (21), `fischer` (14), `host8` (4), and `omni` (21). Exact aliases `hilbra`, `atlas recall`, `recall`, `construction`, `construction yard`, and `yard` returned 0 on this Liris index, so the migration map must add explicit alias rows that point those operator names to the RECAL Atlas / Hilbra-local surface instead of treating them as absent.
- `MEASURED_LIRIS`: the three Liris fronts are live/openable: RECAL `http://127.0.0.1:4791/`, unified dashboard `http://127.0.0.1:4944/`, and Hilbra / Atlas front end `http://127.0.0.1:4790/asolaria-multi-cylinder-v2.html`.
- `OPERATOR_OBSERVED` + `MEASURED_ACER`: Acer opened the owning Acer fronts in browser: Hilbra `http://127.0.0.1:4790/asolaria-unified-fabric-map.html` ("Asolaria · Unified Fabric Map"), NEW RECAL Rust `http://127.0.0.1:4796/?v=ka` ("Asolaria Recall + Atlas · ACER (Rust)"), and unified dashboard `http://127.0.0.1:4949/` ("SUPER ASOLARIA OS · v3 · LIVE"). Loopback is colony-local; Liris `127.0.0.1` and Acer `127.0.0.1` are different owning seats.
- `MEASURED_LIRIS`: Liris reached Acer node RECAL health over LAN at `http://192.168.1.9:4791/api/health` earlier in this pass; response reported `colony=acer`, `rows=591286`, `bind=0.0.0.0`, `key_configured=true`, OP-JESSE/OP-RAYSSA L9 grants, and peer `liris` base `http://192.168.1.10:4791`. Final verification later in the same pass regressed to timeout on both `192.168.1.9:4791` and `192.168.1.16:4791`, so the current cross-vantage status is **intermittent / not stable-green**.
- `MEASURED_LIRIS`: after OP-authorized Acer admin exposure, Acer Rust RECAL is LAN-reachable from Liris at `http://192.168.1.9:4796`. Health returns `200` (`schema=asolaria.recall.rust.v1`, `colony=acer`, `rows=591286`, `bind=0.0.0.0`, `key_configured=true`, OP-JESSE/OP-RAYSSA L9 grants). Public search `q=brown-hilbert` returns `200`, `count=49`, real Brown-Hilbert hits. Node `:4791` remains untouched.
- `MEASURED_LIRIS`: pre-detach soak of Acer Rust RECAL `192.168.1.9:4796` passed 6/6 spaced probes over ~75 s: health `200` each time (`47-64 ms`) and public search `q=brown-hilbert` `200` each time (`2-16 ms`). This proves peer-side stability before Acer detaches/autostarts the service.
- `MEASURED_LIRIS`: Liris RECAL health reports `bind=0.0.0.0`, `port=4791`, `rows=10644`, `key_configured=true`, OP-JESSE/OP-RAYSSA L9 grants. Current Acer-reachable Liris LAN base is `http://192.168.1.10:4791` (Ethernet). Liris Wi-Fi also had address `192.168.1.19` but the Wi-Fi interface was disconnected during this pass; do not use stale `192.168.1.4`.
- `UNVERIFIED`: reverse Acer->Liris live HTTP call is still to be measured from the Acer seat. Driver packet created for read-only reverse probe: `packet_sha256=71e8c378ae77f5af7bd0ebc066b160c560c29570dca150a9f6b85cca17fd03e2`.

## Acer Reference Maps Mirrored Onto Liris Branch

The following Acer-branch artifacts are mirrored on this Liris branch as reference maps. They remain tagged `MEASURED_ACER` or `CANON` unless remeasured locally:

- `ASOLARIA-HYPERBEHCS-SUBSTRATE-MAP.md`
- `ASOLARIA-DAEMON-HOST8-MIGRATION-MAP.md`
- `ASOLARIA-OMNI-SYSTEMS-MULTILEVEL-MULTIFABRIC-MAP-2026-06-24.md`
- `BOOT-AUTOSTART-SUPERVISED-RESTART-SPEC.md`

## OMNI Definition To Preserve

`OPERATOR_OBSERVED` + `CANON`: multi-level plus multi-fabric equals OMNI systems. An OMNI system is not one daemon and not one hierarchy rank. It must be mapped across both axes:

- level axis: OP, council, supervisor, agent, route, sector, substrate, cube, omni-system.
- fabric axis: Acer, Liris, immutable bus, device/falcon lane, sovereignty USB, hidden/shadow layers, GitHub, Google Drive / NotebookLM lane when gated.

## Liris Delta Against Acer OMNI Map

- `MEASURED_LIRIS`: Liris can currently verify its local mirror, local Fischer live node, repaired Wi-Fi transport, PR #9 green GitHub publication, and local Recall/Atlas presence.
- `MEASURED_ACER`: Acer branch carries the broader live `:4949` route enumeration, the daemon migration scoreboard, and Acer loopback Rust RECAL `:4796`.
- `MEASURED_LIRIS`: cross-vantage Liris->Acer Rust RECAL `192.168.1.9:4796` is now stable-green for health + public search. The old Node `:4791` is preserved but no longer the recommended Liris peer target.
- `UNVERIFIED_LIRIS`: Liris has not locally remeasured Acer's full 47-daemon census, Acer SOVLINUX 2TB raw substrate, Acer `:4949` live subroutes, or Acer-side 591,286-row recall corpus.
- `CANON`: the Liris branch must keep Acer's maps visible as reference, but must not relabel Acer measurements as Liris measurements.

## Next Migration Cells

1. `Fischer Eval Host-8`: code PR is green and mergeable; runtime cutover remains operator-gated.
2. `RECAL Atlas / Hilbra-local`: map `http://127.0.0.1:4791/` as the local communication / pipe-tracking layer, not just keyword search. Add alias rows for `hilbra`, `atlas recall`, and `recall` so the operator's names resolve to this Brown-Hilbert / Atlas surface instead of disappearing under exact-search gaps.
   - Peer target update: Liris should target Acer Rust RECAL at `http://192.168.1.9:4796` for stable cross-vantage recall. Keep Acer Node `:4791` as preserved legacy surface until operator-gated retire/swap.
   - Durability gate: Acer still needs detach/autostart confirmation for Rust `:4796`; pre-detach soak is green, but post-detach/post-autostart verification remains pending.
3. `Registration Office`: supervisors without PIDs register into sector offices; do not flatten 113+ sectors into one count.
4. `Construction Yard`: candidate upgrade sector; add RECAL aliases for `construction`, `yard`, and `construction yard`, then give it its own host8/stub-room role map.
5. `Remote-control agents`: map as route/runtime surfaces inside the structure; do not treat them as one external UI action.
6. `Boot-autostart`: host8 supervisor must bring councils-and-above warm at system startup; no fire/cutover without parity and operator gate.

## Guardrails

- Keep hot-path receipts `json=0` / HBP where possible.
- Do not retire Node/Python/browser daemons until Rust Host-8 parity, swap, and retire are proven.
- Do not claim cube/fabric absorption from GitHub publication alone.
- Do not emit Slack/QDD/Brian/external messages or operator contact data without exact operator approval of destination and body.
