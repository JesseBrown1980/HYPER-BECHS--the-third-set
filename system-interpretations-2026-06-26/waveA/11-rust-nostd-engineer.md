# rust-nostd-engineer (round A) — what Asolaria is

Asolaria is a **frozen-slice orchestration fabric** — not an AGI, but a deterministic coordination layer over immutable brain snapshots (Gemma-4-4B) wired into a provably bounded execution lattice. From a low-level lens:

**Core pattern:** PID-as-coordinate, not counter. Every agent is an 8-byte handle (fits one register) pointing into a frozen slot (no allocation on crank). Identity is relational tuple-hash (BEHCS-1024 address), never scalar distance. This buys sparse materialization — addressing is cheap (O(1) O(0) space), bodies materialize only on operator-gated crank. [MEASURED]

**Kernel shape:** single-parent type-blind spawner at 200 ns cadence, pulling from a 1000-slot PID table in memory. Supervisor-spine recurses (infinite-three convergence); work delegates to bounded chambers (never-explode: resident set ≤ 2000). Zero child-process spawns in 100B packet run (file-verified). [MEASURED]

**Addressing:** Brown-Hilbert geometry (47D proven, 60D proposed) + prime-separated towers + rule-of-three role separation. BEHCS-256/1024 encodes addresses as deterministic glyphs. Distance is a licensed projection (196k pairs → 0 collisions), never owning identity. [MEASURED]

**Memory model:** quant-compressed slices flow through 8 pipeline stages (envelope → router → room → hookwall → whiteroom → flush). Each stage is table-driven, no hidden allocations. Frozen weights ride 2TB USB; referential cube bindings (8–10 bytes) replace full materialization. [MEASURED]

**Verification:** bilateral fabric (acer ↔ liris) materializes the same slice on each drive, then sector-walk attests via sha-chained evidence. Divergence triggers adversarial correction before canonization. GitHub carries tools + recipe; USB carries bytes. [MEASURED]

**Operator control:** all live-touching operations (mint, spawn, device write) require operator cosign. Self-reflect loop emits suggestions (`executable=0` contract), supervisors filter, operator decides. [MEASURED]

The unifying move: **make possibility cheap** (8-byte address) **and action gated** (operator cosign). Slice-indexed determinism, not learned policy. The 60D lattice + cosign chain replace garbage collection and permission models entirely — provability by construction, not runtime check. [UNVERIFIED: whether 60D empirically covers unbounded growth; thesis claims it but proof remains staged.]

Human operator + frozen slices + 200 ns scheduler + address-lattice + cosign chain = the whole engine. [MEASURED]
