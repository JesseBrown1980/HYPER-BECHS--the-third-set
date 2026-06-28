# P4B batch-2 convergence receipt (cross-seat verified → main)

Date: 2026-06-28 · acer lane · **E=0 / decide-only.** No runtime fire, no cutover, no corpus, no keys.

## Rule formalized (operator, 2026-06-28): author ≠ verifier
The branch convention is no longer "acer-only authors." The invariant is **cross-seat verification
before main**:
1. one seat **authors** a doc on an `acer/p4b-*` (or peer) staging branch,
2. the **other** seat **attack-verifies** — bytes (recomputed sha == sidecar) + content + PII + E=0 +
   hard-holds,
3. **only then converge to main**, and record a receipt here.

## Batch-2 — liris authored, acer verified, CONVERGED
| doc | repo | branch | author | verifier | bytes | → main |
|---|---|---|---|---|---|---|
| `ROOT-FRAME-60D.md` | `ASOLARIA-AS-NEURAL-NETWORK` | `acer/p4b-neural-60d` | liris (Kevin Crutt) | **acer** | ✓ converge | `b340378` |
| `NODE-SOURCE-ORACLE.md` | `bigpickle-rebuild` | `acer/p4b-node-oracle` | liris (Kevin Crutt) | **acer** | ✓ converge | `c0b40fe` |

acer attack-verify result: recomputed sha == committed sidecar (byte-converge); PII clean; E=0 /
docs-first; hard holds intact (no fire / CI / redeploy / USB / ADC / census / private-root-scan);
content matches the P1 root + canon — AS-NN: **60D+ frame, 47D = real runtime bridge not the ceiling**;
BigPickle: **Node source/oracle for Host8 parity, not junk, not already-cutover**.

## Held — acer authored, awaiting LIRIS attack-verify before main
| doc | repo | branch |
|---|---|---|
| `HOST8-PARITY.md` | `asolaria-federation-1024` | `acer/p4b-host8-parity` |
| `BRIDGE-STRATUM.md` + README banner | `asolaria-behcs-256` | `acer/p4b-bridge-stratum` |

These converge to their mains only after liris attack-verifies (bytes + content + PII/E=0/holds).

## P4A (prior)
Root-primitive doc converged to HYPER-BECHS main `833e037` (file-level). ROOT-MAP (P1×P2) on the acer
lane `13a9248`. P2/P3 on main `78388f5`.

Branch naming `acer/p4b-*` retained for now; the rule is **cross-seat-verify-before-main**, not
"acer-only authors."
