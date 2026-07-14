#!/usr/bin/env python3
"""Restore and optionally extract a WOLFRAM-REVERSIBLE-GLYPH-CUBE-v1 artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

import numpy as np
import zstandard as zstd

MAGIC = b"WOLFRAM-CUBE-CORPUS-v1\x00"


def expand(tokens: list[int], level: dict) -> list[int]:
    start = int(level["start_id"])
    rules = level["rules"]
    limit = start + len(rules)
    out: list[int] = []
    stack = list(reversed(tokens))
    while stack:
        token = int(stack.pop())
        if start <= token < limit:
            left, right = rules[token - start]
            stack.append(int(right))
            stack.append(int(left))
        else:
            out.append(token)
    return out


def decode(model_path: Path, payload_path: Path) -> bytes:
    model = json.loads(model_path.read_text(encoding="utf-8"))
    payload = payload_path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != model["payload_sha256"]:
        raise ValueError("payload SHA-256 mismatch")
    raw_tokens = zstd.ZstdDecompressor().decompress(payload, max_output_size=int(model["token_count"]) * 2)
    if len(raw_tokens) != int(model["token_count"]) * 2:
        raise ValueError("token payload length mismatch")
    tokens = list(np.frombuffer(raw_tokens, dtype=">u2").astype(np.uint16))
    for level in reversed(model["levels"]):
        tokens = expand(tokens, level)
    if any(int(token) > 255 for token in tokens):
        raise ValueError("non-byte token after reverse traversal")
    restored = bytes(int(token) for token in tokens)
    restored = restored[: int(model["orig_len"])]
    if hashlib.sha256(restored).hexdigest() != model["orig_sha256"]:
        raise ValueError("restored corpus SHA-256 mismatch")
    return restored


def extract(corpus: bytes, destination: Path) -> list[dict]:
    if not corpus.startswith(MAGIC):
        raise ValueError("bad corpus magic")
    destination.mkdir(parents=True, exist_ok=True)
    pos = len(MAGIC)
    rows = []
    while pos < len(corpus):
        if pos + 44 > len(corpus):
            raise ValueError("truncated frame")
        repo_len, path_len, data_len = struct.unpack(">HHQ", corpus[pos:pos + 12])
        pos += 12
        digest = corpus[pos:pos + 32]
        pos += 32
        repo = corpus[pos:pos + repo_len].decode("utf-8")
        pos += repo_len
        rel = corpus[pos:pos + path_len].decode("utf-8")
        pos += path_len
        data = corpus[pos:pos + data_len]
        pos += data_len
        if hashlib.sha256(data).digest() != digest:
            raise ValueError(f"file digest mismatch: {repo}:{rel}")
        safe_repo = repo.replace("/", "__")
        target = destination / safe_repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        rows.append({"repo": repo, "path": rel, "bytes": len(data), "sha256": digest.hex()})
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--payload", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--extract-dir")
    args = p.parse_args()
    restored = decode(Path(args.model), Path(args.payload))
    Path(args.output).write_bytes(restored)
    rows = extract(restored, Path(args.extract_dir)) if args.extract_dir else []
    print(
        "WOLFRAMCUBERESTORE|"
        f"bytes={len(restored)}|sha256={hashlib.sha256(restored).hexdigest()}|"
        f"files={len(rows)}|status=PASS|json=0"
    )


if __name__ == "__main__":
    main()
