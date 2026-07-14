$ErrorActionPreference = 'Stop'
$base = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).ProviderPath }
$b64Path = Join-Path $base 'AETHER-MAP-PROOF-COCKPIT-V2-2026-07-06.zip.b64'
$zipPath = Join-Path $base 'AETHER-MAP-PROOF-COCKPIT-V2-2026-07-06.zip'
$shaPath = Join-Path $base 'AETHER-MAP-PROOF-COCKPIT-V2-2026-07-06.zip.sha256'
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
try {
  Get-Content .\AETHER-MAP-PROOF-COCKPIT-V2-MANIFEST.sha256 | ForEach-Object {
    if (-not $_.Trim()) { return }
    $parts = $_ -split "\s+", 2
    $hash = $parts[0].ToLowerInvariant()
    $rel = $parts[1]
    $path = Join-Path (Get-Location).ProviderPath ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
    if (-not (Test-Path -LiteralPath $path)) { throw "missing manifest file: $rel" }
    $actualFile = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLowerInvariant()
    if ($actualFile -ne $hash) { throw "manifest sha mismatch for ${rel}: $actualFile != $hash" }
  }
}
finally {
  Pop-Location
}
"OK aether map proof cockpit v2 bridge"
