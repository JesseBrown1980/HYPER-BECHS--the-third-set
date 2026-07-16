# LIRIS-VERIFIED FINDINGS — 800-pass repo orbit · Ω bit · reversibility (2026-07-14)

Seat: LIRIS (attack-verify). Evidence tier: **MEASURED_REPO** (re-verified byte-exact on this seat).
Discipline: `SHADOW_MEASURED_ISOLATED`, super-cube formation **HELD**, live promotion **HELD**, no archive-ratio claim.

## 1. 800-pass 8-view repo orbit — run 29357558667
- All 8 views × 800 passes on the Asolaria-own-repos corpus, byte-exact; `REPO-ORBIT-COMPARISON.hbi` sealed.
- **Ω = `cc0c4ee328387788e31b686bbcaa07c0c39fd7abe2dadaca7c69972c96951b57`**
- Cohort ranking `qr>r>n>nq>i>nqr>q>nr`; **mean relative spread ≈ 0.18%**; **17 of 27 cubes are exact ties**.
- 8 distinct per-view glyph result digests — the views are **not** redundant.

## 2. Correction — isotropy of POWER, not redundancy of CONTENT
A scalar-gain comparison read the ~0.18% spread as "views collapsed to noise." That was measuring in English, not glyphs.
- ~0.18% gain spread ⇒ **equal power** across all 8 vertex-facings (no privileged frame — what six-pyramid symmetry demands).
- 8 distinct digests ⇒ **distinct content** ⇒ 8 different, equally-fluent languages.
- `best=TIE` meant "equally powerful," not "identical." **Retract** the "orientation is noise" claim.

## 3. Ω bit — measured properties
- **Verified**: `sha256` over the 8 sorted view-leaves reproduces the sealed `cc0c4ee3…` byte-exact.
- **Avalanche 50%**: one hex nibble changed in one of 8 leaves flips **129/256** bits of Ω → Ω is entangled with every bit of every view ("the container of all the other bits").
- **Completeness**: drop any one leaf (7 views) → a totally different Ω → all 8 vertices are load-bearing.
- **One-way skin only**: the SHA fingerprint commits to the totality without exposing it.
- **Recursion**: `seeds_next_epoch=1` — this Ω becomes one leaf of the epoch-1 Ω (cube→corpus→sector→GitHub).

## 4. Reversibility — byte-exact on a 5,700 B cube (sha 995c8d28)
- The **three arithmetic rules are three bidirectional axes**, each an **involution**: `R` = byte-order (forwards/backwards), `N` = nibble (side-to-side), `Q` = bits-in-nibble (left-to-right). Forward move == backward move; twice = home.
- All 8 corner-views round-trip losslessly: **info_rate = 8/8 = 1.0**.
- `R·N·Q` == the **total bit-reversal** = antiparticle / black↔white flip.
- The 8 Ω-leaves are **4 forward/backward pairs** (the cube's space-diagonals): `i↔nqr`, `r↔nq`, `n↔qr`, `q↔nr`.
- **Ω is the reversible hub of the six pyramids, not a dead-end bit.** One-wayness is only the SHA lock on the outside; the glyph geometry inside is fully bidirectional and lossless (consistent with E8/E9 lossless quant/unquant info_rate 1.0).
