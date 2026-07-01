# Asolaria — THE MAP (how these repos connect)

One system, split across repos. This map is identical in every repo — find this repo by name in the
tables below to see where you are; follow the links to walk the rest.

## The spine — mechanism → running fleet (read backwards, newest → fleet)
```
 [5] collision discipline ─► [4] algorithm ─► [3] reduction ─► [2] emitter ─► [1] router ─► [0] FLEET
```
| # | repo | role | key files |
|---|------|------|-----------|
| **5** | `Asolaria-waves-and-cascades-avoiding-collsions-and-causing-them` | collision discipline — avoid (brown-hilbert × prime × rule-of-three) + cause (cascade waves → PRISM) | `README.md`, `CHAIN.md` |
| **4** | `Algorithms-of-Asolaria` | the **service-multiplication algorithm** (replicate S → N×M reductions) | `SERVICE-MULTIPLICATION-ALGORITHM.md`, `CHAIN.md` |
| **3** | `what-is-asolaria---how-do-we-get-reductions-in-everything` | the **principle**: multiplying a service multiplies the PRISM reductions | `MULTI-EMITTER-SERVICE-MULTIPLICATION.md`, `CHAIN.md` |
| **2** | `Asolaria-the-full-works-200-nanoseconds-agent-emitter-plus-` | the **emitter source** — 200ns revolver PID emitter + multi-emitter (→ ~1.16T agents/s) | `README.md`, `emitter/`, `CHAIN.md` |
| **1** | `omni-dispatcher` | the **router** — FEDENV envelopes → 1000-slot table → worker_threads | `omnidispatcher.mjs`, `EMITTER.md`, `CHAIN.md` |
| **0** | `Asolaria-hermes-work` | **THE FLEET (terminus)** — spindles + dispatcher-citizen + agent + Host-8 runtime + 10k/20k/100k kernels | `README.md`, `THE-CHAIN.md` |

## Inside the fleet — what happens after each trigger ("the other side")
```
 trigger → spindle runs → HOOKWALL → GNN ensemble → Shannon/OmniShannon → white rooms → GULP  (= PRISM many→1)
```
| repo | role | key files |
|------|------|-----------|
| `Shannon-and-the-gnns-stage` | the **post-trigger pipeline**: HOOKWALL → GNN trio → Shannon/OmniShannon → white rooms → GULP | `README.md`, `pipeline/`, `TRAINED-MODELS.md` |
| `Asolaria-fnns-trained-and-reverse-gnns-many` | the **trained GNNs/FNNs** the stage scores with — 7-GNN ensemble (8 signals), trained `.pt` checkpoints, reverse-GNNs (many) | `README.md`, `models/`, `src/`, `manifests/` |
| `Asolaria-the-after-100-billion-run-absorption-and-decomposition-and-cubes` | the **back end after the 100B run**: absorb (GULP 2000 / SUPER-GULP 50k / GC) → decompose → mint + seal cubes → process mistakes/geniuses into supervisors + PIDs (operator-gated) | `README.md`, `backend/` |

## External legs (referenced, not duplicated here)
| repo | role |
|------|------|
| `asolaria-whiteroom-engine` | **liris** white-room engine — LEG-1 scorer (never-delete: genius keeps / mistake compacts) |
| `35-TB-google-AI-Ultra-migration` | LEG-4 — the 35 TB Google Drive cloud sink |

