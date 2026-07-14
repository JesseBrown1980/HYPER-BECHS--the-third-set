# Multiplex Fleet — activation guide (operator one-clicks)

This branch stages cross-provider fleets. Configs are inert until each platform is connected;
pushing this branch triggers NOTHING on GitHub Actions (no PR; workflows are pull_request-only).

## 1. Cirrus CI (free, ~16 tasks, 2h limit) — determinism anchors
File: `.cirrus.yml` — four 100-pass mid-corpus anchor views (sealed numbers exist; every Cirrus
task independently verifies a known receipt from a new host family).
**Activate:** install the Cirrus CI GitHub App on this repo → https://github.com/apps/cirrus-ci
(select JesseBrown1980/HYPER-BECHS--the-third-set). Cirrus then builds this branch automatically.

## 2. Azure Pipelines (free OSS grant, ~10 parallel, 6h jobs) — second full-depth provider
File: `azure-pipelines.yml` — the complete 8-view × 800-pass wide orbit.
**Activate:** dev.azure.com → create org/project (free) → Pipelines → New → GitHub →
select this repo → "Existing Azure Pipelines YAML file" → branch
`agent/liris-multiplex-platforms-2026-07-14`, path `/azure-pipelines.yml` → Run.
(First-time OSS parallelism may require the free-grant request form.)

## 3. Self-hosted GitHub runners (uncapped) — colony hardware
Any colony machine (ACER, Gaia when reachable, spare boxes) registers with:
```bash
mkdir actions-runner && cd actions-runner
curl -o r.tar.gz -L https://github.com/actions/runner/releases/latest/download/actions-runner-linux-x64.tar.gz  # (or -win-x64.zip)
tar xzf r.tar.gz
./config.sh --url https://github.com/JesseBrown1980/HYPER-BECHS--the-third-set --token <REG_TOKEN>
./run.sh
```
`<REG_TOKEN>` mints per-machine via: `gh api -X POST repos/JesseBrown1980/HYPER-BECHS--the-third-set/actions/runners/registration-token --jq .token`
Then any workflow can target `runs-on: self-hosted`. Plan concurrency caps do NOT apply.

## Provenance law (applies to every provider)
Each task stamps its true SEAT (CIRRUS_COMMUNITY_CONTAINER / AZURE_PIPELINES_CONTAINER /
SELF_HOSTED_<HOST>) — per-view host provenance is preserved, and RELIC's acceptance protocol
(verify pins → compare payloads → accept matches) governs entry into any Ω lineage.
