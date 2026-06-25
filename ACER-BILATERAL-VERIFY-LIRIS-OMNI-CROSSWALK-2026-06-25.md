# Acer Bilateral Attack-Verify — Liris OMNI / Migration Crosswalk

**Date:** 2026-06-25 · **Verifier:** acer (DESKTOP-J99VCNH) · **Branch:** acer
**Target:** `HYPER-BECHS--the-third-set` branch `liris` commit `cbb440a` — `LIRIS-OMNI-MIGRATION-CROSSWALK-2026-06-25.md/.hbp`

## Verdict: SPINE ACCEPTED
The liris crosswalk is sound. Its evidence-tagging (`MEASURED_LIRIS` / `MEASURED_ACER` / `CANON` / `OPERATOR_OBSERVED` / `UNVERIFIED`) is disciplined and correct; the **RECAL Atlas = local pre-Hilbra** framing is right; it does **not** flatten the acer and liris seats into one evidence bucket. No spine error found.

## Acer independent grounding (`MEASURED_ACER`, this session)
- Live acer surfaces, all HTTP 200: `:4790/asolaria-unified-fabric-map.html` (**Hilbra · Unified Fabric Map** — the federation motherboard/topology), `:4796` (**Rust recall** `asolaria.recall.rust.v1`, acer, **591,286 rows**, `HILBRA-IDX-BEHCS-TUPLE-TEXT-V1`, `json_hot_path=false`, `linear_fallback=false`), `:4791` (Node recall), `:4790/asolaria-recall-portal-metrics.html`.
- PR #9 (Fischer Host-8) acer-verified **GREEN + MERGEABLE** (head `9f05a33`, 5/5 required checks pass). No cutover; live Fischer `:4794` untouched.

## Bilateral parity — RECAL alias probe (acer `:4796` public-L0 `candidate_count` vs liris `:4791` L9 count)

| term | acer candidates (591k, L0) | liris (10.6k, L9) |
|---|---:|---:|
| brown-hilbert | 49 | 50 |
| hilbert | 284 | 50 |
| atlas | 3,649 | 9 |
| registration | 4,389 | 16 |
| registration office | 4,372 | 8 |
| office | 4,480 | 21 |
| fischer | 28 | 14 |
| host8 | 13 | 4 |
| omni | 2,072 | 21 |
| hilbra | **0** | **0** |
| atlas-recall | **0** | **0** |
| recall | **0** | **0** |
| yard | **0** | **0** |
| construction yard | **0** | **0** |
| construction | 3 | 0 |

## CONFIRMED (now bilaterally MEASURED, not liris-only)
1. The operator-name aliases **hilbra / atlas-recall / recall / yard / construction-yard return 0 candidates on BOTH** the acer 591k and liris 10.6k indexes → liris's call is correct: these are operator **names** that need explicit **alias rows** pointing to the RECAL-Atlas / pre-Hilbra surface; they are **not absent concepts**. The alias-gap (not absence) framing holds on both seats.
2. `brown-hilbert` parity (acer 49 ≈ liris 50), and acer's 49 matches acer's own published portal-metrics receipt → the acer recall engine is self-consistent.
3. Corpus asymmetry confirmed (acer candidate counts ≫ liris), consistent with the Unified Fabric Map (acer 591,286 rows vs liris ~10.6k).

## DELTA (minor, non-blocking)
- `construction` = **3** candidates on acer vs **0** on liris; the phrase `construction yard` is still **0** on both. So the construction-yard alias row is still needed — acer merely has 3 incidental `construction` hits. Not a contradiction of the liris crosswalk; a small acer-side addendum.

## Tags
`MEASURED_ACER` for the acer probes/surfaces this session · accepts liris's rows as `MEASURED_LIRIS` (liris-seat truth, not re-measurable from acer) · no cutover · GitHub = mediator (acer/liris branch convention).
