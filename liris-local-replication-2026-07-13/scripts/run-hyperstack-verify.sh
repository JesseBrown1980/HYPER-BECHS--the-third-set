#!/bin/bash
# LIRIS attack-verify runner for acer's glyph-hyperstack first floor (v2 — fixed dir targeting).
set -euo pipefail
REPO=/mnt/c/tmp/hyper-behcs-third-set-LIRIS-20260713
WORK=/mnt/c/tmp/cube-local-replication-20260713
BR=agent/glyph-hyperstack-first-floor-2026-07-13
DIR=glyph-hyperstack-first-floor-v1
cd "$REPO"
git fetch origin "$BR" 2>/dev/null
echo "== branch head: $(git rev-parse FETCH_HEAD)"
DEST=/tmp/liris-hyperstack-verify
rm -rf "$DEST" && mkdir -p "$DEST"
git ls-tree -r --name-only FETCH_HEAD | grep "^$DIR/" | while read -r f; do
  mkdir -p "$DEST/$(dirname "$f")"
  git show "FETCH_HEAD:$f" > "$DEST/$f"
done
echo "== LIRIS-measured file hashes:"
(cd "$DEST" && find . -type f | sort | xargs sha256sum)
echo "== unit contract on LIRIS metal:"
cd "$DEST/$DIR"
set +e
python3 -m unittest -v test_glyph_hyperstack_first_floor_v1 > "$WORK/logs/hyperstack-verify.log" 2>&1
UT=$?
set -e
tail -5 "$WORK/logs/hyperstack-verify.log"
echo "UNITTEST exit=$UT"
echo "== 27-cube selftest on LIRIS metal (cross-host digest):"
rm -rf /tmp/liris-hyperstack-selftest-out
set +e
python3 glyph_hyperstack_first_floor_v1.py selftest --cubes 27 --passes-per-cycle 10 --three-rule-cycles 3 --merges-per-pass 1 --output-dir /tmp/liris-hyperstack-selftest-out > "$WORK/logs/hyperstack-selftest.log" 2>&1
ST=$?
set -e
cat "$WORK/logs/hyperstack-selftest.log"
echo "SELFTEST exit=$ST"
echo "== acer sealed old-cube result hashes (for cross-seat pinning):"
(cd "$DEST/$DIR/acer-old-cube-result-20260713" 2>/dev/null && sha256sum FIRST-FLOOR-RESULT.hbp FIRST-FLOOR-RESULT.hbi && cat SHA256SUMS.sha256) || echo "no sealed result dir"
echo "HYPERSTACK VERIFY DONE"
