#!/usr/bin/env python3
"""Fischer bidirectional predictor-transform codec v3.

Five black experts predict from already-decoded left context. Five white experts
predict from already-decoded right context under a deterministic pyramid schedule.
A fixed-point Shannon mixer chooses the consensus prediction. The stream records a
hit bit when consensus predicted the byte and otherwise records the actual miss byte.
Both streams are losslessly entropy-coded. The decoder recreates the same schedule,
models, and mixer and must restore the original bytes exactly.

This is a bounded-memory research codec and causal bidirectional test, not a Hutter
Prize submission and not a claim of physical quantum cloning.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import time
import zlib
from array import array
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MAGIC = b"FSC3"
VERSION = 3
PRIMES = {
    ("black", 1): 11, ("black", 2): 13, ("black", 3): 17,
    ("black", 4): 19, ("black", 5): 23,
    ("white", 1): 29, ("white", 2): 31, ("white", 3): 37,
    ("white", 4): 41, ("white", 5): 43,
}
MASK64 = (1 << 64) - 1


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


def _compress(data: bytes, backend: str, level: int = 19) -> bytes:
    if backend == "zstd":
        import zstandard as zstd
        return zstd.ZstdCompressor(level=level).compress(data)
    if backend == "zlib":
        return zlib.compress(data, 9)
    raise ValueError(backend)


def _decompress(data: bytes, backend: str, max_output: int | None = None) -> bytes:
    if backend == "zstd":
        import zstandard as zstd
        return zstd.ZstdDecompressor().decompress(data, max_output_size=max_output or 0)
    if backend == "zlib":
        return zlib.decompress(data)
    raise ValueError(backend)


def choose_backend(requested: str) -> str:
    if requested != "auto":
        return requested
    try:
        import zstandard  # noqa: F401
        return "zstd"
    except Exception:
        return "zlib"


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
        for left_edge, right_edge in intervals:
            if right_edge - left_edge <= 1:
                continue
            midpoint = (left_edge + right_edge) // 2
            lo, hi = 0, len(known)
            while lo < hi:
                q = (lo + hi) // 2
                if known[q] < midpoint:
                    lo = q + 1
                else:
                    hi = q
            j = lo
            left = tuple(reversed(known[max(0, j - max_context):j]))
            right = tuple(known[j:min(len(known), j + max_context)])
            tasks.append(Task(midpoint, left, right, right_edge - left_edge, phase))
            mids.append(midpoint)
            if midpoint - left_edge > 1:
                nxt.append((left_edge, midpoint))
            if right_edge - midpoint > 1:
                nxt.append((midpoint, right_edge))
        known = sorted(known + mids)
        intervals = nxt
        phase += 1
    if len(tasks) != n or len({task.index for task in tasks}) != n:
        raise AssertionError("pyramid schedule must be a permutation")
    return tasks


def tasks_for(n: int, schedule: str, stride: int) -> list[Task]:
    if schedule == "sequential":
        return sequential_tasks(n)
    if schedule == "pyramid":
        return pyramid_tasks(n, stride)
    raise ValueError(schedule)


class Expert:
    """One bounded hash-table Bobby: context -> current best byte + confidence."""

    def __init__(self, direction: str, order: int, table_bits: int) -> None:
        self.direction = direction
        self.order = order
        self.prime = PRIMES[(direction, order)]
        self.size = 1 << table_bits
        self.mask = self.size - 1
        self.tags = array("Q", [0]) * self.size
        self.symbols = bytearray(self.size)
        self.conf = array("H", [0]) * self.size
        self.calls = 0
        self.correct = 0
        self.high_conf_misses = 0
        self.sum_conf = 0
        self.replacements = 0
        self.touched = bytearray(self.size)

    def context_hash(self, buf: bytearray, task: Task) -> int:
        idxs = task.left if self.direction == "black" else task.right
        h = mix64(self.prime * 0x9E3779B185EBCA87 ^ (task.scale << 17) ^
                  (task.phase << 5) ^ len(idxs) ^ (self.order << 56))
        used = 0
        for idx in idxs:
            h = mix64(h ^ (buf[idx] + 1 + used * 257))
            used += 1
            if used >= self.order:
                break
        return mix64(h ^ (used << 48)) or 1

    def predict(self, base: int, fallback: int) -> tuple[int, int, int]:
        slot = base & self.mask
        if self.tags[slot] == base and self.conf[slot] > 0:
            return self.symbols[slot], int(self.conf[slot]), slot
        return fallback, 0, slot

    def update(self, base: int, slot: int, actual: int, predicted: int, confidence: int) -> None:
        self.calls += 1
        self.correct += int(predicted == actual)
        self.high_conf_misses += int(predicted != actual and confidence >= 16)
        self.sum_conf += confidence
        if self.tags[slot] != base:
            self.tags[slot] = base
            self.symbols[slot] = actual
            self.conf[slot] = 1
            if not self.touched[slot]:
                self.touched[slot] = 1
            else:
                self.replacements += 1
            return
        if self.symbols[slot] == actual:
            self.conf[slot] = min(65535, self.conf[slot] + 3)
        elif self.conf[slot] > 1:
            self.conf[slot] -= 1
        else:
            self.symbols[slot] = actual
            self.conf[slot] = 1
            self.replacements += 1

    def report(self, best_error: float, trust_pct: float) -> dict[str, Any]:
        error = 1.0 - self.correct / max(1, self.calls)
        cpl = round(1000 * max(0.0, error - best_error))
        verdict = "BLOCK" if cpl >= 500 else ("HOLD" if cpl >= 150 else "PROCEED")
        return {
            "expert": f"{self.direction}-o{self.order}",
            "direction": self.direction,
            "order": self.order,
            "prime": self.prime,
            "actor_pid": sha256_hex(f"FISCHER|{self.direction}|{self.order}|{self.prime}".encode())[:16],
            "accuracy": self.correct / max(1, self.calls),
            "error_rate": error,
            "mean_confidence": self.sum_conf / max(1, self.calls),
            "high_confidence_blunders": self.high_conf_misses,
            "touched_slots": int(sum(self.touched)),
            "replacements": self.replacements,
            "codec_cpl_vs_best": cpl,
            "fischer_verdict": verdict,
            "trust_pct": trust_pct,
        }


class ShannonMixer:
    def __init__(self, n: int) -> None:
        self.weights = [1024] * n
        self.calls = 0
        self.correct = 0
        self.disagreements = 0
        self.fallback_uses = 0

    def choose(self, predictions: list[tuple[int, int]], fallback: int) -> int:
        scores: dict[int, int] = {}
        for j, (symbol, confidence) in enumerate(predictions):
            scores[symbol] = scores.get(symbol, 0) + self.weights[j] * (1 + min(confidence, 255))
        if not scores:
            self.fallback_uses += 1
            return fallback
        best_score = max(scores.values())
        winners = [symbol for symbol, score in scores.items() if score == best_score]
        if len(set(symbol for symbol, _ in predictions)) > 1:
            self.disagreements += 1
        return fallback if fallback in winners else min(winners)

    def update(self, predictions: list[tuple[int, int]], actual: int, chosen: int) -> None:
        self.calls += 1
        self.correct += int(chosen == actual)
        for j, (symbol, confidence) in enumerate(predictions):
            if symbol == actual:
                self.weights[j] = min(1 << 24, self.weights[j] + 8 + min(confidence, 64))
            else:
                self.weights[j] = max(1, self.weights[j] - 1)


class Model:
    def __init__(self, mode: str, table_bits: int) -> None:
        specs: list[tuple[str, int]] = []
        if mode in ("black", "both"):
            specs.extend(("black", order) for order in range(1, 6))
        if mode in ("white", "both"):
            specs.extend(("white", order) for order in range(1, 6))
        self.experts = [Expert(direction, order, table_bits) for direction, order in specs]
        self.mixer = ShannonMixer(len(self.experts))
        self.global_counts = [1] * 256
        self.global_mode = 32
        self.global_mode_count = 1
        self.mode = mode
        self.hits = 0
        self.misses = 0

    def predict(self, buf: bytearray, task: Task) -> tuple[int, list[tuple[int, int, int, int]]]:
        details = []
        votes = []
        for expert in self.experts:
            base = expert.context_hash(buf, task)
            symbol, confidence, slot = expert.predict(base, self.global_mode)
            details.append((base, slot, symbol, confidence))
            votes.append((symbol, confidence))
        return self.mixer.choose(votes, self.global_mode), details

    def update(self, actual: int, chosen: int, details: list[tuple[int, int, int, int]]) -> None:
        votes = [(symbol, confidence) for _, _, symbol, confidence in details]
        self.mixer.update(votes, actual, chosen)
        for expert, (base, slot, symbol, confidence) in zip(self.experts, details):
            expert.update(base, slot, actual, symbol, confidence)
        self.hits += int(chosen == actual)
        self.misses += int(chosen != actual)
        self.global_counts[actual] += 1
        if self.global_counts[actual] > self.global_mode_count:
            self.global_mode = actual
            self.global_mode_count = self.global_counts[actual]

    def report(self) -> dict[str, Any]:
        errors = [1.0 - expert.correct / max(1, expert.calls) for expert in self.experts]
        best_error = min(errors) if errors else 0.0
        total_weight = sum(self.mixer.weights) or 1
        experts = [expert.report(best_error, 100.0 * weight / total_weight)
                   for expert, weight in zip(self.experts, self.mixer.weights)]
        black_trust = sum(row["trust_pct"] for row in experts if row["direction"] == "black")
        white_trust = sum(row["trust_pct"] for row in experts if row["direction"] == "white")
        return {
            "mode": self.mode,
            "prediction_calls": self.mixer.calls,
            "hit_rate": self.hits / max(1, self.hits + self.misses),
            "miss_rate": self.misses / max(1, self.hits + self.misses),
            "mixer_accuracy": self.mixer.correct / max(1, self.mixer.calls),
            "disagreement_rate": self.mixer.disagreements / max(1, self.mixer.calls),
            "black_trust_pct": black_trust,
            "white_trust_pct": white_trust,
            "global_mode": self.global_mode,
            "experts": experts,
        }


HEADER_PREFIX = struct.Struct(">4sI")


def pack_bits(bits: bytearray) -> bytes:
    out = bytearray((len(bits) + 7) // 8)
    for i, bit in enumerate(bits):
        if bit:
            out[i >> 3] |= 1 << (7 - (i & 7))
    return bytes(out)


def bit_at(buf: bytes, index: int) -> int:
    return (buf[index >> 3] >> (7 - (index & 7))) & 1


def encode(data: bytes, *, mode: str = "both", schedule: str = "pyramid",
           stride: int = 32, block_size: int = 4096, table_bits: int = 17,
           backend: str = "auto") -> tuple[bytes, dict[str, Any]]:
    backend = choose_backend(backend)
    model = Model(mode, table_bits)
    hit_bits = bytearray()
    misses = bytearray()
    schedule_cache: dict[int, list[Task]] = {}
    started = time.perf_counter()
    for offset in range(0, len(data), block_size):
        block = data[offset:offset + block_size]
        tasks = schedule_cache.setdefault(len(block), tasks_for(len(block), schedule, stride))
        buf = bytearray(block)
        for task in tasks:
            actual = block[task.index]
            chosen, details = model.predict(buf, task)
            hit = int(chosen == actual)
            hit_bits.append(hit)
            if not hit:
                misses.append(actual)
            model.update(actual, chosen, details)
    encode_model_s = time.perf_counter() - started
    packed_hits = pack_bits(hit_bits)
    hit_comp = _compress(packed_hits, backend)
    miss_comp = _compress(bytes(misses), backend)
    metadata = {
        "version": VERSION, "mode": mode, "schedule": schedule, "stride": stride,
        "block_size": block_size, "table_bits": table_bits, "backend": backend,
        "raw_len": len(data), "hit_count": model.hits, "miss_count": model.misses,
        "hit_bits_len": len(hit_bits), "packed_hits_len": len(packed_hits),
        "hit_comp_len": len(hit_comp), "miss_comp_len": len(miss_comp),
        "sha256_raw": sha256_hex(data), "sha256_hit_stream": sha256_hex(packed_hits),
        "sha256_miss_stream": sha256_hex(bytes(misses)),
    }
    meta = json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode()
    archive = HEADER_PREFIX.pack(MAGIC, len(meta)) + meta + hit_comp + miss_comp
    report = model.report()
    baseline = _compress(data, backend)
    report.update(metadata)
    report.update({
        "archive_bytes": len(archive), "archive_bpc": len(archive) * 8 / max(1, len(data)),
        "payload_bytes": len(hit_comp) + len(miss_comp),
        "payload_bpc": (len(hit_comp) + len(miss_comp)) * 8 / max(1, len(data)),
        "baseline_bytes": len(baseline), "baseline_bpc": len(baseline) * 8 / max(1, len(data)),
        "delta_vs_baseline_pct": (len(archive) / max(1, len(baseline)) - 1) * 100,
        "encode_model_s": encode_model_s, "sha256_archive": sha256_hex(archive),
    })
    return archive, report


def decode(archive: bytes) -> tuple[bytes, dict[str, Any]]:
    if len(archive) < HEADER_PREFIX.size:
        raise ValueError("archive too short")
    magic, meta_len = HEADER_PREFIX.unpack(archive[:HEADER_PREFIX.size])
    if magic != MAGIC:
        raise ValueError("bad magic")
    start = HEADER_PREFIX.size
    metadata = json.loads(archive[start:start + meta_len])
    if metadata["version"] != VERSION:
        raise ValueError("unsupported version")
    position = start + meta_len
    hit_comp = archive[position:position + metadata["hit_comp_len"]]
    position += metadata["hit_comp_len"]
    miss_comp = archive[position:position + metadata["miss_comp_len"]]
    packed_hits = _decompress(hit_comp, metadata["backend"], metadata["packed_hits_len"])
    misses = _decompress(miss_comp, metadata["backend"], metadata["miss_count"])
    if len(packed_hits) != metadata["packed_hits_len"] or len(misses) != metadata["miss_count"]:
        raise ValueError("decompressed stream length mismatch")
    if sha256_hex(packed_hits) != metadata["sha256_hit_stream"] or sha256_hex(misses) != metadata["sha256_miss_stream"]:
        raise ValueError("stream digest mismatch")
    model = Model(metadata["mode"], metadata["table_bits"])
    output = bytearray(metadata["raw_len"])
    schedule_cache: dict[int, list[Task]] = {}
    hit_index = 0
    miss_index = 0
    started = time.perf_counter()
    for offset in range(0, len(output), metadata["block_size"]):
        size = min(metadata["block_size"], len(output) - offset)
        tasks = schedule_cache.setdefault(size, tasks_for(size, metadata["schedule"], metadata["stride"]))
        buf = bytearray(size)
        for task in tasks:
            chosen, details = model.predict(buf, task)
            if bit_at(packed_hits, hit_index):
                actual = chosen
            else:
                actual = misses[miss_index]
                miss_index += 1
            hit_index += 1
            buf[task.index] = actual
            model.update(actual, chosen, details)
        output[offset:offset + size] = buf
    decode_model_s = time.perf_counter() - started
    if hit_index != metadata["hit_bits_len"] or miss_index != metadata["miss_count"]:
        raise ValueError("stream consumption mismatch")
    restored = bytes(output)
    report = model.report()
    report.update(metadata)
    report.update({"archive_bytes": len(archive),
                   "archive_bpc": len(archive) * 8 / max(1, len(restored)),
                   "decode_model_s": decode_model_s, "sha256_out": sha256_hex(restored),
                   "restore": sha256_hex(restored) == metadata["sha256_raw"]})
    return restored, report


def audit(data: bytes, *, direction: str, order: int, schedule: str = "pyramid",
          stride: int = 32, block_size: int = 4096, table_bits: int = 17) -> dict[str, Any]:
    expert = Expert(direction, order, table_bits)
    global_counts = [1] * 256
    global_mode = 32
    global_mode_count = 1
    schedule_cache: dict[int, list[Task]] = {}
    started = time.perf_counter()
    for offset in range(0, len(data), block_size):
        block = data[offset:offset + block_size]
        tasks = schedule_cache.setdefault(len(block), tasks_for(len(block), schedule, stride))
        buf = bytearray(block)
        for task in tasks:
            actual = block[task.index]
            base = expert.context_hash(buf, task)
            predicted, confidence, slot = expert.predict(base, global_mode)
            expert.update(base, slot, actual, predicted, confidence)
            global_counts[actual] += 1
            if global_counts[actual] > global_mode_count:
                global_mode = actual
                global_mode_count = global_counts[actual]
    elapsed = time.perf_counter() - started
    report = expert.report(1.0 - expert.correct / max(1, expert.calls), 100.0)
    report.update({"raw_bytes": len(data), "schedule": schedule, "stride": stride,
                   "block_size": block_size, "table_bits": table_bits, "elapsed_s": elapsed,
                   "sha256_in": sha256_hex(data)})
    return report


def property_test() -> None:
    import random
    rng = random.Random(20260713)
    lengths = list(range(80)) + [100, 255, 256, 999, 4095, 4096, 4097]
    for n in lengths:
        data = bytes(rng.randrange(256) for _ in range(n))
        for mode, schedule in [("black", "sequential"), ("black", "pyramid"),
                               ("white", "pyramid"), ("both", "pyramid")]:
            archive, _ = encode(data, mode=mode, schedule=schedule, stride=16,
                                block_size=64, table_bits=10, backend="zlib")
            restored, report = decode(archive)
            if restored != data or not report["restore"]:
                raise AssertionError((n, mode, schedule))
    print(f"FISCHER_PROPERTY|cases={len(lengths)*4}|status=PASS|json=0")


def bench(data: bytes, output_dir: Path, backend: str, block_size: int, stride: int,
          table_bits: int) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    configs = [("black-sequential", "black", "sequential"),
               ("black-pyramid", "black", "pyramid"),
               ("white-pyramid", "white", "pyramid"),
               ("blackwhite-pyramid", "both", "pyramid")]
    rows = []
    for name, mode, schedule in configs:
        archive, enc_report = encode(data, mode=mode, schedule=schedule, stride=stride,
                                     block_size=block_size, table_bits=table_bits, backend=backend)
        restored, dec_report = decode(archive)
        if restored != data or not dec_report["restore"]:
            raise AssertionError(name)
        (output_dir / f"{name}.fsc3").write_bytes(archive)
        row = {"name": name, **enc_report, "restore": True,
               "sha256_out": dec_report["sha256_out"],
               "decode_model_s": dec_report["decode_model_s"]}
        (output_dir / f"{name}.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
        rows.append(row)
        print(f"FISCHER_BENCH|name={name}|bpc={row['archive_bpc']:.6f}|baseline_bpc={row['baseline_bpc']:.6f}|hit_rate={row['hit_rate']:.6f}|black_trust={row['black_trust_pct']:.3f}|white_trust={row['white_trust_pct']:.3f}|restore=1|json=0")
    by = {row["name"]: row for row in rows}
    black = by["black-pyramid"]["archive_bytes"]
    both = by["blackwhite-pyramid"]["archive_bytes"]
    summary = {
        "raw_bytes": len(data), "backend": choose_backend(backend),
        "black_pyramid_bytes": black, "blackwhite_pyramid_bytes": both,
        "white_gain_vs_black_pct": (1 - both / black) * 100,
        "black_pyramid_bpc": by["black-pyramid"]["archive_bpc"],
        "blackwhite_pyramid_bpc": by["blackwhite-pyramid"]["archive_bpc"],
        "blackwhite_black_trust_pct": by["blackwhite-pyramid"]["black_trust_pct"],
        "blackwhite_white_trust_pct": by["blackwhite-pyramid"]["white_trust_pct"],
        "all_restore": all(row["restore"] for row in rows), "sha256": sha256_hex(data),
    }
    (output_dir / "bench.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=2), encoding="utf-8")
    print("FISCHER_VERDICT|" + "|".join(
        f"{key}={value:.6f}" if isinstance(value, float) else f"{key}={value}"
        for key, value in summary.items()) + "|json=0")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("property")
    enc = sub.add_parser("encode")
    enc.add_argument("input"); enc.add_argument("output"); enc.add_argument("--bytes", type=int)
    enc.add_argument("--mode", choices=["black", "white", "both"], default="both")
    enc.add_argument("--schedule", choices=["sequential", "pyramid"], default="pyramid")
    enc.add_argument("--stride", type=int, default=32); enc.add_argument("--block-size", type=int, default=4096)
    enc.add_argument("--table-bits", type=int, default=17)
    enc.add_argument("--backend", choices=["auto", "zstd", "zlib"], default="auto")
    enc.add_argument("--report")
    dec = sub.add_parser("decode")
    dec.add_argument("input"); dec.add_argument("output"); dec.add_argument("--report")
    aud = sub.add_parser("audit")
    aud.add_argument("input"); aud.add_argument("--bytes", type=int)
    aud.add_argument("--direction", choices=["black", "white"], required=True)
    aud.add_argument("--order", type=int, choices=range(1, 6), required=True)
    aud.add_argument("--schedule", choices=["sequential", "pyramid"], default="pyramid")
    aud.add_argument("--stride", type=int, default=32); aud.add_argument("--block-size", type=int, default=4096)
    aud.add_argument("--table-bits", type=int, default=17); aud.add_argument("--report")
    ben = sub.add_parser("bench")
    ben.add_argument("input"); ben.add_argument("--bytes", type=int, default=150000)
    ben.add_argument("--output-dir", default="fischer-out")
    ben.add_argument("--backend", choices=["auto", "zstd", "zlib"], default="auto")
    ben.add_argument("--stride", type=int, default=32); ben.add_argument("--block-size", type=int, default=4096)
    ben.add_argument("--table-bits", type=int, default=17)
    args = parser.parse_args()
    if args.cmd == "property":
        property_test(); return
    if args.cmd == "decode":
        archive = Path(args.input).read_bytes(); raw, report = decode(archive)
        Path(args.output).write_bytes(raw)
        if args.report: Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, sort_keys=True)); return
    data = Path(args.input).read_bytes()
    if args.bytes is not None: data = data[:args.bytes]
    if args.cmd == "audit":
        report = audit(data, direction=args.direction, order=args.order, schedule=args.schedule,
                       stride=args.stride, block_size=args.block_size, table_bits=args.table_bits)
        if args.report: Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, sort_keys=True)); return
    if args.cmd == "bench":
        bench(data, Path(args.output_dir), args.backend, args.block_size, args.stride, args.table_bits); return
    archive, report = encode(data, mode=args.mode, schedule=args.schedule, stride=args.stride,
                             block_size=args.block_size, table_bits=args.table_bits, backend=args.backend)
    Path(args.output).write_bytes(archive)
    if args.report: Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
