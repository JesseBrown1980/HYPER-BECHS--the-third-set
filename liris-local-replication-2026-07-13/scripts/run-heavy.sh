#!/bin/sh
# Cube local replication — heavy battery R6-R13, sequential, receipt-gated
WORK=/mnt/c/tmp/cube-local-replication-20260713
ART=/mnt/c/tmp/claude-container-cube-artifacts-20260713-LIRIS
XCK=$ART/cube-ab-e8-e100-crosscheck
GPT=$XCK/gpt-crosscheck
FIS=$ART/fischer-bidirectional-10-runner/fischer-codec-v3
CMP="python3 $WORK/scripts/compare_json.py"
cd $WORK && mkdir -p out logs

echo "=== R6 catalog zstd holdout ($(date -u +%H:%M:%S))"
python3 -u $GPT/catalog_zstd_holdout_v1.py $WORK/corpora/enwik8 --output $WORK/out/catalog-holdout-read20.local.json > logs/r6-catalog.log 2>&1
echo "R6 run exit=$?"
$CMP $WORK/out/catalog-holdout-read20.local.json $XCK/catalog-holdout-read20.json > logs/r6-catalog-compare.log 2>&1
echo "R6 compare: $(tail -1 logs/r6-catalog-compare.log)"

echo "=== R7 quant8 corpus crosscheck on enwik8 ($(date -u +%H:%M:%S))"
python3 -u $GPT/quant8_corpus_crosscheck_v1.py $WORK/corpora/enwik8 --output $WORK/out/quant8-enwik8-local.json > logs/r7-quant8.log 2>&1
echo "R7 run exit=$?"
$CMP $WORK/out/quant8-enwik8-local.json $XCK/quant8-enwik8.json > logs/r7-quant8-compare.log 2>&1
echo "R7 compare: $(tail -1 logs/r7-quant8-compare.log)"

echo "=== R8 multilevel BPE at 1MB ($(date -u +%H:%M:%S))"
python3 -u $GPT/multilevel_bpe_zstd_v1.py $WORK/corpora/enwik8 --bytes 1000000 --levels 3 --merges 512 --output $WORK/out/multilevel-bpe-enwik8.local.json > logs/r8-multilevel.log 2>&1
echo "R8 run exit=$?"
$CMP $WORK/out/multilevel-bpe-enwik8.local.json $XCK/multilevel-bpe-enwik8.json > logs/r8-multilevel-compare.log 2>&1
echo "R8 compare: $(tail -1 logs/r8-multilevel-compare.log)"

echo "=== R9 persistent order-2 prior curve, 20 reads ($(date -u +%H:%M:%S))"
python3 -u $GPT/persistent_order2_curve_v1.py $WORK/corpora/enwik8 --chunk-bytes 1000000 --reads 20 --offset 0 --checkpoint-every 5 --output $WORK/out/persistent-prior-20.local.json > logs/r9-prior.log 2>&1
echo "R9 run exit=$?"
$CMP $WORK/out/persistent-prior-20.local.json $XCK/persistent-prior-20.json > logs/r9-prior-compare.log 2>&1
echo "R9 compare: $(tail -1 logs/r9-prior-compare.log)"

echo "=== R10 BEHCS framed full enwik8, RAM-heaviest ($(date -u +%H:%M:%S))"
free -h
python3 -u $GPT/behcs_ladder_framed_v1.py $WORK/corpora/enwik8 > logs/r10-behcs-enwik8.log 2>&1
echo "R10 run exit=$?"
cat logs/r10-behcs-enwik8.log
free -h

echo "=== R11 Fischer 10 expert audits at 150k ($(date -u +%H:%M:%S))"
for o in 1 2 3 4 5; do for d in black white; do
  python3 -u $FIS/fischer_bidirectional_codec_v3.py audit $WORK/corpora/enwik8 --bytes 150000 --direction $d --order $o --table-bits 17 --report $WORK/out/audit-$d-o$o.json >> logs/r11-audits.log 2>&1
done; done
echo "R11 runs exit=$?"
for o in 1 2 3 4 5; do for d in black white; do
  echo "== $d-o$o =="; $CMP $WORK/out/audit-$d-o$o.json $FIS/out/expert-audits/$d-o$o.json
done; done > logs/r11-audits-compare.log 2>&1
grep -cE '^MATCH$' logs/r11-audits-compare.log | xargs -I{} echo "R11 compare: {} of 10 MATCH"

echo "=== R12 Fischer bench 150k table_bits=17 ($(date -u +%H:%M:%S))"
python3 -u $FIS/fischer_bidirectional_codec_v3.py bench $WORK/corpora/enwik8 --bytes 150000 --backend zstd --table-bits 17 --output-dir $WORK/out/bench-150k > logs/r12-bench150k.log 2>&1
echo "R12 run exit=$?"
{ $CMP $WORK/out/bench-150k/bench.json $FIS/out/150k/bench.json
  for c in black-sequential black-pyramid white-pyramid blackwhite-pyramid; do
    echo "== $c =="; $CMP $WORK/out/bench-150k/$c.json $FIS/out/150k/$c.json
  done; } > logs/r12-bench150k-compare.log 2>&1
grep -cE '^MATCH$' logs/r12-bench150k-compare.log | xargs -I{} echo "R12 compare: {} of 5 MATCH"

echo "=== R13 Fischer bench 1M table_bits=18 ($(date -u +%H:%M:%S))"
python3 -u $FIS/fischer_bidirectional_codec_v3.py bench $WORK/corpora/enwik8 --bytes 1000000 --backend zstd --table-bits 18 --output-dir $WORK/out/bench-1m > logs/r13-bench1m.log 2>&1
echo "R13 run exit=$?"
{ $CMP $WORK/out/bench-1m/bench.json $FIS/out/1m/bench.json
  for c in black-sequential black-pyramid white-pyramid blackwhite-pyramid; do
    echo "== $c =="; $CMP $WORK/out/bench-1m/$c.json $FIS/out/1m/$c.json
  done; } > logs/r13-bench1m-compare.log 2>&1
grep -cE '^MATCH$' logs/r13-bench1m-compare.log | xargs -I{} echo "R13 compare: {} of 5 MATCH"

echo "=== HEAVY BATTERY DONE ($(date -u +%H:%M:%S))"
