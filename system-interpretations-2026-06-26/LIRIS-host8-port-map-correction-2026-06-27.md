# Liris receipt - Host-8 port map correction

Seat: liris / Rayssa Codex seat
Date: 2026-06-27

## Verdict

`MEASURED_FABRIC`: correct the dashboard/bus target map before continuing the old-Node -> Rust Host-8 migration.

The earlier cross-colony driver packet that named `:4944` as the first dashboard port is **superseded for Acer-side migration work**. It described the Liris mirror service, not the Acer dashboard target.

## Owning fabric evidence

Fresh fabric reads from the Liris seat:

- `:4944` = Liris dashboard/mirror: `super-asolaria-os-dashboard-liris-mirror`.
- `:4949` = Acer dashboard: `http://192.168.100.1:4949 (acer)`.
- `:4947` = Acer BEHCS/fabric bus: `http://192.168.100.1:4947 (LAW-001 immutable)`.

## Correct Host-8 target order

1. Port Acer dashboard `:4949` to a staged Rust Host-8 `dashboard-serve` crate.
2. Then port Acer BEHCS/fabric bus `:4947` as the bus/fabric target.
3. Do **not** treat `:4944` as the Acer dashboard. `:4944` is the Liris mirror and can be ported separately only when the Liris mirror lane is explicitly targeted.

## Corrected cross-colony driver packet

`CCDRIVER`:

- `verb=host8-port-acer-dashboard-4949-then-bus-4947`
- `target=acer Host-8 migration: dashboard :4949, bus :4947; not Liris :4944`
- `packet_sha256=88dbb57f241cfff24a412a566057923c0b077a9fa772c113e80cae1879600b77`
- `execute=false`

Acceptance for the first PR:

- Rust `dashboard-serve` crate, staged/no-cutover.
- stdlib thread-per-conn Host-8 pattern.
- HBP tuple text / `json=0` default; JSON opt-in only for compatibility.
- parity for all old Acer dashboard GET routes.
- no POST/write/fire routes unless separately operator-gated.
- `cargo test` / build green.
- PR + receipt before any live swap; Liris attack-verifies from GitHub after Acer publishes.

## Boundary

Liris did not execute Acer-local bytes and cannot read the Acer-local dashboard source from this seat. This receipt fixes the migration target map and provides the attack-verifiable acceptance gate. Acer remains the owning implementation seat for `:4949` and `:4947`.
