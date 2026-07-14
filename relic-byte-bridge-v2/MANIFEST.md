# Relic Byte Bridge V2

Purpose: preserve original Relic-local receipt bytes for Acer/Liris verification. The earlier text-file bridge on PR #1 is known not to byte-verify because text blobs were reconstructed with different line endings.

Files:
- RELIC-BYTE-BRIDGE-V2-2026-07-06.zip.b64: base64 encoded ZIP of original Relic receipt files.
- RELIC-BYTE-BRIDGE-V2-2026-07-06.zip.sha256: SHA-256 for decoded ZIP bytes.
- RELIC-BYTE-BRIDGE-V2-PAYLOAD-MANIFEST.sha256: SHA-256 manifest for files inside the decoded ZIP.
- VERIFY-RELIC-BYTE-BRIDGE-V2.ps1: PowerShell verifier.

Hashes:
- zip_sha256=e0ec30b85c73d7243f1ad87424a0bd2c47376dc396a86da9113c28b2e2ab6a7d
- payload_manifest_sha256=ddffd920849b079fe5aa7f8b293a2de19a9d3f2734dec6054be60ba51f7683cf

Verification boundary:
- Decode base64 to ZIP.
- Verify decoded ZIP SHA-256.
- Extract ZIP.
- Verify RELIC-BYTE-BRIDGE-V2-MANIFEST.sha256 inside the ZIP.
- Verify each included original .sha256 sidecar.

Queue boundary: #20 remains MEASURED_RELIC_LOCAL / OPERATOR_RELAYED_TO_ACER_LIRIS until Acer/Liris decode and verify this packet.
