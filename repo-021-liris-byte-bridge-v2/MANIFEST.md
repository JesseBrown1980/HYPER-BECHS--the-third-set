# Repo 021 Liris Byte Bridge V2

Purpose: preserve exact Liris-local #21 report packet bytes for Acer verification. This is not a Relic packet; Relic #21 bytes were not present on the Liris filesystem when this bridge was built.

Repository reviewed: JesseBrown1980/Asolaria-the-full-works-200-nanoseconds-agent-emitter-plus-
Classification: READ_REPORTED_PATCH_RECOMMENDED
Source seat: Liris/Rayssa

Files:
- REPO-021-LIRIS-BYTE-BRIDGE-V2-2026-07-06.zip.b64: base64 encoded ZIP of exact Liris report packet files.
- REPO-021-LIRIS-BYTE-BRIDGE-V2-2026-07-06.zip.sha256: SHA-256 for decoded ZIP bytes.
- REPO-021-LIRIS-BYTE-BRIDGE-V2-PAYLOAD-MANIFEST.sha256: SHA-256 manifest for files inside the decoded ZIP.
- VERIFY-REPO-021-LIRIS-BYTE-BRIDGE-V2.ps1: PowerShell verifier.

Hashes:
- zip_sha256=a481367cac5bbd02e249f665abe853807aeee2da28bd6e986894a9e7395ebae6
- payload_manifest_sha256=4c2ca80e886f0d964cb46a049257ab45c097ff6af156b0faa2e086165cbf8dae

Boundary:
- Liris packet bytes are exact from C:\tmp\jessebrown1980-readme-review-20260706\reports\021_Asolaria-the-full-works-200ns-emitter.*
- Relic #21 packet hashes remain operator-relayed unless Relic publishes its own byte bridge.
- Acer should verify this packet before marking Liris-byte bridge verified for #21.
