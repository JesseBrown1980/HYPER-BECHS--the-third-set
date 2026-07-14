# Wolfram lens / clean white-room cubes — measured CI receipt

**Date:** 2026-07-14  
**Repository:** `JesseBrown1980/HYPER-BECHS--the-third-set`  
**Pull request:** `#32`  
**Tested head:** `f42cd4be24ed81af244a8f18a1f606ff5bc2bad1`  
**Workflow run:** `29303616380`  
**Aggregate job:** `86992558128`  
**Aggregate artifact:** `8299437166`  
**Artifact SHA-256:** `63f7598f963089bfad3ac1c9d8abeb53ecebb63a962ff6851223c95d0fa3b1fa`  
**Receipt-integrity run:** `29303616396` — PASS

## Outcome

The complete lens, reversible-cube, and isolated white-room workflow passed:

```text
Wolfram Data Repository lens                 PASS
Wolfram Function Repository lens             PASS
Wolfram Neural Net Repository lens           PASS

WolframResearch/codeparser cube              PASS
WolframResearch/WolframClientForPython cube  PASS
WolframResearch/QuantumFramework cube        PASS
WolframResearch/LSPServer cube               PASS
WolframResearch/WolframLanguageForJupyter    PASS
DeepMind mathematics_dataset cube            PASS
SymPy cube                                   PASS

independent white-room implementation         PASS
aggregate receipt verification               PASS
receipt integrity                            PASS
```

Registry verdict:

```text
non-reconstructive lens cubes     3
open-license reversible cubes     7
independent white-room build      PASS
invalid receipts                  0
all cube digests verified         true
all reversible restores           true
```

## Non-reconstructive Wolfram service lenses

The three public landing pages were fetched only long enough to compute a shadow. The emitted cubes
contain hashes, factual category/task labels, counts, and coarse histograms. They contain no raw HTML,
paragraphs, examples, code, model weights, or resource payloads.

| Lens | Observed bytes | Categories | Types/tasks | Raw body retained | Expressive text bytes | Source reconstructable |
|---|---:|---:|---:|---|---:|---|
| Wolfram Data Repository | 116,442 | 35 | 10 | no | 0 | no |
| Wolfram Function Repository | 93,536 | 27 | 0 | no | 0 | no |
| Wolfram Neural Net Repository | 236,412 | 5 | 14 | no | 0 | no |

Source-page SHA-256 values:

```text
Wolfram Data Repository
30a3b5a1f8ad28770a9d48c07d38d7ea982d43a106efdc3af653aa16c8d6ccc9

Wolfram Function Repository
202dab111bf0aa53b55986ee8f7d188caec27ac363d319aff32cc257121df377

Wolfram Neural Net Repository
ac5f7e16b7a7d297bef3cff10ca0b780e139124931c0f9d44c263a8b60ac9f80
```

These source hashes identify what the observer saw. The source bodies are not in the cube artifacts.

## Explicit-license reversible cubes

Each source repository was cloned at an exact commit. Its license file was checked and hashed before
any corpus bytes entered the cube. The deterministic selected corpus was then encoded through one,
two, and three BPE/glyph levels; every candidate was completely reversed and SHA-checked.

| Source cube | License | Commit | Corpus bytes | Files | Best level | Catalog | Payload | Total | bpc | Best conventional baseline |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `WolframResearch/codeparser` | MIT | `8c6f94947181884b3d6f14a69857d6a01404d1fc` | 1,000,000 | 67 | 1 | 1,044 | 128,386 | 129,430 | **1.035440** | xz-6, 0.956672 |
| `WolframResearch/WolframClientForPython` | MIT | `a5762a406e75bde042a43b012e895ed5b6249372` | 614,199 | 144 | 2 | 2,074 | 114,091 | 116,165 | **1.513060** | bzip2-9, 1.361748 |
| `WolframResearch/QuantumFramework` | MIT | `ebcccce034e745fd1312f0c7125864c213d1d8e4` | 1,000,000 | 20 | 1 | 1,044 | 158,715 | 159,759 | **1.278072** | xz-6, 1.120736 |
| `WolframResearch/LSPServer` | MIT | `cecb4b310270d39fb7ba05564e5d5ae89d27802d` | 783,871 | 74 | 3 | 3,104 | 128,646 | 131,750 | **1.344609** | xz-6, 1.239837 |
| `WolframResearch/WolframLanguageForJupyter` | MIT | `9a26ac78743cc47084c9c99ff75c5aee2657a409` | 95,711 | 13 | 1 | 1,044 | 25,246 | 26,290 | **2.197449** | xz-6, 1.885677 |
| `google-deepmind/mathematics_dataset` | Apache-2.0 | `427f45075f84b8b9774950196ad63867ca20ffb3` | 272,460 | 43 | 1 | 1,044 | 52,852 | 53,896 | **1.582500** | bzip2-9, 1.414226 |
| `sympy/sympy` | BSD-3-Clause | `15e21aca70f79e9b45e05ac1b474aafd05c919a6` | 1,000,000 | 84 | 2 | 2,074 | 259,002 | 261,076 | **2.088608** | xz-6, 1.882240 |

All 21 level candidates restored byte-identically. The glyph cubes are valid reversible learned
languages, but none beat the strongest same-corpus conventional baseline in this first configuration.
That negative result is preserved.

The reversible package for each source contains:

```text
catalog.bin
payload.zst
license.txt
source-files.json
cube-manifest.json
cube.hbp
SHA256SUMS
```

The transient repository checkout is not retained in the artifact.

## Independent white-room result

The builder received only three aggregate shadow cubes and their functional specifications. It
received no Wolfram Service page body and no third-party source checkout.

```text
observer specifications received       3
source-page bodies received             false
third-party checkouts received          false
unexpected files                        none
test exit code                          0
status                                  PASS
```

Independent implementation SHA-256:

```text
1d00129906ef0342bd76326acced15069c031addabaf2a07a478477d4acb69f7
```

Property-test source SHA-256:

```text
f14054daa654005afb5d23295940dc18fb0bda7efd137d5e32697f6e82afad06
```

The independent builder implemented and tested:

```text
prime-field rank and linear solve
continued-fraction expansion and exact reconstruction
graph-Laplacian spectra
minimal symbolic expression parsing and canonicalization
single- and two-qubit state-vector gates, including a Bell state
LSP Content-Length framing and source line/column mapping
```

Six property-test groups passed.

## What was built

```text
3 non-reconstructive Wolfram service shadow cubes
7 exact reversible open-license mathematical-program cubes
1 independent clean-room mathematical implementation
1 provenance graph joining sources, methods, cubes, and builder
1 aggregate JSON/HBP registry with full digest verification
```

## Interpretation

The service lens demonstrates the narrow operation:

```text
observe
-> measure and classify
-> discard expressive body
-> retain a non-reconstructive shadow
-> independently implement the general method
```

The explicit-license source lane demonstrates a different operation:

```text
clone licensed source at a pinned commit
-> preserve license and attribution
-> compile selected bytes into an exact reversible cube
-> require byte-identical restoration
```

The distinction is deliberate. A service shadow is non-reconstructive. An open-source cube is
reconstructive and therefore carries its exact license, source, catalog, payload, and restore receipt.

As with the existing Asolaria codec, a small output is never accepted merely because it looks
impressive: the reversible lanes are valid only because the decoder restored every source byte.
