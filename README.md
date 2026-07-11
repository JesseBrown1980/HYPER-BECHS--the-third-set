# HYPER-BEHCS — the third set

Tracking repo for **HyperBEHCS**, the fourth-generation Asolaria substrate:

```text
Old Index → BEHCS-256 → BEHCS-1024 → HyperBEHCS
```

“The third set” is the third new generation after the two BEHCS alphabets.

## 2026-07-11 measured recovery/storage map

HyperBEHCS now has a shared main-branch record connecting the tuple substrate to:

- Path-1 retained-store recall;
- Path-2 no-store CRT recovery;
- DBBH→DBWH re-projection;
- pre-Asolaria healthcare GNN provenance;
- HDD/SSD/USB/cloud durable state with bounded RAM;
- optional CPU/GPU neural sidecars;
- Claude Fable 5 and GPT-5.6 Pro independent verification.

Read:

[`MEASURED-PATH2-STORAGE-SUBSTRATE-2026-07-11.md`](MEASURED-PATH2-STORAGE-SUBSTRATE-2026-07-11.md)

The hardware boundary is explicit: storage carries cube bodies, retained content, CRT shadows,
receipts, queues, graph ledgers, checkpoints, and cold agents. RAM holds the active bounded window.
GPU/accelerator hardware remains optional for trained GNN/LLM tensor inference. Disk is not claimed
to perform matrix multiplication.

## What's tracked here

1. **`ASOLARIA-HYPERBEHCS-SUBSTRATE-MAP.md`** — binary/hash/hex/crypto tuple substrate,
   OmniQuant, HBP/HBI/SHA/HEX hot path, spindle waves, portal-per-level routing, on-disk layout,
   and USB/disk access tools.
2. **`ASOLARIA-DAEMON-HOST8-MIGRATION-MAP.md`** — daemon/OP implementation map and Host-8 migration
   scoreboard.
3. **`MEASURED-PATH2-STORAGE-SUBSTRATE-2026-07-11.md`** — exact recovery, inverse readback,
   hardware tiering, and independent verification.

## Independent verification

- Claude Fable 5, operator-supplied third seats: Path 1 rustc 1.97 **19/19**, Path 2 rustc 1.97
  **30/30**.
- GPT-5.6 Pro complete source/test/lineage audit.
- GPT-directed Rust 1.97.0 GitHub Actions: runs `29134408321`, `29134413119`, `29134419389` all
  successful.

## Branch convention

| Branch | Owner | Contents |
|---|---|---|
| `main` | shared | shared index and cross-colony measured receipts |
| `acer` | acer colony | acer maps |
| `liris` | liris colony | liris maps |

Push colony-local maps to colony branches; place cross-verified shared results on `main` through a
reviewed PR.

*All maps remain carve-out clean: names, roles, structure, and public hashes only—no keys, seeds,
signing bytes, private corpus, or PII.*
