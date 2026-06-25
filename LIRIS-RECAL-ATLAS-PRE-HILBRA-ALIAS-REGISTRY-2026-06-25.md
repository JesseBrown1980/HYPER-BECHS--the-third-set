# Liris RECAL Atlas / Hilbra-Local Alias Registry

**Date:** 2026-06-25  
**Branch:** `liris`  
**Purpose:** keep Liris-side RECAL / Atlas / Hilbra vocabulary from being misread as missing just because exact local search aliases are not indexed yet. This registry does **not** claim Hilbra is unbuilt. Hilbra / Atlas were literally created; this file maps the Liris-local RECAL+Atlas portal into that built fabric.

## Evidence Tags

- `MEASURED_LIRIS`: measured directly on this Liris seat.
- `OPERATOR_OBSERVED`: operator-sourced naming / meaning that must not be deflated by exact-search gaps.
- `CANON`: published architecture/canon mapping that still requires the fabric/council lane for promotion.
- `UNVERIFIED`: not yet materialized into the live RECAL index.

## Live Surface

- `MEASURED_LIRIS`: `http://127.0.0.1:4791/` returns the page title **Asolaria Recall + Atlas**.
- `MEASURED_LIRIS`: page subtitle says "liris measured recall surface beside the live atlas server."
- `MEASURED_LIRIS`: local summary on the page reports `rows=10644`, `seek=3/3`, `sig=287`, `text=8229`.
- `MEASURED_LIRIS`: the page links the 3D atlas surfaces at `:4790` and the local file-backed atlas under `C:\Users\rayss\Asolaria-ASI-On-Metal-Fabric-and-matrix\reports\`.
- `MEASURED_LIRIS`: `http://127.0.0.1:4790/asolaria-multi-cylinder-v2.html` serves **Asolaria MULTI-CYLINDER Map v2**, with metadata for `81,434` surfaces, `6,112` plotted markers, `1,591` pipes, and anti-flattening child-count/index hashes.
- `MEASURED_LIRIS`: `file:///C:/Users/rayss/Asolaria-ASI-On-Metal-Fabric-and-matrix/reports/acer-scientific-voxel-atlas.html` is **ACER · Scientific 3D Voxel Atlas**: `726` real PIDs plotted at real Brown-Hilbert coordinates, Hilbert band `[892..1642]`, GNN-watched, with a real bus pipe `:4947`.
- `OPERATOR_OBSERVED`: `:4791` is **RECAL Atlas**, basically local/pre-Hilbra in the sense of a local Recall+Atlas portal in the built Hilbra family. It is not evidence that Hilbra is missing or unbuilt.

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
| `hilbra` | 0 | alias to RECAL Atlas / Hilbra-local Brown-Hilbert communication layer |
| `atlas recall` | 0 | alias to RECAL Atlas |
| `recall` | 0 | alias to RECAL Atlas |
| `construction` | 0 | alias to Construction Yard upgrade sector |
| `construction yard` | 0 | alias to Construction Yard upgrade sector |
| `yard` | 0 | alias to Construction Yard upgrade sector |

## Registry Rows To Add

These rows are the migration instruction for the next RECAL / map update. They do **not** claim the live index has already been mutated.

| Alias | Canonical local surface | Role label | Status |
|---|---|---|---|
| `hilbra` | `http://127.0.0.1:4791/` + `http://127.0.0.1:4790/asolaria-multi-cylinder-v2.html` | Hilbra-local RECAL Atlas pipe-tracking layer | `UNVERIFIED live alias; MAP-REGISTERED` |
| `atlas recall` | `http://127.0.0.1:4791/` | Recall + Atlas combined surface | `UNVERIFIED live alias; MAP-REGISTERED` |
| `recall` | `http://127.0.0.1:4791/` | local recall search/seek surface | `UNVERIFIED live alias; MAP-REGISTERED` |
| `construction` | Construction Yard sector | candidate upgrade / build sector | `UNVERIFIED live alias; MAP-REGISTERED` |
| `construction yard` | Construction Yard sector | candidate upgrade / build sector | `UNVERIFIED live alias; MAP-REGISTERED` |
| `yard` | Construction Yard sector | candidate upgrade / build sector | `UNVERIFIED live alias; MAP-REGISTERED` |

## Guardrail

Do not answer "Hilbra missing" from an exact `hilbra=0` search on Liris. The correct reading is: **Hilbra / Atlas are built; Liris has RECAL Atlas live at `:4791` and atlas renderers at `:4790`; alias rows still need to be registered into the live index/fabric.**
