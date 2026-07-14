#!/usr/bin/env python3
"""Build one exact reversible cube from an explicitly licensed source repository."""
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
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

TEXT_EXTENSIONS_DEFAULT = {".py", ".wl", ".wlt", ".m", ".rs", ".c", ".cc", ".cpp", ".h", ".hpp", ".md", ".rst", ".txt", ".json", ".toml", ".yaml", ".yml", ".sh"}
MAX_FILE_BYTES = 400_000

LICENSE_MARKERS = {
    "MIT": ["Permission is hereby granted, free of charge", "THE SOFTWARE IS PROVIDED \"AS IS\""],
    "Apache-2.0": ["Apache License", "Version 2.0", "http://www.apache.org/licenses/"],
    "BSD-3-Clause": ["Redistribution and use in source and binary forms", "Neither the name", "THIS SOFTWARE IS PROVIDED"],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 900) -> str:
    result = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True, timeout=timeout)
    return result.stdout


def load_manifest(path: Path, source_id: str) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    return next(item for item in manifest["open_sources"] if item["id"] == source_id)


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_license(repo: Path, source: dict[str, Any]) -> tuple[Path, bytes]:
    expected = source["expected_license"]
    markers = LICENSE_MARKERS[expected]
    for candidate in source["license_paths"]:
        path = repo / candidate
        if not path.exists():
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        if all(marker.lower() in text.lower() for marker in markers):
            return path, raw
    raise RuntimeError(f"license gate failed: expected {expected}")


def select_corpus(repo: Path, source: dict[str, Any]) -> tuple[bytes, list[dict[str, Any]]]:
    extensions = set(source.get("include_extensions") or TEXT_EXTENSIONS_DEFAULT)
    limit = int(source.get("max_corpus_bytes", 1_000_000))
    selected: list[tuple[str, Path]] = []
    for path in repo.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in extensions:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size == 0 or size > MAX_FILE_BYTES:
            continue
        selected.append((str(path.relative_to(repo)), path))
    selected.sort(key=lambda item: item[0].lower())

    chunks: list[bytes] = []
    files: list[dict[str, Any]] = []
    total = 0
    for relative, path in selected:
        raw = path.read_bytes()
        header = f"\n===== FILE {relative} =====\n".encode("utf-8")
        available = limit - total
        if available <= 0:
            break
        content = header + raw
        if len(content) > available:
            content = content[:available]
        chunks.append(content)
        files.append({"path": relative, "source_bytes": len(raw), "included_bytes": max(0, len(content) - len(header)), "sha256": sha256(raw)})
        total += len(content)
        if total >= limit:
            break
    corpus = b"".join(chunks)
    if not corpus:
        raise RuntimeError("deterministic corpus selection produced no bytes")
    return corpus, files


