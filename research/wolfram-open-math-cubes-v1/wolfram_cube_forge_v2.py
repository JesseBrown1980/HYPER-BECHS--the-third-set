#!/usr/bin/env python3
"""Corrected wrapper for wolfram_cube_forge.py.

The first executions proved the 20-runner fan-out and exact decoder, then exposed
four audit/selection issues rather than source failures:
1. canonical MIT files can omit the literal heading "MIT License" and wrap clauses;
2. bundle lanes must give each repository a deterministic corpus share;
3. method shadows must exclude binary framing headers;
4. mathematical program files must be selected before CI, contributor, and editor
   metadata so the cube represents code rather than repository administration.

This wrapper patches those functions and then runs the original forge unchanged.
"""
from __future__ import annotations

import collections
import hashlib
import struct
from pathlib import Path

import wolfram_cube_forge as forge

PROGRAM_EXTENSIONS = {
    ".wl", ".wls", ".m", ".mt", ".wlt",
    ".py", ".rs", ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp",
    ".java", ".scala", ".js", ".jsx", ".ts", ".tsx", ".cmake",
}
NOTEBOOK_EXTENSIONS = {".nb", ".ipynb"}
ADMIN_PARTS = {".github", ".claude", ".claude-plugin", ".vscode", ".circleci"}
ADMIN_NAMES = {
    "contributing.md", "changelog.md", "code_of_conduct.md", "security.md",
    "authors", "authors.md", "readme.md", "readme.rst", "readme.txt",
}


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


def path_priority(path: Path, root: Path) -> tuple[int, str]:
    rel = path.relative_to(root)
    parts_lower = {part.lower() for part in rel.parts}
    suffix = path.suffix.lower()
    name = path.name.lower()
    if parts_lower & ADMIN_PARTS:
        tier = 8
    elif suffix in PROGRAM_EXTENSIONS and any(part.lower() in {"kernel", "src", "source", "codeparser", "packages", "libraryresources"} for part in rel.parts):
        tier = 0
    elif suffix in PROGRAM_EXTENSIONS:
        tier = 1
    elif suffix in NOTEBOOK_EXTENSIONS:
        tier = 2
    elif name in ADMIN_NAMES:
        tier = 7
    elif suffix in {".json", ".toml", ".yaml", ".yml", ".xml"}:
        tier = 3
    elif suffix in {".md", ".rst", ".txt"}:
        tier = 5
    else:
        tier = 4
    return tier, str(rel).lower()


def selected_paths_for_repo(repo: str, root: Path, include_paths):
    if include_paths and repo in include_paths:
        out = []
        for rel in include_paths[repo]:
            path = root / rel
            if path.is_file():
                out.append(path)
            elif path.is_dir():
                out.extend(p for p in path.rglob("*") if p.is_file())
    else:
        out = [p for p in root.rglob("*") if p.is_file()]
    return sorted(set(out), key=lambda path: path_priority(path, root))


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
        for path in selected_paths_for_repo(repo, root, include_paths):
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
                "selection_tier": path_priority(path, root)[0],
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
    tiers = collections.Counter(str(file.get("selection_tier", "unknown")) for file in files)
    bigrams = collections.Counter()
    tokens = forge.IDENTIFIER_RE.findall(text[:5_000_000])
    for a, b in zip(tokens, tokens[1:]):
        if a != b:
            bigrams[(a, b)] += 1
    return {
        "schema": "WOLFRAM-WHITE-ROOM-METHOD-SHADOW-v3",
        "focus": focus,
        "nonreconstructive": True,
        "framing_excluded": True,
        "program_files_prioritized": True,
        "source_corpus_sha256": forge.sha256(corpus),
        "source_text_sha256": forge.sha256(text.encode("utf-8", errors="replace")),
        "file_count": len(files),
        "extension_counts": dict(sorted(ext.items())),
        "selection_tier_counts": dict(sorted(tiers.items())),
        "top_identifiers": [{"name": k, "count": v} for k, v in identifiers.most_common(512)],
        "top_wolfram_symbols": [{"name": k, "count": v} for k, v in builtins.most_common(512)],
        "top_identifier_edges": [
            {"from": a, "to": b, "count": v} for (a, b), v in bigrams.most_common(512)
        ],
        "formula_candidates": formulas,
    }


forge.classify_license = classify_license
forge.selected_paths_for_repo = selected_paths_for_repo
forge.build_corpus = build_corpus
forge.method_shadow = method_shadow
forge.main()
