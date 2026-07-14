#!/usr/bin/env python3
"""Transform native E9 cubes through one of the 8 vertex views of the cube group.

v2 — generators corrected after the GENESIS/RECENTER cross-seat review caught
that even/odd nesting is NOT an involution (it has a distinct inverse), so the
earlier C2^3 group claim was unproven. The corrected generators are the three
SCALES OF REVERSAL, each a genuine involution, all mutually commuting:

  R = reverse the byte stream              (stream scale; Fischer b/w lineage)
  N = swap the two nibbles in every byte   (byte scale; Ring A top perspective)
  Q = reverse the bits within every nibble (nibble scale; Ring A bit lineage)

Their full composition RNQ is complete bit-order reversal of the message.
Views = all subsets: I, R, N, NR, Q, QR, NQ, NQR  (candidates for C2^3 = the
8 vertices / 8 DBBH-DBWH). The group axioms are NOT assumed: --group-gates
verifies squares, commutators, and distinctness on the actual sha-pinned
inputs and emits a receipt. Round trips remain asserted per cube.
"""
import argparse
import hashlib
import pathlib

NIBBLE_SWAP = bytes((((b << 4) & 0xF0) | (b >> 4)) for b in range(256))
_QNIB = [int(f"{v:04b}"[::-1], 2) for v in range(16)]
BIT_IN_NIBBLE = bytes(((_QNIB[b >> 4] << 4) | _QNIB[b & 0x0F]) for b in range(256))


def t_r(data: bytes) -> bytes:
    return data[::-1]


def t_n(data: bytes) -> bytes:
    return data.translate(NIBBLE_SWAP)


def t_q(data: bytes) -> bytes:
    return data.translate(BIT_IN_NIBBLE)


FUNCS = {"r": t_r, "n": t_n, "q": t_q}
VIEWS = {
    "i": (),
    "r": ("r",),
    "n": ("n",),
    "nr": ("r", "n"),
    "q": ("q",),
    "qr": ("r", "q"),
    "nq": ("n", "q"),
    "nqr": ("r", "n", "q"),
}


def apply(chain, data: bytes) -> bytes:
    for name in chain:
        data = FUNCS[name](data)
    return data


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def group_gates(cubes) -> list[str]:
    """Verify the C2^3 axioms on actual cube bytes; return receipt rows."""
    rows = [
        "GGATESHDR|schema=LIRIS-PV-GROUP-GATES-V1|generators=R,N,Q"
        "|axioms=squares,commutators,distinctness|inputs=actual_sha_pinned_cubes|json=0"
    ]
    all_distinct = True
    for name, raw in cubes:
        sq = all(apply((g, g), raw) == raw for g in ("r", "n", "q"))
        comm = all(
            apply((a, b), raw) == apply((b, a), raw)
            for a, b in (("r", "n"), ("r", "q"), ("n", "q"))
        )
        outs = {v: sha(apply(chain, raw)) for v, chain in VIEWS.items()}
        distinct = len(set(outs.values())) == len(outs)
        all_distinct = all_distinct and distinct
        total_reversal = apply(("r", "n", "q"), raw)
        bits_fwd = "".join(f"{b:08b}" for b in raw)
        bits_rev = "".join(f"{b:08b}" for b in total_reversal)
        full_rev = bits_fwd == bits_rev[::-1]
        assert sq, f"{name}: generator square failed"
        assert comm, f"{name}: commutator failed"
        assert full_rev, f"{name}: RNQ is not total bit reversal"
        rows.append(
            f"GGATE|cube={name}|squares=PASS|commutators=PASS"
            f"|views_distinct={'PASS' if distinct else 'COINCIDE_ON_THIS_INPUT'}"
            f"|rnq_total_bit_reversal=PASS|json=0"
        )
    rows.append(
        f"GGATESEND|group=C2^3_CONFIRMED_ON_INPUTS"
        f"|all_inputs_distinct={'1' if all_distinct else '0'}|json=0"
    )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--native-snapshot", required=True)
    ap.add_argument("--view", required=True, choices=sorted(VIEWS))
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--group-gates", action="store_true",
                    help="emit GROUP-GATES.hbp verifying the C2^3 axioms on the inputs")
    args = ap.parse_args()

    chain = VIEWS[args.view]
    native = sorted(pathlib.Path(args.native_snapshot, "e9").glob("LX-*.md"))
    assert native, "no native cubes found"

    out = pathlib.Path(args.output_dir)
    snap = out / "snapshot" / "e9"
    snap.mkdir(parents=True, exist_ok=True)

    if args.group_gates:
        rows = group_gates([(p.name, p.read_bytes()) for p in native])
        (out / "GROUP-GATES.hbp").write_text("\n".join(rows) + "\n", encoding="utf-8")
        print(rows[-1])

    manifest = []
    mapping = [
        f"PVMAPHDR|schema=LIRIS-PYRAMID-VIEWS-V2|view={args.view}"
        "|generators=R_stream_reversal,N_nibble_swap,Q_bits_in_nibble_reversal"
        f"|cubes={len(native)}|roundtrip=ASSERTED_PER_CUBE|json=0"
    ]
    for path in native:
        raw = path.read_bytes()
        transformed = apply(chain, raw)
        assert apply(chain, transformed) == raw, f"round-trip FAILED for {path.name}"
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
