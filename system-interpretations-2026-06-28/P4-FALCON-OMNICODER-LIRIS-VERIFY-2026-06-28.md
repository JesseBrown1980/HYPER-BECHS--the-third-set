# P4 Falcon omnicoder - liris verification receipt

Date: 2026-06-28 - liris verifier lane - **docs-first / E=0.**

## Scope

This receipt verifies the public front-door correction for
`JesseBrown1980/omnicoder---better-than-termux` and records the Falcon USB attach as an
operator/Acer-side live-substrate observation. It does **not** execute on Falcon, start a service,
control ADB, spawn agents, publish device identifiers, or lift any hard hold.

## Claim

The omnicoder is not "a Node app inside Termux." It is the AI-native device host target that replaces
the human terminal path: the phone runs the 8-byte-host-process equivalent directly as a fabric node.

## Evidence

- `MEASURED`: `omnicoder---better-than-termux` main contains the corrected README at commit `5095fb1`
  (README commit `d964720`, sidecar commit `5095fb1`).
- `MEASURED`: README Git-blob SHA256 matches sidecar:
  `22da9df5ee776e67f7e68b0c22e79ef7423c3997895df69d4115b3882536eeb1`.
- `MEASURED`: targeted public-safety scan found no serial, fingerprint, private key, token, email, or
  phone-number value in the public front door.
- `OPERATOR_OBSERVED`: OP-JESSE reports Falcon connected over USB on the Acer side.
- `SYSTEM_AFFIRMED`: cross-colony driver packet emitted for a read-only Acer USB presence receipt:
  `b241c3d57797dc06aea5a186051fdb8ba741e0fbdd286e47ef5b0d04c46783ed`.

## Boundary

- `BOUNDARY`: liris cannot see Acer's USB bus. Falcon USB attach remains Acer-side/operator-observed
  until Acer publishes a carve-out-clean presence receipt.
- `BOUNDARY`: `:8789` is Falcon loopback. Other seats must not call local darkness a failure.
- `BOUNDARY`: a Windows checkout can hash differently because of line endings. Verify the README
  sidecar using Git/GitHub blob bytes.

## Accepted framing

- Termux is a legacy human terminal path, not the target runtime.
- Omnicoder is the AI-native replacement: no terminal UI, no human typing, no screen-proof requirement.
- The device-native 8-byte-host realization is still a build target until observed serving on the
  owning device.
- Autonomy remains watcher-gated, observable, killable, and execution-gated.

## Hard holds

No ADB control, no device start, no service launch, no spawn, no execution authority, no serial or
fingerprint publication, no private auth path, no private-root scan.
