$ErrorActionPreference = 'Stop'
$b64Path = '.\REPO-021-LIRIS-BYTE-BRIDGE-V2-2026-07-06.zip.b64'
$zipPath = '.\REPO-021-LIRIS-BYTE-BRIDGE-V2-2026-07-06.zip'
$b64 = Get-Content -Raw -LiteralPath $b64Path
$bytes = [Convert]::FromBase64String(($b64 -replace '\s',''))
[IO.File]::WriteAllBytes($zipPath, $bytes)
$actualZip = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
$expectedZip = ((Get-Content -Raw -LiteralPath '.\REPO-021-LIRIS-BYTE-BRIDGE-V2-2026-07-06.zip.sha256').Trim() -split '\s+', 2)[0].ToLowerInvariant()
if ($actualZip -ne $expectedZip) { throw "zip sha mismatch: $actualZip != $expectedZip" }
$decoded = '.\decoded'
if (Test-Path -LiteralPath $decoded) { Remove-Item -Recurse -Force -LiteralPath $decoded }
Expand-Archive -Force -LiteralPath $zipPath -DestinationPath $decoded
$manifest = Join-Path $decoded 'REPO-021-LIRIS-BYTE-BRIDGE-V2-MANIFEST.sha256'
Get-Content -LiteralPath $manifest | ForEach-Object {
  if (-not $_.Trim()) { return }
  $p = $_ -split '\s+', 2
  $expected = $p[0].ToLowerInvariant()
  $rel = $p[1].Trim()
  $target = Join-Path $decoded $rel
  $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $target).Hash.ToLowerInvariant()
  if ($actual -ne $expected) { throw "payload sha mismatch: $rel $actual != $expected" }
}
Write-Output "OK repo 021 liris byte bridge v2"
