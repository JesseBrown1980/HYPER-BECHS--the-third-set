#!/usr/bin/env python3
"""Corrected wrapper for wolfram_cube_forge.py.

Attempt 1 proved the 20-runner fan-out and exact decoder, but exposed three audit
issues rather than source failures:
1. many canonical MIT files omit the literal heading "MIT License";
2. bundle lanes allowed the first large repository to consume the whole corpus;
3. method shadows tokenized binary framing headers along with source bytes.

Attempt 2 fixed those three paths but showed that canonical MIT notices may wrap
"to deal in the Software" across lines. License text is therefore normalized to
single-space form before exact phrase classification.

This wrapper patches those functions and then runs the original forge unchanged.
"""
from __future__ import annotations

import collections
import hashlib
import struct
from pathlib import Path

import wolfram_cube_forge as forge


def classify_license(text: str) -> str:
    low = " ".join(text.lower().split())
    if (
        "permission is hereby granted, free of charge" in low
        and "to deal in the software without restriction" in low
        and "the software is provided \"as is\"" in low
    ):
        return "MIT"
    if "apache license" in low and "version 2.0" in low:
        return "Apache-2.0"
    if "redistribution and use in source and binary forms" in low:
        if "neither the name" in low or "contributors may be used" in low:
            return "BSD-3-Clause"
        return "BSD-2-Clause"
    return "UNKNOWN"


def frame(repo: str, rel: str, raw: bytes) -> bytes:
    repo_b = repo.encode("utf-8")
    path_b = rel.encode("utf-8")
    digest = hashlib.sha256(raw).digest()
    return struct.pack(">HHQ", len(repo_b), len(path_b), len(raw)) + digest + repo_b + path_b + raw


def build_corpus(accepted, include_paths):
    corpus = bytearray(forge.MAGIC)
    files = []
    if not accepted:
        return bytes(corpus), files
    total_available = forge.MAX_CORPUS_BYTES - len(corpus)
    base_quota = max(1, total_available // len(accepted))
    for source_index, source in enumerate(accepted):
        repo = source["repo"]
        root = Path(source["local_path"])
        repo_budget = base_quota
        if source_index == len(accepted) - 1:
            repo_budget = forge.MAX_CORPUS_BYTES - len(corpus)
        repo_used = 0
        for path in forge.selected_paths_for_repo(repo, root, include_paths):
            if not forge.should_include(path, root):
                continue
            raw = path.read_bytes()
            rel = str(path.relative_to(root)).replace("\\", "/")
            overhead = 2 + 2 + 8 + 32 + len(repo.encode()) + len(rel.encode())
            remaining_repo = repo_budget - repo_used
            remaining_total = forge.MAX_CORPUS_BYTES - len(corpus)
            allowed = min(len(raw), remaining_repo - overhead, remaining_total - overhead)
            if allowed <= 0:
                break
            raw = raw[:allowed]
            record = frame(repo, rel, raw)
            corpus.extend(record)
            repo_used += len(record)
            files.append({
                "repo": repo,
                "path": rel,
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "extension": path.suffix.lower(),
            })
            if len(corpus) >= forge.MAX_CORPUS_BYTES:
                break
    return bytes(corpus), files


def source_text(corpus: bytes) -> str:
    if not corpus.startswith(forge.MAGIC):
        raise ValueError("bad corpus magic")
    pos = len(forge.MAGIC)
    chunks = []
    while pos < len(corpus):
        repo_len, path_len, data_len = struct.unpack(">HHQ", corpus[pos:pos + 12])
        pos += 12 + 32
        pos += repo_len + path_len
        data = corpus[pos:pos + data_len]
        pos += data_len
        chunks.append(data.decode("utf-8", errors="ignore"))
    return "\n\n".join(chunks)


def method_shadow(corpus, files, focus):
    text = source_text(corpus)
    identifiers = collections.Counter(forge.IDENTIFIER_RE.findall(text))
    builtins = collections.Counter(
        x for x in identifiers if x[:1].isupper() or "`" in x or x.startswith("$")
    )
    formulas = []
    for line in text.splitlines():
        clean = " ".join(line.strip().split())
        if 8 <= len(clean) <= 260 and forge.FORMULA_RE.search(clean) and clean not in formulas:
            formulas.append(clean)
        if len(formulas) >= 150:
            break
    ext = collections.Counter(file["extension"] or "<none>" for file in files)
    bigrams = collections.Counter()
    tokens = forge.IDENTIFIER_RE.findall(text[:5_000_000])
    for a, b in zip(tokens, tokens[1:]):
        if a != b:
            bigrams[(a, b)] += 1
    return {
        "schema": "WOLFRAM-WHITE-ROOM-METHOD-SHADOW-v2",
        "focus": focus,
        "nonreconstructive": True,
        "framing_excluded": True,
        "source_corpus_sha256": forge.sha256(corpus),
        "source_text_sha256": forge.sha256(text.encode("utf-8", errors="replace")),
        "file_count": len(files),
        "extension_counts": dict(sorted(ext.items())),
        "top_identifiers": [{"name": k, "count": v} for k, v in identifiers.most_common(512)],
        "top_wolfram_symbols": [{"name": k, "count": v} for k, v in builtins.most_common(512)],
        "top_identifier_edges": [
            {"from": a, "to": b, "count": v} for (a, b), v in bigrams.most_common(512)
        ],
        "formula_candidates": formulas,
    }


forge.classify_license = classify_license
forge.build_corpus = build_corpus
forge.method_shadow = method_shadow
forge.main()
