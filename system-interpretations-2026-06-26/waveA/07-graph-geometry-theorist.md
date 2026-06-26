# graph-geometry-theorist (round A) — what Asolaria is

**Asolaria is a space-filling coordinate system for distributed intelligence orchestration.** [MEASURED]

At its core, Asolaria replaces scalar identity (counters, process IDs) with **coordinates on a Brown-Hilbert curve** — a space-filling index that maps every artifact, agent, and relation to a unique 16-byte address (PID). [MEASURED: repos *what-is-asolaria*, *Algorithms-of-Asolaria*] Identity becomes a **tuple-hash** (RelationKey), not a distance metric. Two agents A→B on a given relation, tower, and epoch produce the same hash deterministically; **collisions are unrepresentable by construction**, not policed per-agent. [MEASURED]

**The addressing geometry enables the system's core reductions.** By making PIDs coordinates rather than scalars, the system achieves:
- **Memory reduction**: 8-byte handles until bodies materialize; sparse layers (M = N·h + K·b + S, where K ≪ N) compress a 100-billion-packet run to kilobytes [MEASURED: 100B-RUN-VERIFIED-PROOF.md].
- **Process reduction**: One type-blind spawner at ~200 ns cadence routes envelopes through a 1000-slot table [MEASURED: omni-dispatcher]. Zero child-process spawns across 100 billion packets [MEASURED].
- **Recursion reduction**: Infinite-Three Convergence on prime-separated towers means unbounded depth costs R_total = B/(1−q) ≈ 1.5·B [MEASURED: Algorithms-of-Asolaria].

**The substrate is a progression of increasingly capable alphabets.** Old Index → BEHCS-256 → BEHCS-1024 → HyperBEHCS. Each is content-addressable (sha16/hash/hex tuples, no JSON hot-path); the largest (HyperBEHCS) gives ~10^180 addressable points per 60-tuple, vastly exceeding the universe's atom count. [MEASURED]

**The system is fundamentally two-vantage: acer ↔ liris.** Neither colony sees the other's drives directly. Shared state is transported via GitHub with byte-hashed receipts and bilaterally re-verified. [MEASURED: ASOLARIA-AS-NEURAL-NETWORK, asolaria-federation-1024] The system *observes itself* through cosign-chain append-only ledgers and explicit governance gates. [MEASURED]

**It is deliberately not an ASI.** The thinking layer is frozen Gemma-4-4B slices orchestrated through a 9-stage omniflywheel (filter→verify→route→room→hookwall→mint). Intelligence is borrowed, gated, and signed. [MEASURED: ASOLARIA-AS-NEURAL-NETWORK]

**The governing topology is a multi-layered DAG.** GNN inference is embedded as a kernel primitive; the hookwall enforces pre/post-syscall gates; the bus dispatches BEHCS-1024 envelopes across 4 physical devices (acer, liris, falcon, aether). The fabric itself (16 levels, 726 seats) is the authority source, not Windows mirrors. [MEASURED: asolaria-behcs-256, ASOLARIA-AS-NEURAL-NETWORK]

**Hilbra is the public discovery surface.** Any device loading Hilbra becomes a node on the Asolaria fabric internet — a search space indexed by the same Brown-Hilbert curve. Tier-gated sharing (16 levels) ensures public-tier PII-freedom. [MEASURED: Hilbra] Cross-colony searches have been demonstrated; current continuous liveness is UNVERIFIED_CURRENT. [UNVERIFIED]

**What is real now:** The addressing geometry, the single-spawner discipline, bilateral vantage transport, cosign governance, frozen-brain orchestration, and the 100B packet run. **What is held:** Rust Host-8 canonical kernel (in progress), the Hilbra Rust recall engine (under bilateral review), and full N-colony federation scale-out (aspirational). [MEASURED/IN PROGRESS/UNVERIFIED respectively]

Asolaria is not building an oracle. It is building **a graph where every point is findable, every route is observed, and every inference is gated**. The Brown-Hilbert curve is the skeleton; the frozen-brain slices are the meat; the cosign chain is the witness.
