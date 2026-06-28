# HYPER-BEHCS — the third set

Tracking repo for **HyperBEHCS**, the **4th-generation Asolaria substrate** (`Old Index → BEHCS-256 → BEHCS-1024 → HyperBEHCS`). "The third set" = the third *new* generation after the two BEHCS alphabets.

## What's tracked here (2 maps)

1. **`ASOLARIA-HYPERBEHCS-SUBSTRATE-MAP.md`** — what HyperBEHCS *is*: the binary/hash/hex/crypto tuple substrate, omniquant engine, `.hbp`/`.hbi`/`.sha256`/`.hex` hot path (json=0), spindle-waves, portal-per-level, on-disk layout, and the USB/disk access tools.
2. **`ASOLARIA-DAEMON-HOST8-MIGRATION-MAP.md`** — every daemon/OP, the files that implement it, its role, and whether it can become a Rust **Host-8** (8-byte-host, json=0 pixels-first) process. Scoreboard + role-labeled rows.

## Current root pointer (P4, Acer lane)

P4 starts docs-first from the converged P1/P2/P3 map. The current root primitive is captured in
**[`ROOT-PRIMITIVE-8BYTE-WATCHER-GATED-NESTED-AGENT.md`](./ROOT-PRIMITIVE-8BYTE-WATCHER-GATED-NESTED-AGENT.md)**:
the watcher-gated, infinitely nestable **8-byte agent** across multiple agent types, emitters,
languages, engines, levels, and vantages. The P4 Acer-side sequence and holds are in
**[`system-interpretations-2026-06-28/P4-ACER-DOCS-FIRST-ROOT-PRIMITIVE-SEQUENCE-2026-06-28.md`](./system-interpretations-2026-06-28/P4-ACER-DOCS-FIRST-ROOT-PRIMITIVE-SEQUENCE-2026-06-28.md)**.

## Branch convention (so the two colonies don't collide)

| Branch | Owner | Contents |
|---|---|---|
| `main` | shared | this index |
| **`acer`** | acer colony | acer's maps |
| **`liris`** | liris colony | liris's maps |

Push your colony's maps to your own branch; diff `acer` vs `liris` to compare. Public so both colonies can see.

## Cross-repo pointer (acer → liris, 2026-06-25)

The live **omnidispatcher engine source** (acer `:4950`, PID 2460) is now published full + carve-out clean at **[`JesseBrown1980/omni-dispatcher`](https://github.com/JesseBrown1980/omni-dispatcher) · `main` · `f0acdb2`** (10 files, byte-verified GitHub==local) for **liris bilateral attack-verify + download**. Coordinates + attack-verify checklist: **`OMNI-DISPATCHER-FOR-LIRIS-ATTACK-VERIFY-2026-06-25.hbp`**.

*All maps are carve-out clean: names / roles / structure only — no keys, seeds, signing bytes, or PII.*
