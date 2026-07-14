# Relic Colony Onboarding Record

Date: 2026-07-06
Repository: `JesseBrown1980/HYPER-BECHS--the-third-set`
Branch: `relic`
Host name supplied by operator: `Relic`

This is an additive onboarding record for the Relic machine/colony surface. It is carve-out clean: names, roles, structure, boundaries, and next gates only. No keys, secrets, signing material, private topology, operator-only evidence, or PII are included.

## Status

| Field | Value |
|---|---|
| Colony | Relic |
| Host / machine label | Relic |
| Start mode | onboarding candidate |
| Authority state | not promoted, not cut over |
| GitHub surface | branch `relic` |
| Runtime mutation | none |
| Evidence posture | `OPERATOR_OBSERVED` for host name; all integration claims remain `UNVERIFIED` until measured |

## Intent

Relic is being introduced as a new Asolaria colony surface. The initial task is to join the GitHub-mediated coordination layer without disturbing Acer, Liris, existing runtime gates, or live substrate state.

The operator stated that Acer and Liris seats will be informed that Relic is entering as the new colony. This record does not claim Acer/Liris acceptance; it only records the start of Relic onboarding and the gates needed before coordination claims are upgraded.

## Operating boundaries

- No cutover.
- No daemon stop/start.
- No live runtime mutation.
- No credential, key, signing byte, token, seed, private path, or PII publication.
- Treat GitHub as a publication and coordination surface, not the sole authority source.
- Use `MEASURED`, `CANON`, `OPERATOR_OBSERVED`, and `UNVERIFIED` tags for claims.
- Keep original evidence and saved internal data read-only; derived reports must preserve provenance.

## Initial role hypothesis

Relic should begin as a coordination and verification colony, not as an authority seat. Its first useful functions are:

1. Inventory the local Aether/Asolaria repository set on the Relic machine.
2. Run read-only onboarding discovery against local docs, manifests, and saved evidence packs.
3. Produce derived onboarding reports without rewriting original data.
4. Verify OpenCode/API tooling and repository access.
5. Ask Acer/Liris/operator gates before promoting any runtime, substrate, or seat claim.

## Known setup already performed on Relic

- OpenCode CLI installed as `opencode-ai@1.17.13`.
- OpenCode HTTP API validated at `127.0.0.1:4096`.
- Local OpenCode global directive created for Aether/Asolaria data work.
- OpenCode sharing disabled in global config.
- Edit and shell permissions configured as ask-gated.
- GitHub repository access confirmed through the connected GitHub app.

## Onboarding gates

| Gate | Required evidence | Current state |
|---|---|---|
| Identity gate | Operator confirms host label and intended role | `OPERATOR_OBSERVED`: host label `Relic` supplied by operator |
| GitHub gate | Branch and record exist on shared map repo | `MEASURED`: branch `relic`, this file |
| Acer notice | Acer seat acknowledges Relic onboarding | `UNVERIFIED` |
| Liris notice | Liris seat acknowledges Relic onboarding | `UNVERIFIED` |
| Local corpus inventory | Relic inventories local Aether/Asolaria repos and evidence packs without mutation | pending |
| Tooling gate | OpenCode provider auth and model selection configured by operator | pending |
| Runtime gate | Any live daemon/substrate change explicitly authorized | blocked until operator + owning seats approve |

## Next actions

1. Operator notifies Acer and Liris seats that Relic is entering onboarding.
2. Relic performs read-only inventory of `C:\Users\user\asolaria-repos` and local evidence packs.
3. Relic emits a derived onboarding report with source paths, repo remotes, manifests, validation scripts, and unresolved gates.
4. Acer/Liris/operator decide whether Relic gets a persistent branch convention, map files, or additional repo-specific onboarding artifacts.

## Non-claims

This record does not claim that Relic is accepted as an authority seat, that Acer or Liris acknowledged it, that any runtime was migrated, that any daemon was started or stopped, or that any private substrate was scanned.
