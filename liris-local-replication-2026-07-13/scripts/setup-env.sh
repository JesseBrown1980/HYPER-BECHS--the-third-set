#!/bin/sh
# Cube local replication — environment probe + drive-as-RAM swap setup
echo "== user: $(whoami)"
echo "== swap before:"
swapon --show
free -h
echo "== rootfs space:"
df -h / | tail -1
echo "== deps:"
python3 -c 'import numpy; print("numpy", numpy.__version__)' 2>&1
for b in zstd xz bzip2 gzip 7z 7zz; do command -v "$b" >/dev/null 2>&1 && echo "have $b" || echo "MISSING $b"; done
python3 -c 'import zstandard; print("py-zstandard", zstandard.__version__)' 2>&1 | head -1
echo "== creating 16G drive-backed swapfile (idempotent):"
if [ ! -f /swapfile-cube ]; then
  fallocate -l 16G /swapfile-cube && chmod 600 /swapfile-cube && mkswap /swapfile-cube
fi
swapon /swapfile-cube 2>&1 || echo "(already active or failed)"
echo "== swap after:"
swapon --show
free -h
