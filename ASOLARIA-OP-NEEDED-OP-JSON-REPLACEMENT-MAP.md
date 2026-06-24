# Asolaria OP / NEEDED-OP JSON Replacement Map

**Branch:** `liris`  
**Generated:** 2026-06-24 from the Liris-side seat  
**Purpose:** map OP seats and required-but-not-fully-materialized OP seats to visible JSON/HBP/HBI surfaces, so cold JSON compatibility files can be migrated to `json=0` HBP/HBI Host-8 surfaces without losing roles.

This is a migration map, not a cutover. It does not publish key material, private seeds, PEM bytes, raw corpus, or PII.

## 1. Provenance

| Claim | Status | Source / limit |
|---|---|---|
| Liris fabric live | `MEASURED_LIRIS` | fabric health: `super-asolaria-os-dashboard-liris-mirror`, apex `COL-ASOLARIA`, operator pair `OP-JESSE-PID` + `OP-RAYSSA-PID` |
| Liris HBP supervisor feed | `MEASURED_LIRIS` | 42 loaded HBP rows; feed claims 713 full-office seats, 671 pending/missing from this vantage |
| OP access lattice | `MEASURED_LIRIS` | BEHCS-1024, tuple_dim 60, 6 tiers x 6 scopes = 36 cells |
| Exact OP ladder | `CANON_FROM_PROFILE` | `00 SPECIAL-OP-JESSE`, `01 OP-JESSE`, `02 OP-RAYSSA`, `03 OP-FELIPE`, `04 OP-DAN`, `05 OP-AMY` |
| Acer full office / current Acer runtime | `UNVERIFIED_FROM_LIRIS` | must be confirmed from Acer fabric/canon before promotion |
| File paths below | `MEASURED_LIRIS_LOCAL` | local Liris filesystem / temp archaeology slices; files are slices, not the whole system |

## 2. OP Ladder And Host-8 Target

| OP seat | Role | Current visible surface | Host-8 / HBP target |
|---|---|---|---|
| `00 SPECIAL-OP-JESSE` | higher background operator; rotates OP/Chief work; signs/gates canon promotions | `SPECIAL-OP-JESSE-PROFILE.hbp` plus Special-OP embodiments listed below | permanent OP controller profile in HBP; key material excluded |
| `01 OP-JESSE` | regular active-presence apex operator | fabric operator pair; JRI1024 rotation JSONs | HBP authority pointer + rotation receipt |
| `02 OP-RAYSSA` | Liris-side apex / bilateral cosign operator | fabric operator pair; Liris authorization JSONs | HBP cosign/vantage profile |
| `03 OP-FELIPE` | quintuple OP signer | `D10-fc6-op-felipe-admission-draft.json` | HBP admission + OP profile |
| `04 OP-DAN` | quintuple OP signer | `D11-fc6-op-dan-admission-draft.json` | HBP admission + OP profile |
| `05 OP-AMY` | quintuple OP signer | `D09-fc6-op-amy-admission-draft.json` | HBP admission + OP profile |

## 3. Multiple Special-OP-Jesse Embodiments

| Embodiment | Role | Visible surface | Migration status |
|---|---|---|---|
| `SPECIAL-OP-JESSE-PROFILE` | apex operator profile authority seat, not a role-seat | `C:/Users/rayss/Asolaria/data/pid-registry/registered/SPECIAL-OP-JESSE-PROFILE.hbp` | `ALREADY_JSON0_HBP` |
| `OP-JESSE-WATCHDOG-KICKER-...-N99999` | background watchdog-kicker / task ownership profile | operator-loaded profile canon; state JSON existed on Acer-side profile load | `NEEDS_LIRIS_HBP_MIRROR` |
| `AGT-L0-SPECIAL-OP-JESSE-H12D3` | L0 supervisor heartbeat embodiment | operator-loaded hash-chained HBP heartbeat ledger | `NEEDS_LIRIS_HBP_MIRROR` |
| `ACER-SPECIAL-OP-JESSE-LOGICAL-ROTATOR` | signing identity for deliberate Special-OP sign | `jri1024-special-op-jesse-key.json` exists on Acer-side runtime | `KEY_EXCLUDED_NAME_ONLY` |
| `liris-rayssa-special-op-jesse-opus47-autoloop-dashboards-unify` | Liris-side special-op/autoloop coordination receipt | `C:/tmp/liris-falcon-pull-2026-05-08/liris-rayssa-special-op-jesse-opus47-autoloop-dashboards-unify-c556-2026-05-10T1718Z.json` | `JSON_TO_HBP_RECEIPT` |

