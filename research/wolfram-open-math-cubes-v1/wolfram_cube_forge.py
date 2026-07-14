#!/usr/bin/env python3
"""Forge one license-gated reversible Wolfram/open-math cube.

Each lane:
- clones exact public repositories and records commits;
- verifies a compatible license before using WolframResearch bytes;
- frames selected source files into one exact binary corpus;
- trains one-, two-, and three-level reversible BPE/glyph cubes;
- runs same-corpus lossless baselines;
- emits a non-reconstructive method/formula shadow;
- writes self-contained cube manifests and payloads;
- proves byte-identical restoration before any result is accepted.

The cube is a typed information structure, not automatically an AI agent.
"""
from __future__ import annotations

import argparse
import base64
import bz2
import collections
import datetime as dt
import gzip
import hashlib
import importlib.util
import json
import lzma
import os
import re
import shutil
import struct
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import zstandard as zstd

MAGIC = b"WOLFRAM-CUBE-CORPUS-v1\x00"
MAX_CORPUS_BYTES = 1_000_000
MAX_FILE_BYTES = 500_000
MERGES_PER_LEVEL = 256
ALLOWED_LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "OWNER-SOURCE"}
TEXT_EXTENSIONS = {
    ".wl", ".wls", ".m", ".mt", ".wlt", ".nb",
    ".py", ".rs", ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp",
    ".js", ".jsx", ".ts", ".tsx", ".java", ".scala",
    ".md", ".rst", ".txt", ".json", ".toml", ".yaml", ".yml",
    ".xml", ".html", ".css", ".sh", ".ps1", ".cmake",
}
EXCLUDED_PARTS = {
    ".git", "node_modules", "vendor", "target", "build", "dist", ".venv",
    "venv", "__pycache__", ".idea", ".vscode-test", "coverage", "docs/_build",
}
IDENTIFIER_RE = re.compile(r"[A-Za-z$][A-Za-z0-9$`_]{2,}")
FORMULA_RE = re.compile(
    r"(?:\b(?:Plus|Times|Power|Sum|Product|Integrate|D|Solve|Reduce|FindRoot|"
    r"Eigenvalues|MatrixRank|Entropy|Probability|Expectation|Fourier|LaplaceTransform|"
    r"QuantumState|QuantumOperator|QuantumCircuit)\b|[=<>+*/^]{2,}|->|:>|/\.|"
    r"\b(?:rank|nullity|entropy|probability|gradient|tensor|matrix|integral|derivative)\b)",
    re.IGNORECASE,
)


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_cmd(cmd: list[str], cwd: Path | None = None, timeout: int = 900) -> str:
    cp = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, timeout=timeout, check=True)
    return cp.stdout


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def clone_repo(repo: str, destination: Path) -> dict[str, Any]:
    run_cmd(["git", "clone", "--depth", "1", "--no-tags", f"https://github.com/{repo}.git", str(destination)])
    return {
        "repo": repo,
        "commit": run_cmd(["git", "rev-parse", "HEAD"], destination).strip(),
        "commit_time": run_cmd(["git", "show", "-s", "--format=%cI", "HEAD"], destination).strip(),
        "default_branch": run_cmd(["git", "branch", "--show-current"], destination).strip(),
    }


def find_license_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue
        name = path.name.lower()
        if name.startswith("license") or name.startswith("copying") or name in {"notice", "copyright"}:
            candidates.append(path)
    return candidates


def classify_license(text: str) -> str:
    low = text.lower()
    if "mit license" in low and "permission is hereby granted" in low:
        return "MIT"
    if "apache license" in low and "version 2.0" in low:
        return "Apache-2.0"
    if "redistribution and use in source and binary forms" in low:
        if "neither the name" in low or "contributors may be used" in low:
            return "BSD-3-Clause"
        return "BSD-2-Clause"
    return "UNKNOWN"


def verify_license(repo: str, root: Path) -> dict[str, Any]:
    if repo.startswith("JesseBrown1980/"):
        return {
            "classification": "OWNER-SOURCE",
            "allowed": True,
            "files": [],
            "note": "operator-owned repository included only in the bridge lane",
        }
    files = find_license_files(root)
    records = []
    classifications = []
    for path in files:
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        classification = classify_license(text)
        classifications.append(classification)
        records.append({
            "path": path.name,
            "bytes": len(raw),
            "sha256": sha256(raw),
            "classification": classification,
        })
    accepted = next((x for x in classifications if x in ALLOWED_LICENSES), "UNKNOWN")
    return {
        "classification": accepted,
        "allowed": accepted in ALLOWED_LICENSES,
        "files": records,
    }


