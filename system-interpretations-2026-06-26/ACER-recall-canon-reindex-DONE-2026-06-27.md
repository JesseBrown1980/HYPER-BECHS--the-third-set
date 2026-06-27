# acer recall/Hilbra canon re-index — DONE (closes liris driver packet 70d030b)

Seat: acer (Claude Opus 4.8) · Date: 2026-06-27
Scope: the operator's "re-index the canon — use it [recall/Hilbra]." Executed on the **owning seat** (the recall stack + live `:4796` are acer-local; liris correctly handed off, cannot reach acer `:4796`).

## What was actually wrong (grounded, MEASURED)
The `:4949` canon-index "**39 indexed / 619 orphans**" is the **naive MEMORY.md-pointer** metric, not the real index. The real index is the **Rust recall/Hilbra engine (`:4796`)**. Probed it: the **660-file memory canon** (`C:/Users/acer/.claude/projects/C--/memory`) was **NOT in the recall corpus** (`search wedged`=0; corpus = the 5-drive archaeology only). So the canon was genuinely unindexed in the real engine — the re-index = **ingest the memory canon into recall**, not chase the pointer count.

## What was done (MEASURED, reversible, E=0)
1. **Backup** byte-identical: `.hbi` 98,639,268 + `.hbp` 159,157,140 → `.bak-20260627` (`cmp` OK).
2. Generated `rows-MEMORY.ndjson` (660) + `memory-text-overlay.ndjson` (626; **name+description summaries, NOT raw bodies** — the builder's own PII discipline) into the unified-archaeology corpus.
3. **Made it permanent:** `build-acer-recall-index.cjs` `ROW_FILES += rows-MEMORY`, `OVERLAY_FILES += memory-text-overlay` — future rebuilds keep the canon indexed.
4. **Rebuilt to a TEMP dir** (live index untouched): `rows_indexed = 591,946` (591,286 + 660 memory), 0 skipped, 0 malformed, 626 overlays folded.
5. **PII gate on temp** (authoritative classifier): memory rows → **0 at L0 PUBLIC**, 658 at L5 federation, 2 at L9 owner-private. PII-SAFE.
6. **Swap** (stop `recall-serve.exe` → copy temp→data → relaunch via the operator launcher) + verify.

## Verified live (`:4796`, MEASURED post-swap)
- health: `engine=recall-serve(rust)`, **`rows=591946`** (was 591286).
- `search wedged @L9` → **count=3**, returns memory paths — canon searchable (was 0).
- `search wedged @L0` (public) → **count=0** — memory is NOT public; PII gate holds live.
- Engine restarted PID 19580 → 27864. Backup `.bak-20260627` retained.

## Boundary
Data-layer index only; **E=0** (builder = pure file I/O, no spawn, no network); no engine crank/fire; fully reversible (restore `.bak` + relaunch). liris attack-verifies via this receipt + GitHub (cannot reach acer loopback `:4796`). Companion canon (both seats): the lossy ~3kb cube is a **distilled routing prior**, authority rehydratable via HBI/SHA/recall — re-indexing the canon strengthens exactly that recall-authority layer.

Tool note: `cmd.exe /c <batfile>` from Git Bash needs `MSYS_NO_PATHCONV=1` or the `/c` + path get mangled (the first swap attempt no-op'd from this; caught + fixed).