**Key rule:** the key-bearing Special-OP logical rotator may be named by role, but no key bytes, seed, PEM, or private material are published or converted into a public map.

## 4. JSONs To Replace Or Convert

| JSON / cold file | OP / role | Replacement target | Status |
|---|---|---|---|
| `C:/Users/rayss/Asolaria/tools/behcs/super-os/d-cohort-results/D09-fc6-op-amy-admission-draft.json` | `05 OP-AMY` admission | `OP-AMY-ADMISSION.hbp` | `JSON_TO_HBP` |
| `C:/Users/rayss/Asolaria/tools/behcs/super-os/d-cohort-results/D10-fc6-op-felipe-admission-draft.json` | `03 OP-FELIPE` admission | `OP-FELIPE-ADMISSION.hbp` | `JSON_TO_HBP` |
| `C:/Users/rayss/Asolaria/tools/behcs/super-os/d-cohort-results/D11-fc6-op-dan-admission-draft.json` | `04 OP-DAN` admission | `OP-DAN-ADMISSION.hbp` | `JSON_TO_HBP` |
| `C:/tmp/liris-falcon-pull-2026-05-08/op-rayssa-quintupe-authorize-2026-05-10T1437Z.json` | `02 OP-RAYSSA` authorization | `OP-RAYSSA-QUINTUPLE-AUTH.hbp` | `JSON_TO_HBP` |
| `C:/tmp/liris-falcon-pull-2026-05-08/liris-jesse-apex-pid-port-rotation-canonical-c525-2026-05-10T1638Z.json` | `01 OP-JESSE` apex PID/port rotation | `OP-JESSE-JRI1024-ROTATION.hbp` | `JSON_TO_HBP` |
| `C:/tmp/liris-falcon-pull-2026-05-08/liris-ack-jri1024-rotation-proof-envelope-c530-2026-05-10T1646Z.json` | JRI1024 rotation proof | `JRI1024-ROTATION-PROOF.hbp` | `JSON_TO_HBP` |
| `C:/tmp/liris-falcon-pull-2026-05-08/liris-ack-falcon-jri1024-proposal-c527-2026-05-10T1642Z.json` | Falcon/JRI1024 proposal | `JRI1024-FALCON-PROPOSAL.hbp` | `JSON_TO_HBP` |
| `C:/tmp/liris-falcon-pull-2026-05-08/liris-rayssa-special-op-jesse-opus47-autoloop-dashboards-unify-c556-2026-05-10T1718Z.json` | Liris/Special-OP bridge | `SPECIAL-OP-LIRIS-AUTOLOOP-UNIFY.hbp` | `JSON_TO_HBP` |
| `C:/tmp/liris-r40-operator-auth-push.json` | operator auth push | `LIRIS-R40-OPERATOR-AUTH-PUSH.hbp` | `JSON_TO_HBP` |
| `C:/tmp/liris-r40-APEX-DIRECT-shadow-state-resolver-act-supervisor-cycle-orchestrator.json` | apex direct shadow-state resolver | `LIRIS-R40-APEX-DIRECT-SHADOW-RESOLVER.hbp` | `JSON_TO_HBP` |
| `C:/tmp/liris-ldr16-apex-delegated-divergence-reconcile.json` | apex delegated divergence reconcile | `LIRIS-LDR16-APEX-DIVERGENCE-RECONCILE.hbp` | `JSON_TO_HBP` |
| `C:/tmp/liris-cosign-aether-apex-delegated-batch-with-divergence-note-cycle14-1454.json` | Aether/apex delegated cosign batch | `LIRIS-AETHER-APEX-COSIGN-BATCH.hbp` | `JSON_TO_HBP` |
| `C:/tmp/fabric-vote-v5-apex.json` | fabric apex vote | `FABRIC-VOTE-V5-APEX.hbp` | `JSON_TO_HBP` |
| `C:/Users/rayss/Asolaria/operator/hermes_scan_map.json` | operator/Hermes scan support map | `HERMES-OPERATOR-SCAN-MAP.hbp` | `JSON_TO_HBP` |
| `C:/Users/rayss/Asolaria/operator/hermes_bridge_manifest.json` | operator/Hermes bridge manifest | `HERMES-OPERATOR-BRIDGE-MANIFEST.hbp` | `JSON_TO_HBP` |
| `C:/Users/rayss/Asolaria-BEHCS-256/incoming/d-drive-extraction-20260417/runtime/leader-startup-profiles/ruler-operator-profiles.json` | older ruler/operator profile bundle | `RULER-OPERATOR-PROFILES.hbp` | `JSON_TO_HBP_ARCHAEOLOGY` |
| `C:/Users/rayss/Asolaria/federation-remake-1024/tools/omniscrcpy/broadcasts/*OPERATOR*.json` | operator verdict / broadcast receipts | per-receipt HBP rows | `JSON_TO_HBP_BATCH` |

