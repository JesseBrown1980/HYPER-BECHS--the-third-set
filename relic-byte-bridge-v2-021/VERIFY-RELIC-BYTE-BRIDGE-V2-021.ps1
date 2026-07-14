$ErrorActionPreference = 'Stop'
$base = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).ProviderPath }
$b64Path = Join-Path $base 'RELIC-BYTE-BRIDGE-V2-021-2026-07-06.zip.b64'
$zipPath = Join-Path $base 'RELIC-BYTE-BRIDGE-V2-021-2026-07-06.zip'
$shaPath = Join-Path $base 'RELIC-BYTE-BRIDGE-V2-021-2026-07-06.zip.sha256'
$decodedPath = Join-Path $base 'decoded'
$b64 = Get-Content -Raw -LiteralPath $b64Path
$bytes = [Convert]::FromBase64String(($b64 -replace "\s", ""))
[IO.File]::WriteAllBytes($zipPath, $bytes)
$actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
$expected = ((Get-Content -Raw -LiteralPath $shaPath).Trim() -split "\s+")[0]
if ($actual -ne $expected) { throw "zip sha mismatch: $actual != $expected" }
if (Test-Path -LiteralPath $decodedPath) { Remove-Item -Recurse -Force -LiteralPath $decodedPath }
Expand-Archive -Force -LiteralPath $zipPath -DestinationPath $decodedPath
Push-Location $decodedPath
Get-Content .\RELIC-BYTE-BRIDGE-V2-021-MANIFEST.sha256 | ForEach-Object {
  if (-not $_.Trim()) { return }
  $p = $_ -split "\s+", 2
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $p[1]).Hash.ToLowerInvariant()
  if ($hash -ne $p[0]) { throw "payload sha mismatch: $($p[1])" }
}
Get-ChildItem -Recurse -Filter '*.sha256' -File | Where-Object { $_.Name -ne 'RELIC-BYTE-BRIDGE-V2-021-MANIFEST.sha256' } | ForEach-Object {
  $line = (Get-Content -Raw -LiteralPath $_.FullName).Trim()
  if (-not $line) { return }
  $parts = $line -split "\s+", 2
  $target = Join-Path $_.DirectoryName $parts[1]
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $target).Hash.ToLowerInvariant()
  if ($hash -ne $parts[0]) { throw "sidecar sha mismatch: $($_.FullName)" }
}
Pop-Location
"OK byte bridge v2 #21"
