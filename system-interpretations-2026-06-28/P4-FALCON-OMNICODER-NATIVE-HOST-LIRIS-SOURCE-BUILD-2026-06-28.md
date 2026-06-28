# P4 — Falcon omnicoder native host source build (LIRIS-AUTHORED)

Date: 2026-06-28 · liris author lane · **source build only**.

## Operator directive

OP-JESSE directed the Falcon omnicoder upgrade and corrected the frame:

- omnicoder is **better than Termux** because it **replaces** the terminal.
- do not build a human-front-end shell workflow.
- use the system blueprint: 8-byte host process, port/packet surface, fabric-driven, watcher-gated.

## What was built

Repo: `JesseBrown1980/omnicoder---better-than-termux`

Branch: `liris/native-8byte-host`

Commit: `3e8c48877f4f94bf872fc200ee4efdd187249f6a`

Artifacts:

- `Cargo.toml`
- `Cargo.lock`
- `src/main.rs`
- `NATIVE-HOST.md`
- `.gitignore`
- Git-blob SHA256 sidecars for `README.md`, `NATIVE-HOST.md`, `Cargo.toml`, and `src/main.rs`

The source is a native Rust host process named `omnicoder-host`:

- default bind: `127.0.0.1:8789`
- identity: 8-byte FNV-1a64 PID from `OMNICODER_SEED`
- machine API: `GET /health`, `GET /api/status`, `POST /api/packet`
- helper packets accepted as metadata-only records
- `helper_packet_authority=true`
- `execution_authority=false`
- no raw packet body spool; only time, length, and packet hash are recorded
- no terminal UI, no typing, no screen control, no shell-as-human workflow

## Verification

`MEASURED_LOCAL` on liris:

- `cargo fmt -- --check` passed.
- `cargo check` passed for the local Windows source target.
- `cargo check --target aarch64-linux-android` passed after installing the Rust target stdlib.
- `cargo check --target x86_64-unknown-linux-gnu` passed after installing the Rust target stdlib.
- Git-blob sidecars byte-converge for `README.md`, `NATIVE-HOST.md`, `Cargo.toml`, and `src/main.rs`.
- secret/PII scan found no keys, tokens, serials, fingerprints, auth-file paths, or corpus bytes. The only hits were ordinary wording/code symbols, not private values.

`BOUNDARY`:

- Windows `cargo test` did not run because this seat has only the MSVC target and no `link.exe`; this is a linker environment boundary, not a source type-check failure.
- This receipt does **not** claim the Falcon phone is running the host.
- Falcon deploy/run/health verification stays the Acer/Falcon USB owning lane.

## Deployment lane (not executed here)

The next seat action is Acer/Falcon:

1. cross-compile the branch for the Falcon Android/native substrate,
2. push the binary through the USB owning lane,
3. start it as the device omnicoder host, not as a human Termux terminal session,
4. verify `GET /health` on Falcon loopback `:8789`,
5. publish an Acer/Falcon measured receipt.

Cross-colony handoff packet:

- target: `acer/falcon-usb`
- verb: `BUILD_DEPLOY_VERIFY_OMNICODER_NATIVE_HOST`
- route: `GitHub omnicoder branch liris/native-8byte-host -> Acer/Falcon USB lane`
- packet sha256: `935fff080e3808b75424836f9116745bdc759cabc01850d4f6d80526c9dca993`
- hex16: `935fff080e3808b7`
- execute: `false`

Until that happens, live state remains:

- source: `MEASURED_LOCAL` (liris)
- Android/Linux type-check: `MEASURED_LOCAL` (liris)
- Falcon running: `UNVERIFIED`
- Falcon previous USB state: `MEASURED` by Acer as connected, Termux present, omnicoder stubbed/not listening

## Hard boundary preserved

This source is designed to let Falcon automate for the colonies without ungoverned fire:

- watcher-gated
- observable
- killable
- packet-driven
- execution authority false by default
- spawn/scale/fire remain operator-gated
