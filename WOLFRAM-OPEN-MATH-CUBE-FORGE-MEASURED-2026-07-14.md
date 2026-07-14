# Wolfram open-math cube forge - measured receipt

**Date:** 2026-07-14  
**Repository:** `JesseBrown1980/HYPER-BECHS--the-third-set`  
**Pull request:** `#31`  
**Tested head:** `d96ae782f1984bfbd072ba99fa55fc7ce3bac3b4`  
**Workflow run:** `29302445380`  
**Aggregate artifact:** `8299021174`  
**Aggregate artifact SHA-256:** `defcddc114c0b8d7907ed36d11f67d4c1cd78d50baa47e1b44a5c908acd1395b`  
**Receipt-integrity run:** `29302445381` - PASS

## Outcome

```text
requested cube lanes             20
returned cube lanes              20
maximum concurrent runners       20
MEASURED lanes                    20
invalid cube receipts              0
winning-cube restore failures      0
license-held lane failures         0
```

Every lane completed source cloning, commit pinning, license classification, exact framed-corpus
construction, one/two/three-level reversible glyph-cube training, independent decoder restoration,
per-file re-extraction, same-corpus codec baselines, method-shadow generation, and artifact sealing.

The cubes are typed as:

```text
LEARNED_CODEBOOK_PLUS_EXACT_REPRESENTATION
source_reconstructable = 1
byte_exact_restore     = 1
executable_agent       = 0
```

They are passive source/codebook artifacts, not autonomous agents.

## License and provenance gate

Across repeated source appearances in individual, combined, and bridge lanes:

```text
MIT            32
Apache-2.0      1
OWNER-SOURCE    2
UNKNOWN         0 accepted
```

Each WolframResearch source was pinned to an exact public commit and carried its detected license-file
digest. Unknown or unsupported licenses would have been held. No Wolfram cloud/service content was
scraped.

## Exact repositories and commits

```text
WolframResearch/WolframLanguageForJupyter        9a26ac78743cc47084c9c99ff75c5aee2657a409  MIT
WolframResearch/WolframClientForPython           a5762a406e75bde042a43b012e895ed5b6249372  MIT
WolframResearch/codeparser                       8c6f94947181884b3d6f14a69857d6a01404d1fc  MIT
WolframResearch/Chatbook                         acafd5ed5bba6e340007bf503b8e086697afa796  MIT
WolframResearch/WolframWebEngineForPython        d1bdd91d8b754d1996ed8ca1949a2fa889344931  MIT
WolframResearch/AgentTools                       e75c126c0f0d6da53993dd5bfe78f0e7811172c9  MIT
WolframResearch/codeinspector                    3f1d5935b9b81c61bf92b78cd0dc68044abe13d7  MIT
WolframResearch/wolfram-notebook-embedder        a335c6c871fe1cbcd8d446df5ea22a5d86bac375  MIT
WolframResearch/LSPServer                        cecb4b310270d39fb7ba05564e5d5ae89d27802d  MIT
WolframResearch/codeformatter                    023922634ebf3ac93d35baacad54208b4fbaaa0d  MIT
WolframResearch/LibraryLinkUtilities             e258c2a65bab5a1e9d0776e52dde6ea72edf7ef4  MIT
WolframResearch/AWSLambda-WolframLanguage        c85d96b8625c5935b3bffe094cc456fd0b477ab2  MIT
WolframResearch/GurobiLink                       928dff1fab5e44573612570deb2dc6860e33d8ac  MIT
WolframResearch/Sublime-WolframLanguage          4a79a5e607c9467dd90e57fd5b209f0487ce6f9a  MIT
WolframResearch/WL-FunctionCompile-CI-Template   d130d1fef06f0597a2e81987140fd21eedb4dd3f  MIT
WolframResearch/QuantumFramework                 ebcccce034e745fd1312f0c7125864c213d1d8e4  MIT
WolframResearch/vscode-wolfram                   c864d4d7bebf0df7310710e090541f88eac8070f  MIT
WolframResearch/wolfram-library-link-rs          ef96e6d87e2a0985ee2e69f44e21ea98da027bbb  Apache-2.0
```

## Reversible cube results

Every row below restored its framed corpus and every framed source file byte-identically.
`Cube bpc` includes the serialized model/catalog plus compressed payload.

