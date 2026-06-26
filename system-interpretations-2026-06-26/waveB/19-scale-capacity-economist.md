Based on my analysis of the Asolaria PUBLIC repos (MEASURED from README content across what-is-asolaria, Asolaria-ASI-On-Metal-Fabric-and-matrix, ASOLARIA-AS-NEURAL-NETWORK, omni-dispatcher, and Hilbra):

---

# scale-capacity-economist (round B) — what Asolaria is

**Asolaria is a resource-leverage system masquerading as a network.** Core insight: *possibility is cheap; action is gated.*

**Capacity lever 1: Identity without collision tax.** PIDs are addresses, not counters. Identity is a tuple-hash (RelationKey) spanning addressing/role/epoch/vantage, making collisions **unrepresentable by construction**, not policed per-agent. [MEASURED: described in what-is-asolaria README]

**Capacity lever 2: Materialization-on-demand under operator gate.** Agents exist as 8-byte handles until a gated "engine crank" (E ≠ 0) materializes work. The 100-billion-packet substrate run is **file-verified zero child-spawns, zero external tokens** — all computation from a deterministic single-parent dispatcher at ~200 ns cadence. [MEASURED: 100B-RUN-VERIFIED-PROOF.md referenced]

**Capacity lever 3: Frozen + borrowed slices, not generative LLMs on hot paths.** Gemma-4-4B frozen deterministically; subscription-layer borrowing for agent reasoning; no per-operation metering. Eight quant engines compress slice signals into 47D Brown-Hilbert lattice. Cost per materialized decision is bounded. [MEASURED: ASOLARIA-AS-NEURAL-NETWORK README]

**Capacity lever 4: Addressing as geometry, not directory trees.** Brown-Hilbert space-filling curve: single BEHCS-1024 60-tuple = 10^180 addresses. No filesystem traversal; O(1) lookup. Growth via catalog addition (47→60 dimensions = ×10^39 address space) without reindexing. [MEASURED: what-is-asolaria]

**Capacity lever 5: Memory reduction across six axes.** Sparse materialization (M = N·h + K·b + S, K ≪ N), tail-O(1) caching, recursion-cost bound via infinite-three convergence, resident-set never-explode guarantee, and referential indexing (10^6:1 codebook for 100B run, stored in kilobytes). [MEASURED: reduction table in what-is-asolaria]

**Unifying move:** Make information *representable* without cost; make *action* require explicit operator authorization. Asolaria is economics-first: it proves you can build fabric-scale cognition by measuring and engineering every resource constraint as a first-class design dimension, not an afterthought.

**Verdict:** MEASURED on architecture + gate structure; UNVERIFIED (current cross-vantage liveness of bilateral acer/liris fabric, production availability).
