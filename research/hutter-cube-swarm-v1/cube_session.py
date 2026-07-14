#!/usr/bin/env python3
"""Run one source-pinned Asolaria/Hutter research cube session.

The runner is deliberately deterministic where source bytes are stable. It performs
source archaeology, extracts algorithm/formula/people vocabulary, optionally trains
an exact reversible BPE/glyph cube, and emits JSON/HBP/Markdown receipts. A missing
private input is a HELD result, not an excuse to substitute unrelated data.
"""
from __future__ import annotations

import argparse
import base64
import bz2
import collections
import datetime as dt
import gzip
import hashlib
import html
import json
import lzma
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable

TEXT_EXTENSIONS = {
    ".md", ".txt", ".rst", ".hbp", ".json", ".yaml", ".yml", ".toml",
    ".py", ".rs", ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".mjs",
    ".js", ".ts", ".sh", ".ipynb", ".xml", ".html", ".htm", ".csv",
}
MAX_FILE_BYTES = 800_000
MAX_CORPUS_BYTES = 12_000_000
TRAIN_BYTES = 1_000_000
USER_AGENT = "Asolaria-Hutter-Cube-Swarm/1.0 (+https://github.com/JesseBrown1980)"

ALGORITHM_VOCAB = [
    "arithmetic coding", "range coder", "ans", "rans", "tans", "fse",
    "context mixing", "context map", "context tree weighting", "ctw", "ppm", "ppmd",
    "match model", "sparse match", "lstm", "transformer", "mamba", "state space model",
    "apm", "sse", "state map", "mixer", "logistic mixer", "stemmer", "dictionary transform",
    "reverse dictionary", "article ordering", "tsne", "t-sne", "k-means", "embedding",
    "bpe", "glyph", "behcs", "hyperbehcs", "quant", "turbo", "polar", "zeta",
    "triple", "quadruple", "von mangoldt", "crt", "q-prism", "dbbh", "dbwh",
    "shannon", "omnishannon", "fischer", "hookwall", "gnn", "white room",
    "minimum description length", "mdl", "prequential", "online learning", "preprocessing",
    "burrows wheeler", "bwt", "lz", "lzp", "huffman", "word model", "byte model",
    "probability calibration", "probability matching", "pmatic", "mmap", "disk backed",
]

FORMULA_HINTS = re.compile(
    r"(?:\bH\s*\(|\bI\s*\(|\bP\s*\(|entropy|log2?|rank|nullity|bpc|bits?\s*/|"
    r"\bR\s*=|\bL\s*=|\bQ\s*=|\bSE\s*\(|\bargm(?:in|ax)|>=|<=|→|->|≈|∑|Σ|Π|Δ)",
    re.IGNORECASE,
)
NUMBER_HINT = re.compile(r"(?<![A-Za-z])(?:\d{1,3}(?:[,_ ]\d{3})+|\d+\.\d+|\d+)(?:\s*(?:bpc|bytes?|bits?|MB|GB|GiB|MiB|%|x|×))", re.IGNORECASE)
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_+./-]{2,}")
PERSON_RE = re.compile(r"\b([A-Z][a-zA-Z'’-]+(?:\s+[A-Z][a-zA-Z'’-]+){1,3})\b")


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "svg", "noscript"}:
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "svg", "noscript"} and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)

    def text(self) -> str:
        return html.unescape("\n".join(self.parts))


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_cmd(cmd: list[str], cwd: Path | None = None, timeout: int = 600,
            check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=timeout, check=check)


