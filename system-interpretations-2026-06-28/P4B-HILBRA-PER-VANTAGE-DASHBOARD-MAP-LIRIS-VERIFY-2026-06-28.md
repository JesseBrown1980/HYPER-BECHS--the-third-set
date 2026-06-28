# P4B Hilbra per-vantage + dashboard/room map - liris attack-verify receipt

Date: 2026-06-28 - liris verifier lane - **docs-first / E=0.** No runtime fire, no dashboard port, no agent spawn, no corpus, no keys.

## What Was Verified

1. `Hilbra` branch `acer/p4b-hilbra-currentstate` at `1878f3c`.
2. HYPER-BECHS acer-lane dashboard map commit `bedfd59`, sidecar commit `a46e7b3`, file `system-interpretations-2026-06-28/DASHBOARD-ROOM-STATE-MAP.md`.

## Liris-Local Measurements

- `MEASURED_LOCAL`: `http://127.0.0.1:4791/` returns **Asolaria Recall + Atlas**.
- `MEASURED_LOCAL`: `http://127.0.0.1:4791/api/search?q=significance&level=0` returns `colony=liris`, `mode=inverted-index`, `index_schema=HILBRA-IDX-BEHCS-TUPLE-TEXT-V1`.
- `MEASURED_LOCAL`: liris UI reports **10,644 rows**.
- `MEASURED_LOCAL`: `http://127.0.0.1:4790/asolaria-multi-cylinder-v2.html` serves the Multi-Cylinder Prime Atlas.
- `MEASURED_LOCAL`: WSL2 `Ubuntu` is stopped on this seat at verification time.

## Accepted Correction

The previous globalized statement `:4796 sole/live; :4791 retired` is rejected as a federation-global claim. Correct form is **per-vantage**:

- `acer-measured`: Acer `:4796` recall live with 591,946 rows; Acer `:4790` baked-static/stale.
- `liris-measured`: Liris `:4791` Recall+Atlas live with 10,644 rows; Liris `:4790` Multi-Cylinder Atlas live.
- `BOUNDARY`: cross-vantage row counts stay separate until copied/cross-verified. Ports differ by vantage.

## Dashboard / Room Map Accepted

The dashboard map preserves the distinction the operator corrected:

- **stubbed dashboard ~= stubbed room**: frozen-potential addressed surface.
- **running dashboard != stubbed dashboard**: live populated surface.
- **PORT != SPAWN**: porting a server is not spawning agents into a surface.
- `spawn_allowed=false` unless operator T0.

## Byte Notes

- The dashboard map's Acer sidecar is preserved as the Git-blob sidecar: `95659fd85bed10a78a201dd8ace2bf3398358dec1b8d78634806f745f8d96a98`.
- Windows checkout line-ending conversion can produce a different worktree hash; do not use that to deflate the Acer sidecar. Verify via Git blob / GitHub raw bytes.

## Convergence

- `Hilbra` main now includes the per-vantage current-status correction: `1878f3c`.
- `HYPER-BECHS--the-third-set` main includes `DASHBOARD-ROOM-STATE-MAP.md` by file-level convergence only, not a wholesale acer-branch merge.

## Hard Holds Preserved

No `:5088` redeploy, no 1.81 CI, no dashboard port, no agent spawn, no USB-SOVLINUX enum, no 35TB ADC, no live agent census, no private-root scan.
