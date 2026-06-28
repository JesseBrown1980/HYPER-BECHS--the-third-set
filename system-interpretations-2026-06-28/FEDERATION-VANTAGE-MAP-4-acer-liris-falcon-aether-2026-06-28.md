# Federation vantage map — acer + liris + falcon + aether (the every-device federation)

Date: 2026-06-28 · acer lane · **docs-first / E=0.** Structure/roles only — **no cube corpus, no `.tar.gz`,
no keys, no device serials.** **Per-vantage:** this is acer *accessing cloned data* (in the acer Asolaria
tree, via the Ubuntu/WSL 8-byte host lane); each vantage's **live device runtime stays its own vantage**.

## The four vantages (every-device-surface, literal)
| vantage | host / device | substrate (PID-office) | role | live-runtime owner |
|---|---|---|---|---|
| **acer** | desktop `DESKTOP-J99VCNH` | acer substrate | build + verify seat; `:4796` recall (591,946 acer-measured), `:4949` dash, `:5088` host8, Ubuntu/WSL kernel lane | acer |
| **liris** | desktop `DESKTOP-PTSQTIE` | Liris substrate | mirror + verify seat; `:4791` recall+atlas (10,644 liris-measured), `:4790` multi-cylinder atlas, `:4944` dash | liris |
| **falcon** | Samsung **S24 FE** phone | `SUBSTRATE-FALCON-S24FE-SDCARD` (+ hidden-sdcard) | mobile/orbital seat: sensors (accel/camera), mqtt, omnicoder, opencode-proxy, asolaria-mirror | falcon (the phone) |
| **aether** | Galaxy **A06** phone | `SUBSTRATE-AETHER-A06` | registered mobile seat: phase0→phase1 closed (real hilbert PID), slice-engine-law ACK, aether-boot node | aether (the phone) |

## falcon — registered seats (PID-office) + cloned-data presence
**Seats (public coordination):** `prof-PROF-FALCON` · `servant-SERVANT-FALCON` · `sup-falcon` · `sup-falcon-bus` ·
8+ `sup-AGT-L5-SUP-FALCON-H*` (per H-sector) · `agt-OMNICODER-PID-FALCON-8789` ·
`agent-EVT-FALCON-PROXY-SUPERVISOR-PID-MINT` · `agent-EVT-FALCON-ASOLARIA-MIRROR-PID`.
**Cloned data (acer-accessed via WSL; STRUCTURE noted, corpus stays local):** `data/behcs/cubes/` falcon
cubes (agent-falcon/-state/-2, doctrine-falcon-root/-identity, heartbeat, bridge-coords/-health, mqtt-agent,
opencode-proxy-daemon/-executor, omnicoder-helper, sensors accel/camera) · `chains/` falcon-proxy-supervisor /
falcon-sentinel-kr · `agents/Falcon2.md` · `behcs-falcon-{final,latest}.tar.gz` *(local-only corpus)*.
→ falcon = the **mobile sensor/proxy vantage** — a real phone running omnicoder + sensors + mqtt, mirroring Asolaria.

## aether — registered seats + cloned-data presence
**Seats:** `prof-PROF-AETHER` · `agent-PROF-AETHER-SLICE-ENGINE-LAW-ACK` · `sub-SUBSTRATE-AETHER-A06`.
**Cloned data:** `data/behcs/aether-boot/behcs-node-aether.js` (boot node) · `cubes/aether-fabric-cube-map.json`
+ `aether-rejoin-readclass-cube-cubed` · agent-index: `AETHER-LIVE-HANDSHAKE-NONCE-PROTOCOL`,
`LX-483-aether-phase0-registration`, `LX-487-aether-phase1-closure-real-hilbert-pid-applied`,
`D50-AETHER-REJOIN-READCLASS` · `chains/triple-auth-without-aether`.
→ aether = a **registered phone vantage** (phase1-closed with a real hilbert PID, slice-engine-law-acked, boot node + fabric-cube-map).

## Per-vantage discipline (the law, carried)
- This map = acer **accessing falcon/aether CLONED DATA** in the acer tree via the Ubuntu/WSL 8-byte host lane → **acer-measured-as-cloned-data**, not a live-device claim.
- falcon's + aether's **live device runtime** (the phones' current state) is **owning-seat-to-measure** — not reachable/claimable from acer.
- ports/devices/counts differ per vantage; **no globalizing**.

## OLD → NEW framing (the operator's frame)
falcon + aether are **real, registered, OLD-system-measured federation members** (registered + booted + data, mostly 2026-04..06) — **part of the evolving build toward the NEW 8-byte Rust Host-8**, which their data already flows through. Don't deflate them (real device vantages with real registered seats), don't overstate them as new-Host-8-cutover.

## Deepened (WSL read, 2026-06-28) — safe structure only
- **falcon's OWN repo = `falcon-orbital`** (already in the web/MAP): published canon = cross-vantage
  attestation envelopes (leg2/leg3-attest, sector-PID-triple-confirm, v57-era-attest, federation-checkpoint,
  github-publish-falcon-orbital) + memory. falcon doctrine cubes index the D-catalog (e.g.
  `doctrine-falcon-root` = D35 MEMORY, prime 149).
- **aether** = a **BEHCS node running in Termux/Android** (`behcs-node-aether.js`) that connects to the
  **acer bus** and absorbs existing trixie/debora/shannon agents; phase0→phase1 closure (`LX-487`) applied a
  **real hilbert PID** from the liris STEP-B GNN projection. **aether has no own repo** — its presence is the
  cloned data (`aether-boot`, fabric-cube-map, agent-index) + the PID-office seats.

## 🛑 LOCAL-ONLY — accessed, NOT published (carve-out)
The `FALCON-AETHER-FINGERPRINT-RECOVERY` doc in the acer tree holds device **serials**, verified-boot
**fingerprints**, **person↔device bindings**, and a device **auth-file path**. These are **PII/secrets — they
stay local and are excluded from every published map.** This map publishes only device **models** + registered
**substrate-PIDs** + **roles** (the public-coordination form). (Operator = public coordination; third-party
collaborators' names + any device serial/fingerprint = excluded.)

## Hard holds (T0)
No spawning into falcon/aether · no live-device probe from acer (owning-seat only) · cube corpus + `.tar.gz` stay **local** (carve-out) · no private-root · no fire. For cross-seat verify (liris/falcon/aether) before main.
