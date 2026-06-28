# P4E agent-readable maps queue

Date: 2026-06-28 - liris-authored candidate - **docs-first / E=0.**

This queues `llms.txt` style maps for the core repos that agents most often need to read first. These
maps are not runtime claims and do not replace each repo's README, MAP, receipts, or owning fabric
routes. They are front-door indexes for future agents so a single vantage does not flatten the system.

## Branches staged for cross-seat attack-verify

| repo | branch | file | role |
|---|---|---|---|
| `asolaria-federation-1024` | `p4e-liris-agent-map` | `llms.txt` | Host8 kernel / Rust target map |
| `Asolaria-hermes-work` | `p4e-liris-agent-map` | `llms.txt` | Hermes fleet, dispatcher, spindle, kernel fleet |
| `N-Nest-Prime-INFINITE-SELF-REFLECT-AGENTS-NESTED` | `p4e-liris-agent-map` | `llms.txt` | root primitive: nested watcher gate |
| `Shannon-and-the-gnns-stage` | `p4e-liris-agent-map` | `llms.txt` | post-trigger proof/scoring stage |
| `Asolaria-the-after-100-billion-run-absorption-and-decomposition-and-cubes` | `p4e-liris-agent-map` | `llms.txt` | after-run absorption, GC, cubes, gated promotion |

## Agent-read rules encoded in every map

- Ask fabric/canon/owning seat before treating repo bytes as system truth.
- Preserve per-vantage port maps and row counts.
- Preserve source/built/running/live/stubbed/fired distinctions.
- Keep `PORT != SPAWN`.
- Keep all hard holds under operator T0.
- Do not publish corpus, keys, PID-office bytes, private root, or PII.

## Attack-verify checklist

- Bytes: recompute each `llms.txt.sha256`.
- Content: verify read order and boundaries match the current front doors.
- PII/secrets: scan both map and sidecar.
- Holds: confirm no runtime action is requested or implied.
- Vantage: confirm live claims are tagged per-seat or omitted.
