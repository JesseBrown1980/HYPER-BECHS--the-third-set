# devops-ci-release (round B) — what Asolaria is

Asolaria is a **federated, deterministic, on-metal coordination system for heterogeneous intelligence slices** — not an ASI, but an orchestration geometry that routes frozen + borrowed intelligence (Gemma-4B cached, subscription LLMs) through a bilateral address fabric. MEASURED: two physical seats (acer/liris desktops) drive each other via GitHub as bilateral mediator; state is shared through explicit byte-verifiable receipts, not silent assumption.

**Core infrastructure (MEASURED):**
The system runs on a single HTTP dispatcher (`:4950`, 1000-slot PID-table, worker_threads pool) that routes `FEDENV-v1` envelopes to downstream workers. BEHCS-256/1024 is the content-addressable substrate (not bolt-on); addressing uses Brown-Hilbert geometry + prime-tower cylinders + rule-of-three (mod-3 role separation). A 9-stage OMNIFLYWHEEL pipeline (filter→verify→translate→catalog→route→room→schedule→hookwall→whiteroom-mint) orchestrates slice invocation. CANON: the "100-billion-packet substrate run" is file-verified (zero child-process spawns, zero external tokens, ~5.84 h paced session).

**CI/release discipline (MEASURED):**
Harness-edit implements a SkillOpt-style validation gate: candidate edits must improve a held-out scenario set without regression. Every claim is tagged MEASURED (verified against running code) / CANON (from doctrine) / OPERATOR (exact human-given numbers) / UNVERIFIED. A 9-law claims-gate prevents 8 recurring mistakes (conflating Windows mirrors with Linux authority; flat tuples vs 60D axes; missing vs clean-zero; source vs live). Cosign-v2 wraps integrity as Merkle chains; physical USB (2TB SOVLINUX) carries frozen artifacts + tools; bilateral vantage law: neither seat silently trusts the other's unseen substrate — shared state requires transported byte-receipts + hash verification.

**What it's becoming (CANON + UNVERIFIED):**
A self-improving neural-network topology where supervisors watch the backprop (self-reflect + corrective gates as learning signal), all running lawfully on borrowed subscriptions (no API metering — only ordinary individual usage). The road: scale from BEHCS-256 to BEHCS-1024 native OS; integrate GNN as kernel primitive; federate across 4+ devices with hookwall + cosign witness tiers.

Human authority remains explicit: operator cosign gates every mint, public push, and device write.
