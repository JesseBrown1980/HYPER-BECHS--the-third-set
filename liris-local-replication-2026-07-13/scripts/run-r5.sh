#!/bin/sh
# R5 — Cube A/B vantage verify, inputs restored blob-exact from agent/cube-ab-vantage-comint-2026-07-13
set -e
REPO=/mnt/c/tmp/hyper-behcs-third-set-LIRIS-20260713
ART=/mnt/c/tmp/claude-container-cube-artifacts-20260713-LIRIS
XCK=$ART/cube-ab-e8-e100-crosscheck
GPT=$XCK/gpt-crosscheck
DEST=$XCK/cube-ab-vantage-comint-v1
WORK=/mnt/c/tmp/cube-local-replication-20260713
mkdir -p "$DEST"
cd "$REPO"
for f in ASOLARIA-CUBE-A.json ASOLARIA-CUBE-A.json.sha256 ASOLARIA-CUBE-B.json ASOLARIA-CUBE-B.json.sha256 CUBE-AB-VANTAGE-COMINT-2026-07-13.hbp CUBE-AB-VANTAGE-COMINT-2026-07-13.hbp.sha256 CUBE-AB-VANTAGE-COMINT-SPEC.md CUBE-AB-VANTAGE-COMINT-SPEC.md.sha256; do
  git show "FETCH_HEAD:third-seat-2026-07-12/cube-ab-vantage-comint-v1/$f" > "$DEST/$f"
done
echo "== hash gate:"
cd "$DEST"
sha256sum ASOLARIA-CUBE-A.json ASOLARIA-CUBE-B.json
echo "A must be 0b99a6c864f625f4b808c28adc31fd05140693fa619dc16462c294e06bfc7682"
echo "B must be b23cf246d7e4d671cbbf15ea5001fb5db1b3c31791c92e0b52e4dd1c9d76a5df"
A=$(sha256sum ASOLARIA-CUBE-A.json | cut -d' ' -f1)
B=$(sha256sum ASOLARIA-CUBE-B.json | cut -d' ' -f1)
[ "$A" = "0b99a6c864f625f4b808c28adc31fd05140693fa619dc16462c294e06bfc7682" ] || { echo "A HASH FAIL"; exit 1; }
[ "$B" = "b23cf246d7e4d671cbbf15ea5001fb5db1b3c31791c92e0b52e4dd1c9d76a5df" ] || { echo "B HASH FAIL"; exit 1; }
echo "HASH GATE PASS"
echo "== R5 run:"
cd "$GPT"
python3 cube_ab_vantage_verify_v1.py 2>&1 | tee "$WORK/logs/r5-cubeab-verify.log"
echo "R5 exit=$?"
