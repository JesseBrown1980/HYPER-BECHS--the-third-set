# Adversarial second-review — verdicts (read-only)

_16 independent verdicts. Each agent was told to REFUTE/critique. PII the agents quoted from other repos is redacted here._

## [REFUTED] Council responder merged to fed-1024 main and deployment status
- **mode:** refute
- **summary:** The claim is REFUTED on the most material point: the council responder code is NOT merged to fed-1024 main (it resides on acer/council-host8-responder branch, 5+ commits ahead of main). The secondary claim about lack of :5090 deployment is CONFIRMED — no service is running on either :5090 or the legacy :4949 port. The binary exists but remains undeployed with no automation to launch it.
- **findings:**
  - (critical, REAL, MEASURED) Code is NOT merged into fed-1024 main branch — only on acer/council-host8-responder feature branch
  - (high, REAL, MEASURED) No live :5090 service is running — port check via /proc/net/tcp shows zero listeners
  - (high, REAL, MEASURED) No council-serve process active — ps aux shows zero matches, no systemd service registered
  - (high, REAL, MEASURED) No :4949 service running either — neither old wedged service nor new responder are live
  - (medium, REAL, MEASURED) Binary artifact exists but not deployed — /mnt/c/tmp/council-build contains built binary with design intent for :5090, no deployment automation active

## [REFUTED] PR#1 (Harness-edit) and PR#11 (asolaria-federation-1024) are actually MERGED to main
- **mode:** refute
- **summary:** The claim that PR#1 and PR#11 are merged to main in JesseBrown1980/HYPER-BECHS--the-third-set is FALSE. No such PRs exist in this repository. The main branch contains only the init commit; references to "PR#1" and "PR#11" in commit messages refer to pull requests in the liris repository, not GitHub PRs in this repo. Commits mentioning these work items are only on the acer branch, which has 28 commits not on main.
- **findings:**
  - (high, REAL, MEASURED) PR#1 does not exist as a GitHub pull request in this repository
  - (high, REAL, MEASURED) PR#11 does not exist as a GitHub pull request in this repository
  - (high, REAL, MEASURED) main branch contains only 1 commit (init commit 58ecc3d), no merged PRs
  - (high, REAL, MEASURED) Commits referencing PR#1 and PR#11 are on acer branch only, not merged to main
  - (medium, REAL, MEASURED) PR references in commit messages are to 'liris PR#1' and 'liris PR#11' (different repository), not GitHub PRs in HYPER-BECHS repo
  - (high, REAL, MEASURED) acer branch has 28 commits diverged from main (merge-base is init commit), indicating no merge to main has occurred

