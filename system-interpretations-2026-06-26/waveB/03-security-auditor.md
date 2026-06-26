# security-auditor (round B) — what Asolaria is

## Essence
Asolaria is a **federated, deterministic neural-network shape built from orchestrated frozen intelligence slices**. It is *not* an autonomous superintelligence (operators explicitly tag all claims MEASURED, CANON, or UNVERIFIED). Instead, it is a lawful addressing + routing fabric that routes work across multiple devices via deterministic content-addressable tuples, where identity is cryptographic tuple-hash (never scalar distance), and every load-bearing action requires human operator cosign.

## Architecture (MEASURED from repos)
- **Four-device federation** (acer laptop + liris laptop + falcon mobile + aether mobile) running a **single-parent dispatcher** that routes FEDENV-v1 envelopes to a 1000-slot PID-table without forking child processes.
- **Brown-Hilbert space-filling curve** as the universal index: every entity (process, vector, concept, relation) sits on one continuous 47D–60D lattice. This enables O(1) centrality lookups and tie-free novelty detection.
- **BEHCS alphabet progression**: Index-language (legacy) → BEHCS-256 (23 ES-module supervisors + 39 Node packages) → BEHCS-1024 (1024-glyph alphabet, kernel-native) → HyperBEHCS (binary/hash/hex/crypto tuples, json=0 hot path).
- **Frozen-slice orchestration**: One Gemma-4-4B (quantized to 4-10 byte cube-weights), borrowed subscription LLM slices (legal "ordinary use", never metered), and 8 quantization engines compress signals into addressable cube/GNN tuple space.
- **Lawful gates at three tiers**: Tier-1 (single-agent micro approvals) → Tier-2 (2–3 named-roster cosigns) → Tier-3 (quintuple-cosign: Jesse + Rayssa + Amy + Felipe + Dan).

## What it is trying to become (UNVERIFIED inference)
1. **A fabric internet (Hilbra protocol)**: Non-profit indexing layer where any device loads Asolaria and becomes a discoverable, searchable surface. PII-free at L0 by design; deeper tiers shared only by owner explicit consent + expiring key.
2. **Compression / addressing efficiency**: Move from 100B-row JSON corpuses (MB scale) to 8-byte handles + 47D cube references (KB scale). The measured reduction curve: **38.5×** on root corpus (1,084 docs → 292-byte floor).
3. **Self-correcting neural loop**: Watcher subagents emit suggestions; supervisors see all three (worker + reflection + witness); self-reflect + auto-loop drives corrective feedback without external grading.
4. **Fabric-as-authority** (not Windows mirrors): Ask the local fabric first (HTTP endpoints `:4949`, `/hbp/supervisors`, `/hbp/any`), record evidence (404s, timeouts, stale fallbacks), and let fabric facts constrain proposals before spawning token-heavy work.

## Security lens (what an auditor sees)
- **Strengths**: Deterministic dispatch (no hidden spawns); tuple-hash identity (hash collision treated as crypto-negligible, not mathematically solved); lawful multi-actor cosign (no single operator can mint unilaterally); PII oracle (measured L0 PII-free on 591k corpus); fabric-as-authority (decentralizes truth-seeking from one machine).
- **Open questions (UNVERIFIED)**: Hookwall pre/post-syscall gate robustness under adversarial input; GNN inference correctness when fabric edges are stale or disputed; cross-device consensus during transient network splits; whether "borrowed subscription slices" remain lawful under actual usage scale.
- **Honest boundaries**: The 100B packet tally is a counter, not materialized rows; the Rust metal kernel is promised, not yet live; cross-colony index scale-out (3+ devices) is aspirational, not proven.

## Grounding
All observations sourced from public repos (JesseBrown1980 org): `what-is-asolaria`, `asolaria-behcs-256`, `Hilbra`, `asolaria-federation-1024`, `omni-dispatcher`, `ASOLARIA-AS-NEURAL-NETWORK`, `Asolaria-ASI-On-Metal-Fabric-and-matrix`. Repos explicitly carve out secrets/keys/PII (published as "carve-out clean"). No source code modified; findings are read-only.
