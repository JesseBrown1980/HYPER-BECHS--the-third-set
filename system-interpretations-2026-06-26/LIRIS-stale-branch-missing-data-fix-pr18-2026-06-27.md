# LIRIS stale-branch missing-data fix — PR #18 (2026-06-27)

Seat: Liris/Rayssa · Repo: `JesseBrown1980/asolaria-federation-1024`

## Verdict

`ACCEPT_FIXED_AND_MERGED`

## Claim

PR #17 added Host-8 stale-branch detection, but Liris retro-review found an anti-fake-clean bug: missing or invalid `ahead_by` / `behind_by` / conflict evidence could default to `fresh -> ready`.

## Evidence

- `MEASURED_GITHUB`: PR #18 `fix: stale-branch detector fails closed on missing data`
  - URL: https://github.com/JesseBrown1980/asolaria-federation-1024/pull/18
  - Head after fix: `d0343f792cb14929ea6c4d02a4571af3798c922e`
  - PR CI: 5/5 green on the owning GitHub Actions gate.
- `MEASURED_GITHUB`: merged to `main`
  - Merge commit: `21ad5f9744e48db1782800a48591c969bae1a4f8`
  - Post-merge main CI: 5/5 green.

## Fix

- `Freshness::Unknown` added for missing ahead/behind evidence.
- `assess()` now takes optional counts and returns `unknown` when evidence is absent.
- `recommend()` now fails closed:
  - missing counts -> `block`
  - non-fresh branch with missing conflict status -> `block`
  - fresh branch remains `ready`
- Route parsing now preserves missing evidence instead of defaulting to zero.
- Negative/fractional branch counts are rejected.
- Regression tests cover missing counts, missing conflict evidence, negative/fractional counts, and route-level `block` rendering.

## Boundary

This is a staged Host-8 code fix only. It does not rebase, merge, fire, cut over, probe live branches, or mutate runtime state. It prevents the detector from calling incomplete branch evidence clean.

