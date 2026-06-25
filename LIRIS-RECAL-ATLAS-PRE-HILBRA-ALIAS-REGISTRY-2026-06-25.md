# Liris RECAL Atlas / Pre-Hilbra Alias Registry

**Date:** 2026-06-25  
**Branch:** `liris`  
**Purpose:** keep Liris-side RECAL / Atlas / Hilbra vocabulary from being misread as missing just because exact local search aliases are not indexed yet.

## Evidence Tags

- `MEASURED_LIRIS`: measured directly on this Liris seat.
- `OPERATOR_OBSERVED`: operator-sourced naming / meaning that must not be deflated by exact-search gaps.
- `CANON`: published architecture/canon mapping that still requires the fabric/council lane for promotion.
- `UNVERIFIED`: not yet materialized into the live RECAL index.

## Live Surface

- `MEASURED_LIRIS`: `http://127.0.0.1:4791/` returns the page title **Asolaria Recall + Atlas**.
- `MEASURED_LIRIS`: page subtitle says "liris measured recall surface beside the live atlas server."
- `MEASURED_LIRIS`: local summary on the page reports `rows=10644`, `seek=3/3`, `sig=287`, `text=8229`.
- `MEASURED_LIRIS`: the page links the 3D atlas surfaces at `:4790` (`acer-multi-cylinder-atlas.html`, `acer-scientific-voxel-atlas.html`).
- `OPERATOR_OBSERVED`: this surface is **RECAL Atlas**, basically **pre-Hilbra** locally / the local Hilbra precursor.

## Alias Probe

`MEASURED_LIRIS` from RECAL L9 searches on `:4791`:

| Term | Count | Reading |
|---|---:|---|
| `brown hilbert` | 50 | indexed Brown-Hilbert route vocabulary |
| `hilbert` | 50 | indexed Brown-Hilbert route vocabulary |
| `atlas` | 9 | indexed Atlas vocabulary |
| `registration` | 16 | indexed Registration vocabulary |
| `registration office` | 8 | indexed Registration Office phrase |
| `office` | 21 | indexed office vocabulary |
| `fischer` | 14 | indexed Fischer vocabulary |
| `host8` | 4 | indexed Host-8 vocabulary |
| `omni` | 21 | indexed OMNI vocabulary |

Exact aliases returning `0` on this Liris index are **alias gaps, not absence claims**:

| Operator / migration alias | Local current search count | Target meaning |
|---|---:|---|
| `hilbra` | 0 | alias to RECAL Atlas / pre-Hilbra / Brown-Hilbert communication layer |
| `atlas recall` | 0 | alias to RECAL Atlas |
| `recall` | 0 | alias to RECAL Atlas |
| `construction` | 0 | alias to Construction Yard upgrade sector |
| `construction yard` | 0 | alias to Construction Yard upgrade sector |
| `yard` | 0 | alias to Construction Yard upgrade sector |

## Registry Rows To Add

These rows are the migration instruction for the next RECAL / map update. They do **not** claim the live index has already been mutated.

| Alias | Canonical local surface | Role label | Status |
|---|---|---|---|
| `hilbra` | `http://127.0.0.1:4791/` | local pre-Hilbra / RECAL Atlas pipe-tracking layer | `UNVERIFIED live alias; MAP-REGISTERED` |
| `atlas recall` | `http://127.0.0.1:4791/` | Recall + Atlas combined surface | `UNVERIFIED live alias; MAP-REGISTERED` |
| `recall` | `http://127.0.0.1:4791/` | local recall search/seek surface | `UNVERIFIED live alias; MAP-REGISTERED` |
| `construction` | Construction Yard sector | candidate upgrade / build sector | `UNVERIFIED live alias; MAP-REGISTERED` |
| `construction yard` | Construction Yard sector | candidate upgrade / build sector | `UNVERIFIED live alias; MAP-REGISTERED` |
| `yard` | Construction Yard sector | candidate upgrade / build sector | `UNVERIFIED live alias; MAP-REGISTERED` |

## Guardrail

Do not answer "Hilbra missing" from an exact `hilbra=0` search on Liris. The correct reading is: **Liris has RECAL Atlas live; operator identifies it as local pre-Hilbra; alias rows still need to be registered into the live index/fabric.**
