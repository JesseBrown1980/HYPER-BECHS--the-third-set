# Liris recall-canon re-index driver packet

Seat: liris / Rayssa Codex seat
Date: 2026-06-27
Scope: canon re-index request after operator/Acer correction: "use recall/Hilbra, not hand pointer counts."

## Verdict

`ACCEPT_WITH_BOUNDARY`: the correct re-index surface is Acer recall/Hilbra (`:4796`) and its builder stack, not `MEMORY.md` pointer counts. Liris cannot execute the Acer re-index from this seat because the owning builder/index files are not present locally and the cross-colony route is read/status/driver-packet only unless OP/Acer executes.

## Evidence

`OPERATOR_OBSERVED` / Acer transcript:
- Acer recall engine is live at `http://127.0.0.1:4796/?v=ka` on Acer.
- Recall summary shown by operator: `591,286` rows, `2,614,638` terms, `23,930,053` postings, `skipped=0`.
- Acer recall stack identified by Acer: `C:/asolaria-acer/recall-atlas/build-acer-recall-index.cjs`, `audit-public-pii.cjs`, `serve-recall*.cjs`, Rust launcher, and `data/ASOLARIA-ACER-RECALL.{hbi,hbp}`.
- Existing Acer index files were reported as built `2026-06-22` and stale relative to canon growth.

`MEASURED_LIRIS_LOCAL`:
- `C:/asolaria-acer/recall-atlas/build-acer-recall-index.cjs` absent on Liris.
- `C:/asolaria-acer/recall-atlas/audit-public-pii.cjs` absent on Liris.
- `C:/asolaria-acer/recall-atlas/data/ASOLARIA-ACER-RECALL.{hbi,hbp}` absent on Liris.
- Liris has only the public/Liris recall serve layer under `Asolaria-ASI-On-Metal-Fabric-and-matrix/tools/recall-atlas/` (`serve-recall.cjs`, `start-recall-liris.ps1`, receipts).

`MEASURED_FABRIC`:
- Liris fabric health: `super-asolaria-os-dashboard-liris-mirror`, port `4944`, `ok=true`.
- Liris fabric canon-index: `427` entries / `134` sections.
- Liris local `127.0.0.1:4796` refused connection; direct LAN probes to Acer `192.168.100.1:4796` and `192.168.100.1:4949` timed out from this seat.
- Cross-colony bridge inventory permits read/status/catalog packets; live exec/write requires OP or explicit cosign.

## Driver packet

`CCDRIVER`:

```text
CCDRIVER|schema=asolaria.cross_colony.driver_packet.v1|ts=2026-06-27T14:16:43.553Z|nonce=10842594-f9d8-4320-95d6-da81e716e6df|target=acer: C:/asolaria-acer/recall-atlas|verb=re-index-canon-via-recall|route=cross-colony GitHub/fabric handoff; Acer executes locally on Linux/WSL lane|risk=exec|authority=OP or Acer seat; Liris proposes only|payload_sha256=f5008d6f1292278051ead53c083184d8aea2046da10db2cf7ddb36aeab236dd2|packet_sha256=b1afe0e96571e4ad02f5e300b00e37fe88aaf4393f79c6f905f792259ba35303|hex16=b1afe0e96571e4ad|bin32=10110001101011111110000011101001|execute=false
CCHBI|key=b1afe0e96571e4ad|offset=0|length=573|sha256=b1afe0e96571e4ad02f5e300b00e37fe88aaf4393f79c6f905f792259ba35303|target=acer: C:/asolaria-acer/recall-atlas|route=cross-colony GitHub/fabric handoff; Acer executes locally on Linux/WSL lane
```

Payload summary:

```text
Back up C:/asolaria-acer/recall-atlas/data/ASOLARIA-ACER-RECALL.{hbi,hbp}; run build-acer-recall-index.cjs over current unified archaeology corpus incl memory canon; run audit-public-pii.cjs; verify :4796 /api/summary rows/terms/postings/skipped and search for recent memory keys; publish carve-out-clean receipt with before/after index mtimes, sizes, counts, PII audit result.
```

## Required Acer execution protocol

1. Back up existing Acer recall index artifacts first:
   - `C:/asolaria-acer/recall-atlas/data/ASOLARIA-ACER-RECALL.hbi`
   - `C:/asolaria-acer/recall-atlas/data/ASOLARIA-ACER-RECALL.hbp`
2. Run the Acer builder from the owning machine / Linux-WSL lane:
   - `C:/asolaria-acer/recall-atlas/build-acer-recall-index.cjs`
3. Re-run the public PII audit:
   - `C:/asolaria-acer/recall-atlas/audit-public-pii.cjs`
4. Verify the running recall surface:
   - `http://127.0.0.1:4796/api/summary`
   - search for recent memory/canon keys that were missing from the old `2026-06-22` index.
5. Publish a carve-out-clean receipt with:
   - before/after `.hbi` and `.hbp` mtimes + sizes
   - row/term/posting/skipped counts
   - PII audit result proving L0 remains PII-free
   - example successful searches for recent canon/memory keys.

## Boundary

`BOUNDARY`: No re-index was executed by Liris. This is a hashed cross-colony driver packet and public handoff. Acer/operator owns the exec step because the builder, data index, and live `:4796` recall surface are Acer-local.

