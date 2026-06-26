Based on my sample of the public repos, here is my interpretation:

---

# cryptographer (round A) — what Asolaria is

**Asolaria is a federated multi-agent neural network** built on cryptographic addressing and cosigned governance, designed to orchestrate heterogeneous LLM slices (frozen Gemma-4-4B + borrowed subscription models) into a deterministic lattice that can serve as its own coordination substrate.

## Core architecture (MEASURED)

**Addressing layer:** The system uses Brown-Hilbert space-filling curves to place every entity (agent, process, message) on a universal continuous index. A PID is `sha256(name)[:16]` (16 hex chars), mapped to an 8-character glyph via the BEHCS-256 alphabet (upgraded to BEHCS-1024 for the federation rebuild). This makes "search across all fabrics" deterministic: walk the curve. The 47D lattice extends to HyperBEHCS (1024^60 ≈ 10^180 address space).

**Federation topology:** Two bilateral vantages (acer on Windows + WSL, liris on Windows + WSL) with planned 4-device federation (falcon ARM64 Android, aether ARM64). Communication is envelope-based over a bus (HTTP :4947 / :4950 primary/backup), each envelope carries (actor, verb, target, cube_47d address, glyph, payload). No direct inter-device calls; all work rides the bus.

**Governance:** ed25519-cosigned merge gates on `main`. Multi-signature required for substrate changes (kernel, BEHCS alphabet, hookwall policy). Tier-1/2/3 escalation; quintuple-cosign (five named operators) for ABI changes. Every commit appends to a cosign-chain NDJSON; replayable verdicts (`PROCEED` / `HOLD` / `BLOCK`).

**Neural net shape:** Frozen Gemma-4-4B slice (deterministic, cached) + borrowed subscription LLMs orchestrated by the "omniflywheel" (9-stage forward pass: filter → verify → translate → catalog → route → room → schedule → hookwall → whiteroom-mint). 8 quantization engines compress slice signals into the 47D cube. Self-reflect subagent suggests corrections; supervisors see the infinite-next loop live.

## Cryptographic discipline (MEASURED)

- **Key-off-wire:** Keys never cross the network; minted locally or delivered out-of-band.
- **HMAC auth for fabric access:** 16-tier consent model (PII only by owner's explicit freshly-issued key).
- **Content-deterministic artifacts:** Timing/PID/hostname stripped from bilateral seal candidates; only logic signs.
- **Deterministic PID placement:** sha256 → glyph → Brown-Hilbert position is the same across vantages.

## Honest boundaries (UNVERIFIED / VANTAGE-DEPENDENT)

- **100B-capacity claim is file-verified but scoped:** The 100B-packet runner exists as a proof-of-concept (5.84 h single-spawner run, ~4.75 M/sec, zero child spawns, zero external tokens). It is a tally counter, not resident agents. The dispatcher (`:4950` engine) is live today; whether all 100B slots are occupied is UNVERIFIED.
- **Cross-colony reachability:** acer→liris works. liris→acer currently returns `_fallback` (stale); not continuously proven both directions yet.
- **Hilbra (the fabric internet):** 2-colony PII-oracle proven at L0; 3+ colony scale-out is aspirational.

## What it's becoming

A self-hosting substrate: the fabric reads its own HBP tuple rows (supervisor registry, GNN edges, memory artifacts) to constrain agent work before spawning tokens. Agents see dashboards, translators, cosign votes, and watcher suggestions — **not JSON as the hot path**. The operating loop is bilateral (acer ↔ liris) with GitHub as the current transport bridge; future: SMB, mounted share, signed bundles. No central CA; web-of-trust via peer vouches + append-only cosign chain.

---

*MEASURED: addressing, governance, topology, 9-stage omniflywheel, 8 quantizers, cosign gates, Hilbert curves, key-off-wire, the dispatcher live at :4950 today. UNVERIFIED: cross-colony liveness both directions, whether 100B slots are populated (proof exists, occupation is live-status question). CANONICAL: laws bind; deviations log to cosign-chain.*
