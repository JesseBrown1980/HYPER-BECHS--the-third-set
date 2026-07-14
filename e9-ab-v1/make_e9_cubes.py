#!/usr/bin/env python3
"""Cut 27 sha-pinned base cubes from enwik9 and emit an OLDCUBEREF-format manifest.

Slices are contiguous from a pinned offset deep in enwik9 (beyond the enwik8
prefix), so every byte is genuine E9 data the earlier tests never touched.
Stdlib only; exact values only; deterministic given (offset, slice_bytes, count).
"""
import argparse
import hashlib
import pathlib


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enwik9", required=True)
    ap.add_argument("--offset", type=int, default=500_000_000)
    ap.add_argument("--slice-bytes", type=int, default=37_037)
    ap.add_argument("--count", type=int, default=27)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    out = pathlib.Path(args.output_dir)
    snap = out / "snapshot" / "e9"
    snap.mkdir(parents=True, exist_ok=True)

    rows = [
        "E9CUBEHDR|schema=LIRIS-E9-AB-CUBES-V1|source=enwik9"
        f"|offset={args.offset}|slice_bytes={args.slice_bytes}|count={args.count}"
        "|region=beyond_enwik8_prefix|json=0"
    ]
    with open(args.enwik9, "rb") as fh:
        fh.seek(args.offset)
        for i in range(1, args.count + 1):
            body = fh.read(args.slice_bytes)
            assert len(body) == args.slice_bytes, f"short read at slice {i}"
            name = f"LX-{i:03d}.md"
            (snap / name).write_bytes(body)
            digest = hashlib.sha256(body).hexdigest()
            rows.append(
                f"OLDCUBEREF|file={name}|axis=e9|bytes={len(body)}"
                f"|sha256={digest}|snapshot=e9/{name}|json=0"
            )
            print(f"cube e9-LX-{i:03d} offset={args.offset + (i-1)*args.slice_bytes} sha256={digest}")
    rows.append(f"E9CUBEEND|count={args.count}|total_bytes={args.count * args.slice_bytes}|json=0")
    manifest = out / "manifest.hbp"
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"manifest={manifest} rows={len(rows)}")


if __name__ == "__main__":
    main()