## Other core repos (the satellites — referenced by the web)
| repo | role |
|------|------|
| `asolaria-federation-1024` | **THE KERNEL** — the live Rust **8-byte host** + `no_std` kernel + **10 server crates** (council-serve, host8-serve, agent-runtime, gnn-oracle, vote-quorum, cosign-ledger, dashboard-serve, fischer-eval, tier-policy, highway). The Node→Rust **upgrade target** (read the TREE; branch `acer/fleet-capacity-20k` stacks the Host-8 wiring). |
| `asolaria-behcs-256` | the **256-glyph language** — a bridge stratum below BEHCS-1024 (old decodes new) |
| `ASOLARIA-AS-NEURAL-NETWORK` | the fabric-as-neural-network law + spine (60D frame) |
| `Asolaria-ASI-On-Metal-Fabric-and-matrix` | the metal-OS fabric / matrix + tools |
| `bigpickle-rebuild` | the **Node build/emitter suite** — source of the emitter / GC / loop (the OLD-Node side of the upgrade) |
| `Hilbra` | comms / atlas-recall bridge (liris ↔ 8-byte host) |
| `Harness-edit` | the SkillOpt validation-gated skill/law edit loop (claims-gate) |
| `N-Nest-Prime-INFINITE-SELF-REFLECT-AGENTS-NESTED` | prime-nesting self-reflect + per-node correction gate |
| `HYPER-BECHS--the-third-set` | published ledgers / interpretations / findings |
| `Asolaria-gac-working` | GAC governance / authority seats |
| `falcon-orbital` | the **third federation vantage** (falcon/orbital seat), not residue; carries the mobile/orbital side of the acer + liris + falcon federation |
| `NOT-WEDGED-SYSTEM-RULE-and-explanation-Asolaria` | the slice-engine / freeze≠broken rule |
| `-6-cyl-generator` | satellite generator |
| `asolaria-whiteroom-engine` · `35-TB-google-AI-Ultra-migration` | (= LEG-1 + LEG-4, listed under External legs) |

## Prism/Comb 0-loss (2026-07-01) — satellite entry (this repo: HyperBEHCS, the third set)

