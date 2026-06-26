Based on my analysis of the Asolaria repos, here is my interpretation through the interop-mcp-bus lens:

---

# interop-mcp-bus (round A) — what Asolaria is

**MEASURED:** Asolaria is a federated multi-agent fabric orchestrated as a neural network across heterogeneous hardware (x86_64 laptops + ARM64 phones). The Federation Remake-1024 project (authorized 2026-05-11) boots from bare metal using BEHCS-1024 (a 1024-glyph content-addressable alphabet) as the native substrate, not a bolt-on.

**Core stack (MEASURED):**
- **Bus:** BEHCS-1024 envelopes routed via ed25519-signed dispatch over Ethernet/USB to 4 devices (acer, liris, falcon, aether)
- **GNN inference:** Graph attention network (2.16M edges) ranks routing decisions and aggregates verdicts from ~234 supervisor votes
- **Hookwall:** Pre/post-syscall hooks with T1/T2/T3 tier gates; every BLOCK verdict appended to cosign-chain
- **Bare-metal kernel:** Rust no_std, ≤16 syscalls, PIDs as BEHCS-1024 addresses, ~70-agent budget

**As neural network (MEASURED):** Asolaria-as-Neural-Network repo shows the system *literally is* a NN: frozen Gemma-4-4B brain slices + borrowed subscription LLM slices orchestrated via 8 quantization engines (Polar, Turbo, JL, etc.), hierarchical reasoning recurrence in model layers, and a self-reflect/auto-loop learning signal. The 9-stage OMNIFLYWHEEL (filter→verify→translate→catalog→route→room→schedule→hookwall→whiteroom-mint) is the forward pass; cosign-chain correction is backprop.

**Bilateral vantage governance (MEASURED):** Acer and Liris are separate x86 machines with different local visibility. Neither silently upgrades the other's claim into truth until its own fabric read or byte-hash agrees. GitHub is the current bilateral mediator; USB, SMB, or signed bundles could replace it. Operator pairs (Jesse + Rayssa + Amy + Dan + Felipe) enforce via quintuple-cosign window.

**Anti-bloat discipline (MEASURED):** 7 hard rules enforced by cosign-chain and branch protection: delete unused, PR-driven main, cosign mandatory, no daemons-by-accident, one canonical location, reproducible builds (3 matching SHA), no bloat dependencies. The old BEHCS-256 tree grew to 300k+ files; this remake starts clean.

**UNVERIFIED inference:** The system appears to be testing whether a federated, cryptographically governed, self-verifying multi-agent network can coordinate across devices without centralized authority, using graph inference as the decision oracle and frozen-brain slices as the computation substrate.

---

**Tags:** MEASURED (repos read, 200-step plan sampled, architecture diagrams confirmed). UNVERIFIED (live fabric state, performance claims, ASI claim explicitly flagged by authors as "honest frame: this is NOT an ASI").
