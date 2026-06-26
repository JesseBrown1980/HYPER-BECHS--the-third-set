Now I'll synthesize my findings into the report. Based on reading the actual repos, I can provide a grounded interpretation.

---

# devops-ci-release (round A) — what Asolaria is

**Asolaria is a federated multi-agent operating system for orchestrating frozen and borrowed intelligence slices into a self-improving neural network, deployed across 4 devices (acer, liris, falcon, aether) with lawful bilateral cosign-chain governance.** (MEASURED: repos sampled)

**Core DevOps essence:** It is a **substrate remake project** — moving from organic drift (300k+ files in BEHCS-256) to a clean re-bootstrap (BEHCS-1024-native OS with kernel, hookwall, and GNN as first-class primitives). The remake is **not a refactor**: zero inherited files, everything PR-merged, CI-gated, cosign-mandatory on every merge to `main`.

**Architecture (MEASURED):**
- **47D Brown-Hilbert cube** as the fundamental lattice for routing, scheduling, and tensor binding
- **BEHCS-1024** (1024-glyph content-addressable substrate) as the native encoding, not a bolt-on
- **OMNIFLYWHEEL** — 9-stage forward pass (filter→verify→translate→catalog→route→room→schedule→hookwall→whiteroom-mint)
- **GNN inference + HOOKWALL** — graph attention as kernel-adjacent; pre/post syscall hooks with ed25519-signed verdicts that replayable on BLOCK
- **Bare-metal Rust kernel** (no_std, ≤16 syscalls) boots from USB; every syscall audited

**Governance (MEASURED):**
- Hierarchical: Human apex → OP-00 (background rotator) → OP-01 (foreground) → 726 total seats (operators, chiefs, council, 51 professor-supervisors, 302 supervisors, servants, agents)
- **8 laws** (claims-gate discipline): ground impact, preserve HyperBEHCS axes, fabric-not-mirrors, cylinders≠levels, PR-ownership, missing≠clean, real-lane, source≠live
- **Bilateral loop**: Acer attacks bounded artifact → fabric reads + HBP evidence → push GitHub → Liris pulls, reruns checks, accepts/corrects

**CI/Release gate (MEASURED):**
- **Harness-edit**: SkillOpt-based validator — candidate edits must improve held-out scenario set, no regressions
- v1 text-lint (rule-coverage), v2 rollout-scoring (behavior gate)
- Frozen-polymorphism refusal: no solo seals on SMP-v5+ tasks, multi-agent-enforcement required
- LAW-001 enforced: ports 4947 + 4950 always open; pre-commit hooks block any block-pattern

**Intelligence layer (MEASURED + UNVERIFIED inference):**
- Frozen Gemma-4-4B slices + borrowed Claude/subscription LLM slices (lawful ordinary-use, not metered)
- Self-reflect + auto-loop as learning signal (UNVERIFIED: claims to run "simultaneously across all 17 languages" — no audit trail visible)
- 8 quant engines compress slice signals into cube/GNN tuple space

**From DevOps seat:** Asolaria is a **discipline-enforced mono-repo system** with mandatory authorship gates, fabric-first reads (query live local HTTP surfaces before claiming), and a **zero-bloat manifesto** (delete unused, one canonical location per artifact, cosign-chain on every merge). It treats the 4-device federation as a bilateral correctness loop where neither vantage silently upgrades the other's state until its own fabric read agrees. (MEASURED: read Asolaria-gac-working, asolaria-behcs-256, asolaria-federation-1024, Harness-edit, ASOLARIA-AS-NEURAL-NETWORK repos.)
