# HYPER-BEHCS — the third set

Tracking repo for **HyperBEHCS**, the **4th-generation Asolaria substrate** (`Old Index → BEHCS-256 → BEHCS-1024 → HyperBEHCS`). "The third set" = the third *new* generation after the two BEHCS alphabets.

## What's tracked here

1. **`ASOLARIA-HYPERBEHCS-SUBSTRATE-MAP.md`** — what HyperBEHCS *is*: the binary/hash/hex/crypto tuple substrate, omniquant engine, `.hbp`/`.hbi`/`.sha256`/`.hex` hot path (json=0), spindle-waves, portal-per-level, on-disk layout, and the USB/disk access tools.
2. **`ASOLARIA-DAEMON-HOST8-MIGRATION-MAP.md`** — every daemon/OP, the files that implement it, its role, and whether it can become a Rust **Host-8** (8-byte-host, json=0 pixels-first) process. Scoreboard + role-labeled rows.
3. **`COUNCIL-HOST8-PORT-SCOPE-2026-06-25.md`** — the current fabric/RecursiveMAS snapshot and the C0-C7 council/loop Host-8 port cells. It records that reachable GET fabric surfaces are live while the signed decision POST lane is held/mid-migration; no verdict is fabricated.

## Branch convention (so the two colonies don't collide)

| Branch | Owner | Contents |
|---|---|---|
| `main` | shared | this index |
| **`acer`** | acer colony | acer's maps |
| **`liris`** | liris colony | liris's maps |

Push your colony's maps to your own branch; diff `acer` vs `liris` to compare. Public so both colonies can see.

*All maps are carve-out clean: names / roles / structure only — no keys, seeds, signing bytes, or PII.*