def baseline_rows(data: bytes) -> list[dict[str, Any]]:
    rows = []
    for name, encode, decode in [
        ("gzip-9", lambda x: gzip.compress(x, compresslevel=9), gzip.decompress),
        ("bzip2-9", lambda x: bz2.compress(x, compresslevel=9), bz2.decompress),
        ("xz-6", lambda x: lzma.compress(x, preset=6), lzma.decompress),
    ]:
        payload = encode(data)
        restored = decode(payload)
        rows.append({"name": name, "payload_bytes": len(payload), "bpc": len(payload) * 8 / len(data), "restore": restored == data})
    try:
        import zstandard as zstd
        payload = zstd.ZstdCompressor(level=19).compress(data)
        restored = zstd.ZstdDecompressor().decompress(payload, max_output_size=len(data))
        rows.append({"name": "zstd-19", "payload_bytes": len(payload), "bpc": len(payload) * 8 / len(data), "restore": restored == data})
    except Exception as exc:
        rows.append({"name": "zstd-19", "status": "HELD", "error": f"{type(exc).__name__}: {exc}"})
    return rows


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    source = load_manifest(Path(args.manifest), args.source_id)
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="asolaria-open-cube-") as temp:
        checkout = Path(temp) / "source"
        run(["git", "clone", "--depth", "1", "--branch", source["ref"], f"https://github.com/{source['repo']}.git", str(checkout)])
        commit = run(["git", "rev-parse", "HEAD"], cwd=checkout).strip()
        commit_time = run(["git", "show", "-s", "--format=%cI", "HEAD"], cwd=checkout).strip()
        license_path, license_bytes = verify_license(checkout, source)
        corpus, files = select_corpus(checkout, source)

        bpe_path = repo_root / "third-seat-2026-07-12" / "gpt-crosscheck" / "multilevel_bpe_zstd_v1.py"
        bpe = import_module(bpe_path, f"open_cube_{args.source_id.replace('-', '_')}")
        candidates = []
        packages = []
        for levels_n in (1, 2, 3):
            catalog, payload, levels, tokens, trace = bpe.encode(corpus, levels_n, 256)
            restored = bpe.decode(catalog, payload, levels, len(tokens), len(corpus))
            total = len(catalog) + len(payload)
            row = {
                "levels": levels_n,
                "merges_per_level": 256,
                "catalog_bytes": len(catalog),
                "payload_bytes": len(payload),
                "total_bytes": total,
                "bpc": total * 8 / len(corpus),
                "token_count": len(tokens),
                "restore": restored == corpus,
                "sha_in": sha256(corpus),
                "sha_out": sha256(restored),
                "trace": trace,
            }
            candidates.append(row)
            packages.append((catalog, payload))
        if not all(row["restore"] for row in candidates):
            raise RuntimeError("restore gate failed")
        best_index = min(range(len(candidates)), key=lambda index: candidates[index]["total_bytes"])
        best = candidates[best_index]
        catalog, payload = packages[best_index]

        manifest = {
            "schema": "OPEN-LICENSE-REVERSIBLE-CUBE-v1",
            "source_id": args.source_id,
            "repo": source["repo"],
            "ref_requested": source["ref"],
            "commit": commit,
            "commit_time": commit_time,
            "license": source["expected_license"],
            "license_path": str(license_path.relative_to(checkout)),
            "license_sha256": sha256(license_bytes),
            "corpus_bytes": len(corpus),
            "corpus_sha256": sha256(corpus),
            "included_file_count": len(files),
            "best_level": best["levels"],
            "best_catalog_bytes": len(catalog),
            "best_payload_bytes": len(payload),
            "best_total_bytes": len(catalog) + len(payload),
            "best_bpc": best["bpc"],
            "byte_identical_restore": True,
            "candidates": candidates,
            "baselines": baseline_rows(corpus),
            "attribution_required": True,
            "raw_checkout_retained": False,
            "cube_reconstructs_selected_open_license_corpus": True,
        }
        manifest_sha = sha256(canonical(manifest))
        manifest["cube_manifest_sha256"] = manifest_sha

        (out / "catalog.bin").write_bytes(catalog)
        (out / "payload.zst").write_bytes(payload)
        (out / "license.txt").write_bytes(license_bytes)
        (out / "source-files.json").write_text(json.dumps(files, indent=2), encoding="utf-8")
        (out / "cube-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        (out / "cube.hbp").write_text(
            "OPENCUBEv1"
            f"|source={args.source_id}|repo={source['repo']}|commit={commit}|license={source['expected_license']}"
            f"|corpus_bytes={len(corpus)}|corpus_sha256={sha256(corpus)}|levels={best['levels']}"
            f"|catalog_bytes={len(catalog)}|payload_bytes={len(payload)}|bpc={best['bpc']:.9f}"
            f"|restore=1|manifest_sha256={manifest_sha}|json=0\n",
            encoding="utf-8"
        )
        sums = []
        for name in ("catalog.bin", "payload.zst", "license.txt", "source-files.json", "cube-manifest.json", "cube.hbp"):
            sums.append(f"{sha256((out / name).read_bytes())}  {name}")
        (out / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
        print(f"OPENCUBE|source={args.source_id}|repo={source['repo']}|commit={commit}|license={source['expected_license']}|corpus_bytes={len(corpus)}|bpc={best['bpc']:.9f}|restore=1|json=0")


if __name__ == "__main__":
    main()
