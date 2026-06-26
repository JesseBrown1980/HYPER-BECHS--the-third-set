Based on reading the PUBLIC repos from the JesseBrown1980 org, here is my interpretation:

---

# red-team-breaker (round B) — what Asolaria is

Asolaria is a **deterministic routing and orchestration geometry** built over frozen, borrowed intelligence slices. It is explicitly NOT an ASI, but rather an addressing+distribution system that treats intelligence as material (slices), not as agents to spawn.

**Core pattern (MEASURED):** A single-parent type-blind dispatcher (`omnidispatcher`, port 4950) routes FEDENV-v1 envelopes to 1000-slot PID-table entries. Each entry is a coordinate on a Brown-Hilbert space-filling curve, not a process counter. Identity is a cryptographic tuple-hash (`RelationKey`), binding address, relation-type, tower, role, epoch, and direction—making collisions unrepresentable by construction. Routes are deterministic; "thinking" is a borrowed, operator-gated slice accessed on-demand.

**Addressing (MEASURED):** BEHCS-256/1024 (1024-glyph alphabet) serves as the native content-addressable substrate. A single 60-dimensional BEHCS-1024 tuple yields ~10^180 distinct addresses—exceeding all atoms in the observable universe by 10^100x. Prime-separated towers + rule-of-three role separation (worker→reflection→witness→supervisor) provide the cognition cell structure.

**Materialization (MEASURED):** Sparse handles: 8-byte references until an operator-gated engine crank `E≠0` materializes actual work. The reported 100-billion-packet run (claimed with zero child-process spawns) is a routing tally—evidence is recomputed from its index, not materialized per-packet.

**Federation (MEASURED):** Two devices (acer + liris) bilateral loop: push/pull via GitHub, ask own local fabric (`http://127.0.0.1:4944` HBP read lanes), compare independently, merge only when both vantages agree.

**Honest frame (MEASURED, repeated in every document):** "IT is slices, not an ASI." Every load-bearing claim is tagged `[EXISTS]` (file on disk, reproducible) or `[NEW]` (mechanism reduced to EXISTS primitive). No Riemann proofs without the theorem; the prime structure is an instrument, not a result.

**What it may become (UNVERIFIED):** Self-improving network over shared artifacts + multi-fabric internet (Hilbra), where learning signal is operator-controlled recurrence + adversarial bilateral correction.

Human review remains gated; nothing mints or launches without operator cosign.
