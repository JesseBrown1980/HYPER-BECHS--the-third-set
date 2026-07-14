#!/usr/bin/env python3
"""Observe one public Wolfram landing page through a non-reconstructive lens.

The raw HTML is held only in process memory. The emitted shadow cube contains
hashes, counts, category/task/type labels, and coarse histograms, but no page
paragraphs, examples, code, model weights, or reconstructive token sequences.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import math
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

USER_AGENT = "Asolaria-Wolfram-Lens/1.0 (+https://github.com/JesseBrown1980)"

KNOWN_LABELS = {
    "wolfram-data-repository": {
        "categories": [
            "Agriculture", "Astronomy", "Chemistry", "Computational Universe", "Computer Systems",
            "Culture", "Demographics", "Earth Science", "Economics", "Education", "Engineering",
            "Geography", "Geometry Data", "Government", "Graphics", "Health", "Healthcare", "History",
            "Human Activities", "Images", "Language", "Life Science", "Machine Learning", "Manufacturing",
            "Mathematics", "Medicine", "Meteorology", "Physical Sciences", "Politics", "Reference",
            "Social Media", "Sociology", "Statistics", "Text & Literature", "Transportation"
        ],
        "types": ["Audio", "Entity Store", "Geospatial Data", "Graphs", "Image", "Numerical Data", "Text", "Time Series", "Vector Database", "Video"],
        "capability_keywords": ["public resource", "computable datasets", "visualization", "analysis", "data-backed publication"],
        "clean_room_methods": ["dataset metadata normalization", "category classification", "numeric summary statistics", "graph and matrix descriptors"]
    },
    "wolfram-function-repository": {
        "categories": [
            "Core Language & Structure", "Data Manipulation & Analysis", "Visualization & Graphics",
            "Machine Learning", "Symbolic & Numeric Computation", "Higher Mathematical Computation",
            "Strings & Text", "Graphs & Networks", "Images", "Geometry", "Sound & Video",
            "Knowledge Representation & Natural Language", "Time-Related Computation",
            "Geographic Data & Computation", "Scientific and Medical Data & Computation",
            "Engineering Data & Computation", "Financial Data & Computation",
            "Social, Cultural & Linguistic Data", "Notebook Documents & Presentation",
            "User Interface Construction", "System Operation & Setup", "External Interfaces & Connections",
            "Cloud & Deployment", "Repository Tools", "Programming Utilities", "Just For Fun",
            "Wolfram Physics Project"
        ],
        "types": [],
        "capability_keywords": ["public resource", "standalone functions", "immediate use", "wolfram language computation"],
        "clean_room_methods": ["expression parsing", "canonicalization", "continued fractions", "prime-field linear algebra", "graph Laplacians"]
    },
    "wolfram-neural-net-repository": {
        "categories": ["Audio", "Image", "Numeric", "Text", "Video"],
        "types": [
            "Audio Analysis", "Classification", "Data Generation", "Denoising", "Feature Extraction",
            "Image Captioning", "Image Processing", "Language Modeling", "Object Detection",
            "Question Answering", "Regression", "Semantic Segmentation", "Speech Recognition", "Translation"
        ],
        "capability_keywords": ["public resource", "trained and untrained", "evaluation", "training", "visualization", "transfer learning"],
        "clean_room_methods": ["state-vector simulation", "model task taxonomy", "feature-vector shape contracts", "probability normalization"]
    }
}


class PageLens(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.anchor_parts: list[str] = []
        self.all_text_parts: list[str] = []
        self.tag_counts: collections.Counter[str] = collections.Counter()
        self.link_domains: collections.Counter[str] = collections.Counter()
        self.in_title = False
        self.in_anchor = False
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self.tag_counts[tag] += 1
        if tag == "title":
            self.in_title = True
        elif tag == "a":
            self.in_anchor = True
            href = dict(attrs).get("href")
            if href:
                domain = urllib.parse.urlparse(href).netloc
                if domain:
                    self.link_domains[domain.lower()] += 1
        elif tag in {"script", "style", "svg", "noscript"}:
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "a":
            self.in_anchor = False
        elif tag in {"script", "style", "svg", "noscript"} and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        compact = " ".join(data.split())
        if not compact:
            return
        self.all_text_parts.append(compact)
        if self.in_title:
            self.title_parts.append(compact)
        if self.in_anchor:
            self.anchor_parts.append(compact)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def histogram(values: list[int], buckets: tuple[int, ...] = (0, 5, 10, 20, 40, 80, 160, 320)) -> dict[str, int]:
    result: dict[str, int] = {}
    for lo, hi in zip(buckets, buckets[1:]):
        result[f"{lo + 1}-{hi}"] = sum(lo < value <= hi for value in values)
    result[f">{buckets[-1]}"] = sum(value > buckets[-1] for value in values)
    return result


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if args.source_id not in KNOWN_LABELS:
        raise SystemExit(f"unknown source id: {args.source_id}")
    request = urllib.request.Request(args.url, headers={"User-Agent": USER_AGENT})
    fetched_at = dt.datetime.now(dt.timezone.utc).isoformat()
    with urllib.request.urlopen(request, timeout=90) as response:
        raw = response.read()
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()

    lens = PageLens()
    lens.feed(raw.decode("utf-8", errors="replace"))
    all_text = "\n".join(lens.all_text_parts)
    anchors = [" ".join(value.split()) for value in lens.anchor_parts if value.strip()]
    anchor_set = set(anchors)
    profile = KNOWN_LABELS[args.source_id]
    categories = [label for label in profile["categories"] if label in anchor_set or label.lower() in all_text.lower()]
    types = [label for label in profile["types"] if label in anchor_set or label.lower() in all_text.lower()]
    capability_flags = {keyword: keyword in all_text.lower() for keyword in profile["capability_keywords"]}
    title = " ".join(lens.title_parts).strip()

    # The page body is never included below. Only aggregate measurements and short factual labels survive.
    cube = {
        "schema": "NONRECONSTRUCTIVE-LENS-CUBE-v1",
        "source_id": args.source_id,
        "source_url": args.url,
        "final_url": final_url,
        "fetched_at": fetched_at,
        "content_type": content_type,
        "source_bytes": len(raw),
        "source_sha256": sha256(raw),
        "page_text_sha256": sha256(all_text.encode("utf-8")),
        "title": title[:160],
        "measurements": {
            "html_tag_counts": dict(sorted(lens.tag_counts.items())),
            "anchor_count": len(anchors),
            "unique_anchor_count": len(anchor_set),
            "anchor_length_histogram": histogram([len(value) for value in anchors]),
            "text_fragment_count": len(lens.all_text_parts),
            "text_fragment_length_histogram": histogram([len(value) for value in lens.all_text_parts]),
            "link_domain_counts": dict(sorted(lens.link_domains.items())),
            "category_count": len(categories),
            "type_or_task_count": len(types),
        },
        "public_factual_labels": {
            "categories": categories,
            "types_or_tasks": types,
            "capability_flags": capability_flags,
        },
        "white_room_handoff": {
            "clean_room_methods": profile["clean_room_methods"],
            "functional_requirements": [
                "deterministic input/output contract",
                "explicit domain and error handling",
                "independent implementation without source-page body",
                "property tests and mathematical identity checks",
                "no source expression or examples embedded in builder output"
            ]
        },
        "retention": {
            "raw_body_retained": False,
            "raw_html_retained": False,
            "full_page_text_retained": False,
            "expressive_text_bytes": 0,
            "source_reconstructable": False,
            "service_payload_downloaded": False,
            "landing_page_only": True
        }
    }
    cube_sha = sha256(canonical(cube))
    cube["cube_sha256"] = cube_sha

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "shadow-cube.json").write_text(json.dumps(cube, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "white-room-spec.json").write_text(json.dumps(cube["white_room_handoff"], indent=2), encoding="utf-8")
    (out / "shadow-cube.hbp").write_text(
        "LENSCUBEv1"
        f"|source_id={args.source_id}|source_bytes={len(raw)}|source_sha256={sha256(raw)}"
        f"|categories={len(categories)}|types={len(types)}|raw_retained=0|reconstructable=0"
        f"|cube_sha256={cube_sha}|json=0\n",
        encoding="utf-8"
    )
    sums = []
    for name in ("shadow-cube.json", "white-room-spec.json", "shadow-cube.hbp"):
        sums.append(f"{sha256((out / name).read_bytes())}  {name}")
    (out / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print(f"LENSCUBE|source={args.source_id}|bytes={len(raw)}|categories={len(categories)}|types={len(types)}|raw_retained=0|status=PASS|json=0")


if __name__ == "__main__":
    main()
