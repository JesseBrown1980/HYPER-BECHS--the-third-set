#!/usr/bin/env python3
"""Run one base cube through 8 + 10 + 10 deterministic perspectives.

Sets:
- ``first``: the original 30-lane Asolaria/Hutter research swarm.
- ``wolfram``: the 20-lane Wolfram open-math cube forge.

Per eligible source:
1. Train one exact one-level BPE/glyph base cube (128 merges).
2. Reuse that fixed language through eight reversible transforms.
3. Measure five black and five white adaptive prediction viewpoints.
4. Carry one exact adaptive order-2 prior through ten recurrence passes.

Every reconstructive path must restore the original bytes and SHA exactly.
Predictor rows are measurements, not claimed standalone archives.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import math
import os
import random
import struct
import sys
import time
import traceback
import zlib
from pathlib import Path
from typing import Any, Callable

import numpy as np
import zstandard as zstd

MAX_CORPUS_BYTES = 1_000_000
BASE_MERGES = 128
PREDICTOR_BYTES = 150_000
RECURRENCE_BYTES = 100_000
GENESIS = "0" * 64

RING_A_NAMES = [
    "DBBH_FORWARD_IDENTITY",
    "DBBH_REVERSE_BYTES",
    "DBWH_FORWARD_XOR_DELTA",
    "DBWH_REVERSE_ROTATE_BITS",
    "MIRROR_NIBBLE_SWAP",
    "PI_SLICE_BLOCK_REVERSE",
    "NESTED_EVEN_ODD",
    "QPRISM_PRIME_BLOCK",
]


def now_utc() -> str:
    import datetime as dt
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pid8(label: str) -> str:
    return sha256(label.encode("utf-8"))[:16]


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def zero_order_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    arr = np.frombuffer(data, dtype=np.uint8)
    counts = np.bincount(arr, minlength=256).astype(np.float64)
    p = counts[counts > 0] / len(arr)
    return float(-(p * np.log2(p)).sum())


def apply_level(tokens: list[int], level: Any) -> list[int]:
    """Apply trained BPE rules by their training rank to a new token stream."""
    n = len(tokens)
    if not n or not level.rules:
        return list(tokens)
    ranks: dict[tuple[int, int], tuple[int, int]] = {}
    for rank, pair in enumerate(level.rules):
        ranks.setdefault(tuple(pair), (rank, int(level.start_id) + rank))

    val = list(tokens)
    prev = [i - 1 for i in range(n)]
    nxt = [i + 1 for i in range(n)]
    nxt[-1] = -1
    alive = [True] * n

    import heapq
    heap: list[tuple[int, int, tuple[int, int]]] = []

    def pair_at(i: int) -> tuple[int, int] | None:
        if i < 0 or i >= n or not alive[i]:
            return None
        j = nxt[i]
        if j < 0 or not alive[j]:
            return None
        return val[i], val[j]

    def push(i: int) -> None:
        pair = pair_at(i)
        if pair is not None and pair in ranks:
            heapq.heappush(heap, (ranks[pair][0], i, pair))

    for i in range(n - 1):
        push(i)

    while heap:
        rank, i, pair = heapq.heappop(heap)
        current = pair_at(i)
        if current != pair or ranks.get(pair, (-1, -1))[0] != rank:
            continue
        j = nxt[i]
        left = prev[i]
        right = nxt[j]
        val[i] = ranks[pair][1]
        nxt[i] = right
        if right >= 0:
            prev[right] = i
        alive[j] = False
        prev[j] = nxt[j] = -2
        push(left)
        push(i)

    out: list[int] = []
    i = 0
    while i >= 0:
        if not alive[i]:
            raise AssertionError("broken BPE application list")
        out.append(int(val[i]))
        i = nxt[i]
    return out


def encode_tokens(tokens: list[int], zstd_level: int = 19) -> bytes:
    packed = np.asarray(tokens, dtype=">u2").tobytes()
    return zstd.ZstdCompressor(level=zstd_level).compress(packed)


def decode_tokens(payload: bytes, count: int) -> list[int]:
    raw = zstd.ZstdDecompressor().decompress(payload, max_output_size=count * 2)
    if len(raw) != count * 2:
        raise ValueError("token payload length mismatch")
    return [int(x) for x in np.frombuffer(raw, dtype=">u2")]


def transform_identity(data: bytes) -> bytes:
    return data


def inverse_identity(data: bytes, n: int, source_sha: str) -> bytes:
    return data


def transform_reverse(data: bytes) -> bytes:
    return data[::-1]


def inverse_reverse(data: bytes, n: int, source_sha: str) -> bytes:
    return data[::-1]


def transform_xor_delta(data: bytes) -> bytes:
    if not data:
        return data
    arr = np.frombuffer(data, dtype=np.uint8)
    out = np.empty_like(arr)
    out[0] = arr[0]
    out[1:] = np.bitwise_xor(arr[1:], arr[:-1])
    return out.tobytes()


def inverse_xor_delta(data: bytes, n: int, source_sha: str) -> bytes:
    if not data:
        return data
    arr = np.frombuffer(data, dtype=np.uint8)
    return np.bitwise_xor.accumulate(arr).astype(np.uint8).tobytes()


def transform_rotate(data: bytes) -> bytes:
    arr = np.frombuffer(data, dtype=np.uint8)
    out = np.bitwise_or(np.left_shift(arr, 1) & 255, np.right_shift(arr, 7))
    return out.astype(np.uint8).tobytes()


def inverse_rotate(data: bytes, n: int, source_sha: str) -> bytes:
    arr = np.frombuffer(data, dtype=np.uint8)
    out = np.bitwise_or(np.right_shift(arr, 1), np.left_shift(arr & 1, 7))
    return out.astype(np.uint8).tobytes()


def transform_nibble(data: bytes) -> bytes:
    arr = np.frombuffer(data, dtype=np.uint8)
    out = np.bitwise_or(np.left_shift(arr & 15, 4), np.right_shift(arr, 4))
    return out.astype(np.uint8).tobytes()


def inverse_nibble(data: bytes, n: int, source_sha: str) -> bytes:
    return transform_nibble(data)


def transform_block_reverse(data: bytes, block: int = 256) -> bytes:
    return b"".join(data[i:i + block][::-1] for i in range(0, len(data), block))


def inverse_block_reverse(data: bytes, n: int, source_sha: str) -> bytes:
    return transform_block_reverse(data)


def transform_even_odd(data: bytes) -> bytes:
    return data[::2] + data[1::2]


def inverse_even_odd(data: bytes, n: int, source_sha: str) -> bytes:
    even_n = (n + 1) // 2
    evens = data[:even_n]
    odds = data[even_n:]
    out = bytearray(n)
    out[::2] = evens
    out[1::2] = odds
    return bytes(out)


def prime_permutation(nblocks: int, source_sha: str) -> list[int]:
    seed = int(source_sha[:16], 16) ^ 257 ^ (nblocks << 7)
    order = list(range(nblocks))
    random.Random(seed).shuffle(order)
    return order


def transform_prime_block(data: bytes, block: int = 257) -> bytes:
    nblocks = len(data) // block
    prefix_len = nblocks * block
    order = prime_permutation(nblocks, sha256(data))
    blocks = [data[i * block:(i + 1) * block] for i in range(nblocks)]
    return b"".join(blocks[i] for i in order) + data[prefix_len:]


def inverse_prime_block(data: bytes, n: int, source_sha: str, block: int = 257) -> bytes:
    nblocks = n // block
    prefix_len = nblocks * block
    order = prime_permutation(nblocks, source_sha)
    transformed_blocks = [data[i * block:(i + 1) * block] for i in range(nblocks)]
    original = [b""] * nblocks
    for output_index, original_index in enumerate(order):
        original[original_index] = transformed_blocks[output_index]
    return b"".join(original) + data[prefix_len:]


TRANSFORMS: list[tuple[str, Callable[[bytes], bytes], Callable[[bytes, int, str], bytes]]] = [
    (RING_A_NAMES[0], transform_identity, inverse_identity),
    (RING_A_NAMES[1], transform_reverse, inverse_reverse),
    (RING_A_NAMES[2], transform_xor_delta, inverse_xor_delta),
    (RING_A_NAMES[3], transform_rotate, inverse_rotate),
    (RING_A_NAMES[4], transform_nibble, inverse_nibble),
    (RING_A_NAMES[5], transform_block_reverse, inverse_block_reverse),
    (RING_A_NAMES[6], transform_even_odd, inverse_even_odd),
    (RING_A_NAMES[7], transform_prime_block, inverse_prime_block),
]


def collect_corpus(source_set: str, lane_id: str, repo_root: Path, work: Path) -> tuple[bytes, dict[str, Any], str]:
    if source_set == "wolfram":
        manifest = json.loads((repo_root / "research/wolfram-open-math-cubes-v1/sources.json").read_text())
        lane = next(item for item in manifest["lanes"] if item["id"] == lane_id)
        forge = import_module(repo_root / "research/wolfram-open-math-cubes-v1/wolfram_cube_forge.py",
                              f"recurrence_wolfram_{lane_id.replace('-', '_')}")
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
            return b"", {"lane": lane, "sources": sources, "held": held}, "HELD_NO_LICENSED_SOURCE"
        corpus, files = forge.build_corpus(accepted, lane.get("include_paths"))
        return corpus[:MAX_CORPUS_BYTES], {
            "lane": lane,
            "sources": sources,
            "held": held,
            "files": files,
            "framing": "WOLFRAM-CUBE-CORPUS-v1",
        }, "MEASURED"

    if source_set == "first":
        manifest = json.loads((repo_root / "research/hutter-cube-swarm-v1/sources.json").read_text())
        lane = next(item for item in manifest["lanes"] if item["id"] == lane_id)
        first = import_module(repo_root / "research/hutter-cube-swarm-v1/cube_session.py",
                              f"recurrence_first_{lane_id.replace('-', '_')}")
        kind = lane["kind"]
        status = "MEASURED"
        if kind in {"github_repo", "github_paths"}:
            text, source = first.collect_github_repo(lane, work)
            corpus = text.encode("utf-8", errors="replace")
        elif kind == "github_bundle":
            text, source = first.collect_github_bundle(lane, work)
            corpus = text.encode("utf-8", errors="replace")
        elif kind == "web_bundle":
            text, source = first.collect_web_bundle(lane)
            corpus = text.encode("utf-8", errors="replace")
        elif kind == "arxiv":
            text, source = first.collect_arxiv(lane, work)
            corpus = text.encode("utf-8", errors="replace")
        elif kind == "google_doc_bundle":
            text, source = first.collect_google_docs(lane)
            corpus = text.encode("utf-8", errors="replace")
        elif kind in {"train_public_plan_b", "train_hutter_methods", "train_combined_benchmark"}:
            corpus, source = first.gather_training_corpus(kind, work)
        elif kind == "private_input_gate":
            corpus, source, status = first.private_input_gate(lane, repo_root)
        else:
            raise ValueError(f"unsupported first-set kind: {kind}")
        return corpus[:MAX_CORPUS_BYTES], {"lane": lane, "source": source}, status

    raise ValueError(source_set)


def train_base_cube(corpus: bytes, bpe: Any, output: Path) -> tuple[Any, dict[str, Any], bytes]:
    level = bpe.train_level(list(corpus), BASE_MERGES)
    tokens = [int(x) for x in level.tokens]
    payload = encode_tokens(tokens)
    restored_tokens = decode_tokens(payload, len(tokens))
    restored = bytes(int(x) for x in bpe.expand_level(restored_tokens, level))
    if restored != corpus or sha256(restored) != sha256(corpus):
        raise AssertionError("base cube restore mismatch")

    model = {
        "schema": "ASOLARIA-BASE-CUBE-v1",
        "source_bytes": len(corpus),
        "source_sha256": sha256(corpus),
        "merges": len(level.rules),
        "start_id": int(level.start_id),
        "rules": [[int(a), int(b)] for a, b in level.rules],
        "token_count": len(tokens),
        "payload_file": "base-cube.payload.zst",
        "payload_sha256": sha256(payload),
    }
    model_bytes = json.dumps(model, sort_keys=True, separators=(",", ":")).encode()
    (output / "base-cube.model.json").write_text(json.dumps(model, indent=2), encoding="utf-8")
    (output / "base-cube.payload.zst").write_bytes(payload)
    result = {
        "source_bytes": len(corpus),
        "source_sha256": sha256(corpus),
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


def run_ring_a(corpus: bytes, level: Any, bpe: Any, model_bytes: int,
               base_payload_bytes: int) -> list[dict[str, Any]]:
    rows = []
    source_sha = sha256(corpus)
    for index, (name, transform, inverse) in enumerate(TRANSFORMS, 1):
        t0 = time.perf_counter()
        view = transform(corpus)
        transform_s = time.perf_counter() - t0
        if len(view) != len(corpus):
            raise AssertionError(f"{name}: transform length changed")
        t0 = time.perf_counter()
        tokens = apply_level(list(view), level)
        payload = encode_tokens(tokens)
        encode_s = time.perf_counter() - t0
        t0 = time.perf_counter()
        decoded_tokens = decode_tokens(payload, len(tokens))
        expanded = bytes(int(x) for x in bpe.expand_level(decoded_tokens, level))
        restored = inverse(expanded, len(corpus), source_sha)
        decode_s = time.perf_counter() - t0
        exact = restored == corpus and sha256(restored) == source_sha
        if not exact:
            raise AssertionError(f"{name}: inverse restore mismatch")
        rows.append({
            "ring": "A_REPRESENTATION",
            "pass": index,
            "perspective": name,
            "actor_pid": pid8(f"RINGA|{name}|{source_sha}"),
            "view_sha256": sha256(view),
            "view_entropy_bpb": zero_order_entropy(view),
            "tokens": len(tokens),
            "payload_bytes": len(payload),
            "payload_bpc": len(payload) * 8 / len(corpus),
            "standalone_bytes": model_bytes + len(payload),
            "standalone_bpc": (model_bytes + len(payload)) * 8 / len(corpus),
            "delta_vs_base_payload_pct": (len(payload) / base_payload_bytes - 1) * 100,
            "transform_s": transform_s,
            "encode_s": encode_s,
            "decode_s": decode_s,
            "restore": True,
            "source_sha256": source_sha,
            "payload_sha256": sha256(payload),
        })
    return rows


def predictor_measure(data: bytes, order: int, direction: str) -> dict[str, Any]:
    sequence = data if direction == "BLACK_FORWARD" else data[::-1]
    mask = (1 << (8 * order)) - 1
    ctx = 0
    states: dict[int, list[Any]] = {}
    log_loss = 0.0
    correct = 0
    predictions = 0
    blunders = 0
    nonzero_counts = 0
    for byte in sequence:
        state = states.get(ctx)
        if state is None:
            # total, counts, best_symbol, best_count
            state = [0, {}, 0, 0]
            states[ctx] = state
        total = int(state[0])
        counts: dict[int, int] = state[1]
        count = int(counts.get(byte, 0))
        probability = (count + 0.5) / (total + 128.0)
        log_loss -= math.log2(probability)
        if total:
            predictions += 1
            if byte == state[2]:
                correct += 1
            confidence = state[3] / total
            if confidence >= 0.90 and byte != state[2]:
                blunders += 1
        new_count = count + 1
        counts[byte] = new_count
        if count == 0:
            nonzero_counts += 1
        state[0] = total + 1
        if new_count > state[3] or (new_count == state[3] and byte < state[2]):
            state[2] = int(byte)
            state[3] = new_count
        ctx = ((ctx << 8) | int(byte)) & mask
    n = max(1, len(sequence))
    return {
        "ring": "B_FISCHER_PREDICTOR",
        "perspective": f"{direction}_ORDER_{order}",
        "direction": direction,
        "order": order,
        "sample_bytes": len(sequence),
        "estimated_bpc": log_loss / n,
        "top1_accuracy": correct / predictions if predictions else 0.0,
        "prediction_count": predictions,
        "contexts": len(states),
        "nonzero_symbol_counts": nonzero_counts,
        "high_confidence_blunders": blunders,
        "log_loss_bits": log_loss,
    }


def run_ring_b(corpus: bytes, lane_key: str) -> list[dict[str, Any]]:
    sample = corpus[: min(len(corpus), PREDICTOR_BYTES)]
    rows = []
    pass_no = 0
    for direction in ("BLACK_FORWARD", "WHITE_REVERSE"):
        for order in range(1, 6):
            pass_no += 1
            t0 = time.perf_counter()
            row = predictor_measure(sample, order, direction)
            row["elapsed_s"] = time.perf_counter() - t0
            row["pass"] = pass_no
            row["actor_pid"] = pid8(
                f"RINGB|{lane_key}|{direction}|{order}|{sha256(corpus)}"
            )
            row["source_sha256"] = sha256(corpus)
            rows.append(row)
    minimum = min(row["estimated_bpc"] for row in rows)
    weights = [math.exp(-(row["estimated_bpc"] - minimum)) for row in rows]
    total = sum(weights)
    for row, weight in zip(rows, weights):
        row["omnishannon_trust"] = weight / total
    return rows


def exact_prior_message(prior: Any, data: bytes, model: np.ndarray) -> tuple[dict[str, Any], np.ndarray]:
    pre = model.copy()
    decoder = pre.copy()
    t0 = time.perf_counter()
    comp, enc_ctx = prior.compress_with_model(data, model, 0)
    enc_s = time.perf_counter() - t0
    t0 = time.perf_counter()
    restored, dec_ctx = prior.decompress_with_model(comp, len(data), decoder, 0)
    dec_s = time.perf_counter() - t0
    exact = restored == data and sha256(restored) == sha256(data)
    state_match = np.array_equal(model, decoder) and enc_ctx == dec_ctx
    if not exact or not state_match:
        raise AssertionError("persistent prior restore/state mismatch")
    return {
        "compressed_bytes": len(comp),
        "bpc": len(comp) * 8 / len(data),
        "ratio": len(data) / len(comp),
        "restore": True,
        "state_match": True,
        "enc_s": enc_s,
        "dec_s": dec_s,
        "payload_sha256": sha256(comp),
    }, model


def run_ring_c(corpus: bytes, prior: Any, lane_key: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if len(corpus) < 2:
        raise ValueError("corpus too small for recurrence")
    if len(corpus) >= 2 * RECURRENCE_BYTES:
        train = corpus[:RECURRENCE_BYTES]
        holdout = corpus[RECURRENCE_BYTES:2 * RECURRENCE_BYTES]
    else:
        midpoint = max(1, len(corpus) // 2)
        train = corpus[:midpoint]
        holdout = corpus[midpoint:]
        if not holdout:
            holdout = train
    model = prior.make_model()
    rows = []
    holdouts = []
    for epoch in range(1, 11):
        row, model = exact_prior_message(prior, train, model)
        row.update({
            "ring": "C_PERSISTENT_RECURRENCE",
            "pass": epoch,
            "perspective": f"WHITE_ROOM_EPOCH_{epoch:02d}",
            "actor_pid": pid8(f"RINGC|{lane_key}|{epoch}|{sha256(corpus)}"),
            "train_bytes": len(train),
            "train_sha256": sha256(train),
            "source_sha256": sha256(corpus),
        })
        rows.append(row)
        if epoch in {1, 5, 10}:
            eval_model = model.copy()
            eval_row, _ = exact_prior_message(prior, holdout, eval_model)
            eval_row.update({
                "epoch": epoch,
                "holdout_bytes": len(holdout),
                "holdout_sha256": sha256(holdout),
            })
            holdouts.append(eval_row)
    nondefault, sparse = prior.sparse_estimate(model)
    checkpoint = zlib.compress(model.tobytes(), 9)
    metadata = {
        "first_bpc": rows[0]["bpc"],
        "last_bpc": rows[-1]["bpc"],
        "change_pct": (rows[-1]["bpc"] / rows[0]["bpc"] - 1) * 100,
        "holdouts": holdouts,
        "model_dense_bytes": int(model.nbytes),
        "model_nondefault_cells": int(nondefault),
        "model_sparse_estimate_bytes": int(sparse),
        "model_zlib_checkpoint_bytes": len(checkpoint),
        "all_restore": True,
        "all_state_match": True,
    }
    return rows, metadata


def hbp_result(result: dict[str, Any]) -> str:
    lines = [
        "CUBERECURRENCEv1"
        f"|set={result['source_set']}|lane={result['lane_id']}|status={result['status']}"
        f"|corpus_bytes={result['corpus']['bytes']}|source_sha256={result['corpus']['sha256']}"
        f"|base_bpc={result.get('base_cube', {}).get('bpc', 'NA')}"
        f"|passes={len(result.get('perspectives', []))}|receipt_sha256={result['receipt_sha256']}|json=0"
    ]
    for row in result.get("perspectives", []):
        lines.append(
            "PERSPECTIVE"
            f"|ring={row['ring']}|pass={row['pass']}|name={row['perspective']}"
            f"|value={row.get('standalone_bpc', row.get('estimated_bpc', row.get('bpc', 'NA')))}"
            f"|restore={int(bool(row.get('restore', False)))}"
            f"|state_match={int(bool(row.get('state_match', False)))}|json=0"
        )
    return "\n".join(lines) + "\n"


def summary_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Cube recurrence — {result['source_set']} / {result['lane_id']}",
        "",
        f"- Status: `{result['status']}`",
        f"- Corpus: **{result['corpus']['bytes']:,} B**",
        f"- Source SHA-256: `{result['corpus']['sha256']}`",
        f"- Perspective rows: **{len(result.get('perspectives', []))}**",
        f"- Receipt SHA-256: `{result['receipt_sha256']}`",
        "",
    ]
    if result.get("base_cube"):
        base = result["base_cube"]
        lines.extend([
            "## Base cube",
            "",
            f"- Rules: {base['rules']}",
            f"- Model: {base['model_bytes']:,} B",
            f"- Payload: {base['payload_bytes']:,} B",
            f"- Total: {base['total_bytes']:,} B",
            f"- Rate: {base['bpc']:.6f} bpc",
            f"- Restore: `{base['restore']}`",
            "",
        ])
    ring_a = [r for r in result.get("perspectives", []) if r["ring"] == "A_REPRESENTATION"]
    if ring_a:
        lines.extend([
            "## Ring A — eight reversible perspectives",
            "",
            "| Pass | Perspective | Payload bpc | Standalone bpc | Δ payload | Restore |",
            "|---:|---|---:|---:|---:|---|",
        ])
        for row in ring_a:
            lines.append(
                f"| {row['pass']} | `{row['perspective']}` | {row['payload_bpc']:.6f} | "
                f"{row['standalone_bpc']:.6f} | {row['delta_vs_base_payload_pct']:.3f}% | {row['restore']} |"
            )
        lines.append("")
    ring_b = [r for r in result.get("perspectives", []) if r["ring"] == "B_FISCHER_PREDICTOR"]
    if ring_b:
        lines.extend([
            "## Ring B — ten Fischer viewpoints",
            "",
            "| Pass | Perspective | Estimated bpc | Accuracy | Blunders | Trust |",
            "|---:|---|---:|---:|---:|---:|",
        ])
        for row in ring_b:
            lines.append(
                f"| {row['pass']} | `{row['perspective']}` | {row['estimated_bpc']:.6f} | "
                f"{row['top1_accuracy']:.4%} | {row['high_confidence_blunders']} | "
                f"{row['omnishannon_trust']:.6f} |"
            )
        lines.append("")
    ring_c = [r for r in result.get("perspectives", []) if r["ring"] == "C_PERSISTENT_RECURRENCE"]
    if ring_c:
        lines.extend([
            "## Ring C — ten exact recurrence passes",
            "",
            "| Epoch | bpc | Bytes | Restore | State match |",
            "|---:|---:|---:|---|---|",
        ])
        for row in ring_c:
            lines.append(
                f"| {row['pass']} | {row['bpc']:.6f} | {row['compressed_bytes']} | "
                f"{row['restore']} | {row['state_match']} |"
            )
        recurrence = result["recurrence"]
        lines.extend([
            "",
            f"Change from epoch 1 to 10: **{recurrence['change_pct']:.3f}%**.",
            "",
            "### Holdout evaluations",
            "",
            "| Epoch | Holdout bpc | Restore | State match |",
            "|---:|---:|---|---|",
        ])
        for row in recurrence["holdouts"]:
            lines.append(
                f"| {row['epoch']} | {row['bpc']:.6f} | {row['restore']} | {row['state_match']} |"
            )
    if result.get("errors"):
        lines.extend(["", "## Preserved errors", "", "```text", "\n".join(result["errors"]), "```"])
    return "\n".join(lines) + "\n"


def verify_base_artifact(output: Path) -> None:
    model = json.loads((output / "base-cube.model.json").read_text())
    payload = (output / "base-cube.payload.zst").read_bytes()
    if sha256(payload) != model["payload_sha256"]:
        raise AssertionError("base payload digest mismatch")
    level = type("Level", (), {})()
    level.start_id = int(model["start_id"])
    level.rules = [tuple(map(int, pair)) for pair in model["rules"]]
    tokens = decode_tokens(payload, int(model["token_count"]))
    # local exact expansion
    out: list[int] = []
    stack = list(reversed(tokens))
    limit = level.start_id + len(level.rules)
    while stack:
        token = int(stack.pop())
        if level.start_id <= token < limit:
            left, right = level.rules[token - level.start_id]
            stack.append(int(right))
            stack.append(int(left))
        else:
            out.append(token)
    if any(token > 255 for token in out):
        raise AssertionError("base artifact leaves non-byte tokens")
    restored = bytes(out)
    if len(restored) != int(model["source_bytes"]) or sha256(restored) != model["source_sha256"]:
        raise AssertionError("base artifact independent restore mismatch")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--set", dest="source_set", choices=["first", "wolfram"], required=True)
    p.add_argument("--lane", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--repo-root", default=".")
    p.add_argument("--min-runtime", type=float, default=120.0)
    p.add_argument("--verify-output", action="store_true")
    args = p.parse_args()

    output = Path(args.output).resolve()
    if args.verify_output:
        verify_base_artifact(output)
        print("CUBERECURRENCEVERIFY|base_restore=PASS|json=0")
        return

    output.mkdir(parents=True, exist_ok=True)
    work = output / "work"
    work.mkdir(exist_ok=True)
    repo_root = Path(args.repo_root).resolve()
    started_at = now_utc()
    started_epoch = time.time()
    start_mono = time.monotonic()
    errors: list[str] = []
    status = "MEASURED"
    corpus = b""
    source_receipt: dict[str, Any] = {}
    base_cube = None
    perspectives: list[dict[str, Any]] = []
    recurrence = None

    try:
        corpus, source_receipt, status = collect_corpus(
            args.source_set, args.lane, repo_root, work
        )
        if not corpus:
            if not status.startswith("HELD"):
                status = "HELD_EMPTY_CORPUS"
        else:
            bpe = import_module(
                repo_root / "third-seat-2026-07-12" / "gpt-crosscheck" /
                "multilevel_bpe_zstd_v1.py",
                "cube_recurrence_bpe",
            )
            prior = import_module(
                repo_root / "third-seat-2026-07-12" / "gpt-crosscheck" /
                "persistent_order2_curve_v1.py",
                "cube_recurrence_prior",
            )
            level, base_cube, base_payload = train_base_cube(corpus, bpe, output)
            model_bytes = base_cube["model_bytes"]
            ring_a = run_ring_a(
                corpus, level, bpe, model_bytes, base_cube["payload_bytes"]
            )
            ring_b = run_ring_b(corpus, f"{args.source_set}|{args.lane}")
            ring_c, recurrence = run_ring_c(
                corpus, prior, f"{args.source_set}|{args.lane}"
            )
            perspectives = ring_a + ring_b + ring_c
            if len(perspectives) != 28:
                raise AssertionError(f"expected 28 perspectives, got {len(perspectives)}")
            if not all(row.get("restore", False) for row in ring_a):
                raise AssertionError("Ring A restore failure")
            if not all(row.get("restore", False) and row.get("state_match", False)
                       for row in ring_c):
                raise AssertionError("Ring C restore/state failure")
            if not all(math.isfinite(row["estimated_bpc"]) for row in ring_b):
                raise AssertionError("Ring B non-finite estimate")
    except Exception as exc:
        status = "HELD_ERROR"
        errors.append(f"{type(exc).__name__}: {exc}")
        errors.append(traceback.format_exc(limit=30))

    elapsed = time.monotonic() - start_mono
    if elapsed < args.min_runtime:
        time.sleep(args.min_runtime - elapsed)
    ended_at = now_utc()
    ended_epoch = time.time()

    result_body = {
        "schema": "ASOLARIA-CUBE-RECURRENCE-28-v1",
        "source_set": args.source_set,
        "lane_id": args.lane,
        "status": status,
        "source_receipt": source_receipt,
        "corpus": {
            "bytes": len(corpus),
            "sha256": sha256(corpus),
        },
        "base_cube": base_cube,
        "perspectives": perspectives,
        "recurrence": recurrence,
        "errors": errors,
        "runtime": {
            "started_at": started_at,
            "ended_at": ended_at,
            "started_epoch": started_epoch,
            "ended_epoch": ended_epoch,
            "elapsed_seconds": ended_epoch - started_epoch,
            "runner_name": os.environ.get("RUNNER_NAME"),
            "runner_os": os.environ.get("RUNNER_OS"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_sha": os.environ.get("GITHUB_SHA"),
        },
    }
    digest = sha256(json.dumps(
        result_body, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode())
    result = {**result_body, "receipt_sha256": digest}

    (output / "perspective-result.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    (output / "perspective-result.hbp").write_text(
        hbp_result(result), encoding="utf-8"
    )
    (output / "source-receipt.json").write_text(
        json.dumps(source_receipt, indent=2), encoding="utf-8"
    )
    (output / "runtime.json").write_text(
        json.dumps(result["runtime"], indent=2), encoding="utf-8"
    )
    (output / "SUMMARY.md").write_text(
        summary_markdown(result), encoding="utf-8"
    )

    names = [
        "perspective-result.json",
        "perspective-result.hbp",
        "source-receipt.json",
        "runtime.json",
        "SUMMARY.md",
    ]
    if (output / "base-cube.model.json").exists():
        names.extend(["base-cube.model.json", "base-cube.payload.zst"])
    (output / "SHA256SUMS").write_text(
        "\n".join(f"{sha256((output / name).read_bytes())}  {name}" for name in names)
        + "\n",
        encoding="utf-8",
    )
    print(
        f"CUBERECURRENCE|set={args.source_set}|lane={args.lane}|status={status}|"
        f"corpus_bytes={len(corpus)}|passes={len(perspectives)}|receipt_sha256={digest}|json=0"
    )


if __name__ == "__main__":
    main()
