#!/usr/bin/env python3
"""Corrections for cube_recurrence_50x28.py.

Two issues exposed by the first preserved run:
1. Text-only corpora minted glyph IDs at max(source)+1, sometimes below 256.
   Reversible XOR/rotation views then produced literal bytes that collided with
   those glyph IDs. The corrected base cube reserves the full 0..255 alphabet.
2. Standard MIT grants without a literal ``MIT License`` heading were held by
   the older classifier. The corrected gate recognizes the complete MIT grant
   text while preserving UNKNOWN holds.

The first run remains evidence; this wrapper reruns the same 8+10+10 contract
with only those two corrections.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import cube_recurrence_50x28 as base


_original_collect = base.collect_corpus


def _robust_mit(classifier, text: str) -> str:
    result = classifier(text)
    if result != "UNKNOWN":
        return result
    low = " ".join(text.lower().split())
    markers = (
        "permission is hereby granted, free of charge",
        "to deal in the software without restriction",
        "the above copyright notice and this permission notice",
        "the software is provided",
    )
    return "MIT" if all(marker in low for marker in markers) else "UNKNOWN"


def collect_corpus(source_set: str, lane_id: str, repo_root: Path, work: Path):
    if source_set != "wolfram":
        return _original_collect(source_set, lane_id, repo_root, work)

    manifest = json.loads(
        (repo_root / "research/wolfram-open-math-cubes-v1/sources.json").read_text()
    )
    lane = next(item for item in manifest["lanes"] if item["id"] == lane_id)
    forge = base.import_module(
        repo_root / "research/wolfram-open-math-cubes-v1/wolfram_cube_forge.py",
        f"recurrence_v2_wolfram_{lane_id.replace('-', '_')}",
    )
    original_classifier = forge.classify_license
    forge.classify_license = lambda text: _robust_mit(original_classifier, text)

    sources = []
    accepted = []
    held = []
    for index, repo in enumerate(lane["repos"]):
        local = work / f"repo-{index:02d}"
        source = forge.clone_repo(repo, local)
        license_info = forge.verify_license(repo, local)
        source["license"] = license_info
        source["local_path"] = str(local)
        sources.append({k: v for k, v in source.items() if k != "local_path"})
        if license_info["allowed"]:
            accepted.append(source)
        else:
            held.append({"repo": repo, "license": license_info})
    if not accepted:
        return (
            b"",
            {"lane": lane, "sources": sources, "held": held},
            "HELD_NO_LICENSED_SOURCE",
        )
    corpus, files = forge.build_corpus(accepted, lane.get("include_paths"))
    return (
        corpus[: base.MAX_CORPUS_BYTES],
        {
            "lane": lane,
            "sources": sources,
            "held": held,
            "files": files,
            "framing": "WOLFRAM-CUBE-CORPUS-v1",
        },
        "MEASURED",
    )


def train_base_cube(corpus: bytes, bpe: Any, output: Path):
    t0 = time.perf_counter()
    trainer = bpe.BPETrainer(list(corpus))
    rules = trainer.train(base.BASE_MERGES, 256)
    level = bpe.Level(256, rules, trainer.output(), time.perf_counter() - t0)
    tokens = [int(x) for x in level.tokens]
    payload = base.encode_tokens(tokens)
    restored_tokens = base.decode_tokens(payload, len(tokens))
    restored = bytes(int(x) for x in bpe.expand_level(restored_tokens, level))
    if restored != corpus or base.sha256(restored) != base.sha256(corpus):
        raise AssertionError("corrected base cube restore mismatch")

    model = {
        "schema": "ASOLARIA-BASE-CUBE-v2",
        "source_bytes": len(corpus),
        "source_sha256": base.sha256(corpus),
        "alphabet_reserved": 256,
        "merges": len(level.rules),
        "start_id": int(level.start_id),
        "rules": [[int(a), int(b)] for a, b in level.rules],
        "token_count": len(tokens),
        "payload_file": "base-cube.payload.zst",
        "payload_sha256": base.sha256(payload),
    }
    model_bytes = json.dumps(model, sort_keys=True, separators=(",", ":")).encode()
    (output / "base-cube.model.json").write_text(
        json.dumps(model, indent=2), encoding="utf-8"
    )
    (output / "base-cube.payload.zst").write_bytes(payload)
    result = {
        "schema": "ASOLARIA-BASE-CUBE-v2",
        "source_bytes": len(corpus),
        "source_sha256": base.sha256(corpus),
        "alphabet_reserved": 256,
        "rules": len(level.rules),
        "token_count": len(tokens),
        "model_bytes": len(model_bytes),
        "payload_bytes": len(payload),
        "total_bytes": len(model_bytes) + len(payload),
        "bpc": (len(model_bytes) + len(payload)) * 8 / len(corpus),
        "payload_bpc": len(payload) * 8 / len(corpus),
        "restore": True,
        "train_s": float(level.train_s),
    }
    return level, result, payload


base.collect_corpus = collect_corpus
base.train_base_cube = train_base_cube
base.main()
