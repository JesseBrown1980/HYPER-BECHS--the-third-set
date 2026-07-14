#!/bin/bash
# seal_hbi.sh <file.hbp> -> writes <file>.hbi (exact per-row projection) + .sha256 sidecars.
set -euo pipefail
hbp="$1"; hbi="${hbp%.hbp}.hbi"
n=$(wc -l < "$hbp")
{
  echo "HBIHDR|artifact=$(basename "$hbp")|rows=$n|encoding=utf8|newline=LF|offset_unit=utf8_bytes|offset_base=0|row_hash=sha256|json=0"
  off=0; i=0
  while IFS= read -r line; do
    i=$((i+1)); rb=$(printf '%s\n' "$line" | wc -c)
    rsha=$(printf '%s' "$line" | sha256sum | cut -d' ' -f1)
    echo "HBIROW|n=$i|tag=${line%%|*}|offset=$off|bytes=$rb|sha256=$rsha|json=0"
    off=$((off+rb))
  done < "$hbp"
  echo "HBIEND|rows=$i|bytes=$off|json=0"
} > "$hbi"
for f in "$hbp" "$hbi"; do sha256sum "$f" | sed "s| .*| *$(basename "$f")|" > "$f.sha256"; done
echo "sealed: $hbi + sidecars"
