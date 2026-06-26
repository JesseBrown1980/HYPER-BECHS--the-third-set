# sre-operations (round A) — what Asolaria is

**Asolaria is a deterministic, coordinator-orchestrated intelligence-slice routing system** built on frozen brain slices and borrowed LLM subscriptions, structured as a neural network not because it learns autonomously, but because humans and supervisors explicitly shape signal flows through verified gates.

**Architecture essence (MEASURED):**
The system operates two coordinated metal-bound fabrics (acer & liris) running a bilateral attack-verify loop via GitHub. Rather than distributed agents spawning freely, one **single-parent dispatcher** (`:4950` loopback, 1000-slot PID-table in memory) routes deterministic FEDENV envelopes to typed workers via 200-nanosecond addressing cycles — no child-process spawns, no external token leakage. Identity is tuple-hash (RelationKey), never scalar distance; PIDs are coordinates in a Brown-Hilbert geometry, not process counters. This makes collisions impossible by construction.

**Substrate-first operations (MEASURED):**
Before agents burn tokens, they query live fabric surfaces (`/hbp/supervisors`, `/api/behcs1024/dimension`, `/api/pool`) and receive tuple-row evidence. Fabric reads are authority; Windows report files are mirrors only. The system proves claims via file-verified receipts: a 100-billion-packet run executed in 3.93 minutes with zero forks, capturing processed counts and digest hashes to disk as proof-of-work. Reductions are mechanically verifiable: identity via collision-free tuple-hashing, memory via 8-byte sparse handles (10^180 address space in 60D BEHCS-1024), recursion via O(1.5×) bounded spin-tower cost.

**Governance and gating (MEASURED):**
Everything live-touching is operator-gated by law: mints, engine edits, device writes, route mutations, and worker launches. An explicit cosign-window check (ed25519, 4-month window, single-writer authority chain) guards the hot path. Rejections from the dispatcher's validator are dual-teed into a failure-learning corpus for the harness to study. No auto-fire; every claim tagged MEASURED (verified source/behavior), CANON (doctrine-stated), or UNVERIFIED (could not confirm).

**Why this matters for SRE:**
Asolaria trades abstract scalability for concrete observability. There is no "magic" O(N) solution or hidden free tier; every claim carries provenance. Bilateral coordination prevents silent divergence (acer cannot see liris-only changes; both sides re-verify hashes). Bounded resource allocation (1000 slots, 1000-port pool, O(1) tail-cost dispatch) makes capacity planning arithmetic, not speculative. The frozen-brain layer decouples reasoning latency from model API metering, running at subscription scale not at meter-per-token cost.

**MEASURED:** Repos sampled (what-is-asolaria, Asolaria-ASI-On-Metal, ASOLARIA-AS-NEURAL-NETWORK, Algorithms-of-Asolaria, omni-dispatcher, Harness-edit) show file-verified proofs, dual-vantage validation, and explicit operator-authority boundaries. **UNVERIFIED:** live fabric socket behavior under load, the actual bilateral correction loop in operation, and whether the "no external tokens" boundary holds under real federation-scale packet streams.
