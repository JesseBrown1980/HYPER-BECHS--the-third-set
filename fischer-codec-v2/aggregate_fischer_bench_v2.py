#!/usr/bin/env python3
"""Aggregate ten independent Fischer lenses and legal bidirectional codec runs."""
from __future__ import annotations

import argparse
import base64
import bz2
import gzip
import hashlib
import importlib.util
import json
import lzma
import os
import re
import sys
import zlib
from pathlib import Path
from typing import Any

import zstandard as zstd


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def read_jsons(root: Path, pattern: str) -> list[tuple[Path, dict[str, Any]]]:
    out = []
    for path in sorted(root.rglob(pattern)):
        out.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return out


def bpc(n: int, raw: int) -> float:
    return n * 8 / max(1, raw)


def pct_gain(new: float, old: float) -> float:
    return 100.0 * (1.0 - new / old)


def hbp(tag: str, **fields: Any) -> str:
    def esc(x: Any) -> str:
        return str(x).replace("\\", "\\\\").replace("|", "\\p").replace("\n", "\\n")
    return tag + "".join(f"|{k}={esc(v)}" for k, v in fields.items()) + "|json=0"


def same_slice_baselines(data: bytes, v01_path: Path) -> dict[str, Any]:
    zstd19 = zstd.ZstdCompressor(level=19).compress(data)
    rows = {
        "gzip9": gzip.compress(data, compresslevel=9),
        "bzip2_9": bz2.compress(data, compresslevel=9),
        "xz6": lzma.compress(data, preset=6),
        "zstd19": zstd19,
    }
    result: dict[str, Any] = {
        name: {"bytes": len(body), "bpc": bpc(len(body), len(data)),
               "sha256": sha256_hex(body)}
        for name, body in rows.items()
    }
    v01 = import_module(v01_path, "fischer_v01")
    comp = v01.compress(data)
    restored = v01.decompress(comp, len(data))
    result["asolaria_codec_v0_1"] = {
        "bytes": len(comp), "bpc": bpc(len(comp), len(data)),
        "sha256": sha256_hex(comp), "restore": restored == data,
    }
    return result


