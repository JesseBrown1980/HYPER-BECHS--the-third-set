Based on my read of the Asolaria PUBLIC repos, here is my interpretation:

---

# cryptographer (round B) — what Asolaria is

**MEASURED:** Asolaria is a lawfully orchestrated neural network built from frozen intelligence slices (Gemma-4 deterministic layers + borrowed subscription LLMs) encoded onto a **Brown-Hilbert space-filling curve** (`Hilbra`). Every artifact lives at a single continuous address in that curve. The system is **not an ASI**; it is a self-improving network of borrowed + frozen slices orchestrated within cryptographic gates.

The mathematical spine: content-addressable **BEHCS-256/1024 encoding** (1024^60 ≈ 10^180 address space) + **47D Brown-Hilbert lattice** for cube/room addressing + FNV-1a64 hashing + prime-power classification for glyph binding. Addressing is deterministic, globally unique, and route-able via a single curve walk.

**MEASURED:** Two physical machines (`acer` + `liris`, Windows 11 + USB-boot kernel) drive the fabric bilaterally — **adversarially**. Each side re-runs checks, re-reads shared state via GitHub, and refuses to canonize anything until byte-hashes and fabric-reads agree. The cosign-chain (ed25519, append-only) enforces quintet operator authority. No admin key mints; all state mutations require human T0-signature across the window.

The runtime: Omni-dispatcher (single-parent spawner, 1000-slot PID table) routes `FEDENV-v1` envelopes through a 9-stage **Omniflywheel** (filter → verify → translate → catalog → route → room → schedule → hookwall → mint). **Hookwall** sits between user-space and bare-metal kernel — every syscall carries a cryptographic pre/post gate.

**MEASURED:** The system proved a **100-billion-packet run** (zero spawned processes, zero API calls, ~5.84 h paced at 4.75 M/sec) against hash-receipted proof files. Governance is **explicit**: Hilbra (16-tier fabric internet) uses owner-consent + scoped keys for PII-gated access. Cross-fabric discovery walks the shared Brown-Hilbert curve; reachability is vantage-dependent, tagged honestly as `UNVERIFIED_CURRENT` where not re-proven from both seats.

The coherence: **bilateral parity under adversarial verification**. No silent upgrades. No mirrors become authority. Shared truth is origin-local receipts transported + byte-verified, never inference from memory.

---
