#!/bin/sh
# Cube local replication — deps + swap persistence + corpus slice verification
set -e
R=/mnt/c/tmp/cube-local-replication-20260713
echo "== persist swapfile across distro restarts:"
grep -q swapfile-cube /etc/fstab || echo '/swapfile-cube none swap sw 0 0' >> /etc/fstab
grep swapfile-cube /etc/fstab
echo "== apt deps:"
export DEBIAN_FRONTEND=noninteractive
apt-get install -y -qq zstd p7zip-full python3-pip >/dev/null 2>&1 || apt-get update -qq && apt-get install -y -qq zstd p7zip-full python3-pip >/dev/null
echo "zstd: $(zstd --version 2>&1 | head -1)"
echo "7z:   $(7z i 2>/dev/null | head -2 | tail -1 || echo installed)"
echo "== pip deps (numpy, zstandard):"
pip3 install --break-system-packages -q numpy zstandard 2>&1 | tail -1 || true
python3 -c 'import numpy, zstandard; print("numpy", numpy.__version__, "| py-zstandard", zstandard.__version__)'
echo "== corpus verification:"
cd "$R/corpora"
echo "expected: $(cat enwik8.sha256)"
sha256sum enwik8
head -c 150000 enwik8 > slice-150k.bin
head -c 1000000 enwik8 > slice-1m.bin
sha256sum slice-150k.bin slice-1m.bin
echo "== targets:"
echo "150k must be 3803c167dfeb4a91936ac52011be24639822204896b8d0a4658e0480f0f5dc1f"
echo "1m   must be 369b688978f649681136198fb96db14c1616756260c55fb4b65e9bc049552cad"
echo "e8   must be 2b49720ec4d78c3c9fabaee6e4179a5e997302b3a70029f30f2d582218c024a8"