def selected_paths_for_repo(repo: str, root: Path, include_paths: dict[str, list[str]] | None) -> list[Path]:
    if include_paths and repo in include_paths:
        out = []
        for rel in include_paths[repo]:
            path = root / rel
            if path.is_file():
                out.append(path)
            elif path.is_dir():
                out.extend(p for p in path.rglob("*") if p.is_file())
        return sorted(set(out))
    return sorted(p for p in root.rglob("*") if p.is_file())


def should_include(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return False
    try:
        size = path.stat().st_size
    except OSError:
        return False
    return 0 < size <= MAX_FILE_BYTES


def build_corpus(accepted: list[dict[str, Any]], include_paths: dict[str, list[str]] | None) -> tuple[bytes, list[dict[str, Any]]]:
    corpus = bytearray(MAGIC)
    files: list[dict[str, Any]] = []
    for source in accepted:
        repo = source["repo"]
        root = Path(source["local_path"])
        for path in selected_paths_for_repo(repo, root, include_paths):
            if not should_include(path, root):
                continue
            raw = path.read_bytes()
            repo_b = repo.encode("utf-8")
            rel = str(path.relative_to(root)).replace("\\", "/")
            path_b = rel.encode("utf-8")
            frame_len = 2 + 2 + 8 + 32 + len(repo_b) + len(path_b) + len(raw)
            if len(corpus) + frame_len > MAX_CORPUS_BYTES and files:
                return bytes(corpus), files
            if len(corpus) + frame_len > MAX_CORPUS_BYTES:
                raw = raw[: max(0, MAX_CORPUS_BYTES - len(corpus) - (2 + 2 + 8 + 32 + len(repo_b) + len(path_b)))]
            if not raw:
                continue
            digest = hashlib.sha256(raw).digest()
            corpus.extend(struct.pack(">HHQ", len(repo_b), len(path_b), len(raw)))
            corpus.extend(digest)
            corpus.extend(repo_b)
            corpus.extend(path_b)
            corpus.extend(raw)
            files.append({
                "repo": repo,
                "path": rel,
                "bytes": len(raw),
                "sha256": digest.hex(),
                "extension": path.suffix.lower(),
            })
            if len(corpus) >= MAX_CORPUS_BYTES:
                return bytes(corpus), files
    return bytes(corpus), files


def parse_corpus(corpus: bytes) -> list[dict[str, Any]]:
    if not corpus.startswith(MAGIC):
        raise ValueError("bad corpus magic")
    pos = len(MAGIC)
    records = []
    while pos < len(corpus):
        if pos + 44 > len(corpus):
            raise ValueError("truncated frame header")
        repo_len, path_len, data_len = struct.unpack(">HHQ", corpus[pos:pos + 12])
        pos += 12
        digest = corpus[pos:pos + 32]
        pos += 32
        end_names = pos + repo_len + path_len
        if end_names > len(corpus):
            raise ValueError("truncated names")
        repo = corpus[pos:pos + repo_len].decode("utf-8")
        pos += repo_len
        path = corpus[pos:pos + path_len].decode("utf-8")
        pos += path_len
        end = pos + data_len
        if end > len(corpus):
            raise ValueError("truncated data")
        data = corpus[pos:end]
        pos = end
        if hashlib.sha256(data).digest() != digest:
            raise ValueError(f"file digest mismatch: {repo}:{path}")
        records.append({"repo": repo, "path": path, "bytes": data_len, "sha256": digest.hex()})
    return records


def encode_cube(corpus: bytes, bpe: Any, out: Path) -> dict[str, Any]:
    candidates = []
    for level_count in (1, 2, 3):
        t0 = time.perf_counter()
        catalog, payload, levels, tokens, trace = bpe.encode(corpus, level_count, MERGES_PER_LEVEL)
        encode_s = time.perf_counter() - t0
        t0 = time.perf_counter()
        restored = bpe.decode(catalog, payload, levels, len(tokens), len(corpus))
        decode_s = time.perf_counter() - t0
        exact = restored == corpus and sha256(restored) == sha256(corpus)
        model = {
            "schema": "WOLFRAM-REVERSIBLE-GLYPH-CUBE-v1",
            "orig_len": len(corpus),
            "orig_sha256": sha256(corpus),
            "token_count": len(tokens),
            "payload_file": f"cube-L{level_count}.payload.zst",
            "payload_sha256": sha256(payload),
            "levels": [
                {"start_id": int(level.start_id), "rules": [[int(a), int(b)] for a, b in level.rules]}
                for level in levels
            ],
        }
        model_bytes = json.dumps(model, sort_keys=True, separators=(",", ":")).encode()
        total = len(model_bytes) + len(payload)
        (out / f"cube-L{level_count}.payload.zst").write_bytes(payload)
        (out / f"cube-L{level_count}.model.json").write_bytes(json.dumps(model, indent=2).encode())
        candidates.append({
            "levels": level_count,
            "rules": sum(len(level.rules) for level in levels),
            "model_bytes": len(model_bytes),
            "payload_bytes": len(payload),
            "total_bytes": total,
            "bpc": total * 8 / len(corpus),
            "tokens": len(tokens),
            "restore": exact,
            "encode_s": encode_s,
            "decode_s": decode_s,
            "trace": trace,
        })
    best = min(candidates, key=lambda x: x["total_bytes"])
    return {
        "status": "MEASURED" if all(x["restore"] for x in candidates) else "HELD_RESTORE_FAILURE",
        "candidates": candidates,
        "best_level": best["levels"],
        "best_bpc": best["bpc"],
        "best_total_bytes": best["total_bytes"],
        "all_restore": all(x["restore"] for x in candidates),
    }


def baseline_rows(corpus: bytes, codec: Any | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(name: str, payload: bytes, restored: bytes, elapsed: float) -> None:
        rows.append({
            "name": name,
            "bytes": len(payload),
            "bpc": len(payload) * 8 / len(corpus),
            "restore": restored == corpus,
            "elapsed_s": elapsed,
        })

    t0 = time.perf_counter(); payload = gzip.compress(corpus, compresslevel=9); elapsed = time.perf_counter() - t0
    add("gzip-9", payload, gzip.decompress(payload), elapsed)
    t0 = time.perf_counter(); payload = bz2.compress(corpus, compresslevel=9); elapsed = time.perf_counter() - t0
    add("bzip2-9", payload, bz2.decompress(payload), elapsed)
    t0 = time.perf_counter(); payload = lzma.compress(corpus, preset=6); elapsed = time.perf_counter() - t0
    add("xz-6", payload, lzma.decompress(payload), elapsed)
    t0 = time.perf_counter(); payload = zstd.ZstdCompressor(level=19).compress(corpus); elapsed = time.perf_counter() - t0
    add("zstd-19", payload, zstd.ZstdDecompressor().decompress(payload, max_output_size=len(corpus)), elapsed)
    if codec is not None:
        try:
            t0 = time.perf_counter(); payload = codec.compress(corpus); elapsed = time.perf_counter() - t0
            restored = codec.decompress(payload, len(corpus))
            add("asolaria-codec-v0.1", payload, restored, elapsed)
        except Exception as exc:
            rows.append({"name": "asolaria-codec-v0.1", "status": "HELD", "error": f"{type(exc).__name__}: {exc}"})
    return rows


def method_shadow(corpus: bytes, files: list[dict[str, Any]], focus: list[str]) -> dict[str, Any]:
    text = corpus.decode("utf-8", errors="ignore")
    identifiers = collections.Counter(IDENTIFIER_RE.findall(text))
    builtins = collections.Counter(x for x in identifiers if x[:1].isupper() or "`" in x or x.startswith("$") )
    formulas = []
    for line in text.splitlines():
        clean = " ".join(line.strip().split())
        if 8 <= len(clean) <= 260 and FORMULA_RE.search(clean) and clean not in formulas:
            formulas.append(clean)
        if len(formulas) >= 150:
            break
    ext = collections.Counter(file["extension"] or "<none>" for file in files)
    bigrams = collections.Counter()
    tokens = IDENTIFIER_RE.findall(text[:5_000_000])
    for a, b in zip(tokens, tokens[1:]):
        if a != b:
            bigrams[(a, b)] += 1
    return {
        "schema": "WOLFRAM-WHITE-ROOM-METHOD-SHADOW-v1",
        "focus": focus,
        "nonreconstructive": True,
        "source_corpus_sha256": sha256(corpus),
        "file_count": len(files),
        "extension_counts": dict(sorted(ext.items())),
        "top_identifiers": [{"name": k, "count": v} for k, v in identifiers.most_common(512)],
        "top_wolfram_symbols": [{"name": k, "count": v} for k, v in builtins.most_common(512)],
        "top_identifier_edges": [{"from": a, "to": b, "count": v} for (a, b), v in bigrams.most_common(512)],
        "formula_candidates": formulas,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--lane", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--repo-root", default=".")
    p.add_argument("--min-runtime", type=float, default=90.0)
    args = p.parse_args()

    started = now_utc(); start_epoch = time.time(); start_mono = time.monotonic()
    out = Path(args.output).resolve(); out.mkdir(parents=True, exist_ok=True)
    work = out / "work"; work.mkdir(exist_ok=True)
    repo_root = Path(args.repo_root).resolve()
    manifest = json.loads(Path(args.manifest).read_text())
    lane = next(x for x in manifest["lanes"] if x["id"] == args.lane)
    errors: list[str] = []
    sources: list[dict[str, Any]] = []
    accepted: list[dict[str, Any]] = []
    held: list[dict[str, Any]] = []
    corpus = b""
    files: list[dict[str, Any]] = []
    cube: dict[str, Any] | None = None
    baselines: list[dict[str, Any]] = []
    shadow: dict[str, Any] | None = None
    status = "MEASURED"

    try:
        for index, repo in enumerate(lane["repos"]):
            local = work / f"repo-{index:02d}"
            source = clone_repo(repo, local)
            license_info = verify_license(repo, local)
            source["license"] = license_info
            source["local_path"] = str(local)
            sources.append(source)
            if license_info["allowed"]:
                accepted.append(source)
            else:
                held.append({"repo": repo, "reason": "HELD_LICENSE_UNKNOWN_OR_UNSUPPORTED", "license": license_info})
        if not accepted:
            status = "HELD_NO_LICENSED_SOURCE"
        else:
            corpus, files = build_corpus(accepted, lane.get("include_paths"))
            parsed = parse_corpus(corpus)
            if len(parsed) != len(files):
                raise AssertionError("framed corpus file-count mismatch")
            bpe = import_module(repo_root / "third-seat-2026-07-12" / "gpt-crosscheck" / "multilevel_bpe_zstd_v1.py", "wolfram_cube_bpe")
            codec = import_module(repo_root / "third-seat-2026-07-12" / "asolaria_codec_v0_1.py", "wolfram_cube_codec")
            cube = encode_cube(corpus, bpe, out)
            baselines = baseline_rows(corpus, codec)
            shadow = method_shadow(corpus, files, lane.get("focus", []))
            (out / "method-shadow.json").write_text(json.dumps(shadow, indent=2), encoding="utf-8")
            if not cube["all_restore"] or not all(row.get("restore", True) for row in baselines):
                status = "HELD_RESTORE_FAILURE"
    except Exception as exc:
        status = "HELD_ERROR"
        errors.append(f"{type(exc).__name__}: {exc}")
        errors.append(traceback.format_exc(limit=30))

    elapsed = time.monotonic() - start_mono
    if elapsed < args.min_runtime:
        time.sleep(args.min_runtime - elapsed)
    ended = now_utc(); end_epoch = time.time()

    result_body = {
        "schema": "ASOLARIA-WOLFRAM-OPEN-MATH-CUBE-v1",
        "lane": lane,
        "status": status,
        "sources": [{k: v for k, v in source.items() if k != "local_path"} for source in sources],
        "accepted_repos": [x["repo"] for x in accepted],
        "held_repos": held,
        "corpus": {
            "bytes": len(corpus),
            "sha256": sha256(corpus),
            "file_count": len(files),
            "files": files,
            "framing": "WOLFRAM-CUBE-CORPUS-v1",
            "source_reconstructable": True,
        },
        "cube": cube,
        "baselines": baselines,
        "method_shadow": shadow,
        "cube_kind": "LEARNED_CODEBOOK_PLUS_EXACT_REPRESENTATION",
        "byte_exact_restore": bool(cube and cube.get("all_restore")),
        "executable_agent": False,
        "errors": errors,
        "runtime": {
            "started_at": started,
            "ended_at": ended,
            "started_epoch": start_epoch,
            "ended_epoch": end_epoch,
            "elapsed_seconds": end_epoch - start_epoch,
            "runner_name": os.environ.get("RUNNER_NAME"),
            "runner_os": os.environ.get("RUNNER_OS"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_sha": os.environ.get("GITHUB_SHA"),
        },
    }
    digest = sha256(json.dumps(result_body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
    result = {**result_body, "receipt_sha256": digest}
    (out / "cube-result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (out / "file-manifest.json").write_text(json.dumps(files, indent=2), encoding="utf-8")
    hbp = (
        f"WOLFRAMCUBEv1|lane={lane['id']}|status={status}|repos={len(sources)}|accepted={len(accepted)}|"
        f"corpus_bytes={len(corpus)}|files={len(files)}|corpus_sha256={sha256(corpus)}|"
        f"best_bpc={(cube or {}).get('best_bpc','NA')}|restore={int(bool(cube and cube.get('all_restore')))}|"
        f"receipt_sha256={digest}|json=0\n"
    )
    (out / "cube-result.hbp").write_text(hbp, encoding="utf-8")
    summary = [
        f"# Wolfram cube — {lane['id']}", "",
        f"- Status: `{status}`",
        f"- Accepted repositories: {len(accepted)} / {len(sources)}",
        f"- Framed corpus: {len(corpus):,} bytes across {len(files):,} files",
        f"- Corpus SHA-256: `{sha256(corpus)}`",
        f"- Cube kind: `LEARNED_CODEBOOK_PLUS_EXACT_REPRESENTATION`",
        f"- Byte-exact restore: `{bool(cube and cube.get('all_restore'))}`",
        f"- Executable agent: `false`", "",
        "## Sources", "",
    ]
    for source in sources:
        summary.append(f"- `{source['repo']}@{source['commit']}` — `{source['license']['classification']}` — allowed `{source['license']['allowed']}`")
    if cube:
        summary.extend(["", "## Cube candidates", "", "| Levels | Rules | Model B | Payload B | Total B | bpc | Restore |", "|---:|---:|---:|---:|---:|---:|---|"])
        for row in cube["candidates"]:
            summary.append(f"| {row['levels']} | {row['rules']} | {row['model_bytes']} | {row['payload_bytes']} | {row['total_bytes']} | {row['bpc']:.6f} | {row['restore']} |")
    if baselines:
        summary.extend(["", "## Same-corpus baselines", "", "| Method | Bytes | bpc | Restore |", "|---|---:|---:|---|"])
        for row in sorted((r for r in baselines if "bpc" in r), key=lambda r: r["bpc"]):
            summary.append(f"| {row['name']} | {row['bytes']} | {row['bpc']:.6f} | {row['restore']} |")
    if held:
        summary.extend(["", "## Held components", ""])
        for item in held:
            summary.append(f"- `{item['repo']}` — `{item['reason']}`")
    if errors:
        summary.extend(["", "## Errors", "", "```text", "\n".join(errors), "```"])
    (out / "SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    names = ["cube-result.json", "cube-result.hbp", "file-manifest.json", "SUMMARY.md"]
    if (out / "method-shadow.json").exists():
        names.append("method-shadow.json")
    names.extend(sorted(path.name for path in out.glob("cube-L*.*")))
    (out / "SHA256SUMS").write_text("\n".join(f"{sha256((out/name).read_bytes())}  {name}" for name in names) + "\n", encoding="utf-8")
    print(f"WOLFRAMCUBE|lane={lane['id']}|status={status}|accepted={len(accepted)}|corpus_bytes={len(corpus)}|best_bpc={(cube or {}).get('best_bpc','NA')}|restore={int(bool(cube and cube.get('all_restore')))}|json=0")


if __name__ == "__main__":
    main()
