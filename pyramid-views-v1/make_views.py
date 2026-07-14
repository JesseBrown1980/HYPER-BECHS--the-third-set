#!/usr/bin/env python3
"""Transform native E9 cubes through one of the 8 vertex views of the cube group.

The three generators are involutions, each anchored in measured receipts:
  R = byte reversal        (sequence axis anti-side; Fischer black/white lineage)
  N = nibble mirror        (intra-byte axis anti-side; Ring A top perspective)
  E = even/odd nesting     (block axis anti-side; Ring A measured perspective)
Views = the group they generate: I, R, N, NR, E, ER, NE, NER  (2^3 = 8 vertices).
Application order for composites: R first, then N, then E. All bijective and
size-preserving; every cube's round trip inverse(view(x)) == x is asserted and
both native and view SHA-256 are recorded in views-map.hbp.
"""
import argparse
import hashlib
import pathlib

NIBBLE = bytes((((b << 4) & 0xF0) | (b >> 4)) for b in range(256))


def t_r(data: bytes) -> bytes:
    return data[::-1]


def t_n(data: bytes) -> bytes:
    return data.translate(NIBBLE)


def t_e(data: bytes) -> bytes:
    return data[0::2] + data[1::2]


def t_e_inv(data: bytes) -> bytes:
    half = (len(data) + 1) // 2
    even, odd = data[:half], data[half:]
    out = bytearray(len(data))
    out[0::2] = even
    out[1::2] = odd
    return bytes(out)


VIEWS = {
    "i": ((), ()),
    "r": (("r",), ("r",)),
    "n": (("n",), ("n",)),
    "nr": (("r", "n"), ("n", "r")),
    "e": (("e",), ("e_inv",)),
    "er": (("r", "e"), ("e_inv", "r")),
    "ne": (("n", "e"), ("e_inv", "n")),
    "ner": (("r", "n", "e"), ("e_inv", "n", "r")),
}

FUNCS = {"r": t_r, "n": t_n, "e": t_e, "e_inv": t_e_inv}


def apply(chain, data: bytes) -> bytes:
    for name in chain:
        data = FUNCS[name](data)
    return data


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--native-snapshot", required=True,
                    help="dir containing e9/LX-*.md native cubes")
    ap.add_argument("--view", required=True, choices=sorted(VIEWS))
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    fwd, inv = VIEWS[args.view]
    native = sorted(pathlib.Path(args.native_snapshot, "e9").glob("LX-*.md"))
    assert native, "no native cubes found"

    out = pathlib.Path(args.output_dir)
    snap = out / "snapshot" / "e9"
    snap.mkdir(parents=True, exist_ok=True)

    manifest = []
    mapping = [
        f"PVMAPHDR|schema=LIRIS-PYRAMID-VIEWS-V1|view={args.view}"
        f"|generators=R_byte_reversal,N_nibble_mirror,E_even_odd_nesting"
        f"|cubes={len(native)}|roundtrip=ASSERTED_PER_CUBE|json=0"
    ]
    for path in native:
        raw = path.read_bytes()
        transformed = apply(fwd, raw)
        assert apply(inv, transformed) == raw, f"round-trip FAILED for {path.name}"
        assert len(transformed) == len(raw)
        (snap / path.name).write_bytes(transformed)
        manifest.append(
            f"OLDCUBEREF|file={path.name}|axis=e9|bytes={len(transformed)}"
            f"|sha256={sha(transformed)}|snapshot=e9/{path.name}|json=0"
        )
        mapping.append(
            f"PVMAP|cube={path.name}|view={args.view}|native_sha256={sha(raw)}"
            f"|view_sha256={sha(transformed)}|roundtrip=EXACT|json=0"
        )
    (out / "manifest.hbp").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    (out / "views-map.hbp").write_text("\n".join(mapping) + "\n", encoding="utf-8")
    print(f"view={args.view} cubes={len(native)} roundtrips=ALL_EXACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
