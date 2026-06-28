# P4C Shannon-style proof receipt template

Date: 2026-06-28 - liris-authored candidate - **docs-first / E=0.**

Use this template for high Asolaria claims before a repo, map, bridge, dashboard, kernel, fabric,
agent, or external-comparison statement is treated as converged. The template is "Shannon-style"
because it separates claim, proof, non-proof, authorization, and residual risk before a verifier sees
the statement.

This is a documentation standard only. It does not fire agents, port dashboards, redeploy `:5088`, run
CI, enumerate USB-SOVLINUX, open 35TB ADC, live-census agents, or scan private root.

## Receipt shape

```text
RECEIPT|id=<stable-id>|date=<YYYY-MM-DD>|author_seat=<acer|liris|falcon|gemini|...>|verifier_seat=<pending>

CLAIM|text=<one concrete claim, no stacked claims>
CLAIM_SCOPE|level=<L0-L15|repo|runtime|substrate|bridge>|vantage=<acer|liris|falcon|global-if-proven>|state=<SOURCE|BUILT|RUNNING|LIVE_FIRED|STUBBED|HELD|DESIGN>

INPUTS|surface=<fabric|canon|repo|port|wsL|usb|drive|operator_screen|github>|class=<MEASURED|CANON|SYSTEM_AFFIRMED|OPERATOR_OBSERVED|UNVERIFIED|DESIGN>|detail=<exact route/path/ref>
INPUTS|surface=<repeat as needed>|class=<...>|detail=<...>

ACTION_BOUNDARY|E=0|no_fire=true|no_cutover=true|no_spawn=true|no_private_root=true|hard_holds=<list>

PROOF_BYTES_OR_ROUTE|type=<sha256|git_sha|port_probe|fabric_tuple|sidecar|operator_screen>|value=<hash/ref/route>|how_to_recompute=<short command or route>
PROOF_BYTES_OR_ROUTE|type=<repeat as needed>|value=<...>|how_to_recompute=<...>

NON_PROOF_CAVEAT|text=<what this does NOT prove>
VANTAGE_BOUNDARY|text=<which seat can/cannot see this>
AUTHORIZATION|state=<docs_only|operator_T0_required|quintuple_required|peer_verify_required>|who=<operator/seat>

ATTACK_VERIFY|bytes=<pending|pass|fail>|content=<pending|pass|fail>|pii=<pending|pass|fail>|holds=<pending|pass|fail>|verifier=<seat>
RESULT|status=<CANDIDATE|ACCEPTED_BY_VERIFIER|REJECTED_BUFFER|CONVERGED>|main_ref=<if converged>
```

## Required rules

- One receipt, one primary claim. Split stacked claims.
- Always state the **state**: source, built, running, live/fired, stubbed, held, or design.
- Always state the **vantage**. Loopback ports are never federation-global by default.
- A GitHub file is a publication/mediator slice; it is not the system.
- A dashboard can be stubbed or running, like a room. `PORT != SPAWN`.
- Counts must preserve strata: live process, registered PID, supervisor, hierarchy, logical address,
  route capacity, storage/cube/catalog.
- Security/key claims must ground impact before severity.
- JSON is acceptable for validation scaffolding; Asolaria hot-path claims should prefer HBP/HBI or
  tuple text where the owning surface supports it.
- Hard holds remain hard holds until operator T0.

## Minimal markdown receipt form

```md
# <claim title>

Date: <date> - <author seat> - E=0 / docs-only

## Claim
<one claim>

## Scope
- level:
- vantage:
- state:
- repo/runtime/substrate:

## Inputs
| class | surface | exact ref | note |
|---|---|---|---|
| MEASURED |  |  |  |
| CANON |  |  |  |

## Proof bytes / routes
| type | value | recompute |
|---|---|---|
| git sha |  |  |
| sha256 |  |  |
| route |  |  |

## Non-proof caveats
- This does not prove:
- This seat cannot see:

## Hard holds
No runtime fire; no dashboard port; no agent spawn; no `:5088` redeploy; no 1.81 CI; no
USB-SOVLINUX enum; no 35TB ADC; no live census; no private-root scan.

## Attack verify
- bytes:
- content:
- PII/secrets:
- E=0/holds:
- verifier:
- result:
```

## Where this applies next

Use this for P4C/P4E receipts, dashboard/room maps, Host8 parity claims, bridge-stratum front doors,
Hermes/Shannon comparisons, and any future proof handoff to Gemini/falcon/acer.