| Lane | Corpus bytes | Files | Best level | Cube bpc | Best same-corpus baseline | Delta vs baseline | Restore |
|---|---:|---:|---:|---:|---|---:|---|
| LibraryLink Rust | 1,000,000 | 27 | 1 | **0.548896** | xz 0.494912 | +10.91% | PASS |
| codeparser | 1,000,000 | 47 | 1 | **0.976880** | xz 0.884096 | +10.49% | PASS |
| Chatbook | 1,000,000 | 33 | 2 | **1.203432** | bzip2 1.094256 | +9.98% | PASS |
| AgentTools | 1,000,000 | 107 | 2 | **1.241768** | bzip2 1.131736 | +9.72% | PASS |
| LibraryLinkUtilities | 1,000,000 | 135 | 1 | **1.398752** | xz 1.233952 | +13.36% | PASS |
| codeformatter | 704,787 | 62 | 1 | **1.455668** | xz 1.222270 | +19.10% | PASS |
| combined Wolfram open source | 1,000,000 | 105 | 1 | **1.466416** | xz 1.302336 | +12.60% | PASS |
| codeinspector | 1,000,000 | 58 | 1 | **1.507224** | xz 1.348672 | +11.76% | PASS |
| LSPServer | 1,000,000 | 83 | 1 | **1.660840** | xz 1.450240 | +14.52% | PASS |
| Python client | 657,769 | 159 | 1 | **1.666409** | xz 1.490177 | +11.83% | PASS |
| Wolfram-Asolaria bridge | 728,615 | 77 | 1 | **1.690363** | xz 1.479190 | +14.28% | PASS |
| VS Code client | 770,279 | 42 | 1 | **1.704702** | xz 1.459212 | +16.82% | PASS |
| QuantumFramework | 1,000,000 | 78 | 1 | **2.045760** | xz 1.825632 | +12.06% | PASS |
| GurobiLink | 80,435 | 9 | 1 | **2.080885** | xz 1.636303 | +27.17% | PASS |
| AWS Lambda | 100,763 | 19 | 1 | **2.081717** | xz 1.672360 | +24.48% | PASS |
| Jupyter | 114,339 | 15 | 1 | **2.189069** | xz 1.767656 | +23.84% | PASS |
| notebook embedder | 221,840 | 34 | 1 | **2.513812** | xz 2.103714 | +19.49% | PASS |
| WebEngine Python | 62,171 | 43 | 1 | **2.574705** | xz 1.972367 | +30.54% | PASS |
| Sublime language support | 54,421 | 24 | 1 | **2.680583** | xz 1.953364 | +37.23% | PASS |
| FunctionCompile template | 21,153 | 6 | 1 | **3.888999** | xz 2.499125 | +55.61% | PASS |

The reversible cube did not beat the strongest conventional codec on any lane. That is a useful
negative result: the first value of these cubes is exact learned language, source archaeology,
cross-cube reuse, and White-Room method extraction - not standalone compression leadership.

## Shared method cube

The aggregate minted a separate, explicitly non-reconstructive method cube:

```text
source cubes                   20
minimum occurrence threshold    6 cubes
shared symbols                 189
SHA-256
b2aee01cca34e280856c07a02488b1e2e4d7dfd1ef0feab42c2b76f5df9aa8d6
```

High-coverage symbols included `Function`, `Wolfram`, `True`, `False`, `Language`, `Module`,
`String`, `Association`, `Block`, `Infinity`, `Integer`, `Needs`, `StringQ`, `Symbol`, `Rule`,
`BeginPackage`, `EndPackage`, `Map`, `MatchQ`, and `$Failed`.

This method cube retains symbol counts, formula candidates, identifier edges, and cross-cube overlap.
It cannot reconstruct the original repositories.

## Asolaria integration map

```text
codeparser + codeformatter + codeinspector
  -> parser/AST/source-preservation cube

QuantumFramework
  -> symbolic state/operator/circuit cube
  -> Q-PRISM and N-vantage formula cross-map

AgentTools + Chatbook
  -> tool/agent/OMNIEVENT cube

LibraryLink C++ + Rust
  -> native execution and storage-backed runtime cube

GurobiLink
  -> optimization vocabulary for OmniScheduler admission laws

combined lane + Algorithms-of-Asolaria + HyperBEHCS
  -> first Wolfram-Asolaria White-Room bridge cube
```

## Next tournament

The next measured floor is defined as:

```text
1 parser cube
2 quantum/Q-PRISM cube
3 agent/OMNIEVENT cube
4 native C++/Rust cube
5 optimization/OmniScheduler cube
6 symbolic probability/OmniShannon cube
7 permissively licensed original mathematical datasets
8 deterministic cross-cube encoder law
9 Fischer symbolic expert mixer
10 whole-ledger benchmark
```

Every reconstructive cube must restore exactly. Every shadow must be labeled non-reconstructive.
No source with `license=UNKNOWN` may enter a promoted cube.

## Boundary

These measurements apply to source-code and documentation corpora framed by the forge. They are not
enwik8/enwik9 or Hutter Prize measurements. No Wolfram cloud/service content was ingested. The cube
artifacts are passive exact representations plus learned codebooks, not executable AI agents.
