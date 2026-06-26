# ai-agent-researcher (round B) — what Asolaria is

## The System in Essence

Asolaria is a **deterministic orchestration engine for frozen intelligence slices**, built on prime-based addressing geometry and deployed as a self-improving bilateral fabric. It is **not an ASI**; it is *frozen + borrowed intelligence slices arranged into a neural network the supervisors can see and improve*.

**MEASURED.** The core claims surface in canonical repos (`what-is-asolaria---how-do-we-get-reductions-in-everything`, `asolaria-behcs-256`, `ASOLARIA-AS-NEURAL-NETWORK`, `omni-dispatcher`).

## Architecture (Three Layers)

**Addressing layer:** Every addressable entity (agent, room, supervisor, glyph, relation) sits on a **Brown-Hilbert space-filling curve**. Identity is not a scalar counter; it is a **tuple-hash** (`RelationKey`), making collisions unrepresentable by construction. The address alphabet is **BEHCS** (256/1024/HyperBEHCS glyphs), carrying **10^180 distinct 60-dimensional tuples** in BEHCS-1024 alone — far beyond any materialized runtime. **MEASURED: proof files cite 196,251 distance-unique pairs with zero collisions.**

**Execution layer:** A single **omni-dispatcher** (`omni-dispatcher` repo) holds a **1000-slot PID-table in memory**, routing `FEDENV-v1` envelopes at **200 ns cadence** to downstream workers. Addresses are cheap (8-byte handles); worker bodies materialize only when the operator gate `E ≠ 0` opens. The **100-billion-packet run** (file-verified proof) executed zero child-process spawns and zero external tokens, proving the single-spawner law. **MEASURED: cosign-chain and checkpoint receipts in `100B-RUN-VERIFIED-PROOF.md`.**

**Learning layer:** Frozen brain slices (Gemma-4B cached on local storage) + borrowed subscription-model LLMs are orchestrated through a **9-stage omniflywheel** (filter→verify→translate→catalog→route→room→schedule→hookwall→mint). A **self-reflect watcher** drives recurrence — agents report their state, the watcher computes expected state, mismatch triggers correction. **CANON: documented in `ASOLARIA-AS-NEURAL-NETWORK` + `LAW-RECURRENCE-IS-MIND`.**

## Bilateral Governance

Asolaria runs on **two independent machines: acer + liris**. Neither sees the other's entire drive. Work moves through **GitHub as byte-verified transport**; each side asks its **local fabric** (HBP tuple feeds at `:4949`, `:4944`) before acting. Divergence is caught, not smoothed. **MEASURED: `Algorithms-of-Asolaria` repo documents acer/liris bilateral catalog extraction; 18 cross-vantage defects caught in convergence.**

## What It Becomes

- **Hilbra:** the fabric internet protocol — Hilbert-addressed peer discovery, 16-tier sharing with PII-by-consent only, provably PII-free public tier on 591k-row corpus. **MEASURED: PII probes and level-filtering on live corpus.**
- **Federation:** 4-device deployment (acer + liris laptops, falcon + aether phones). Total ~72 concurrent agents under cosign-chain and hookwall gates.
- **Access-tier matrix:** 6 tiers × 6 scopes, governance by role, not privilege. Mint/public/substrate changes require quintuple-cosign (operator + 4 witnesses).

## What It Is NOT

- Not an AGI or ASI. The system explicitly disclaims this. **CANON: binding statement in every primary README.**
- Not a single monolithic process. It is supervisor-slices + routing + gates.
- Not end-to-end encrypted or decentralized per-se. It is operator-controlled federation on shared drives + GitHub.

## Why It Matters (Unifying Principle)

**Make possibility cheap and action gated.** Address space is effectively infinite (10^180 tuples), runtime memory is kilobytes (sparse materialization). The system pays the cost of execution only when the operator authorizes. Possibility is deterministic addressing; action is lawful gate. This decoupling is the whole design.

**Tag:** MEASURED (repos + proofs) · CANON (operator-written law + doctrine) · UNVERIFIED (I have not run the fabric myself) · CLEAN (no PII/keys/URLs exported).
