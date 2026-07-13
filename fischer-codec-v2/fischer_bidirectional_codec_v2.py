#!/usr/bin/env python3
"""Fischer bidirectional context codec v2.

Legal bidirectional coding is obtained with a deterministic pyramid schedule:
coarse anchors are decoded first, then interval midpoints are decoded level by
level. Black experts use already-decoded values to the left; white experts use
already-decoded values to the right. Five orders per direction are mixed by a
fixed-point Shannon consensus weighter. An optional white-room bridge family
learns joint left/right contexts. Every archive must round-trip exactly.

This is a classical research codec, not physical quantum cloning and not a
Hutter Prize submission.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import time
from array import array
from dataclasses import dataclass
from pathlib import Path

TOP = 1 << 24
BOT = 1 << 16
MASK32 = 0xFFFFFFFF
MASK64 = 0xFFFFFFFFFFFFFFFF
TOT = 1 << 16
MAGIC = b"FSC2"
VERSION = 2
PRIMES = {
    ("black", 1): 11, ("black", 2): 13, ("black", 3): 17,
    ("black", 4): 19, ("black", 5): 23,
    ("white", 1): 29, ("white", 2): 31, ("white", 3): 37,
    ("white", 4): 41, ("white", 5): 43,
    ("bridge", 1): 47, ("bridge", 2): 53, ("bridge", 3): 59,
    ("bridge", 4): 61, ("bridge", 5): 67,
}


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def mix64(x: int) -> int:
    x &= MASK64
    x ^= x >> 30
    x = (x * 0xBF58476D1CE4E5B9) & MASK64
    x ^= x >> 27
    x = (x * 0x94D049BB133111EB) & MASK64
    x ^= x >> 31
    return x & MASK64


class RangeEncoder:
    def __init__(self) -> None:
        self.low = 0
        self.rng = MASK32
        self.out = bytearray()

    def encode_bit(self, bit: int, p1: int) -> None:
        p1 = max(1, min(TOT - 1, int(p1)))
        p0 = TOT - p1
        unit = self.rng // TOT
        if unit <= 0:
            raise ArithmeticError("range coder unit underflow")
        if bit:
            self.low = (self.low + p0 * unit) & MASK32
            self.rng = p1 * unit
        else:
            self.rng = p0 * unit
        while True:
            if ((self.low ^ ((self.low + self.rng) & MASK32)) & MASK32) < TOP:
                pass
            elif self.rng < BOT:
                self.rng = (-self.low) & (BOT - 1)
            else:
                break
            self.out.append((self.low >> 24) & 0xFF)
            self.low = (self.low << 8) & MASK32
            self.rng = (self.rng << 8) & MASK32

    def finish(self) -> bytes:
        for _ in range(4):
            self.out.append((self.low >> 24) & 0xFF)
            self.low = (self.low << 8) & MASK32
        return bytes(self.out)


class RangeDecoder:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 4
        self.low = 0
        self.rng = MASK32
        self.code = int.from_bytes(data[:4].ljust(4, b"\0"), "big")

    def decode_bit(self, p1: int) -> int:
        p1 = max(1, min(TOT - 1, int(p1)))
        p0 = TOT - p1
        unit = self.rng // TOT
        if unit <= 0:
            raise ArithmeticError("range decoder unit underflow")
        target = ((self.code - self.low) & MASK32) // unit
        if target < p0:
            bit = 0
            self.rng = p0 * unit
        else:
            bit = 1
            self.low = (self.low + p0 * unit) & MASK32
            self.rng = p1 * unit
        while True:
            if ((self.low ^ ((self.low + self.rng) & MASK32)) & MASK32) < TOP:
                pass
            elif self.rng < BOT:
                self.rng = (-self.low) & (BOT - 1)
            else:
                break
            nxt = self.data[self.pos] if self.pos < len(self.data) else 0
            self.pos += 1
            self.code = ((self.code << 8) | nxt) & MASK32
            self.low = (self.low << 8) & MASK32
            self.rng = (self.rng << 8) & MASK32
        return bit


@dataclass(frozen=True)
class Task:
    index: int
    left: tuple[int, ...]
    right: tuple[int, ...]
    scale: int
    phase: int


def sequential_tasks(n: int, max_context: int = 5) -> list[Task]:
    return [Task(i, tuple(range(i - 1, max(-1, i - max_context - 1), -1)), (), 1, 0)
            for i in range(n)]


def pyramid_tasks(n: int, stride: int = 32, max_context: int = 5) -> list[Task]:
    if n <= 0:
        return []
    anchors = list(range(0, n, stride))
    if anchors[-1] != n - 1:
        anchors.append(n - 1)
    tasks: list[Task] = []
    for i, pos in enumerate(anchors):
        left = tuple(reversed(anchors[max(0, i - max_context):i]))
        tasks.append(Task(pos, left, (), stride, 0))
    known = sorted(set(anchors))
    intervals = [(known[i], known[i + 1]) for i in range(len(known) - 1)
                 if known[i + 1] - known[i] > 1]
    phase = 1
    while intervals:
        mids: list[int] = []
        nxt: list[tuple[int, int]] = []
        for l, r in intervals:
            if r - l <= 1:
                continue
            m = (l + r) // 2
            lo, hi = 0, len(known)
            while lo < hi:
                mid = (lo + hi) // 2
                if known[mid] < m:
                    lo = mid + 1
                else:
                    hi = mid
            j = lo
            left = tuple(reversed(known[max(0, j - max_context):j]))
            right = tuple(known[j:min(len(known), j + max_context)])
            tasks.append(Task(m, left, right, r - l, phase))
            mids.append(m)
            if m - l > 1:
                nxt.append((l, m))
            if r - m > 1:
                nxt.append((m, r))
        known = sorted(known + mids)
        intervals = nxt
        phase += 1
    if len(tasks) != n or len({t.index for t in tasks}) != n:
        raise AssertionError("pyramid schedule is not a permutation")
    return tasks


def get_tasks(n: int, schedule: str, stride: int) -> list[Task]:
    if schedule == "sequential":
        return sequential_tasks(n)
    if schedule == "pyramid":
        return pyramid_tasks(n, stride)
    raise ValueError(schedule)


class HashExpert:
    """Bounded-memory binary context expert."""

    def __init__(self, direction: str, order: int, table_bits: int) -> None:
        self.direction = direction
        self.order = order
        self.prime = PRIMES[(direction, order)]
        self.table_bits = table_bits
        self.size = 1 << table_bits
        self.mask = self.size - 1
        self.counts = array("H", [1]) * (2 * self.size)
        self.loss_bits = 0.0
        self.bits = 0
        self.correct = 0
        self.blunders = 0
        self.touched = bytearray(self.size)

    def base_hash(self, buf: bytearray, task: Task) -> int:
        if self.direction == "black":
            idxs = task.left
            limit = self.order
        elif self.direction == "white":
            idxs = task.right
            limit = self.order
        else:
            merged: list[int] = []
            for i in range(max(len(task.left), len(task.right))):
                if i < len(task.left):
                    merged.append(task.left[i])
                if i < len(task.right):
                    merged.append(task.right[i])
            idxs = tuple(merged)
            limit = 2 * self.order
        h = mix64(self.prime * 0x9E3779B185EBCA87 ^ (task.scale << 17)
                  ^ (task.phase << 5) ^ len(idxs))
        used = 0
        for idx in idxs:
            h = mix64(h ^ (buf[idx] + 1 + used * 257))
            used += 1
            if used >= limit:
                break
        return mix64(h ^ (used << 48) ^ (self.order << 56))

    def slot(self, base: int, bitpos: int, prefix: int) -> int:
        return mix64(base ^ ((bitpos + 1) * 0xD6E8FEB86659FD93)
                     ^ ((prefix + 1) * 0xA5A3564E27F886A7)) & self.mask

    def predict_slot(self, slot: int) -> int:
        off = 2 * slot
        c0 = self.counts[off]
        c1 = self.counts[off + 1]
        return max(1, min(TOT - 1, (c1 * TOT) // (c0 + c1)))

    def update_slot(self, slot: int, bit: int, p1: int) -> None:
        off = 2 * slot + bit
        self.counts[off] = min(65535, self.counts[off] + 1)
        c0 = self.counts[2 * slot]
        c1 = self.counts[2 * slot + 1]
        if c0 + c1 > 4094:
            self.counts[2 * slot] = max(1, (c0 + 1) // 2)
            self.counts[2 * slot + 1] = max(1, (c1 + 1) // 2)
        self.touched[slot] = 1
        pa = (p1 if bit else TOT - p1) / TOT
        self.loss_bits += -math.log2(max(pa, 1 / TOT))
        self.bits += 1
        self.correct += int((p1 >= TOT // 2) == bool(bit))
        self.blunders += int(pa < 0.10)

    def report(self, best_bpb: float = 0.0, trust_pct: float = 0.0) -> dict:
        bpb = self.loss_bits / max(1, self.bits)
        cpl = round(1000 * max(0.0, bpb - best_bpb))
        verdict = "BLOCK" if cpl >= 500 else ("HOLD" if cpl >= 150 else "PROCEED")
        return {
            "expert": f"{self.direction}-o{self.order}",
            "direction": self.direction,
            "order": self.order,
            "prime": self.prime,
            "actor_pid": sha256_hex(f"FISCHER|{self.direction}|{self.order}|{self.prime}".encode())[:16],
            "ideal_bpb": bpb,
            "accuracy": self.correct / max(1, self.bits),
            "blunders": self.blunders,
            "touched_slots": int(sum(self.touched)),
            "table_slots": self.size,
            "cpl_vs_best": cpl,
            "fischer_verdict": verdict,
            "trust_pct": trust_pct,
        }


class ShannonConsensus:
    def __init__(self, n: int) -> None:
        self.weights = [[TOT // 2 for _ in range(n)] for _ in range(8)]
        self.loss_bits = 0.0
        self.bits = 0
        self.correct = 0
        self.blunders = 0

    def predict(self, probs: list[int], bitpos: int) -> int:
        ws = self.weights[bitpos]
        den = sum(ws)
        return max(1, min(TOT - 1, sum(w * p for w, p in zip(ws, probs)) // den))

    def update(self, probs: list[int], bitpos: int, bit: int, p_mix: int) -> None:
        ws = self.weights[bitpos]
        for j, p in enumerate(probs):
            reward = p if bit else TOT - p
            ws[j] = max(64, min(TOT - 64, (63 * ws[j] + reward) // 64))
        pa = (p_mix if bit else TOT - p_mix) / TOT
        self.loss_bits += -math.log2(max(pa, 1 / TOT))
        self.bits += 1
        self.correct += int((p_mix >= TOT // 2) == bool(bit))
        self.blunders += int(pa < 0.10)


class FischerCodecState:
    def __init__(self, mode: str, table_bits: int) -> None:
        specs: list[tuple[str, int]] = []
        if mode in ("black", "both", "omni"):
            specs.extend(("black", o) for o in range(1, 6))
        if mode in ("white", "both", "omni"):
            specs.extend(("white", o) for o in range(1, 6))
        if mode == "omni":
            specs.extend(("bridge", o) for o in range(1, 6))
        self.experts = [HashExpert(d, o, table_bits) for d, o in specs]
        self.mixer = ShannonConsensus(len(self.experts))
        self.mode = mode

    def bases(self, buf: bytearray, task: Task) -> list[int]:
        return [ex.base_hash(buf, task) for ex in self.experts]

    def predict(self, bases: list[int], bitpos: int, prefix: int) -> tuple[list[int], list[int], int]:
        slots = [ex.slot(base, bitpos, prefix) for ex, base in zip(self.experts, bases)]
        probs = [ex.predict_slot(slot) for ex, slot in zip(self.experts, slots)]
        return slots, probs, self.mixer.predict(probs, bitpos)

    def update(self, slots: list[int], probs: list[int], bitpos: int, bit: int, p_mix: int) -> None:
        self.mixer.update(probs, bitpos, bit, p_mix)
        for ex, slot, p in zip(self.experts, slots, probs):
            ex.update_slot(slot, bit, p)

    def report(self) -> dict:
        bpbs = [ex.loss_bits / max(1, ex.bits) for ex in self.experts]
        best = min(bpbs) if bpbs else 0.0
        avg_weights = [sum(self.mixer.weights[b][j] for b in range(8)) / 8
                       for j in range(len(self.experts))]
        den = sum(avg_weights) or 1.0
        reports = [ex.report(best, 100.0 * w / den)
                   for ex, w in zip(self.experts, avg_weights)]
        return {
            "mode": self.mode,
            "mixer_ideal_bpb": self.mixer.loss_bits / max(1, self.mixer.bits),
            "mixer_accuracy": self.mixer.correct / max(1, self.mixer.bits),
            "mixer_blunders": self.mixer.blunders,
            "black_trust_pct": sum(r["trust_pct"] for r in reports if r["direction"] == "black"),
            "white_trust_pct": sum(r["trust_pct"] for r in reports if r["direction"] == "white"),
            "bridge_trust_pct": sum(r["trust_pct"] for r in reports if r["direction"] == "bridge"),
            "experts": reports,
        }


HEADER = struct.Struct(">4sBBBBBHIQ")
MODE_TO_ID = {"black": 0, "white": 1, "both": 2, "omni": 3}
ID_TO_MODE = {v: k for k, v in MODE_TO_ID.items()}
SCHED_TO_ID = {"sequential": 0, "pyramid": 1}
ID_TO_SCHED = {v: k for k, v in SCHED_TO_ID.items()}


def encode(data: bytes, *, mode: str = "both", schedule: str = "pyramid", stride: int = 32,
           block_size: int = 4096, table_bits: int = 18) -> tuple[bytes, dict]:
    state = FischerCodecState(mode, table_bits)
    coder = RangeEncoder()
    cache: dict[int, list[Task]] = {}
    t0 = time.perf_counter()
    for off in range(0, len(data), block_size):
        block = data[off:off + block_size]
        tasks = cache.setdefault(len(block), get_tasks(len(block), schedule, stride))
        buf = bytearray(block)
        for task in tasks:
            value = block[task.index]
            bases = state.bases(buf, task)
            prefix = 0
            for bitpos in range(8):
                bit = (value >> (7 - bitpos)) & 1
                slots, probs, p_mix = state.predict(bases, bitpos, prefix)
                coder.encode_bit(bit, p_mix)
                state.update(slots, probs, bitpos, bit, p_mix)
                prefix = (prefix << 1) | bit
    payload = coder.finish()
    elapsed = time.perf_counter() - t0
    header = HEADER.pack(MAGIC, VERSION, MODE_TO_ID[mode], SCHED_TO_ID[schedule], 5,
                         table_bits, stride, block_size, len(data))
    archive = header + payload
    report = state.report()
    report.update({
        "raw_bytes": len(data), "payload_bytes": len(payload), "archive_bytes": len(archive),
        "payload_bpc": len(payload) * 8 / max(1, len(data)),
        "bpc": len(archive) * 8 / max(1, len(data)),
        "schedule": schedule, "stride": stride, "block_size": block_size,
        "table_bits": table_bits, "encode_s": elapsed,
        "sha256_in": sha256_hex(data), "sha256_archive": sha256_hex(archive),
    })
    return archive, report


def decode(archive: bytes) -> tuple[bytes, dict]:
    if len(archive) < HEADER.size:
        raise ValueError("archive too short")
    magic, version, mode_id, sched_id, orders, table_bits, stride, block_size, raw_len = HEADER.unpack(archive[:HEADER.size])
    if magic != MAGIC or version != VERSION or orders != 5:
        raise ValueError("unsupported archive")
    mode = ID_TO_MODE[mode_id]
    schedule = ID_TO_SCHED[sched_id]
    state = FischerCodecState(mode, table_bits)
    coder = RangeDecoder(archive[HEADER.size:])
    output = bytearray(raw_len)
    cache: dict[int, list[Task]] = {}
    t0 = time.perf_counter()
    for off in range(0, raw_len, block_size):
        size = min(block_size, raw_len - off)
        tasks = cache.setdefault(size, get_tasks(size, schedule, stride))
        buf = bytearray(size)
        for task in tasks:
            bases = state.bases(buf, task)
            value = 0
            prefix = 0
            for bitpos in range(8):
                slots, probs, p_mix = state.predict(bases, bitpos, prefix)
                bit = coder.decode_bit(p_mix)
                value = (value << 1) | bit
                state.update(slots, probs, bitpos, bit, p_mix)
                prefix = (prefix << 1) | bit
            buf[task.index] = value
        output[off:off + size] = buf
    elapsed = time.perf_counter() - t0
    report = state.report()
    report.update({"raw_bytes": raw_len, "archive_bytes": len(archive),
                   "bpc": len(archive) * 8 / max(1, raw_len),
                   "schedule": schedule, "stride": stride, "block_size": block_size,
                   "table_bits": table_bits, "decode_s": elapsed,
                   "sha256_out": sha256_hex(output)})
    return bytes(output), report


def audit(data: bytes, *, direction: str, order: int, schedule: str = "pyramid",
          stride: int = 32, block_size: int = 4096, table_bits: int = 18) -> dict:
    ex = HashExpert(direction, order, table_bits)
    cache: dict[int, list[Task]] = {}
    t0 = time.perf_counter()
    for off in range(0, len(data), block_size):
        block = data[off:off + block_size]
        tasks = cache.setdefault(len(block), get_tasks(len(block), schedule, stride))
        buf = bytearray(block)
        for task in tasks:
            base = ex.base_hash(buf, task)
            value = block[task.index]
            prefix = 0
            for bitpos in range(8):
                bit = (value >> (7 - bitpos)) & 1
                slot = ex.slot(base, bitpos, prefix)
                p = ex.predict_slot(slot)
                ex.update_slot(slot, bit, p)
                prefix = (prefix << 1) | bit
    report = ex.report(0.0, 100.0)
    report.update({"raw_bytes": len(data), "schedule": schedule, "stride": stride,
                   "block_size": block_size, "table_bits": table_bits,
                   "elapsed_s": time.perf_counter() - t0, "sha256_in": sha256_hex(data)})
    return report


def property_test() -> None:
    import random
    rng = random.Random(20260713)
    lengths = list(range(0, 20)) + [31, 32, 33, 63, 64, 65, 255, 256, 257]
    modes = [("black", "sequential"), ("black", "pyramid"),
             ("white", "pyramid"), ("both", "pyramid"), ("omni", "pyramid")]
    for n in lengths:
        data = bytes(rng.randrange(256) for _ in range(n))
        for mode, schedule in modes:
            archive, _ = encode(data, mode=mode, schedule=schedule, stride=16,
                                block_size=64, table_bits=9)
            restored, _ = decode(archive)
            if restored != data:
                raise AssertionError((n, mode, schedule))
    print(f"FISCHER_PROPERTY|cases={len(lengths)*len(modes)}|status=PASS|json=0")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    enc = sub.add_parser("encode")
    enc.add_argument("input"); enc.add_argument("output"); enc.add_argument("--bytes", type=int)
    enc.add_argument("--mode", choices=["black", "white", "both", "omni"], default="both")
    enc.add_argument("--schedule", choices=["sequential", "pyramid"], default="pyramid")
    enc.add_argument("--stride", type=int, default=32); enc.add_argument("--block-size", type=int, default=4096)
    enc.add_argument("--table-bits", type=int, default=18); enc.add_argument("--report")
    dec = sub.add_parser("decode")
    dec.add_argument("input"); dec.add_argument("output"); dec.add_argument("--report")
    aud = sub.add_parser("audit")
    aud.add_argument("input"); aud.add_argument("--bytes", type=int)
    aud.add_argument("--direction", choices=["black", "white"], required=True)
    aud.add_argument("--order", type=int, choices=range(1, 6), required=True)
    aud.add_argument("--schedule", choices=["sequential", "pyramid"], default="pyramid")
    aud.add_argument("--stride", type=int, default=32); aud.add_argument("--block-size", type=int, default=4096)
    aud.add_argument("--table-bits", type=int, default=18); aud.add_argument("--report")
    sub.add_parser("property")
    args = parser.parse_args()
    if args.cmd == "property":
        property_test(); return
    if args.cmd == "encode":
        data = Path(args.input).read_bytes()
        if args.bytes is not None: data = data[:args.bytes]
        archive, report = encode(data, mode=args.mode, schedule=args.schedule,
                                 stride=args.stride, block_size=args.block_size,
                                 table_bits=args.table_bits)
        Path(args.output).write_bytes(archive)
        if args.report: Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, sort_keys=True)); return
    if args.cmd == "decode":
        raw, report = decode(Path(args.input).read_bytes())
        Path(args.output).write_bytes(raw)
        if args.report: Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, sort_keys=True)); return
    data = Path(args.input).read_bytes()
    if args.bytes is not None: data = data[:args.bytes]
    report = audit(data, direction=args.direction, order=args.order,
                   schedule=args.schedule, stride=args.stride,
                   block_size=args.block_size, table_bits=args.table_bits)
    if args.report: Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