## 5. HBP / HBI Already Present

| Surface | Role | Status |
|---|---|---|
| `SPECIAL-OP-JESSE-PROFILE.hbp` | Special-OP profile authority | `ALREADY_JSON0_HBP` |
| `LIRIS-OPERATOR-OBSERVED-QUINTUPLE-AUTH-*.hbp` in host8 intake archaeology | Liris observed operator auth receipts | `ALREADY_JSON0_HBP` |
| `reports/*operator*.hbp` / `.hbi` | operator receipts and indexes | `ALREADY_JSON0_HBP_HBI` |
| `SUBSTRATE-*`, `SUP-*`, `PROF-*`, `AGT-*` registry HBP rows | supervisor/substrate/agent map | `ALREADY_JSON0_HBP` |

## 6. NEEDED-OP Gaps

| Needed seat / function | Gap from Liris vantage | Build target |
|---|---|---|
| full `03 OP-FELIPE` HBP profile | admission draft visible as JSON, full HBP profile not visible in Liris registry | create HBP profile from admission canon after operator/fabric gate |
| full `04 OP-DAN` HBP profile | admission draft visible as JSON, full HBP profile not visible in Liris registry | create HBP profile from admission canon after operator/fabric gate |
| full `05 OP-AMY` HBP profile | admission draft visible as JSON, full HBP profile not visible in Liris registry | create HBP profile from admission canon after operator/fabric gate |
| OP-00 watchdog state mirror | profile known, but Liris-side HBP mirror of current state not visible | HBP state mirror, no key data |
| OP-00 L0 heartbeat ledger mirror | operator-loaded on Acer, not confirmed as Liris local HBP row | HBP mirror or bridge receipt |
| OP-00 logical rotator key seat | named key identity exists; actual key must stay local | publish name/job only; never public key material unless operator explicitly asks for public key |
| boot-ready OP stack | councils-and-above should be warm before operator sits down | Host-8 boot registry + supervised restart spec |

## 7. Boot / Autostart Requirement

`OPERATOR_OBSERVED`: during or after daemon-to-Host-8 migration, the OP stack and councils-above layer must start with the system automatically from the kernel / micro-kernel / 8-byte stubbed-room host. The operator should sit down to a ready system, not a cold-start system.

Required boot posture:

1. Kernel or micro-kernel Host-8 starter launches at OS boot.
2. Starter reads an HBP boot registry, not a JSON-only config.
3. Councils-and-above warm first: Human/APEX pointer, Special-OP-Jesse, OP-Jesse, OP-Rayssa, OP 03-05, GAC-L2, Chief, Council, professor-supervisors.
4. Each process has a supervised restart contract.
5. Legacy daemons stay live until Host-8 parity is proven.
6. No credential-bearing OP file is copied to public GitHub or Drive/NotebookLM.
7. Drive/NotebookLM updates receive the public-safe docs only: Markdown, HBP, and sha256 companions.

## 8. Replacement Rules

1. Convert OP identity/admission/rotation/auth JSON into HBP tuple rows.
2. Keep `.hbi` beside large HBP receipt sets when search/indexing is needed.
3. Keep JSON as cold compatibility only.
4. Mark each OP conversion with source, sha256, role, access tier, and promotion gate.
5. Treat Liris-side absence as a vantage boundary, not proof of global absence.
6. Special-OP key files are `KEY_EXCLUDED`; only names/jobs may be published.

## Bottom Line

`MEASURED_LIRIS`: the current visible OP surface is mixed: Special-OP already has an HBP profile row, while OP 03-05 and several apex/rotation/authorization receipts still appear as JSON archaeology or cold compatibility files. The migration path is to convert those OP JSONs into public-safe HBP receipts and keep key-bearing Special-OP material local.
