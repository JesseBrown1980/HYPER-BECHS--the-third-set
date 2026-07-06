$ErrorActionPreference = 'Stop'
$b64 = Get-Content -Raw .\RELIC-BYTE-BRIDGE-V2-2026-07-06.zip.b64
$bytes = [Convert]::FromBase64String(($b64 -replace "\s", ""))
[IO.File]::WriteAllBytes('.\RELIC-BYTE-BRIDGE-V2-2026-07-06.zip', $bytes)
$actual = (Get-FileHash -Algorithm SHA256 .\RELIC-BYTE-BRIDGE-V2-2026-07-06.zip).Hash.ToLowerInvariant()
$expected = ((Get-Content -Raw .\RELIC-BYTE-BRIDGE-V2-2026-07-06.zip.sha256).Trim() -split "\s+")[0]
if ($actual -ne $expected) { throw "zip sha mismatch: $actual != $expected" }
Expand-Archive -Force .\RELIC-BYTE-BRIDGE-V2-2026-07-06.zip .\decoded
Push-Location .\decoded
Get-Content .\RELIC-BYTE-BRIDGE-V2-MANIFEST.sha256 | ForEach-Object {
  if (-not $_.Trim()) { return }
  $p = $_ -split "\s+", 2
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $p[1]).Hash.ToLowerInvariant()
  if ($hash -ne $p[0]) { throw "payload sha mismatch: $($p[1])" }
}
Pop-Location
"OK byte bridge v2"
