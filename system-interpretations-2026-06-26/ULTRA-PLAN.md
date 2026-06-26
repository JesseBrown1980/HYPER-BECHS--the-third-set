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
