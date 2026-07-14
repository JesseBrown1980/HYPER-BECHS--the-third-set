# WOLFRAM-LENS-WHITE-ROOM-v1

**Date:** 2026-07-14  
**Mode:** non-reconstructive service lens + open-license reversible source cubes + independent clean-room builds  
**Authority:** research branch only; no live catalog promotion

## Objective

Implement the narrower operation agreed by the operator:

```text
lawfully observe a source
→ extract unprotected facts, methods, interfaces, categories, and measurements
→ retain no expressive service-page body in the lens cube
→ hand a non-expressive specification into a separate white-room builder
→ independently implement and test the method
```

Open-license source repositories are a separate lane. Their exact source bytes may be compiled into
reversible cubes because their license grants the relevant use, modification, and distribution rights
subject to attribution.

## Two cube classes

### 1. `NONRECONSTRUCTIVE_LENS_CUBE`

Used for the public Wolfram Data, Function, and Neural Net Repository landing pages.

The observer records only:

```text
source URL
fetch time
HTTP content type
source byte count and SHA-256
page title
public category/task/type labels
counts and coarse length histograms
link-domain counts
functional capability statements
```

It does **not** persist:

```text
raw HTML
paragraph bodies
examples
notebook code
model weights
resource payloads
full page text
reconstructive token/n-gram sequences
```

The output declares:

```text
raw_body_retained=false
source_reconstructable=false
expressive_text_bytes=0
```

### 2. `OPEN_LICENSE_REVERSIBLE_CUBE`

Used for explicit-license GitHub repositories. Each lane must:

```text
clone and record exact commit
locate and hash the license
verify the expected license family
select a bounded, deterministic source corpus
record every included path and SHA-256
train one-, two-, and three-level reversible glyph cubes
count catalog + payload
restore every corpus byte exactly
run same-corpus lossless baselines
package catalog + payload + attribution + verification receipt
```

The current source set is:

```text
WolframResearch/codeparser                  MIT
WolframResearch/WolframClientForPython      MIT
WolframResearch/QuantumFramework            MIT
WolframResearch/LSPServer                   MIT
WolframResearch/WolframLanguageForJupyter   MIT
google-deepmind/mathematics_dataset         Apache-2.0
sympy/sympy                                 BSD-3-Clause
```

## White-room separation

The build stage receives only:

```text
lens shadow cubes
functional requirements
mathematical input/output contracts
edge cases and test vectors created by the observer
source and license digests
```

It does not receive downloaded Wolfram Service page bodies or cloned third-party source trees.

The first independent builder implements:

```text
prime-field rank/nullity and linear solve
continued-fraction expansion and exact reconstruction
graph Laplacian spectrum
minimal Wolfram-like expression parser/canonicalizer
single- and two-qubit state-vector gates including Bell-state construction
LSP Content-Length framing and line/column mapping
```

These are general mathematical or protocol methods. The builder source is written in this repository
from the specification and tested against independently generated properties and public mathematical
identities.

## Restore and leakage gates

```text
open-source cubes:
  SHA(source corpus) == SHA(restored corpus)

lens cubes:
  raw_body_retained == false
  expressive_text_bytes == 0
  no field contains source paragraphs or code

white-room builder:
  source checkout contains no cloned observer/source tree
  all property tests pass
  deterministic outputs match declared mathematical identities
```

The existing Asolaria doctrine remains binding: a numerical compression claim is valid only after
byte-identical restoration. The prior v0 result was correctly rejected when its decoder failed; the
v0.1 range coder survives because decompression reproduces the input exactly.

## Outputs

```text
lens-*/shadow-cube.json
lens-*/shadow-cube.hbp
lens-*/white-room-spec.json

repo-*/cube-manifest.json
repo-*/cube.hbp
repo-*/catalog.bin
repo-*/payload.zst
repo-*/license.txt
repo-*/source-files.json
repo-*/SHA256SUMS

white-room/implementation.py
white-room/test_white_room.py
white-room/RESULT.json
white-room/RESULT.hbp

aggregate/RESULT.md
aggregate/CUBE-REGISTRY.json
aggregate/CUBE-REGISTRY.hbp
aggregate/PROVENANCE-GRAPH.json
aggregate/SHA256SUMS
```

## Boundary

This pipeline does not claim that a non-reconstructive lens grants permission to download protected
resource payloads. It limits the service-page lane to small, public landing-page metadata and uses
explicit-license or original-license sources for reversible source cubes.
