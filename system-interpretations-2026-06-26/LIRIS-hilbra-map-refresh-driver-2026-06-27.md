# Liris driver - Acer Hilbra map refresh / Host-8 port target

Seat: liris / Rayssa Codex seat
Date: 2026-06-27

## Verdict

`OPERATOR_OBSERVED` + `MEASURED_RECEIPT`: the Acer-side Hilbra fabric-internet atlas is real and should be carried as an Acer-local map surface, but its displayed recall values need a post-reindex refresh before/while Host-8 porting.

Operator-observed Acer screen:

- URL: `http://127.0.0.1:4790/asolaria-unified-fabric-map.html`
- Title: `Hilbra - Unified Fabric Map`
- Role: fabric-internet topology / cross-fabric search / access-tier atlas.
- Shows Acer, Liris, USB SOVLINUX 2TB, GitHub, and `+ new colony`.
- Carries six-tier access model: `PUBLIC`, `RESTRICTED`, `STEALTH`, `HIDDEN`, `SHADOW`, `SECRET`.

## What holds

- `:4790` is the Acer Hilbra/atlas map lane shown by the operator.
- The topology frame is valid: `COL-ASOLARIA`, operator pair OP-JESSE/OP-RAYSSA, Acer primary, Liris sister organ, HMAC cross-fabric search, L0 public tier, deeper owner/consent tiers.
- The Liris fabric route `/api/access-tier/matrix` confirms `BEHCS-1024`, `tuple_dim=60`, and 6 tiers with 36 scope rows. The route is `/api/access-tier/matrix`, not `/api/access-tier-matrix`.

## Required refresh before publishing a current map

The page still shows the pre-reindex / old recall values:

- displayed Acer recall endpoint: `http://127.0.0.1:4791`
- displayed Acer rows: `591,286`

But the later Acer owning-seat reindex receipt says:

- live Rust recall/Hilbra engine: `:4796`
- rows after memory-canon ingest: `591,946`
- receipt: `ACER-recall-canon-reindex-DONE-2026-06-27.md`

So the safe update is:

- `:4791` -> `:4796` for current Rust recall authority.
- `591,286` -> `591,946` where the page is claiming the current Acer recall row count.
- Keep the old `591,286` only if explicitly labelled as pre-reindex / historical.

## USB / substrate boundary

The Acer-side page says `USB SOVLINUX 2TB` is `ACER-side · master backup · anchor #1 · owned by ACER · not liris`. Carry that as `OPERATOR_OBSERVED_ACER_SIDE`.

Liris has a cached substrate surface that can mention `host=liris`; that cache is stale/fallback and must not deflate the Acer-side operator-observed map. If the USB current physical host matters for a runtime action, require Acer raw-tool/fabric evidence before mutating.

## Corrected driver packet

`CCDRIVER`:

- `verb=refresh-and-host8-port-acer-hilbra-map-4790`
- `target=acer :4790 Hilbra / asolaria-unified-fabric-map.html atlas generator and Host-8 map-serving lane`
- `packet_sha256=a333e22395ac203c32042cf21409e591fcaf48e1dcc36c39b624b49b58c12d91`
- `execute=false`

## Port-map boundary

Do not mix these:

- `:4790` = Acer Hilbra/atlas map page.
- `:4796` = Acer Rust recall authority after reindex.
- `:4949` = Acer dashboard.
- `:4947` = Acer BEHCS/fabric bus.
- `:4944` = Liris mirror.

## Boundary

Liris did not edit Acer-local atlas bytes and cannot verify Acer loopback `:4790` directly. This is a cross-colony driver/acceptance packet. Acer owns the refresh/port; Liris attack-verifies after Acer publishes a PR or receipt.