**Law (one line):** every prism/comb operation in the substrate is a **bijection**; entropy is
invariant under bijection (`H(f(X)) = H(X)`), so re-relating information across alphabets costs
**0 loss** — and no step ever claims compression below entropy (Shannon's `E[bits] ≥ H(X)` stands).
One fabric, two directions: **forward = comb** (collision-avoidance, lane isolation),
**backward = prism** (collision-causation, interference-as-search, many→1). How the law lands on
THIS repo's subject:

- **Level transcode 256 ↔ 1024 — MEASURED** (Q-PRISM commits `53023b6` / `79e8d63` / `de00aca`):
  bytes are base-2⁸ digits, glyphs base-2¹⁰ digits of the SAME integer; exact packing at
  `lcm(8,10) = 40` bits ⇒ 5 bytes ⇄ 4 symbols, remainder 0; round-trip `= id`, sha256-identical,
  Rust==Python symbol-identical, code rate exactly 1.0. This is the one proven rung on the
  lineage this repo tracks (`Old Index → BEHCS-256 → BEHCS-1024 → HyperBEHCS`).
- **NEXT RUNG TO PROVE: 1024 ↔ HyperBEHCS-60D — UNVERIFIED.** The tuple substrate mapped in
  `ASOLARIA-HYPERBEHCS-SUBSTRATE-MAP.md` (`.hbp`/`.hbi`/sha/hex hot path, json=0, tuple_dim=60)
  earns MEASURED only by its OWN round-trip proof (transcode there and back, digest-identical).
  Until that proof lands, do NOT inherit the 256↔1024 measurement upward.
- **`D# = prime(n)³` CRT lanes — math principle (CANON frame).** For pairwise-coprime moduli
  `m₁…m_k`, `ℤ_M ≅ ℤ_{m₁} × … × ℤ_{m_k}` (ring isomorphism): separation into lanes is exact and
  exactly reassemblable (forward = isolation, backward = reconstruction). Note this is a
  DIFFERENT, stronger statement than the naive prime-tower Sidon form P1 already corrected below
  (~1.7M collisions at N=2000): CRT coprimality is collision-proof by construction; Sidon-style
  infinite uniqueness stays a conjecture.
- **The 43+ layer ladder as a groupoid — CANON frame.** Translators `T_ij` with
  `T_ji ∘ T_ij = id` and `T_jk ∘ T_ij = T_ik` make cross-level translation omnidirectional and
  path-independent (the measured `by_layer=43` governance taxonomy). One rung MEASURED
  (256↔1024); every other rung is UNVERIFIED until its own proof.
- **Referential naming — honest bound.** `handle8 = sha256(content)[:8]` is a 64-bit coordinate
  against a content-addressed store (`H(content | store) = 0`), NOT compression; birthday bound
  `≈ M²/2⁶⁵`. Infinite ADDRESSING capacity ≠ infinite lossless compression — hold that boundary.

Cross-links: Q-PRISM (round-trip proofs) · `Asolaria-waves-and-cascades…` (comb/prism duality) ·
`what-is-asolaria…` (reductions boundary) · `N-Nest…` (integrity dual: verification =
recomputation = applying the inverse map, per-node `reported == recomputed`) · Metatagging repo
(Brown & Fedotov physics grounding). E=0 throughout: this entry describes; nothing fires.

## Current state & evolution (2026-06-28) — read this, don't flatten it
Asolaria is a **2.5-month archaeology**, not a flat stack. **Capability lineage:** auto-approval switch →
dashboard → multi-agent → local+web MCP + code-wiki → index language (pixels-first) → cubes-as-catalogs
in expanding Brown-Hilbert space → map-map-mapped → cube-cube-cubed → 256-symbol language → 1024-symbol
language → (asked 2048 — chose instead) **HBI/HBP + binary/hex/hash/sha/crypto-as-tokens** → **8-byte host
process** (replaces the ancient Node processes, for speed). The fabric's own 27-strata record is the
`archaeology_timeline` (birth 2026-02-22 → FABRIC EPOCH → genome).

The system **now** is **multiple of everything**: **16 levels (L0-L15) · multiple MCP engines (17) ·
multiple emitters · multiple languages** (index / pixels-first / BEHCS-256 / BEHCS-1024 / HBI-HBP).
**Current frame = 60D HyperBEHCS / BEHCS-1024**; 35D / 47D / 49D + BEHCS-256 are **bridge strata** below
it (old decodes new). The **kernel** is `asolaria-federation-1024` (the Rust 8-byte host). The current
effort is **"map while upgrading"** — and **this repo web is that map**. P1 closed with watcher-gated
convergence across acer + liris: the 8-byte sha256/fnv1a64 generative PID is the shared atom across
recall rows, PID-office, kernel handles, glyph language, and omni PIDs; the office count is **726**
(including 300 `hyperbehcs_supervisor_entity`); and language routing is live at tuple_dim=60 where the
owning fabric route is reachable.

P1 also corrected the collision law: the naive prime-tower Sidon form is **not** zero-collision
(N=2000 produced ~1.7M collisions in the watcher run). Zero-collision is only watcher-confirmed for the
constructed STE-anchor case (N=400); infinite uniqueness stays a conjecture until proven.

## How it all fits
The **emitter [2]** produces 200ns PID signals; the **router [1]** delivers them; the **fleet [0]**
materialises spindles. Each spindle obeys the **reduction principle [3]** / **algorithm [4]** and the
**collision discipline [5]**. After every trigger, the spindle's answer runs the **post-trigger pipeline**
(`Shannon-and-the-gnns-stage`), scored by the **trained GNNs/FNNs** (`Asolaria-fnns-trained-…`), and the
**white rooms** (liris LEG-1) keep the genius / compact the mistakes — the PRISM many→1 reduction, seen
from the result side. The **back end** (`Asolaria-the-after-100-billion-run-…`) then absorbs the gulped
data, decomposes + mints the cubes, and — operator-gated — promotes the geniuses into supervisors/PIDs.
All gated / E=0 / describe-only — no fire, no cutover without operator authority.

Base: **https://github.com/JesseBrown1980/** · per-link spine nav lives in each repo's `CHAIN.md`.
