#!/usr/bin/env python3
"""Cut 27 sha-pinned cubes from the Asolaria repo corpus (self-referential source)."""
import argparse, hashlib, pathlib

ap = argparse.ArgumentParser()
ap.add_argument("--corpus", required=True)
ap.add_argument("--slice-bytes", type=int, default=26000)
ap.add_argument("--count", type=int, default=27)
ap.add_argument("--output-dir", required=True)
a = ap.parse_args()

data = pathlib.Path(a.corpus).read_bytes()
need = a.slice_bytes * a.count
assert len(data) >= need, "corpus too small: %d < %d" % (len(data), need)

out = pathlib.Path(a.output_dir)
snap = out / "snapshot" / "e9"
snap.mkdir(parents=True, exist_ok=True)
rows = ["REPOCUBEHDR|schema=LIRIS-ASOLARIA-REPO-CUBES-V1|source=asolaria_own_repos"
        "|corpus_sha256=%s|slice_bytes=%d|count=%d|json=0"
        % (hashlib.sha256(data).hexdigest(), a.slice_bytes, a.count)]
for i in range(1, a.count + 1):
    off = (i - 1) * a.slice_bytes
    body = data[off:off + a.slice_bytes]
    name = "LX-%03d.md" % i
    (snap / name).write_bytes(body)
    rows.append("OLDCUBEREF|file=%s|axis=repo|bytes=%d|sha256=%s|snapshot=e9/%s|json=0"
                % (name, len(body), hashlib.sha256(body).hexdigest(), name))
    print("cube repo-LX-%03d off=%d sha256=%s" % (i, off, hashlib.sha256(body).hexdigest()))
rows.append("REPOCUBEEND|count=%d|total_bytes=%d|json=0" % (a.count, a.count * a.slice_bytes))
(out / "manifest.hbp").write_text("\n".join(rows) + "\n", encoding="utf-8")
print("manifest rows=%d" % len(rows))
