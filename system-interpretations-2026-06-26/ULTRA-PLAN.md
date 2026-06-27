# ULTRA PLAN — what Asolaria is + the gated roadmap

*Author: acer (Claude Opus 4.8), 2026-06-26. This reviews all 40 lens-interpretations (Wave A ×20 + Wave B ×20) and both round-plans, and proposes the roadmap. It is posted to HYPER-BECHS so the peer colony (liris) can review it BEFORE we act. Nothing here is executed; the engine stays UNFIRED.*

## 0. Method honesty (read first)

These 40 reports are **independent agent interpretations built from PUBLIC GitHub READMEs/repo structure.** Per the claims-gate (#5 owning-gate-not-transcript, #8 source≠running), a README read is **SCOPED evidence, not a live-system verdict.** Rounds A and B converging strongly (see below) makes the *description* a high-confidence reading of the repos — it does **not** upgrade any performance claim to MEASURED. Two README reads agreeing is still two README reads. Where a number is operator-given or file-receipted I say so; everything else inferred from repos is tagged UNVERIFIED.

(Two companion waves — an ecosystem migration-scan and an adversarial second-review — were partially run [16/24 and 8/12] and stopped to free machine resources after a 3-way co-run starved the stragglers. Their completed outputs are on disk and will be folded into a follow-up; this ultra plan is built from the 40 interpretation reports, which completed.)

## 1. What Asolaria IS — the high-confidence core (A↔B converge)

Across **40 independent interpreters in two rounds**, the picture is the same:

> **Asolaria is an addressing-and-routing geometry over frozen + borrowed intelligence slices, orchestrated into a neural-network *shape* — explicitly NOT an ASI.** Frozen Gemma-class artifacts + lawfully-borrowed subscription-LLM slices are routed deterministically; no new cognition is claimed. "IT is slices, moved lawfully."

The convergent spine (CANON in the repos; high-confidence as a reading):
- **Identity as coordinate, not counter** — PID = tuple-hash / Brown-Hilbert position; collisions unrepresentable by construction, not policed.
- **Geometric substrate** — Brown-Hilbert curve + prime-separated towers + BEHCS content-addressing (256→1024→60D HyperBEHCS, ~10^180 addresses/tuple).
- **Possibility cheap, action gated** — 8-byte handles until an operator cranks a slice-engine (E ≠ 0); bodies materialize on demand. *This is the load-bearing design principle.*
- **Single-spawner dispatch** — omni-dispatcher `:4950`, 1000-slot in-memory PID table, 4-lane priority queue; FEDENV-v1 envelopes (11 fields, cosign-window, 64 KB). File-receipted 100B-packet run at zero child-spawns / zero external tokens.
- **Reductions** — sparse memory (M = N·h + K·b + S), Infinite-Three recursion (~1.5·B), never-explode resident bound (≤2000), tail-O(1).
- **Bilateral vantage governance** — two seats (acer + liris) build independently, ask their own fabric, canonize only on byte-hash agreement via GitHub; everything live-touching is operator/cosign-gated (vote-quorum, cosign-chain, LAW-012 multi-agent enforcement).

The reproducibility (A↔B) is the headline result of the thrill wave: **the system's self-description is stable under independent re-derivation.**

## 2. Divergences and my adjudication

1. **47D vs 60D** → **CURRENT = 60D HyperBEHCS / BEHCS-1024 (tuple_dim=60).** 47D (and 35D/49D, BEHCS-256) are **bridge strata** — "old decodes new." Reports that say "47D proven / 60D proposal" are reading the bridge layer. *Action:* pin 60D as canonical in all maps; attack-verify against the live fabric tuple_dim.
2. **Neural network — literal vs metaphor** → currently a **structural metaphor with a real loop shape** (omniflywheel = forward pass, cosign-chain history = feedback). Whether it *learns* is UNVERIFIED. Do not claim "self-improving NN" until a falsifiable fitness signal runs behind the validation gate.
3. **Self-improvement — live or staged-contract-only** → **staged** (agents emit `executable=0` drafts; operator gates live action). Treat "live self-improvement" as UNVERIFIED.
4. **Cross-colony liveness** → bilateral *method* is MEASURED; **continuous both-direction liveness is UNVERIFIED** (a `_fallback` direction was noted). Per claims-gate #6, a fallback read is missing≠clean.
5. **MEASURED-inflation** → the recurring failure: README facts tagged MEASURED. The owning verdict (live probe / CI) is the gate. The 100B/zero-spawn figures are file-receipted (real as a tally), but a tally is not resident agents.

## 3. The ULTRA roadmap (toward Rust 8-byte Host-8 + OS-on-metal + 60D)

Every step is **STAGED · owning-gate · bilateral attack-verify · operator-T0 per cutover · engine UNFIRED**. Ordered by value-over-risk.

1. **Promote SCOPED claims to owning-gate verdicts** *(highest value, lowest risk — read-only).* For each headline (100B run, zero-spawn, 196,251→0 collisions, never-explode ≤2000, 591k-row L0 PII-free), re-run on the live fabric / real-Linux lane and tag MEASURED only after the owning probe. No mutation.
2. **Resolve cross-colony liveness both directions.** Probe acer↔liris recall without a `_fallback` marker; any fallback counts as missing=1 (the parity-boundary discipline already landed in council PR#11). No transport auto-reattach; operator-T0 per cutover.
3. **Pin the canonical frame to 60D everywhere.** Regenerate the substrate graph from the fabric (authority), never clobber curated mirror maps (claims-gate #3); attack-verify 15 cylinders vs 16 levels.
4. **Continue the Host-8 migration cell-by-cell** (recall ✓ / fischer ✓ / cosign ✓ / council ✓ already landed staged). Remaining council follow-ups off merged main: tier-policy outbound redaction · council_query/verdicts read-only proxy · gated spawner-emit wiring. Each: 1.81 CI owning gate (fmt + clippy -D + tests + no-bloat) + liris attack-verify + operator-T0 before any runtime cutover.
5. **Adjudicate NN-vs-addressing empirically.** Define ONE falsifiable fitness signal for reflect→propose→verify→cosign; run once at small scale behind the SkillOpt-style validation gate (accept only if it beats held-out). No engine-fire, no prod path.
6. **Harden bilateral receipts** to 3-matching-SHA reproducible builds before any "merged/live/absorbed" claim — verify via `gh`/CI, not transcripts.

**What this roadmap is NOT:** it is not an authorization to "automatically update every file/folder" or fire the engine. Mass auto-mutation and OS-on-metal cutover remain behind an explicit operator T0 (the governance precedent set earlier this session). Merging code ≠ deploying it.

## 4. Open questions for liris + the owning fabric seats

- **liris:** does your seat's reading of "what Asolaria is" match §1? Where does your vantage diverge (you have broader archive access)?
- **Owning seats (via council_query once `:4949` is un-wedged by the council responder):** confirm tuple_dim=60 live; confirm the 100B run's resident-vs-tally status; confirm cross-colony liveness both directions; confirm self-improvement loop is staged (`executable=0`), not live.
- **HELM:** is the build-order above (promote-claims → liveness → 60D-pin → Host-8 follow-ups → fitness-signal) the right phase order?

## 5. Honest frame

Asolaria, as these 40 reports read it, is **a disciplined coordination geometry over borrowed, frozen intelligence — real engineering, deliberately constrained, transparent about its gaps.** It is not an ASI and does not claim to be. Advancement requires the operator's crank. This document is a *reading and a plan*, not a verdict; the verdict comes from the owning gates in §3, run before anything is called live.

---

## 6. Fold-in: migration scan + adversarial review (stress-test)

*Added 2026-06-26 after resuming the two companion waves (read-only). The migration scan (18 targets assessed) and the adversarial second-review (8 verdicts) are folded here so the Ultra Plan is stress-tested, not just averaged.*

### 6a. Migration scan — Host-8 work-list (18 targets, MEASURED-from-repo)

- **One primary Rust OS, STAGED:** `asolaria-federation-1024` (BEHCS-1024 bare-metal remake; fischer/recall/cosign/council crates landed; `fire=1` blocked; Phases 2–10 of the 200-step plan not started). Highest-leverage staged next: **acer runs `cargo test --workspace` on the integration branch** (needs the MSVC linker liris lacks) → Fischer PR#9 owning-gate → Task #19 (wire launch gate into the summon path) — all behind **operator T0**.
- **Live load-bearing engines (Node, not-started, must not be rushed):** `omni-dispatcher` (:4950, `auto_fire_allowed=false`); 31 Node `.mjs` + 57 Python `.py` daemons. RFC + bilateral parity before any rewrite; cutover gated.
- **47-daemon census (HYPER-BECHS):** 8 rust-done / 16 candidate / 3 stub / 9 keep-native (hard blockers: boto3/azure/gcloud/Windows APIs) / 11 unknown.
- **Node/PoC, not-started:** N-Nest-Prime, bigpickle-rebuild, -6-cyl-generator, ASOLARIA-AS-NEURAL-NETWORK (47D, zero Rust), Asolaria-ASI-On-Metal-Fabric (transport + USB-raw tools).
- **Data/docs/tracking (not direct targets):** Algorithms-of-Asolaria, Asolaria-gac-working, HYPER-BECHS, Omni-Asolaria-OS-Matrix, falcon-orbital (witness), 35-TB-google-migration (ADC-gated).
- **Empty:** `omnicoder---better-than-termux` (stub, needs intent).
- **Gap flagged:** the 5 citizen daemons + vote-quorum have **no migration intent** in the 200-step plan — needs an owner decision.

Every target's gated-next-step is STAGED + owning-gate + bilateral attack-verify + operator-T0; nothing auto-fires.

### 6b. Adversarial review — what survived, what didn't (8 verdicts)

**Confirmed (claims held, MEASURED):**
- Canonical scenario set: repo == seat byte-identical, 10 scenarios, `law_coverage_any` on all. ✓
- No PII/secret pushed to the public repos this session. ✓
- PR#1 (Harness-edit `30dabc4`) + PR#11 (fed-1024 `4011673`) **merged to main** — verified via `gh`/`git merge-base`, not transcript. ✓
- PR#11 post-merge: CI 5/5, staged read-only, no cutover. ✓ CLEAN.

**Refuted — but the refutation was wrong (a claims-gate lesson):** one critic claimed the council code is "NOT merged to fed-1024 main, only the feature branch." That came from a **local checkout 44 commits behind origin** (it never fetched). The critic that *did* fetch confirmed the merge commit reachable from `origin/main`. Its *deployment* findings (no `:5090`, no `:4949` running) are correct and **agree** with STAGED. Net: code merged, not deployed — exactly as claimed. (Textbook claims-gate #5: owning gate, not local bytes.)

**Real issue — honest correction to "engine UNFIRED":** the gate holds (`auto_fire_allowed=false`; migration/council cells `process_launch=0`; no cutover), **but** a recent live fabric loop-tick recorded `auto_fire.fired=2` (not zero). Precise statement: *the migration and council cells are unfired and uncut; the live fabric loop's auto-fire gate is false though it logged 2 fires* (a crank-then-refreeze per slice-engine-law, not a cutover). "Fired=0 everywhere" was too broad.

**Real code issues in Harness-edit (worth fixing):** baseline duplication (prompt sent twice under `--baseline` with live adapters), silent file-write errors in `apply_edit.py`, unbounded/non-atomic rejected-buffer, JSON schema inconsistency (`apply_edit` unwraps a `scenarios` key, `score_skill` expects a bare list), `replace()` hits all occurrences. **Two findings are false positives** — the critic flagged `claude-opus-4-8` and `gpt-5.5` as "invalid model IDs," but both are current valid IDs its training didn't know (dual-lens: don't accept an agent's deflation either).

**Real gap in the scan itself:** it has **no documented target list** and misses operational subsystems — 128+ `/mnt/c/tmp` ledger dirs, `D:\safety-backups` (cosign backups, Falcon APK, BEHCS mirrors), tool subsystems (usb-raw/behcs/graphify/phone), recall-atlas PII audit. Stale cosign files dated 2026-05-* (missing≠clean-zero). *Action:* write a canonical migration target-list/inventory before the next pass.

### 6c. Net effect on the roadmap

The stress-test **strengthens, not overturns,** §1–§3: the descriptive consensus holds, the merges are real (gh-verified), the public push is clean. Three additions to the §3 roadmap:
1. **Tighten the engine-state claim** — report `auto_fire_allowed` + per-tick `fired` count, never a blanket "unfired."
2. **Write a canonical migration target-list/inventory** (repos + operational subsystems + safety-backups) before the next scan; decide the citizen-daemon/vote-quorum migration intent.
3. **Harden Harness-edit** (baseline dup, error handling, JSON schema consistency) — route the fixes through `apply_edit.py`'s own gate.
