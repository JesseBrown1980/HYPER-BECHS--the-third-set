#!/usr/bin/env python3
"""Cut 27 sha-pinned cubes spread evenly across the ENTIRE enwik9 corpus.

Unlike the mid-corpus generator (contiguous 1 MB neighborhood), this samples
the whole gigabyte: cube i starts at base_offset + i*stride, spanning from the
head of the corpus to its tail. Same cube size and manifest format as before,
so every downstream tensor (8 views x 800 uniform passes) compares directly
with the mid-corpus orbit. Stdlib only; deterministic.
"""
import argparse
import hashlib
import pathlib


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enwik9", required=True)
    ap.add_argument("--base-offset", type=int, default=500_000)
    ap.add_argument("--stride", type=int, default=37_000_000)
    ap.add_argument("--slice-bytes", type=int, default=37_037)
    ap.add_argument("--count", type=int, default=27)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    last_end = args.base_offset + (args.count - 1) * args.stride + args.slice_bytes
    corpus_size = pathlib.Path(args.enwik9).stat().st_size
    assert last_end <= corpus_size, f"sampling exceeds corpus: {last_end} > {corpus_size}"

    out = pathlib.Path(args.output_dir)
    snap = out / "snapshot" / "e9"
    snap.mkdir(parents=True, exist_ok=True)

    rows = [
        "E9WIDEHDR|schema=LIRIS-E9-WIDE-CUBES-V1|source=enwik9"
        f"|base_offset={args.base_offset}|stride={args.stride}"
        f"|slice_bytes={args.slice_bytes}|count={args.count}"
        f"|span={args.base_offset}..{last_end}|coverage=FULL_CORPUS_SAMPLED|json=0"
    ]
    with open(args.enwik9, "rb") as fh:
        for i in range(1, args.count + 1):
            offset = args.base_offset + (i - 1) * args.stride
            fh.seek(offset)
            body = fh.read(args.slice_bytes)
            assert len(body) == args.slice_bytes, f"short read at cube {i}"
            name = f"LX-{i:03d}.md"
            (snap / name).write_bytes(body)
            digest = hashlib.sha256(body).hexdigest()
            rows.append(
                f"OLDCUBEREF|file={name}|axis=e9|bytes={len(body)}"
                f"|sha256={digest}|snapshot=e9/{name}|json=0"
            )
            print(f"cube e9-LX-{i:03d} offset={offset} sha256={digest}")
    rows.append(f"E9WIDEEND|count={args.count}|total_bytes={args.count * args.slice_bytes}|json=0")
    (out / "manifest.hbp").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"manifest rows={len(rows)}")


if __name__ == "__main__":
    main()
