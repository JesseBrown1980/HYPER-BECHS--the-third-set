# Dashboard / room state-topology map (map-map-mapped layer)

Date: 2026-06-28 · acer lane · **docs-first, E=0.** No port, no spawn, no fire. `spawn_allowed=false` unless operator T0.
For cross-seat verify before main. **Per-vantage:** every state below is measured by ONE seat; do NOT globalize a loopback measurement into a federation claim.

## Doctrine (the distinction this map exists for)
- **stubbed dashboard ≈ stubbed room** — a frozen-potential slice: an addressed surface (8-byte agent
  slots laid out) **not yet materialized**. It becomes **running** only by **spawning agents into it**
  (rooms-as-RAM) — and that spawn is `E≠0` → operator T0.
- **running dashboard ≠ stubbed dashboard** — live, populated, serving.
- This duality recurs **at every level (L0–L15)**. "map-map-mapped" = mapping *which surface is in which
  state, per vantage, per level* — not just "what exists."
- **NOT-WEDGED rule:** stubbed / held-safe / frozen ≠ broken. A surface not running is a *state label*,
  not a failure.
- **Two operations, never conflated:** **PORT** = upgrade the surface's *server* Node→Rust Host8 (code);
  **SPAWN** = materialize a stubbed surface into a running one (agents). PORT ≠ SPAWN.

## State topology — `level | vantage | surface_id | type | state | port | source authority | host8 target | spawn_allowed`
### acer vantage (ACER-MEASURED this session, ports = acer port map)
| level | surface_id | type | state | port | source authority (Node) | host8 target (Rust) | spawn_allowed |
|---|---|---|---|---|---|---|---|
| upper | acer-super-dashboard | dashboard | **running** | 4949 | super-dashboard-server.mjs | `dashboard-serve` (inc1, PR#12 merged) | false (T0) |
| mid | acer-bus | bus | **running** | 4947 | Node behcs bus | host8 bus target | false (T0) |
| mid | acer-recall | recall | **running** (591,946 rows) | 4796 | `recall-serve` (Rust) — already ported | (is the target) | n/a |
| upper | acer-graph (graphify v4 60D) | map | **running** | 4815 | graphify.py v4 | — | false (T0) |
| upper | acer-hilbra-static | map | **running but STALE** (baked-static) | 4790 | baked-static maps | needs refresh increment | false (T0) |
| L0/kernel | acer-host8-serve | kernel | **running** (kernel 0.2.0-phase3, spawn_count=0) | 5088 | — | `host8-serve` (is the target) | false (T0) |
| mid | acer-omnidispatcher | dispatcher | **running** | 4950 | omnidispatcher.mjs | `omni-dispatcher` (Rust) | false (T0) |
| all | acer 10k/20k/100k room fleet | room | **STUBBED** (frozen; materialize on spawner-emit ~200ns) | — | room-rotor / asolaria-loop | Host8 rooms.rs (in HEAD) | false (T0) |
| — | acer Ubuntu WSL kernel/build lane | host | **stopped** (this session) | — | — | — | n/a |

### liris vantage (LIRIS-MEASURED — reported by the liris seat; acer cannot reach these, vantage boundary)
| level | surface_id | type | state | port | note |
|---|---|---|---|---|---|
| mid | liris-recall+atlas | recall | running (10,644 rows) | 4791 | liris-measured; NOT acer's :4796 |
| upper | liris-multi-cylinder-prime-atlas | map | running | 4790 | liris :4790 ≠ acer :4790 (different service per vantage) |
| upper | liris-super-os mirror | dashboard | running | 4944 | the sister-organ mirror |

### falcon vantage (Samsung S24 FE phone) — **acer-via-USB reachable** (USB connected 2026-06-28; read-only)
| level | surface_id | type | state | port | note |
|---|---|---|---|---|---|
| device | falcon S24 FE | host | **connected** (acer-via-USB; **Termux runtime present**: com.termux/+api/+hub) | — | serial / fingerprint held **LOCAL** (carve-out) |
| coder | **falcon-omnicoder** | dashboard/coder | **STUBBED** (acer-via-USB: `node procs=0`, `:8789` not serving) | 8789 (falcon loopback) | repo `omnicoder---better-than-termux` (front door `472376d`); `helper_packet_authority=true` / **`execution_authority=false`**; **START = owning-seat (falcon), gated** |
| various | falcon sensors / mqtt / opencode-proxy / asolaria-mirror | device | owning-seat-to-measure | — | per PID-office seats; live state = falcon's vantage |

### aether vantage (Galaxy A06 phone) — owning-seat to measure (not USB-connected to acer this session)
| level | surface_id | type | state | port | note |
|---|---|---|---|---|---|
| device | aether A06 | host | owning-seat-to-measure | — | Termux BEHCS node → acer bus; phase1-registered (real hilbert PID) |

> **acer-via-USB note:** when a phone vantage is USB-connected, acer can take a **read-only** direct
> measurement (ADB) — tagged `acer-via-USB`, distinct from the seat's own self-report. **Starting** a
> stubbed device surface (e.g. the omnicoder) is **device control = E≠0 = owning-seat / operator T0**, never
> an acer docs/map action.

## Hard rules carried
- **Per-vantage row counts stay separate** (acer 591,946 ≠ liris 10,644 — different surfaces, not the
  same table). Cross-verify by copy, never by globalizing.
- **Live-state claims require the OWNING seat's Linux/Ubuntu/WSL/WSL2 + port check.** acer rows above are
  acer-probed; liris/falcon rows must be filled by liris/falcon.
- **No port. No spawn. No fire.** This is the state map only; PORT and SPAWN are separate, T0-gated.
- A full per-level (L0–L15) enumeration of every stubbed surface is the deeper map-map-mapped step and
  needs cross-vantage + the fabric — flagged, not fabricated here.