def build_events(summary: dict[str, Any], lenses: list[dict[str, Any]], codecs: dict[str, dict[str, Any]],
                 catalog_path: Path, alphabet_path: Path, omni_path: Path, portal_path: Path,
                 output: Path) -> dict[str, Any]:
    omni = import_module(omni_path, "fischer_omni")
    portal = import_module(portal_path, "fischer_portal")
    catalog, alphabet = omni.load_specs(catalog_path, alphabet_path)
    run_label = f"FISCHER10|{summary['input_sha256']}|{os.environ.get('GITHUB_SHA','local')}"
    ew = omni.EventWriter(catalog, alphabet, run_label, os.environ.get("GITHUB_SHA", "local"))
    ew.emit("RUN_OPENED", "asolaria", "enwik8-slice", "executing",
            {"raw_bytes": summary["raw_bytes"], "sha256": summary["input_sha256"],
             "independent_lenses": 10, "ledger_delta": {"raw_bytes": summary["raw_bytes"]}},
            gate="sovereignty", chain="triggers", proof="chain", surface="fischer-codec")
    for lens in lenses:
        ew.emit("FISCHER_LENS_MEASURED", f"fischer-{lens['direction']}-o{lens['order']}",
                "enwik8-slice", "completed", lens, gate="shannon", chain="observed_on",
                proof="test", surface="fischer-eval", translation="predictive-logloss")
    for name, row in sorted(codecs.items()):
        ew.emit("CODEC_ROUNDTRIP", "fischer-codec", "enwik8-slice",
                "completed" if row.get("restore") else "blocked",
                {"name": name, "bpc": row["bpc"], "archive_bytes": row["archive_bytes"],
                 "restore": row.get("restore", False), "sha256_out": row.get("sha256_out"),
                 "ledger_delta": {"archive_bytes": row["archive_bytes"]}},
                gate="shannon", chain="proves", proof="test",
                surface="hyperhermes-reference", translation=name,
                outcome="PASS" if row.get("restore") else "HOLD")
    ew.emit("OMNISHANNON_CONSENSUS", "omnishannon", "fischer-models", "completed",
            summary["comparisons"], gate="shannon", chain="proves", proof="test",
            surface="omnishannon", translation="adaptive-consensus")
    ew.emit("WHITE_ROOM_SYNTHESIS", "white-room", "fischer-models", "completed",
            {"bridge_models": 5, "gnn_live": False,
             "omni_mode_bpc": codecs.get("omni-pyr32", {}).get("bpc"),
             "claim": "joint contexts are deterministic white-room synthesis, not new source information"},
            gate="omni", chain="feeds", proof="code", surface="white-room")
    ew.emit("FINAL_READBACK_PASS", "shannon", "enwik8-slice", "completed",
            {"all_codec_restores": all(row.get("restore") for row in codecs.values()),
             "input_sha256": summary["input_sha256"]}, gate="shannon", chain="proves",
            proof="hash", surface="reverse-gate")
    ew.emit("RUN_CLOSED", "asolaria", "enwik8-slice", "completed",
            {"final_readback": True, "prize_claim": False}, gate="sovereignty",
            chain="proves", proof="chain", surface="fischer-codec", omega="sealed")
    verification = omni.validate_events(ew.events)
    full = b"".join(omni.canonical(e) + b"\n" for e in ew.events)
    full_path = output / "fischer_events_full.ndjson"
    full_path.write_bytes(full)
    v1 = omni.build_portal(ew.events, catalog)
    (output / "fischer_events_portal_v1.hbp").write_bytes(v1)
    prefix, psummary = portal.build(ew.events)
    v2 = portal.finish(prefix, psummary, {
        "chain_head": verification["chain_head"],
        "merkle_root": verification["merkle_root"],
        "final_readback": True,
    })
    decoded = portal.decode(v2)
    if [x["event_hash"] for x in decoded["events"]] != [x["event_hash"] for x in ew.events]:
        raise AssertionError("portal event hashes mismatch")
    (output / "fischer_events_portal_v2.hbp").write_bytes(v2)
    views = []
    for event in ew.events:
        views.append({"event_pid": event["id"], "actor_pid": event["actor_agent_pid"],
                      "xyz": omni.projection3(event["hyper60"]["selector"]),
                      "selector_sha256": event["hyper60"]["selector_sha256"],
                      "event_hash": event["event_hash"], "lossy_projection": True})
    (output / "fischer_views3d.ndjson").write_text(
        "".join(json.dumps(v, sort_keys=True, separators=(",", ":")) + "\n" for v in views),
        encoding="utf-8")
    return {"count": len(ew.events), "full_bytes": len(full), "portal_v1_bytes": len(v1),
            "portal_v2_bytes": len(v2), "portal_v2_ratio": len(full) / len(v2),
            "chain_head": verification["chain_head"], "merkle_root": verification["merkle_root"]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--slice", required=True)
    p.add_argument("--v01", required=True)
    p.add_argument("--catalog47", required=True)
    p.add_argument("--alphabet256", required=True)
    p.add_argument("--omnievent-script", required=True)
    p.add_argument("--portal-script", required=True)
    p.add_argument("--output-dir", required=True)
    args = p.parse_args()
    root = Path(args.root)
    output = Path(args.output_dir); output.mkdir(parents=True, exist_ok=True)
    data = Path(args.slice).read_bytes()
    input_sha = sha256_hex(data)

    lens_files = read_jsons(root, "lens-*.json")
    codec_files = read_jsons(root, "codec-*.json")
    if len(lens_files) != 10:
        raise AssertionError(f"expected 10 lens reports, got {len(lens_files)}")
    lenses = [row for _, row in lens_files]
    if len({(x["direction"], x["order"]) for x in lenses}) != 10:
        raise AssertionError("lens identities are not unique")
    if len({x["actor_pid"] for x in lenses}) != 10:
        raise AssertionError("actor PIDs are not unique")
    codecs = {re.search(r"codec-(.+)\.json$", path.name).group(1): row
              for path, row in codec_files}
    required = {"black-seq", "black-pyr32", "white-pyr32", "both-pyr32", "omni-pyr32", "both-pyr64"}
    if not required.issubset(codecs):
        raise AssertionError(f"missing codec runs: {sorted(required-set(codecs))}")
    for name, row in codecs.items():
        if not row.get("restore") or row.get("sha256_out") != input_sha:
            raise AssertionError(f"round trip failed: {name}")

    baselines = same_slice_baselines(data, Path(args.v01))
    bseq = codecs["black-seq"]["bpc"]
    bpyr = codecs["black-pyr32"]["bpc"]
    wpyr = codecs["white-pyr32"]["bpc"]
    both = codecs["both-pyr32"]["bpc"]
    omni = codecs["omni-pyr32"]["bpc"]
    comparisons = {
        "white_gain_with_same_pyramid_schedule_pct": pct_gain(both, bpyr),
        "omni_bridge_gain_over_blackwhite_pct": pct_gain(omni, both),
        "blackwhite_pyramid_gain_vs_black_sequential_pct": pct_gain(both, bseq),
        "omni_gain_vs_black_sequential_pct": pct_gain(omni, bseq),
        "legal_backward_adds_predictive_value": both < bpyr,
        "legal_bidirectional_beats_forward_end_to_end": both < bseq,
        "white_room_joint_context_beats_blackwhite": omni < both,
    }
    summary: dict[str, Any] = {
        "schema": "FISCHER-BIDIRECTIONAL-10-SEAT-v2",
        "raw_bytes": len(data), "input_sha256": input_sha,
        "independent_lens_count": 10,
        "black_lenses": 5, "white_lenses": 5,
        "lenses": sorted(lenses, key=lambda x: (x["direction"], x["order"])),
        "codecs": codecs, "baselines": baselines, "comparisons": comparisons,
        "method_boundary": {
            "white_context_legal": "right-side bytes are decoded first by the pyramid schedule",
            "reflection_adds_information": False,
            "new_predictive_model_can_lower_code_length": True,
            "physical_quantum_cloning": False,
            "gnn_live": False,
            "live_omnidispatcher": False,
        },
        "github": {"sha": os.environ.get("GITHUB_SHA"), "run_id": os.environ.get("GITHUB_RUN_ID"),
                   "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT")},
    }
    summary["events"] = build_events(summary, lenses, codecs, Path(args.catalog47),
                                      Path(args.alphabet256), Path(args.omnievent_script),
                                      Path(args.portal_script), output)
    (output / "fischer_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    best_codec_name, best_codec = min(codecs.items(), key=lambda kv: kv[1]["bpc"])
    lens_lines = "\n".join(
        f"| {x['direction']} | {x['order']} | {x['prime']} | {x['ideal_bpb']:.6f} | "
        f"{x['accuracy']:.6f} | {x['blunders']} | {x['fischer_verdict']} |"
        for x in sorted(lenses, key=lambda x: (x["direction"], x["order"]))
    )
    codec_lines = "\n".join(
        f"| {name} | {row['archive_bytes']:,} | {row['bpc']:.6f} | "
        f"{row['mixer_ideal_bpb']:.6f} | {row.get('black_trust_pct',0):.2f}% | "
        f"{row.get('white_trust_pct',0):.2f}% | {row.get('bridge_trust_pct',0):.2f}% | PASS |"
        for name, row in sorted(codecs.items())
    )
    base_lines = "\n".join(
        f"| {name} | {row['bytes']:,} | {row['bpc']:.6f} | {row.get('restore','n/a')} |"
        for name, row in baselines.items()
    )
    md = f"""# Fischer bidirectional ten-seat codec receipt

**Input:** first {len(data):,} bytes of enwik8  
**SHA-256:** `{input_sha}`  
**Independent model seats:** 10 GitHub Actions runners — five black and five white  
**Aggregate codecs:** separate independent runners  
**Restore policy:** every archive must reproduce the input byte-for-byte

## Legal bidirectional mechanism

The white models are not given unknown future bytes during an ordinary forward decode. A deterministic
pyramid schedule decodes anchors first and then interval midpoints. For every midpoint, both the listed
left and right contexts already exist in the decoder. This makes the backward context lawful and
reproducible, while charging the schedule's real coding cost.

## Ten independent Fischer lenses

| direction | order | prime | ideal bpb | accuracy | blunders | Fischer verdict |
|---|---:|---:|---:|---:|---:|---|
{lens_lines}

CPL/verdict uses the public Fischer-kernel shape: an expert is measured against the best expert's
log loss; large loss becomes HOLD/BLOCK rather than being trusted blindly.

## Exact codec runs

| run | archive bytes | bpc | ideal mixer bpb | black trust | white trust | bridge trust | restore |
|---|---:|---:|---:|---:|---:|---:|---|
{codec_lines}

Best tested Fischer run: **`{best_codec_name}` at {best_codec['bpc']:.6f} bpc**.

### Controlled comparisons

```text
white contribution under identical pyramid schedule
  {comparisons['white_gain_with_same_pyramid_schedule_pct']:.6f}%

joint white-room bridge contribution over black+white
  {comparisons['omni_bridge_gain_over_blackwhite_pct']:.6f}%

black+white pyramid versus ordinary black sequential
  {comparisons['blackwhite_pyramid_gain_vs_black_sequential_pct']:.6f}%

omni pyramid versus ordinary black sequential
  {comparisons['omni_gain_vs_black_sequential_pct']:.6f}%
```

Interpretation:

```text
legal backward model adds predictive value
  {comparisons['legal_backward_adds_predictive_value']}

legal bidirectional codec beats the forward end-to-end baseline
  {comparisons['legal_bidirectional_beats_forward_end_to_end']}

white-room joint context beats black+white averaging
  {comparisons['white_room_joint_context_beats_blackwhite']}
```

A positive same-schedule result means the right-context model contributes useful prediction. It does
not mean a reflection creates source information. A negative end-to-end result means the legal
schedule/anchor price exceeded the white-model gain.

## Same-slice baselines

| codec | bytes | bpc | exact restore |
|---|---:|---:|---|
{base_lines}

The original v0.1 lane is retained as the exact predecessor. It only counts a result after
byte-identical decompression.

## Omni integration

The aggregate run emitted {summary['events']['count']} Catalog47/Hyper60 OMNIEVENT rows with actor PIDs,
UTC/HLC ordering, full hashes, Merkle root, two compact portals, and 3D observer shadows.

```text
full event bytes   {summary['events']['full_bytes']}
portal v2 bytes    {summary['events']['portal_v2_bytes']}
portal ratio       {summary['events']['portal_v2_ratio']:.6f}x
Merkle root        {summary['events']['merkle_root']}
```

The workflow also guards the real public Rust Fischer evaluator. The predictive codec reuses its
anti-blunder/CPL/verdict philosophy; it does not claim that the original evaluator was itself a
compression model. The event dispatcher and HyperHermes labels in this receipt are reference
surfaces, not proof of live daemon routing. Trained GNNs were not invoked in this first codec flight.

## Verdict

The experiment tests the precise claim rather than assuming it:

- five black and five white model seats are independently executed;
- one deterministic Shannon mixer combines them in a reconstructible coding schedule;
- every archive is restore-gated;
- backward prediction is credited only against a black model using the same schedule;
- complete end-to-end cost is compared against an ordinary forward codec and standard same-slice tools;
- no physical quantum-cloning, sub-entropy, SOTA, or prize claim is made.
"""
    (output / "FISCHER-BIDIRECTIONAL-10-SEAT-CI-RECEIPT.md").write_text(md, encoding="utf-8")

    hbp_rows = [
        hbp("FISCHER10", raw_bytes=len(data), sha256=input_sha, lenses=10,
            black=5, white=5, best=best_codec_name, best_bpc=f"{best_codec['bpc']:.6f}"),
        hbp("COMPARE", white_gain_same_schedule_pct=f"{comparisons['white_gain_with_same_pyramid_schedule_pct']:.6f}",
            bridge_gain_pct=f"{comparisons['omni_bridge_gain_over_blackwhite_pct']:.6f}",
            both_vs_forward_pct=f"{comparisons['blackwhite_pyramid_gain_vs_black_sequential_pct']:.6f}",
            omni_vs_forward_pct=f"{comparisons['omni_gain_vs_black_sequential_pct']:.6f}"),
        hbp("VERDICT", white_predictive_value=int(comparisons['legal_backward_adds_predictive_value']),
            bidirectional_beats_forward=int(comparisons['legal_bidirectional_beats_forward_end_to_end']),
            bridge_beats_both=int(comparisons['white_room_joint_context_beats_blackwhite']),
            all_restore=1, quantum_physical=0, prize_claim=0),
        hbp("EVENTS", count=summary['events']['count'], full_bytes=summary['events']['full_bytes'],
            portal_v2_bytes=summary['events']['portal_v2_bytes'],
            portal_ratio=f"{summary['events']['portal_v2_ratio']:.6f}",
            merkle_root=summary['events']['merkle_root']),
    ]
    (output / "FISCHER-BIDIRECTIONAL-10-SEAT-CI-RECEIPT.hbp").write_text(
        "\n".join(hbp_rows) + "\n", encoding="utf-8")
    print(hbp_rows[2])


if __name__ == "__main__":
    main()
