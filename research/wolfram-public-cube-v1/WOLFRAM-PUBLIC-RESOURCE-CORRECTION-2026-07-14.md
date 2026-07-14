# Wolfram public-resource correction — 2026-07-14

## Correction

The earlier Hutter cube-swarm treated `wolf ram` as an unidentified private input. The operator has
clarified that this means **Wolfram**: public mathematical datasets, programs, functions, models, and
computational resources.

That correction is accepted. The historical swarm receipt remains immutable; this addendum changes
the forward intake plan.

## What is public

Official Wolfram resources include:

```text
Wolfram Data Repository
  public computable datasets across mathematics, geometry, statistics, text, images,
  machine learning, physical science, engineering, and many other categories

Wolfram Function Repository
  public contributed Wolfram Language functions for symbolic, numeric, mathematical,
  data, graph, text, geometry, and machine-learning computation

Wolfram Neural Net Repository
  public trained and untrained model resources suitable for evaluation, training,
  visualization, and transfer learning inside the applicable Wolfram/resource licenses

Wolfram Demonstrations and Language documentation
  public mathematical programs, notebooks, formulas, examples, and interactive models

WolframResearch GitHub organization
  public source repositories, many under explicit MIT or other open-source licenses
```

## Critical license boundary

`Publicly accessible` is not automatically the same as `licensed for bulk AI training`.

Wolfram's general Terms of Use, effective 2024-07-29, state that Wolfram Service data may not be used
to train, fine-tune, or update AI models; may not be used to generate AI-training datasets; and may
not be systematically scraped or bulk-downloaded without a separate license. Individual resources
may also carry additional or third-party terms.

Therefore the lawful Asolaria intake is divided into three classes:

### A. Trainable now — explicit open-source license

Source code may be used when its repository contains an explicit compatible license. Verified
examples already found:

```text
WolframResearch/codeparser
  MIT License

WolframResearch/WolframClientForPython
  MIT License

WolframResearch/QuantumFramework
  MIT License
```

Additional WolframResearch repositories will enter the cube swarm only after their exact commit and
license file are hashed and classified.

### B. Discover through Wolfram, train from the original licensed source

The Wolfram Data Repository identifies dataset creators, publishers, citations, and original source
locations. For example, its MNIST resource points to the original MNIST source and creator metadata.
The swarm may use Wolfram as a discovery and provenance layer, then obtain the dataset from its
original source only when that source's license permits the proposed training and redistribution.

### C. Metadata/research only unless separately licensed

The following are indexed but not bulk-trained directly from Wolfram's hosted Service pages:

```text
Wolfram Data Repository service content
Wolfram Function Repository service content
Wolfram Neural Net Repository service content
Wolfram documentation, MathWorld, demonstrations, and Wolfram|Alpha service outputs
```

A resource-specific or commercial training license can move a source from C to A/B.

## New public mathematical-program training surface

The next cube extension will use explicit-license originals, including:

```text
WolframResearch/QuantumFramework       MIT
WolframResearch/codeparser             MIT
WolframResearch/WolframClientForPython MIT
other WolframResearch repositories after license verification

leanprover-community/mathlib4          Apache-2.0
sympy/sympy                            BSD-style
scipy/scipy                            BSD-style
google-deepmind/mathematics_dataset    Apache-2.0
other formal-math/program corpora only after exact license verification
```

This provides the large mathematical-program and generated-math surface the operator intended,
without mislabeling Wolfram Service content as unrestricted training data.

## Cube requirements

Every Wolfram/math cube must carry:

```text
source repository or original dataset URL
exact commit/version/digest
license identifier and license-file digest
attribution
files/bytes actually read
training-corpus digest
reversible cube result
catalog/model bytes
byte-identical restore
same-corpus baselines
redistribution boundary
```

No source enters a merged training cube with `license=UNKNOWN`.

## Status change

```text
old:
  wolf_ram = AMBIGUOUS_NOT_IDENTIFIED

corrected:
  wolfram = IDENTIFIED_PUBLIC_RESOURCE_FAMILY
  wolfram_service_bulk_ai_training = HELD_BY_TERMS_UNLESS_SEPARATELY_LICENSED
  wolfram_open_source_github = TRAINABLE_AFTER_PER_REPO_LICENSE_GATE
  wolfram_discovered_original_datasets = TRAINABLE_AFTER_ORIGINAL_LICENSE_GATE
```