def fetch_url(url: str, timeout: int = 90) -> tuple[bytes, dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        headers = {k.lower(): v for k, v in response.headers.items()}
        return response.read(), headers


def strip_html(data: bytes) -> str:
    parser = TextExtractor()
    parser.feed(data.decode("utf-8", errors="replace"))
    return parser.text()


def clone_repo(repo: str, ref: str | None, destination: Path) -> dict[str, Any]:
    url = f"https://github.com/{repo}.git"
    run_cmd(["git", "clone", "--depth", "1", "--no-tags", url, str(destination)], timeout=600)
    if ref and ref not in {"main", "master"}:
        try:
            run_cmd(["git", "fetch", "--depth", "1", "origin", ref], cwd=destination, timeout=600)
            run_cmd(["git", "checkout", "FETCH_HEAD"], cwd=destination)
        except Exception:
            run_cmd(["git", "checkout", ref], cwd=destination)
    commit = run_cmd(["git", "rev-parse", "HEAD"], cwd=destination).stdout.strip()
    commit_time = run_cmd(["git", "show", "-s", "--format=%cI", "HEAD"], cwd=destination).stdout.strip()
    return {"repo": repo, "url": url, "ref_requested": ref, "commit": commit, "commit_time": commit_time}


def iter_text_files(root: Path, selected_paths: list[str] | None = None) -> Iterable[Path]:
    roots: list[Path] = []
    if selected_paths:
        for item in selected_paths:
            p = root / item
            if p.exists():
                roots.append(p)
    else:
        roots.append(root)
    seen: set[Path] = set()
    for base in roots:
        if base.is_file():
            candidates = [base]
        else:
            candidates = base.rglob("*")
        for path in candidates:
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            if ".git" in path.parts or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            try:
                size = path.stat().st_size
            except OSError:
                continue
            if size == 0 or size > MAX_FILE_BYTES:
                continue
            yield path


def collect_repo_text(root: Path, selected_paths: list[str] | None = None) -> tuple[str, list[dict[str, Any]]]:
    chunks: list[str] = []
    files: list[dict[str, Any]] = []
    total = 0
    for path in iter_text_files(root, selected_paths):
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if total + len(raw) > MAX_CORPUS_BYTES:
            remaining = MAX_CORPUS_BYTES - total
            if remaining <= 0:
                break
            raw = raw[:remaining]
        text = raw.decode("utf-8", errors="replace")
        relative = str(path.relative_to(root))
        chunks.append(f"\n\n===== FILE {relative} =====\n{text}")
        files.append({"path": relative, "bytes_read": len(raw), "sha256": sha256_bytes(raw)})
        total += len(raw)
        if total >= MAX_CORPUS_BYTES:
            break
    return "".join(chunks), files


def collect_github_repo(lane: dict[str, Any], work: Path) -> tuple[str, dict[str, Any]]:
    repo_dir = work / "repo"
    source = clone_repo(lane["repo"], lane.get("ref"), repo_dir)
    text, files = collect_repo_text(repo_dir, lane.get("paths"))
    source["files"] = files
    source["text_bytes"] = len(text.encode())
    return text, source


def collect_github_bundle(lane: dict[str, Any], work: Path) -> tuple[str, dict[str, Any]]:
    chunks: list[str] = []
    sources = []
    for index, repo in enumerate(lane["repos"]):
        repo_dir = work / f"repo-{index:02d}"
        source = clone_repo(repo, None, repo_dir)
        text, files = collect_repo_text(repo_dir)
        source["files"] = files
        source["text_bytes"] = len(text.encode())
        sources.append(source)
        chunks.append(f"\n\n######## REPOSITORY {repo} ########\n{text}")
    return "".join(chunks), {"sources": sources}


def collect_web_bundle(lane: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    chunks: list[str] = []
    sources = []
    for url in lane["urls"]:
        try:
            raw, headers = fetch_url(url)
            ctype = headers.get("content-type", "")
            text = strip_html(raw) if "html" in ctype or raw[:100].lower().find(b"<html") >= 0 else raw.decode("utf-8", errors="replace")
            chunks.append(f"\n\n######## URL {url} ########\n{text[:MAX_CORPUS_BYTES]}")
            sources.append({"url": url, "bytes": len(raw), "sha256": sha256_bytes(raw), "content_type": ctype, "status": "FETCHED"})
        except Exception as exc:
            sources.append({"url": url, "status": "HELD_SOURCE_UNAVAILABLE", "error": f"{type(exc).__name__}: {exc}"})
    if not chunks:
        raise RuntimeError("no web source could be fetched")
    return "".join(chunks), {"sources": sources}


def collect_arxiv(lane: dict[str, Any], work: Path) -> tuple[str, dict[str, Any]]:
    arxiv_id = lane["arxiv_id"]
    sources = []
    chunks = []
    abstract_url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    raw, headers = fetch_url(abstract_url)
    chunks.append(raw.decode("utf-8", errors="replace"))
    sources.append({"url": abstract_url, "bytes": len(raw), "sha256": sha256_bytes(raw), "status": "FETCHED"})
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
    try:
        pdf, pdf_headers = fetch_url(pdf_url, timeout=180)
        pdf_path = work / f"{arxiv_id}.pdf"
        pdf_path.write_bytes(pdf)
        sources.append({"url": pdf_url, "bytes": len(pdf), "sha256": sha256_bytes(pdf), "status": "FETCHED"})
        if shutil.which("pdftotext"):
            txt_path = work / f"{arxiv_id}.txt"
            run_cmd(["pdftotext", "-layout", str(pdf_path), str(txt_path)], timeout=180)
            chunks.append(txt_path.read_text(encoding="utf-8", errors="replace")[:MAX_CORPUS_BYTES])
    except Exception as exc:
        sources.append({"url": pdf_url, "status": "PDF_HELD", "error": f"{type(exc).__name__}: {exc}"})
    return "\n\n".join(chunks), {"arxiv_id": arxiv_id, "sources": sources}


def collect_google_docs(lane: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    chunks = []
    sources = []
    for doc_id in lane["document_ids"]:
        candidates = [
            f"https://docs.google.com/document/d/{doc_id}/export?format=txt",
            f"https://docs.google.com/document/d/{doc_id}/export?format=html",
        ]
        fetched = False
        for url in candidates:
            try:
                raw, headers = fetch_url(url)
                if len(raw) < 50:
                    continue
                ctype = headers.get("content-type", "")
                text = strip_html(raw) if "html" in ctype else raw.decode("utf-8", errors="replace")
                chunks.append(f"\n\n######## GOOGLE DOC {doc_id} ########\n{text}")
                sources.append({"document_id": doc_id, "url": url, "bytes": len(raw), "sha256": sha256_bytes(raw), "status": "FETCHED"})
                fetched = True
                break
            except Exception:
                continue
        if not fetched:
            sources.append({"document_id": doc_id, "status": "HELD_PERMISSION_OR_CONNECTOR_REQUIRED"})
    if not chunks:
        raise RuntimeError("public Google documents were not exportable")
    return "".join(chunks), {"sources": sources}


def gather_training_corpus(kind: str, work: Path) -> tuple[bytes, dict[str, Any]]:
    sources = []
    chunks: list[bytes] = []

    def add_repo(repo: str, ref: str | None = None, paths: list[str] | None = None) -> None:
        destination = work / f"train-{len(sources):02d}"
        source = clone_repo(repo, ref, destination)
        text, files = collect_repo_text(destination, paths)
        source["files"] = files
        source["text_bytes"] = len(text.encode())
        sources.append(source)
        chunks.append(text.encode("utf-8", errors="replace"))

    if kind == "train_public_plan_b":
        add_repo("JesseBrown1980/asolaria-behcs-256", "802023a9588cf3c72be9f9b353c847f22c616092",
                 ["data/agent-index/references", "data/agent-index/patterns", "data/agent-index/CHAINS.md"])
    elif kind == "train_hutter_methods":
        for repo, ref in [
            ("kaitz/fx2-cmix", "main"), ("kaitz/fx-cmix", "main"),
            ("saurabhk/fast-cmix", "main"), ("amargaritov/starlit", "master"),
            ("byronknoll/cmix", "master"), ("kaitz/paq8pxd", "master"),
        ]:
            add_repo(repo, ref, ["README.md", "src"])
    elif kind == "train_combined_benchmark":
        add_repo("JesseBrown1980/Algorithms-of-Asolaria", "main")
        add_repo("JesseBrown1980/HYPER-BECHS--the-third-set", "main",
                 ["n-lens-v1", "n-vantage-30-v1", "omni-event-v1", "verification/fischer-bidirectional-10-runner"])
        add_repo("kaitz/fx2-cmix", "main", ["README.md", "src"])
        add_repo("saurabhk/fast-cmix", "main", ["README.md", "src"])
    else:
        raise ValueError(kind)

    corpus = b"\n\n".join(chunks)
    if len(corpus) > TRAIN_BYTES:
        corpus = corpus[:TRAIN_BYTES]
    return corpus, {"sources": sources, "corpus_bytes": len(corpus), "corpus_sha256": sha256_bytes(corpus)}


def import_module(path: Path, name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def train_reversible_cube(corpus: bytes, repo_root: Path, work: Path) -> dict[str, Any]:
    if not corpus:
        return {"status": "HELD_EMPTY_CORPUS"}
    data = corpus[:TRAIN_BYTES]
    source_path = work / "training-corpus.bin"
    source_path.write_bytes(data)
    bpe_path = repo_root / "third-seat-2026-07-12" / "gpt-crosscheck" / "multilevel_bpe_zstd_v1.py"
    if not bpe_path.exists():
        return {"status": "HELD_BPE_IMPLEMENTATION_MISSING"}
    bpe = import_module(bpe_path, "research_cube_bpe")
    rows = []
    for levels_n in (1, 2, 3):
        catalog, payload, levels, tokens, trace = bpe.encode(data, levels_n, 256)
        restored = bpe.decode(catalog, payload, levels, len(tokens), len(data))
        total = len(catalog) + len(payload)
        rows.append({
            "levels": levels_n,
            "merges_per_level": 256,
            "catalog_bytes": len(catalog),
            "payload_bytes": len(payload),
            "total_bytes": total,
            "bpc": total * 8 / len(data),
            "token_count": len(tokens),
            "restore": restored == data,
            "sha_in": sha256_bytes(data),
            "sha_out": sha256_bytes(restored),
            "trace": trace,
        })
    best = min(rows, key=lambda row: row["total_bytes"])
    return {"status": "MEASURED", "rows": rows, "best_level": best["levels"], "best_bpc": best["bpc"], "all_restore": all(row["restore"] for row in rows)}


def lossless_baselines(data: bytes, repo_root: Path) -> dict[str, Any]:
    if not data:
        return {"status": "HELD_EMPTY_CORPUS"}
    sample = data[: min(len(data), TRAIN_BYTES)]
    rows = []

    def add(name: str, payload: bytes, restored: bytes) -> None:
        rows.append({"name": name, "bytes": len(payload), "bpc": len(payload) * 8 / len(sample), "restore": restored == sample})

    gz = gzip.compress(sample, compresslevel=9)
    add("gzip-9", gz, gzip.decompress(gz))
    bz = bz2.compress(sample, compresslevel=9)
    add("bzip2-9", bz, bz2.decompress(bz))
    xz = lzma.compress(sample, preset=6)
    add("xz-6", xz, lzma.decompress(xz))
    try:
        import zstandard as zstd
        comp = zstd.ZstdCompressor(level=19).compress(sample)
        add("zstd-19", comp, zstd.ZstdDecompressor().decompress(comp, max_output_size=len(sample)))
    except Exception as exc:
        rows.append({"name": "zstd-19", "status": "HELD", "error": str(exc)})

    codec_path = repo_root / "third-seat-2026-07-12" / "asolaria_codec_v0_1.py"
    if codec_path.exists() and len(sample) <= 1_000_000:
        try:
            codec = import_module(codec_path, "research_codec_v01")
            comp = codec.compress(sample)
            restored = codec.decompress(comp, len(sample))
            add("asolaria-codec-v0.1", comp, restored)
        except Exception as exc:
            rows.append({"name": "asolaria-codec-v0.1", "status": "HELD", "error": f"{type(exc).__name__}: {exc}"})
    return {"status": "MEASURED", "sample_bytes": len(sample), "sample_sha256": sha256_bytes(sample), "rows": rows}


def private_input_gate(lane: dict[str, Any], repo_root: Path) -> tuple[bytes, dict[str, Any], str]:
    found = []
    hashes = []
    corpus_parts = []
    for expected in lane["expected_paths"]:
        path = repo_root / expected
        if path.exists():
            found.append(expected)
            for file in path.rglob("*") if path.is_dir() else [path]:
                if file.is_file():
                    raw = file.read_bytes()
                    hashes.append({"path": str(file.relative_to(repo_root)), "bytes": len(raw), "sha256": sha256_bytes(raw)})
                    if file.suffix.lower() in TEXT_EXTENSIONS and len(raw) <= MAX_FILE_BYTES:
                        corpus_parts.append(raw)
    if not found:
        return b"", {"expected_paths": lane["expected_paths"], "found": [], "raw_private_bytes_exported": 0}, "HELD_MISSING_PRIVATE_INPUT"
    corpus = b"\n".join(corpus_parts)[:TRAIN_BYTES]
    return corpus, {"expected_paths": lane["expected_paths"], "found": found, "file_hashes": hashes, "raw_private_bytes_exported": 0}, "PRIVATE_INPUT_HASHED_AND_TRAINABLE"


def extract_research(text: str, focus: list[str]) -> dict[str, Any]:
    normalized = text.replace("\x00", " ")
    lower = normalized.lower()
    tokens = [token.lower() for token in TOKEN_RE.findall(normalized)]
    stop = {"the", "and", "for", "with", "from", "this", "that", "are", "was", "were", "into", "using", "used", "use", "not", "can", "will", "file", "data", "code", "source", "https", "http", "github", "com"}
    counts = collections.Counter(token for token in tokens if token not in stop and len(token) > 2)
    bigrams = collections.Counter(zip(tokens, tokens[1:]))
    algorithms = []
    for term in ALGORITHM_VOCAB:
        count = lower.count(term)
        if count:
            algorithms.append({"term": term, "count": count})
    algorithms.sort(key=lambda x: (-x["count"], x["term"]))

    formulas = []
    numbers = []
    for raw_line in normalized.splitlines():
        line = " ".join(raw_line.strip().split())
        if not line or len(line) > 300:
            continue
        if FORMULA_HINTS.search(line) and line not in formulas:
            formulas.append(line)
            if len(formulas) >= 80:
                break
    for match in NUMBER_HINT.finditer(normalized):
        value = " ".join(match.group(0).split())
        if value not in numbers:
            numbers.append(value)
            if len(numbers) >= 80:
                break

    people_counts = collections.Counter()
    for candidate in PERSON_RE.findall(normalized[:4_000_000]):
        if any(word.lower() in {"the", "this", "license", "readme", "github", "human", "natural", "context", "compression", "asymmetric"} for word in candidate.split()):
            continue
        people_counts[candidate] += 1

    return {
        "focus": focus,
        "top_terms": [{"term": term, "count": count} for term, count in counts.most_common(120)],
        "top_bigrams": [{"bigram": f"{a} {b}", "count": count} for (a, b), count in bigrams.most_common(80)],
        "algorithm_hits": algorithms[:100],
        "formula_candidates": formulas,
        "number_candidates": numbers,
        "people_candidates": [{"name": name, "count": count} for name, count in people_counts.most_common(50)],
        "text_characters": len(normalized),
        "text_sha256": sha256_bytes(normalized.encode("utf-8", errors="replace")),
    }


def markdown_summary(cube: dict[str, Any]) -> str:
    lines = [
        f"# Cube session — {cube['lane_id']}", "",
        f"- **Family:** `{cube['family']}`",
        f"- **Kind:** `{cube['kind']}`",
        f"- **Status:** `{cube['status']}`",
        f"- **Started:** `{cube['runtime']['started_at']}`",
        f"- **Ended:** `{cube['runtime']['ended_at']}`",
        f"- **Cube SHA-256:** `{cube['cube_sha256']}`", "",
        "## Source boundary", "", "```json", json.dumps(cube.get("source", {}), indent=2)[:12000], "```", "",
    ]
    research = cube.get("research", {})
    if research:
        lines.extend(["## Highest-frequency algorithm terms", ""])
        for item in research.get("algorithm_hits", [])[:25]:
            lines.append(f"- `{item['term']}` — {item['count']}")
        lines.extend(["", "## Formula candidates", ""])
        for formula in research.get("formula_candidates", [])[:20]:
            lines.append(f"- `{formula}`")
    if cube.get("training"):
        lines.extend(["", "## Reversible cube training", "", "```json", json.dumps(cube["training"], indent=2)[:12000], "```"])
    if cube.get("baselines"):
        lines.extend(["", "## Same-corpus baselines", "", "```json", json.dumps(cube["baselines"], indent=2)[:12000], "```"])
    if cube.get("errors"):
        lines.extend(["", "## Preserved errors", "", "```text", "\n".join(cube["errors"]), "```"])
    return "\n".join(lines) + "\n"


def hbp_summary(cube: dict[str, Any]) -> str:
    def esc(value: Any) -> str:
        return str(value).replace("\\", "\\\\").replace("|", "\\p").replace("\n", "\\n")
    fields = {
        "lane": cube["lane_id"], "family": cube["family"], "kind": cube["kind"],
        "status": cube["status"], "cube_sha256": cube["cube_sha256"],
        "source_sha256": cube.get("research", {}).get("text_sha256", "none"),
        "algorithms": len(cube.get("research", {}).get("algorithm_hits", [])),
        "formulas": len(cube.get("research", {}).get("formula_candidates", [])),
        "people": len(cube.get("research", {}).get("people_candidates", [])),
        "training_status": cube.get("training", {}).get("status", "not-run"),
        "restore": int(bool(cube.get("training", {}).get("all_restore", False))),
        "started_at": cube["runtime"]["started_at"], "ended_at": cube["runtime"]["ended_at"],
        "json": 0,
    }
    return "CUBESESSIONv1" + "".join(f"|{k}={esc(v)}" for k, v in fields.items()) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--lane", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--min-runtime", type=float, default=90.0)
    args = parser.parse_args()

    started_wall = now_utc()
    started_epoch = time.time()
    start_mono = time.monotonic()
    repo_root = Path(args.repo_root).resolve()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    work = output / "work"
    work.mkdir(exist_ok=True)

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    lane = next(item for item in manifest["lanes"] if item["id"] == args.lane)
    status = "MEASURED"
    errors: list[str] = []
    source: dict[str, Any] = {}
    text = ""
    training: dict[str, Any] | None = None
    baselines: dict[str, Any] | None = None

    try:
        kind = lane["kind"]
        if kind in {"github_repo", "github_paths"}:
            text, source = collect_github_repo(lane, work)
        elif kind == "github_bundle":
            text, source = collect_github_bundle(lane, work)
        elif kind == "web_bundle":
            text, source = collect_web_bundle(lane)
        elif kind == "arxiv":
            text, source = collect_arxiv(lane, work)
        elif kind == "google_doc_bundle":
            text, source = collect_google_docs(lane)
        elif kind in {"train_public_plan_b", "train_hutter_methods", "train_combined_benchmark"}:
            corpus, source = gather_training_corpus(kind, work)
            text = corpus.decode("utf-8", errors="replace")
            training = train_reversible_cube(corpus, repo_root, work)
            baselines = lossless_baselines(corpus, repo_root)
        elif kind == "private_input_gate":
            corpus, source, status = private_input_gate(lane, repo_root)
            text = corpus.decode("utf-8", errors="replace") if corpus else ""
            if corpus:
                training = train_reversible_cube(corpus, repo_root, work)
                baselines = lossless_baselines(corpus, repo_root)
        else:
            raise ValueError(f"unknown kind {kind}")
    except Exception as exc:
        status = "HELD_ERROR"
        errors.append(f"{type(exc).__name__}: {exc}")
        errors.append(traceback.format_exc(limit=20))

    research = extract_research(text, lane.get("focus", [])) if text else {
        "focus": lane.get("focus", []), "top_terms": [], "top_bigrams": [],
        "algorithm_hits": [], "formula_candidates": [], "number_candidates": [],
        "people_candidates": [], "text_characters": 0, "text_sha256": sha256_bytes(b""),
    }

    elapsed = time.monotonic() - start_mono
    if elapsed < args.min_runtime:
        time.sleep(args.min_runtime - elapsed)
    ended_wall = now_utc()
    ended_epoch = time.time()

    cube_without_digest = {
        "schema": "ASOLARIA-RESEARCH-CUBE-v1",
        "lane_id": lane["id"], "family": lane["family"], "kind": lane["kind"],
        "status": status, "source": source, "research": research,
        "training": training, "baselines": baselines, "errors": errors,
        "runtime": {
            "runner_name": os.environ.get("RUNNER_NAME", "unknown"),
            "runner_os": os.environ.get("RUNNER_OS", sys.platform),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_job": os.environ.get("GITHUB_JOB"),
            "github_sha": os.environ.get("GITHUB_SHA"),
            "started_at": started_wall, "ended_at": ended_wall,
            "started_epoch": started_epoch, "ended_epoch": ended_epoch,
            "elapsed_seconds": ended_epoch - started_epoch,
        },
    }
    digest = sha256_bytes(json.dumps(cube_without_digest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
    cube = {**cube_without_digest, "cube_sha256": digest}

    (output / "cube.json").write_text(json.dumps(cube, indent=2, ensure_ascii=False), encoding="utf-8")
    (output / "cube.hbp").write_text(hbp_summary(cube), encoding="utf-8")
    (output / "SUMMARY.md").write_text(markdown_summary(cube), encoding="utf-8")
    (output / "source-manifest.json").write_text(json.dumps(lane, indent=2), encoding="utf-8")
    (output / "runtime.json").write_text(json.dumps(cube["runtime"], indent=2), encoding="utf-8")
    hashes = []
    for name in ["cube.json", "cube.hbp", "SUMMARY.md", "source-manifest.json", "runtime.json"]:
        raw = (output / name).read_bytes()
        hashes.append(f"{sha256_bytes(raw)}  {name}")
    (output / "SHA256SUMS").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    print(f"CUBESESSION|lane={lane['id']}|status={status}|cube_sha256={digest}|elapsed={ended_epoch-started_epoch:.3f}|json=0")


if __name__ == "__main__":
    main()
