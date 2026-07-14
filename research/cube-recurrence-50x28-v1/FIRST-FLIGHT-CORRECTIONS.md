# Cube recurrence first-flight corrections

The failed workflow conclusions are preserved rather than rewritten as green evidence.

## Flight 1 — source runner defects exposed

The first 50-lane aggregate returned all fifty receipts but only seven measured surfaces. It exposed
two deterministic defects:

```text
1. learned token IDs could begin below 256 on ASCII-heavy corpora;
   transformed raw bytes then collided with learned glyph IDs

2. the MIT gate required the literal heading "MIT License";
   canonical grants containing all operative MIT clauses but no heading were held
```

Neither problem invalidated the source data. Both were correctly held by the exact restore/license
gates.

## Corrective implementation

`cube_recurrence_50x28_v2.py` now:

```text
reserves byte IDs 0..255 for every source
starts every learned glyph at ID 256
rebuilds the base catalog under that fixed alphabet
recognizes the complete canonical MIT grant by its operative clauses
retains UNKNOWN for sources that still lack an allowlisted license
```

## Flight 2 — corrected measured bodies

The corrected aggregate returned:

```text
50 base-cube receipts
49 MEASURED cubes
1 HELD_MISSING_PRIVATE_INPUT
1,372 exact/predictive perspective rows
20 maximum overlapping runners
0 invalid receipts
```

Every one of the eight reconstructive perspectives restored on every measured cube. Every one of the
forty-nine ten-pass recurrence lanes restored and state-matched. The aggregate data itself passed its
SHA checks. The workflow conclusion still recorded a CI failure outside the aggregate evidence, so it
is not promoted as the final green seat. A clean new-head execution is required before merge.

This document triggers that clean execution while preserving both prior attempts as development
evidence.
