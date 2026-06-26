Based on my sampling of the Asolaria public repos, here is my interpretation:

---

# performance-engineer (round A) — what Asolaria is

**Asolaria is an addressing and routing geometry that runs intelligence slices as a fabric instead of spawning processes.** 

At its core: a **coordinate-based identity system** (tuple-hashes, not counters) overlaid on a **deterministic prime-separated lattice** (Brown-Hilbert cubes, 60D address space ≈10^180 capacity). Resources are addressed cheaply as 8-byte handles; bodies (the actual compute work) materialize only when an operator gate opens (`E ≠ 0`). The system proved this works by running **100 billion packet-transactions in 3.93 minutes (424 M/sec), zero child-process spawns**, with resident set provably capped at 2000 slots under any arrival stream — a never-explode bound.

**From a performance lens:** this is an architecture that decouples addressing from materialization, so possibility stays cheap. Routing becomes O(1) lookups in precomputed distance-unique projections. Recursion costs O(B/(1-q)) ≈ 1.5×B instead of exponential blowup. A single type-blind spawner (not a fork bomb) handles all dispatch at 200 ns cadence, and every repeated request hits a cache or index, not recomputation. Memory efficiency comes from sparse materialization: quant engines (8 variants: Polar, Turbo, JL, Zeta, etc.) compress frozen LLM slices into cube/GNN tuple space; a 100-billion-row run materializes in kilobytes via referential codebooks, not lossless infinite compression.

**Operationally:** the system is built on **bilateral verification (acer ↔ liris vantage)** before canonization, **fabric-first reads** (query local supervisor state before token-heavy operations), and **self-reflection with corrective gates** (N-Nest agents nest infinitely, but every level must prove reported == recomputed truth — the watcher catches confabulation). It uses tuple/HBP formats (not JSON) on hot paths, and keeps an operator-gated approval layer (no autonomous scaling, no "just-fire" semantics).

**MEASURED:** the 100B run's zero-fork claim, the 8-byte-agent capacity, the never-explode resident-set bound, the single-spawner design, the bilateral exchange protocol, and the five-primitive kernel composition. **UNVERIFIED:** whether the full 10^180 addressing space meaningfully reduces collision/centrality problems in practice (the measured 196k pair → 0 collision certificate is proof-of-concept, not production scale); whether the frozen-slice + borrowed-LLM composability generalizes beyond the current Gemma-4B + subscription model.

**What it's trying to become:** a **federated neural-network fabric orchestrated lawfully over borrowed intelligence**, where neither side depends on the other's capacity, both sides independently verify state, and the geometry itself (addressing, routing, recursion cost) proves scalability without requiring exponential resource growth.