## [ISSUE_FOUND] PR#11 merge to fed-1024 main / ENGINE unfired claim (auto_fire=false, no cutover, system unchanged)
- **mode:** critique
- **summary:** Claim contains unsubstantiated base assumption (PR#11 merge) + partially accurate technical state. The auto_fire_allowed=false is MEASURED and confirmed across all 17 pending envelopes. However, (1) PR#11 / fed-1024 branch cannot be verified via owning gate (no git evidence, violates heldout law #5); (2) auto_fire.fired=2 shows limited firing DID occur; (3) infrastructure is held/read-only as designed, but this does not prove no cutover attempt occurred post-PR.
- **findings:**
  - (high, REAL, UNVERIFIED) PR#11 merge to fed-1024 main unverified
  - (low, REAL, MEASURED) auto_fire=false confirmed in all 17 pending envelopes (loop_pending measured 2026-06-26T20:30:41Z)
  - (low, REAL, MEASURED) No new process launches detected; infrastructure engines are held/read-only by design per start-asolaria-engines.ps1:6
  - (medium, REAL, MEASURED) auto_fire.fired=2 shows limited firing DID occur in recent loop tick (not zero)
  - (medium, REAL, MEASURED) Cosign chain shows daemon_revival (seq=3566, 2026-06-17) not a cutover; no recent LAW-SLICE-ENGINE or major mints post-PR claim date

## [ISSUE_FOUND] JesseBrown1980/Harness-edit: merged harness critique (apply_edit.py / score_skill.py / rollout_score.py)
- **mode:** critique
- **summary:** The merged harness contains critical API model ID bugs that will cause runtime failures when using live Claude/OpenAI harnesses, plus a baseline duplication bug that breaks the v2 rollout behavior scoring. File I/O error handling is also insufficient. The transcript-mode testing masks these defects.
- **findings:**
  - (critical, REAL, MEASURED) Critical: Invalid Claude model ID 'claude-opus-4-8' as default (rollout_score.py:49)
  - (critical, REAL, MEASURED) Critical: Invalid OpenAI model ID 'gpt-5.5' as default (rollout_score.py:62)
  - (high, REAL, MEASURED) High: Baseline duplication bug — when using --harness claude/codex with --baseline, the exact same prompt+skill is sent twice, producing identical responses and doubling API costs (rollout_score.py:85-86)
  - (high, REAL, MEASURED) High: File write errors in apply_edit.py silently ignored on line 90 — no try-except around Path.write_text(), program returns 1 with no clear error message
  - (medium, REAL, MEASURED) Medium: Rejected-edits buffer file appended without bounds check or atomic writes (apply_edit.py:95-96) — file can grow unbounded and corrupt on mid-write crash
  - (medium, REAL, MEASURED) Medium: Inconsistent JSON format handling — apply_edit.py load_scenarios() unwraps dict with 'scenarios' key, but score_skill.py main() expects direct list; will error on wrapped JSON (score_skill.py:64 vs apply_edit.py:34-35)
  - (medium, REAL, MEASURED) Medium: replace() operation replaces all occurrences, not just first — no way to replace a single instance if the pattern appears multiple times (apply_edit.py:45)
  - (low, REAL, MEASURED) Low: No validation of scenario structure in rollout_score.py — assumes each scenario has 'id', 'prompt', 'rubric' fields but does not validate; missing rubric.apply_any or rubric.fail_any arrays will cause KeyError at runtime
  - (low, REAL, MEASURED) Low: Generic exception handling in rollout_score.py:106-108 provides insufficient context — cannot distinguish between file not found, API failure, and JSON parse error

## [ISSUE_FOUND] Asolaria Migration Scan #1 Completeness - Critical Gaps Analysis
- **mode:** critique
- **summary:** The "migration scan #1 target list" does not exist as a documented artifact. A migration-state scan focused only on claims-gate would catastrophically MISS: (1) 128+ operational subdirectories in /mnt/c/tmp containing ledgers (cosign-chain.ndjson), verdicts, registries, and manifests; (2) D:\safety-backups containing critical COSIGN_CHAIN backups, Falcon APK, BEHCS-1024 mirrors; (3) Five major tool subsystems (usb-raw, behcs, graphify, phone, exfat-writer) with raw disk/USB extraction code; (4) recall-atlas PII audit and indexing subsystem; (5) federation-remake-1024 Rust project with AGENT_ROSTER and AUTHORIZATION ledgers. No .env files or obvious PII/secret exposure detected in spot checks, but the ABSENCE of a target list itself is the critical gap.
- **findings:**
  - (critical, REAL, MEASURED) Migration scan target list does not exist — no documented specification of what repos/subsystems should be migrated
  - (critical, REAL, MEASURED) Operational ledger subsystems in /mnt/c/tmp (128 subdirectories) not in scan scope — cosign-chain.ndjson (multiple versions), council verdicts, liris manifests, registries
  - (critical, REAL, MEASURED) D:\safety-backups subsystem (5GB+ observed, 35TB potential) contains critical COSIGN_CHAIN backups, Falcon APK archives, BEHCS mirrors not in claims-gate scope
  - (high, REAL, MEASURED) Tool subsystems with raw USB/disk access (usb-raw, behcs, phone, exfat-writer) contain extraction and integrity-critical code NOT scanned or inventoried
  - (high, REAL, MEASURED) recall-atlas subsystem (22MB+) with PII audit and indexing — critical for data integrity migration — not documented in scan list
  - (high, REAL, MEASURED) federation-remake-1024 Rust project (second .git repo) contains AGENT_ROSTER and AUTHORIZATION ledgers — critical operational state NOT audited as part of migration target
  - (high, REAL, UNVERIFIED) User prompt mentions '35TB Drive', 'Falcon phone lane', 'hidden-layer/shadow vaults' but no migration target list includes these subsystems
  - (medium, REAL, MEASURED) Stale operational state in /mnt/c/tmp: cosign-chain files dated 2026-05-* (month old by June 26), unclear if live or archived, violates LAW-2 rule: 'missing ≠ clean-zero'
  - (medium, REAL, MEASURED) No centralized schema/inventory document for the full Asolaria system — safety-backups has inventory CSVs but unclear if synchronized with live state or complete
  - (medium, REAL, MEASURED) usb-raw and recall-atlas subsystems actively handle raw disk/USB extraction and PII auditing, but their access controls and migration readiness not verified

## [ISSUE_FOUND] JesseBrown1980/Asolaria-ASI-On-Metal-Fabric-and-matrix pushed reports (HTML/JSON maps)
- **mode:** critique
- **summary:** The pushed HTML/JSON reports in /asolaria-asi-on-metal-fabric contain real PII: Windows hostnames DESKTOP-J99VCNH and DESKTOP-PTSQTIE, and personal names Jesse/Rayssa linked to operators in public JSON/HTML files (asolaria-unified-fabric-map.html). This directly contradicts the ULTRA-PLAN claim No PII/secret pushed and violates the carve-out-clean policy defined in AGENT-BRIEF law #2.
- **findings:**
  - (high, REAL, MEASURED) Real Windows hostnames (DESKTOP-J99VCNH, DESKTOP-PTSQTIE) exposed in public HTML report asolaria-unified-fabric-map.html
  - (high, REAL, MEASURED) Personal names Jesse and Rayssa exposed in public HTML report line 166 linking them to operators
  - (high, REAL, MEASURED) ULTRA-PLAN claim No PII/secret pushed contradicted by actual git commits of reports with PII
  - (medium, REAL, MEASURED) Carve-out-clean policy violated: embedded hostnames and names in JSON data structure
  - (medium, REAL, MEASURED) Physical device identifier USB SOVLINUX 2TB exposed linked to machine and operator

## [ISSUE_FOUND] JesseBrown1980/Harness-edit merged codebase (apply_edit.py, score_skill.py, rollout_score.py on main)
- **mode:** critique
- **summary:** The merged harness code (apply_edit.py, score_skill.py, rollout_score.py) is syntactically correct and passes the documented gate tests (py_compile, v1 scenario coverage, v2 rollout with good/bad transcripts). However, three real defects exist in edge case handling: (1) load_scenarios() can return a dict instead of list, causing downstream crashes; (2) score() crashes on non-string scenario values; (3) empty scenario lists incorrectly pass the gate. Two medium-severity runtime issues exist around missing library imports and malformed baseline transcripts. The merge testing did not exercise these edge cases. No PII/secret exposure detected. Code is READ-ONLY per LAW-1; no modifications made.
- **findings:**
  - (high, REAL, MEASURED) load_scenarios() in apply_edit.py returns dict instead of list for invalid JSON format. When given {'not_scenarios': [...]}, it returns the dict directly instead of raising an error or extracting a list. Downstream score_skill.score() then iterates over dict keys (strings), causing AttributeError: 'str' object has no attribute 'get' when trying to call .get('must_include_any')
  - (high, REAL, MEASURED) score_skill.score() crashes if any scenario's must_include_any or must_not_include contains non-string values (e.g., integers). The norm() function is called on all phrase values, but norm() calls .lower() which fails on non-strings with AttributeError: 'int' object has no attribute 'lower'
  - (medium, REAL, MEASURED) rollout_score.py returns ok=True/verdict='VALIDATION_ACCEPTED' when scenarios list is empty (0 scenarios). Line 112 sets passed=0, total=0, then line 113 evaluates (0 == 0) = True, passing an empty test suite. This is logically incorrect — zero test coverage should not pass.
  - (medium, REAL, MEASURED) rollout_score.py's claude and codex adapters import anthropic/openai at line 43 and 56 respectively without upfront validation. If library is not installed, function crashes with ImportError at runtime instead of failing at argument parse time with a clear 'missing library' message.
  - (low, REAL, MEASURED) apply_edit.py's apply_op() function uses string.replace() for replace and delete operations, which replaces ALL occurrences. No way to replace only the first occurrence of a phrase. This limits the edit interface but is probably intentional for skill documents.
  - (low, REAL, MEASURED) rollout_score.py's --baseline flag requires transcript file to contain entries with '::baseline' suffix (e.g., 'scenario-id::baseline') for transcript harness. This convention is not documented in script docstring or --help output. If transcript lacks baseline entries, script fails with cryptic KeyError.
  - (low, REAL, MEASURED) rollout_score.py does not validate that --transcript file is provided when --harness is 'transcript'. If harness is 'transcript' but --transcript is not given, store remains empty and script fails at runtime with KeyError inside run() instead of upfront validation.
  - (medium, REAL, UNVERIFIED) No gate catches the case where load_scenarios() receives a dict without 'scenarios' key. The merge message shows 'Local gates passed: py_compile, v1 9/9, v2 good 9/9, v2 bad 0/9' but these tests use well-formed JSON (examples/asolaria-scenarios.json). Malformed input isn't tested.

## [CLEAN] JesseBrown1980/asolaria-federation-1024 PR #11 post-merge completeness
- **mode:** critique
- **summary:** PR #11 (council/loop Host-8 responder) merged successfully with owning CI (1.81) passing all 5 gates. The merged council-serve + vote-quorum crates are correctly staged as read-only, gated-closed engine, with no cutover to live :4949/:4952/:4953. Liris + acer cross-seat review caught and fixed CRLF churn and missing-ledger boundary (now explicitly fails on unreadable ledgers vs silent zero-row masquerade). All unit tests pass, no logic defects found, no PII/secrets, state is current and unbroken.
- **findings:**
  - (high, not-real, MEASURED) Owning CI (1.81) pass status
  - (low, not-real, MEASURED) Council-serve HTTP connection limit race condition
  - (medium, not-real, MEASURED) Vote-quorum canon parity correctly masks missing vs empty ledgers
  - (low, not-real, CANON) Development process discipline and cross-seat review
  - (high, not-real, MEASURED) STAGED scope integrity (no fire, no cutover, no auto-launch)

## [CLEAN] JesseBrown1980/asolaria-behcs-256 — Risk Critique for Secret/Key Leaks
- **mode:** critique
- **summary:** The repository is a PUBLIC GitHub documentation set explicitly designed as "carve-out clean" with NO actual private cryptographic keys, API credentials, database passwords, or trust-anchor keys. Git history contains only intentional public email addresses (account holder + collaborator). System constants are marked DESIGN/example-only, not real secrets. The repository complies with stated carve-out policy; no evidence of accidental secret exposure.
- **findings:**
  - (low, not-real, MEASURED) Intentional public email addresses in git history (plasmatoid@gmail.com, kevin.crutt.kc@gmail.com)
  - (critical, not-real, MEASURED) No BEGIN RSA/EC/PGP PRIVATE KEY patterns found in entire repository
  - (critical, not-real, MEASURED) No API keys, OAuth tokens, database passwords, or service-account credentials found
  - (low, not-real, CANON) System constants (GENESIS_PREV, APPENDED_BY_DAEMON, LAW_ANCHOR) are marked DESIGN/example, not trust-anchor keys
  - (low, not-real, CANON) Repository explicitly claims carve-out clean in all maps and ULTRA-PLAN verdict CONFIRMED
  - (medium, REAL, MEASURED) Real inventory gap: missing documentation for 128+ ledger dirs and tool subsystems
  - (critical, not-real, MEASURED) No evidence of accidentally committed secrets with subsequent removal in git history

## [CLEAN] JesseBrown1980/omnicoder---better-than-termux (GitHub Repository)
- **mode:** critique
- **summary:** The repository JesseBrown1980/omnicoder---better-than-termux is CLEAN of any PII exposure in its current state. The repository is completely empty (created 2026-06-25, zero commits, zero files). No secrets or PII were detected in repository content via GitHub API or git history inspection. The owner's GitHub profile does contain public PII (name and location), but this is standard GitHub profile data, not repository-specific exposure. The "PII-laden/HELD" flag cannot be verified against current content since no history exists to determine if PII was previously present and removed. The repository appears to be either a placeholder or newly created empty project awaiting content. No real security issues found in the repository itself.
- **findings:**
  - (low, REAL, MEASURED) Repository is completely empty with no commits or content
  - (low, REAL, MEASURED) Owner's GitHub profile contains public PII (name: Jesse Daniel Brown, location: Sumter SC)
  - (low, REAL, MEASURED) No evidence of previous content or history; cannot verify if flagged PII was remediated or scrubbed
  - (low, REAL, MEASURED) Repository purpose is undefined - name suggests code project but no implementation exists
  - (critical, not-real, MEASURED) No PII, secrets, or sensitive data currently exposed in repository content

## [CLEAN] JesseBrown1980/asolaria-federation-1024 post-PR#11 main: council code CI pass and merged state
- **mode:** critique
- **summary:** PR #11 merged successfully with all 5 owning CI jobs passing. Rust code compiles cleanly. All 17 unit tests pass (10 vote-quorum + 7 council-serve). Voting logic, canon hashing, and missing-ledger error handling are correct. A potential defect (missing ledgers treated as empty) was introduced in commit 0921620 and fixed in f0f0941, now properly tested. No unresolved defects in merged state. Hardcoded Windows path is configurable via env var and does not prevent execution. No PII/secret exposure. Code is properly staged with engine gating, read-only routes, and comprehensive tests.
- **findings:**
  - (medium, not-real, MEASURED) Defect introduced then fixed: missing ledgers initially treated as 0-row success (commit 0921620), corrected in commit f0f0941 to return 500 with ok=0/missing=1
  - (low, not-real, MEASURED) Hardcoded Windows path in DEFAULT_VOTE_DIR ('C:/HyperBEHCS/data/vote-quorum') not ideal for cross-platform but fully configurable via ASOLARIA_VOTE_DIR env var
  - (low, not-real, MEASURED) Operator names hardcoded in QUINTUPLE array (OP-JESSE, OP-RAYSSA, OP-AMY, OP-DAN, OP-FELIPE) visible in public source but not credentials/secrets
  - (low, not-real, UNVERIFIED) Unverified claim: '3321/3321 on the cosign ledger' cited as proven parity but cosign ledger content not inspected
  - (low, REAL, MEASURED) All CI jobs passed and all 17 unit tests pass in merged state: no code defects detected

## [CONFIRMED] Canonical scenario set claim: repo main asolaria-scenarios.json == acer seat heldout-scenarios.json, 10 scenarios, every scenario has law_coverage_any
- **mode:** refute
- **summary:** The claim is confirmed. The canonical scenario set is a single source maintained in examples/asolaria-scenarios.json (repo main) that is byte-identical to heldout-scenarios.json (acer seat). Both files contain exactly 10 scenarios, and every scenario has a law_coverage_any field with regex patterns. File synchronization is enforced through apply_edit.py's validation gate.
- **findings:**
  - (high, not-real, MEASURED) File identity verification
  - (high, not-real, MEASURED) Scenario count (10)
  - (high, not-real, MEASURED) law_coverage_any field present in all 10 scenarios
  - (high, not-real, CANON) Canonical source enforcement via apply_edit.py
  - (high, not-real, MEASURED) Byte-identical synchronization (size 10348, timestamp Jun 26 16:48)

## [CONFIRMED] Claim: NOTHING PII/secret was pushed to the PUBLIC repos this session (Harness-edit, -6-cyl-generator)
- **mode:** refute
- **summary:** Adversarial verification CONFIRMED the claim. Systematic analysis of all pushed files to both public repositories found no hardcoded API keys, tokens, passwords, real user data, PIIs, email addresses, or infrastructure details. Feed data and rendered outputs are properly excluded via .gitignore. API keys are read from environment variables with proper error handling. Test data is entirely fictional and abstract. The repositories explicitly state they contain only public-safe scaffolding code.
- **findings:**
  - (low, not-real, MEASURED) No hardcoded API keys or credentials in Python/JavaScript source code
  - (low, not-real, MEASURED) No actual office feed data files (*.hbp, *.hbi, office-feed.*) committed to repository
  - (low, not-real, MEASURED) No real user PII, email addresses, or identification data in pushed files
  - (low, not-real, MEASURED) No exposed IP addresses, server names, or infrastructure details in committed code
  - (low, not-real, MEASURED) Test data (transcripts, scenarios) is entirely fictional/synthetic with abstract references
  - (low, not-real, MEASURED) .gitignore properly configured to block sensitive file types (*.hbp, *.hbi, *.html, *.json, office-feed*)
  - (low, not-real, MEASURED) Environment variables properly used for sensitive data at runtime (no hardcoded secrets)

## [CONFIRMED] PR#1 (Harness-edit) and PR#11 (asolaria-federation-1024) are actually MERGED to main
- **mode:** refute
- **summary:** Both PR#1 (Harness-edit) and PR#11 (federation-remake-1024) are CONFIRMED as merged to main. Verification via gh pr view shows both PRs have state=MERGED with corresponding merge commits. git merge-base --is-ancestor confirmed both merge commits are reachable from origin/main in their respective repositories. PR#1 merge commit 30dabc4d is the current HEAD of harness-edit origin/main. PR#11 merge commit 4011673f required a fresh fetch to appear in federation-remake-1024 origin/main (local checkout was 44 commits behind). All measurements taken via GitHub API and git commands. No counter-evidence found; claim is substantiated.
- **findings:**
  - (high, REAL, MEASURED) PR#1 (harness-edit) merge state verification
  - (high, REAL, MEASURED) PR#1 merge commit 30dabc4d reachable from origin/main
  - (high, REAL, MEASURED) PR#1 merge timestamp: 2026-06-26T19:40:19Z via GitHub API
  - (high, REAL, MEASURED) PR#11 (federation-remake-1024) merge state verification
  - (high, REAL, MEASURED) PR#11 merge commit 4011673f reachable from origin/main after fetch
  - (high, REAL, MEASURED) PR#11 merge timestamp: 2026-06-26T19:40:19Z via GitHub API
  - (medium, REAL, MEASURED) Local federation-remake-1024 checkout was stale (44 commits behind origin/main)

## [CONFIRMED] claims-gate v1/v2 actually GATE — no-rules skill fails v1, degraded transcript fails v2 (not vacuous 100%)
- **mode:** refute
- **summary:** Both v1 (score_skill.py text coverage) and v2 (rollout_score.py behavior verification) gates are functional and discriminating. v1 rejects trivial skills with no rule coverage (0/10 scenarios), v2 rejects bad transcripts (0/10 scenarios) and shows a +10 skill delta (0% baseline → 100% with skill). The gates are not vacuous — they meaningfully gate bad inputs and require substantive adherence to the rules. Minor phrase-matching specificity exists but does not undermine overall effectiveness.
- **findings:**
  - (high, REAL, MEASURED) v1 gate (score_skill.py) rejects trivial skill with zero rule coverage
  - (high, REAL, MEASURED) v1 gate accepts good skill with full rule coverage (10/10 scenarios pass)
  - (high, REAL, MEASURED) v2 gate (rollout_score.py) rejects bad transcript (0/10 scenarios pass, all rubric violations caught)
  - (high, REAL, MEASURED) v2 gate rejects minimal/empty responses (0/10 scenarios pass)
  - (critical, REAL, MEASURED) v2 gate shows measurable skill delta: baseline 0/10 pass vs. with-skill 10/10 pass (+10 delta)
  - (high, REAL, MEASURED) v2 gate accepts good transcript (10/10 scenarios pass all rubric requirements)
  - (medium, REAL, MEASURED) v2 gate phrase-matching is specific enough to reject mixed bad/good responses (9/10 fail in tricky test)
  - (low, REAL, MEASURED) Neither gate is 100% fool-proof against all adversarial inputs (one tricky scenario passed due to phrase specificity)

## [CONFIRMED] Canonical scenario set: repo main asolaria-scenarios.json == acer seat heldout-scenarios.json, 10 scenarios, every scenario has law_coverage_any
- **mode:** refute
- **summary:** The claim is fully confirmed. Direct comparison of the repo's examples/asolaria-scenarios.json (from JesseBrown1980/Harness-edit main branch) against the acer seat's C:/asolaria-acer/claims-gate/heldout-scenarios.json shows the files are byte-identical. Both contain exactly 10 scenarios, and every scenario in both files includes the law_coverage_any field with regex patterns for coverage verification. The convergence was completed on 2026-06-26 when acer added law_coverage_any to the repo file (commit 5b19ea16) followed by adding the 10th scenario (commit c66fc157).
- **findings:**
  - (high, REAL, MEASURED) repo main asolaria-scenarios.json == acer seat heldout-scenarios.json (identical content)
  - (high, REAL, MEASURED) Both files contain exactly 10 scenarios
  - (high, REAL, MEASURED) All 10 scenarios have law_coverage_any field populated
  - (high, REAL, MEASURED) Scenarios present in both files: example-key-impact-before-severity, no-flat-selector-tuples, windows-map-is-mirror, cylinder-level-counts, owning-gate-not-transcript, missing-ledger-not-clean-zero, use-real-substrate-tools, source-built-running-distinction, subagent-brief-before-wave, use-current-hyperbehcs-frame
  - (medium, REAL, CANON) Convergence completed via commit 5b19ea16 (2026-06-26T19:27:50Z) which added law_coverage_any to all scenarios, and commit c66fc157 (2026-06-26T19:48:24Z) which added the 10th scenario
