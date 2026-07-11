# Measured Path 2 and the HyperBEHCS storage substrate — 2026-07-11

## HyperBEHCS role

HyperBEHCS is the tuple/index/receipt substrate beneath the exact recovery and neural-scoring planes:

```text
binary / hash / hex / crypto tokens
  -> HBP/HBI/SHA/HEX sidecars
  -> BEHCS-1024 / HyperBEHCS selectors
  -> spindle/portal routing
  -> HDD/SSD/USB/cloud persistence
```

The measured Path-1/Path-2 work clarifies what each token can and cannot do.

## Path 1 — coordinate against retained content

```text
address = sha256(X)
```

The address is small because the receiving store already contains `X`. It selects and verifies the
retained object; it does not independently encode absent bytes.

## Path 2 — distributed shadows carry the source entropy

```text
S_i = X mod p_i
```

Each CRT shadow is non-injective. A selected set becomes exact only when:

```text
product(p_i) >= source_range
```

The original object need not exist in any one retained store. The shadow set itself carries enough
information for exact recovery.

## DBBH→DBWH readback

The recovered candidate is re-projected through the same substrate views:

```text
P(R(P(X))) = P(X)
```

The white-side SHA, complete cylinder shadows, and frequency shells must equal the black-side
projection. Mismatch or insufficient capacity remains `Held`.

## Storage hierarchy

HyperBEHCS makes durable state independent from GPU residency:

```text
HDD/SSD/USB/cloud:
  cube bodies
  retained content
  CRT shadows
  HBP/HBI/SHA/HEX receipts
  graph ledgers
  queues and archives
  model checkpoints
  cold agents/supervisors

RAM:
  bounded active messages
  compact indexes
  active routes and workers

GPU/accelerator:
  optional trained GNN/LLM tensor inference
```

This is the correct meaning of the hardware reduction. Disk is the authoritative durable memory and
proof tier; it is not a substitute tensor core.

## Pre-Asolaria GNN origin

The GNN sidecars that operate above HyperBEHCS descend from Jesse's AI healthcare assistant. Four
model files match byte-for-byte between healthcare and Asolaria. BigPickle later composes L0/L4,
G1/G2/G3/G4, OmniShannon, deterministic fallback, Fischer, and Hookwall.

## Independent verification

### Claude Fable 5 — operator-supplied third-seat runs

```text
dbbh-coms-quant-prism       rustc 1.97   19/19 green
path2-two-shadow-recovery   rustc 1.97   30/30 green
```

### GPT-5.6 Pro — audit and independent CI execution

GPT-5.6 Pro audited the complete recovery, Q-PRISM, healthcare-GNN, BigPickle, trained-GNN,
Hookwall/Shannon, white-room, cube-mint, Dispatcher, HyperHermes, reductions, algorithms,
HyperBEHCS, and N-Nest chain.

GPT-authored Rust 1.97.0 workflows completed successfully:

```text
Path 1      run 29134408321   exact 19-test assertion PASS
Path 2      run 29134413119   exact 30-test assertion PASS
Q-PRISM 3D run 29134419389   all targets PASS
```

## Claim ledger

- `MEASURED`: exact BEHCS rung, Path-1 recall, Path-2 recovery, DBWH re-projection, HBP/HBI storage
  surfaces, bounded active windows.
- `MEASURED_CLAUDE_FABLE5_THIRD_SEAT`: supplied Rust results.
- `MEASURED_GPT_DIRECTED_GITHUB_ACTIONS`: successful independent Rust CI.
- `AUDITED_GPT_5_6_PRO`: complete cross-repository audit.
- `BOUNDARY`: selectors/addresses do not replace missing entropy; storage does not perform neural
  matrix multiplication.
- `UNVERIFIED`: live Hilbra cross-host Path 2, physical quantum transport, and hardware-enforced
  single-use classical shares.
