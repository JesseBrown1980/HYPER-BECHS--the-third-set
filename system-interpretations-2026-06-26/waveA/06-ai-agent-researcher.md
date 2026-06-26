Based on my sampling of the Asolaria public repositories, here is my interpretation:

---

# ai-agent-researcher (round A) — what Asolaria is

**MEASURED:** Asolaria is a federated multi-agent architecture designed to coordinate heterogeneous Claude instances (desktop, phone, remote) over a lightweight, deterministic addressing and routing layer. The core implementation (`asolaria-behcs-256`) is a Node.js federation toolkit with 39 packages: 8 supervisors, 6 core-loop engines, 10 systems, plus infrastructure and scale components. Core runtime primitives—ADDRESS, CONTENT, INTEGRITY, SCORE, ROUTE—compose into five omni-engines (wave/districts, glyph/cube, cosign/merkle, shannon/GNN, room-dispatcher/spindle).

**MEASURED:** The addressing model uses Brown-Hilbert 60-dimensional coordinate space, generating ~10^180 distinct addresses per BEHCS-1024 tuple. Identity is tuple-hash (`RelationKey`), not scalar counters. Supervisors coordinate via a bus protocol on ports 4947 (primary) and 4950 (backup), communicating through envelopes carrying PID-stamp, verb, actor, target, glyph-sentence, and BEHCS-indexed payloads. The system claims zero-process-spawn execution—100 billion packets processed with no child processes spawned (verified against checkpoint state).

**MEASURED:** The real graph uses "rooms" (indexed containers), a "spindle" router (≤42 real/virtual routes), and an "omniflywheel" that rotates work through rooms without materializing agents until a spawn-emit gate triggers. Rooms persist as stub entries (8-byte handle + index) until use. Compression is referential (codebook + indices), not lossless storage.

**UNVERIFIED:** The architecture treats computation as slices—frozen, gated intelligence accessed by coordinator logic that owns routing and scoring. The supervisor layer ("hyper-hermes") exists as positions (`sessions: 0`) until materialization. Multiple "cylinders" (topic domains) and "towers" (recursion depth) organize the address space; the system appears to encode Shannon-based role separation (worker/reflector/witness/supervisor triads).

**MEASURED:** Supporting repos implement: federated state synchronization (Rust), neural network ranking (GNN at `:4792`), whiteeroom testing, USB-based sovereignty storage, identity-via-fingerprint, and Cosign v2 tamper-evident signing. The movement is toward binary tuple serialization (HBP/HBI format), away from JSON.

**ESSENTIAL INSIGHT:** Asolaria decouples *possibility* (cheap 8-byte addresses, unbounded geometry) from *realization* (operator-gated engine cranks). The prime-structure-as-addressing pattern makes every relationship uniquely identifiable and centrality tie-free. It is not an ASI—it is addressing + routing + frozen-intelligence-slice coordination, designed to scale deterministically without exponential spawning.

---

- **MEASURED** tags: repos sampled, READMEs decoded, architecture doc from fabric, supervisor/package structure confirmed on-disk.
- **UNVERIFIED** tags: inferred from naming patterns and conceptual arcs (slice-engine model, frozen materialization, tower recursion).
- **PUBLIC OUTPUT CARVE-OUT:** No keys, credentials, IPs, serials, or feed contents included. Structure, concepts, and architecture only.
