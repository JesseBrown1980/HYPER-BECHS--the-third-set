$ErrorActionPreference = 'Stop'
$b64Path = '.\RELIC-BYTE-BRIDGE-V2-2026-07-06.zip.b64'
$zipPath = '.\RELIC-BYTE-BRIDGE-V2-2026-07-06.zip'
$shaPath = '.\RELIC-BYTE-BRIDGE-V2-2026-07-06.zip.sha256'
$b64 = Get-Content -LiteralPath $b64Path -Raw
$bytes = [Convert]::FromBase64String(($b64 -replace "\s", ""))
[IO.File]::WriteAllBytes((Join-Path (Get-Location) $zipPath), $bytes)
$actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
$expected = ((Get-Content -LiteralPath $shaPath -Raw).Trim() -split "\s+")[0]
if ($actual -ne $expected) { throw "zip sha mismatch: $actual != $expected" }
$decoded = '.\decoded'
Expand-Archive -LiteralPath $zipPath -DestinationPath $decoded -Force
Push-Location $decoded
Get-Content -LiteralPath '.\RELIC-BYTE-BRIDGE-V2-MANIFEST.sha256' | ForEach-Object {
  if (-not $_.Trim()) { return }
  $p = $_ -split "\s+", 2
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $p[1]).Hash.ToLowerInvariant()
  if ($hash -ne $p[0]) { throw "payload sha mismatch: $($p[1])" }
}
Pop-Location
"OK byte bridge v2"

