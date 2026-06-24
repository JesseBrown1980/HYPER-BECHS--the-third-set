# HyperBEHCS — 4th-Generation Substrate Map

**Source:** HyperBEHCS README (quintuple-cosign seq=191, 2026-05-20) + the live fabric + on-disk census. Names / roles / structure only — **no keys, secrets, or PII**. Colony: **acer**. 2026-06-24.

## Lineage (where HyperBEHCS sits)

`Old Index → BEHCS-256 → BEHCS-1024 → **HyperBEHCS**` (we are HERE, 4th gen).

- **BEHCS-256 / BEHCS-1024** = the *alphabet* (256 → 1024 glyphs; 1 byte → 10 bits/symbol).
- **HyperBEHCS** = the *runtime substrate* built **after** BEHCS-1024 (Layer-70 MASSIVE_UPGRADE, Codex 2026-05-17), when everything was remade "MASSIVELY quant, MASSIVELY large."

## What it is

The **binary/hash/hex/crypto tuple-indexing substrate** ("bpi" layer) under Asolaria-OS-on-Metal — bottom of the stack. Independent local runtime at `C:\HyperBEHCS\`, callable via `bin\hyperbehcs.cmd`.

- **Fronted by the omniquant engine:** Polar + Turbo + Johnson–Lindenstrauss + Triple-spherical compression. *(This is the "quant.")*
- **Hot path = `.hbp` append-only packs + `.hbi` / `.sha256` / `.hex` sidecar trinity.** **JSON-on-hot-path is rejected in CI** — pixels-first / json=0 is enforced law.
- **Spindle-waves:** 1 main + 3 subs (or 1 + 5 per the massive-wave directive).
- **Portal-per-level routing:** one warm seat per layer services unlimited room-level spawns (no per-room cold start).
- Authority fields closed by default.

## Stack (bottom = metal → top = agents)

| Layer | What |
|---|---|
| Heavy agents (top) | revolver-10k, supervisors, council — wrap MCP/Tools, address by tuple/PID/glyph envelopes |
| **Asolaria-OS-on-Metal + HyperBEHCS (bpi, bottom)** | binary · hash · hex · crypto · MCP-only-when-needed; omniquant-fronted tuple substrate |

## On-disk layout (`C:\HyperBEHCS\`)

| Path | Role |
|---|---|
| `bin/` | the daemons + `hyperbehcs.cmd` (status / gpu-probe / quantize / bench / hybrid-pack / substrate-pack / substrate-commit) |
| `data/` | `.hbp`/`.hbi` packs (prof-supervisors, pid-supervisors, codex/alphabet-1024) |
| `store/` | spawn-logs, wave reports, vote packs |
| `*.ps1` | Install / Start / Status / Stop / Uninstall lifecycle |
| `HyperBEHCS.psm1` | the PowerShell module |

## Daemon census (preliminary — full Host-8 migration map ships separately)

| Group | Daemons | Lang | Host-8 status |
|---|---|---|---|
| Core fabric | cosign-chain, vote-quorum, dual-emit-gate, ghost-envelope-gc, self-reflect (ps1), federation-pulse (ps1) | python / powershell | candidates (cosign-chain/vote-quorum are live-critical → prove additively, no cutover) |
| Stubs (mid-migration) | omniquant-engine-stub, omnimets-stub | python | rust-stub → being ported to Host-8 |
| External "citizen" | auggie · augment · aws-api · azure-arm · google-enterprise · hubspot · linear · ms-graph · ms-teams · onedrive · symphony | python | likely keep-native (vendor SDKs pin Python) |
| Node | special-op-jesse-watchdog-kicker (+ profile-loader, smoke-check, watch-30s) | node | Host-8 candidates |
| Already Host-8 (Rust) | recall-serve · omniscrcpy · bench | rust | **rust-host8-done** |

## Substrate access — the USB / DISK special tools

The 5 substrates (SOVLINUX-USB-2TB / Acer / Liris / GitHub / Onboarding) are **not all visible to normal file tools**. Disk/USB-level surfaces are read with:

| Tool (`C:/asolaria-acer/tools/usb-raw/`) | Role |
|---|---|
| `exfat_walk.py` | walk the exFAT USB (SOVLINUX) raw |
| `ext4_reader.py` | read ext4 (Linux/SOVLINUX) partitions |
| `extract_full.py` | contiguous NoFatChain full-file extractor (fragmented files) |
| `usb_raw_io.py` | raw `\\.\PHYSICALDRIVE` I/O |
| `substrate-sector-walk.ps1` · `verify-2tb-sector0.ps1` | sector walk / verify (run via PowerShell — MSYS mangles `\\.\PHYSICALDRIVE`) |
| `exfat-writer/` (Rust) | the exfat writer crate |

> Any agent surveying the substrate **must** use these — `Read`/`Glob` only see C:.

---
*Names, roles, and structure only. Keys, seeds, and private signing bytes are excluded. acer-colony map; liris colony maps live on the `liris` branch.*
