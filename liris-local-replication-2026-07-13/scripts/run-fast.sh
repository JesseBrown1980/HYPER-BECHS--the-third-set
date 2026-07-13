#!/bin/sh
# Cube local replication — fast gates R1-R4 (property tests, sha pins, slice roundtrips)
WORK=/mnt/c/tmp/cube-local-replication-20260713
ART=/mnt/c/tmp/claude-container-cube-artifacts-20260713-LIRIS
GPT=$ART/cube-ab-e8-e100-crosscheck/gpt-crosscheck
FIS=$ART/fischer-bidirectional-10-runner/fischer-codec-v3
cd $WORK && mkdir -p out logs
echo "=== versions"
python3 -VV | tee logs/versions.txt
python3 -c 'import numpy,zstandard;print("numpy",numpy.__version__,"| zstandard",zstandard.__version__)' | tee -a logs/versions.txt
echo "=== R1 BEHCS framed property"
python3 -u $GPT/behcs_ladder_framed_v1.py --property 2>&1 | tee logs/r1-behcs-property.log
echo "R1 exit=$?"
echo "=== R2 Fischer sha pin + property"
sha256sum $FIS/fischer_bidirectional_codec_v3.py | tee logs/r2-fischer-sha.log
python3 -u $FIS/fischer_bidirectional_codec_v3.py property 2>&1 | tee logs/r2-fischer-property.log
echo "R2 exit=$?"
echo "=== R3 selftests"
python3 -u $GPT/catalog_zstd_holdout_v1.py --selftest     2>&1 | tee logs/r3-catalog-selftest.log;    echo "catalog exit=$?"
python3 -u $GPT/multilevel_bpe_zstd_v1.py --selftest      2>&1 | tee logs/r3-multilevel-selftest.log; echo "multilevel exit=$?"
python3 -u $GPT/quant8_corpus_crosscheck_v1.py --selftest 2>&1 | tee logs/r3-quant8-selftest.log;     echo "quant8 exit=$?"
python3 -u $GPT/persistent_order2_curve_v1.py --selftest  2>&1 | tee logs/r3-prior-selftest.log;      echo "prior exit=$?"
echo "=== R4 BEHCS file mode on slices"
python3 -u $GPT/behcs_ladder_framed_v1.py $WORK/corpora/slice-150k.bin 2>&1 | tee logs/r4-behcs-150k.log
python3 -u $GPT/behcs_ladder_framed_v1.py $WORK/corpora/slice-1m.bin   2>&1 | tee logs/r4-behcs-1m.log
echo "=== R5 gate check"
ls $ART/cube-ab-e8-e100-crosscheck/cube-ab-vantage-comint-v1 2>/dev/null || echo "R5 BLOCKED: cube-ab-vantage-comint-v1 inputs not in this artifact set"
echo "=== FAST GATES DONE"
