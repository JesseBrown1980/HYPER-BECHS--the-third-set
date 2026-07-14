#!/usr/bin/env python3
"""Build and test independent mathematical utilities from aggregate lens specs only."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


IMPLEMENTATION = r'''#!/usr/bin/env python3
"""Independent white-room mathematical utilities.

No Wolfram Service page body or third-party source checkout is used by this module.
The implementations follow general mathematical definitions and protocol contracts.
"""
from __future__ import annotations

import cmath
import json
import math
import re
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence

import numpy as np


def rank_mod_prime(matrix: Sequence[Sequence[int]], prime: int) -> int:
    if prime <= 1:
        raise ValueError("prime must be greater than one")
    rows = [list(map(lambda value: int(value) % prime, row)) for row in matrix]
    if not rows:
        return 0
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("ragged matrix")
    rank = 0
    for column in range(width):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, prime)
        rows[rank] = [(value * inverse) % prime for value in rows[rank]]
        for r in range(len(rows)):
            if r == rank:
                continue
            factor = rows[r][column]
            if factor:
                rows[r] = [(rows[r][c] - factor * rows[rank][c]) % prime for c in range(width)]
        rank += 1
        if rank == len(rows):
            break
    return rank


def solve_mod_prime(matrix: Sequence[Sequence[int]], rhs: Sequence[int], prime: int) -> list[int]:
    n = len(matrix)
    if n == 0 or len(rhs) != n or any(len(row) != n for row in matrix):
        raise ValueError("square system required")
    aug = [[int(matrix[r][c]) % prime for c in range(n)] + [int(rhs[r]) % prime] for r in range(n)]
    for column in range(n):
        pivot = next((r for r in range(column, n) if aug[r][column]), None)
        if pivot is None:
            raise ValueError("singular system")
        aug[column], aug[pivot] = aug[pivot], aug[column]
        inverse = pow(aug[column][column], -1, prime)
        aug[column] = [(value * inverse) % prime for value in aug[column]]
        for r in range(n):
            if r == column:
                continue
            factor = aug[r][column]
            if factor:
                aug[r] = [(aug[r][c] - factor * aug[column][c]) % prime for c in range(n + 1)]
    return [aug[r][-1] for r in range(n)]


def continued_fraction(value: Fraction) -> list[int]:
    if value.denominator == 0:
        raise ZeroDivisionError
    n, d = value.numerator, value.denominator
    result = []
    while d:
        q, r = divmod(n, d)
        result.append(q)
        n, d = d, r
    return result


def fraction_from_continued_fraction(terms: Sequence[int]) -> Fraction:
    if not terms:
        raise ValueError("at least one term required")
    result = Fraction(int(terms[-1]), 1)
    for term in reversed(terms[:-1]):
        result = Fraction(int(term), 1) + Fraction(1, result)
    return result


def graph_laplacian_spectrum(adjacency: Sequence[Sequence[float]]) -> list[float]:
    matrix = np.asarray(adjacency, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("square adjacency matrix required")
    if not np.allclose(matrix, matrix.T):
        raise ValueError("undirected symmetric adjacency required")
    if np.any(matrix < 0):
        raise ValueError("negative edge weight")
    laplacian = np.diag(matrix.sum(axis=1)) - matrix
    values = np.linalg.eigvalsh(laplacian)
    return [float(value) for value in values]


TOKEN = re.compile(r"\s*(?:(?P<int>[+-]?\d+)|(?P<symbol>[A-Za-z$][A-Za-z0-9$_]*)|(?P<bracket>[\[\]{},]))")


@dataclass(frozen=True)
class Expr:
    head: str
    args: tuple[object, ...]

    def canonical(self) -> str:
        return self.head + "[" + ",".join(canonical_expression(arg) for arg in self.args) + "]"


def canonical_expression(value: object) -> str:
    if isinstance(value, Expr):
        return value.canonical()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, tuple):
        return "{" + ",".join(canonical_expression(item) for item in value) + "}"
    raise TypeError(type(value))


class ExpressionParser:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        position = 0
        while position < len(source):
            match = TOKEN.match(source, position)
            if not match:
                raise ValueError(f"unexpected input at position {position}")
            position = match.end()
            kind = next(name for name, value in match.groupdict().items() if value is not None)
            self.tokens.append((kind, match.group(kind)))
        self.index = 0

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def pop(self, expected: str | None = None):
        token = self.peek()
        if token is None:
            raise ValueError("unexpected end")
        if expected is not None and token[1] != expected:
            raise ValueError(f"expected {expected}, got {token[1]}")
        self.index += 1
        return token

    def parse(self):
        value = self.parse_value()
        if self.peek() is not None:
            raise ValueError("trailing input")
        return value

    def parse_value(self):
        token = self.peek()
        if token is None:
            raise ValueError("unexpected end")
        kind, text = token
        if kind == "int":
            self.pop()
            return int(text)
        if kind == "symbol":
            self.pop()
            if self.peek() and self.peek()[1] == "[":
                self.pop("[")
                args = self.parse_sequence("]")
                return Expr(text, tuple(args))
            return text
        if text == "{":
            self.pop("{")
            return tuple(self.parse_sequence("}"))
        raise ValueError(f"unexpected token {text}")

    def parse_sequence(self, closing: str):
        values = []
        if self.peek() and self.peek()[1] == closing:
            self.pop(closing)
            return values
        while True:
            values.append(self.parse_value())
            token = self.peek()
            if token and token[1] == ",":
                self.pop(",")
                continue
            self.pop(closing)
            return values


def parse_expression(source: str):
    return ExpressionParser(source).parse()


SQRT2_INV = 1 / math.sqrt(2)
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = SQRT2_INV * np.array([[1, 1], [1, -1]], dtype=complex)
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)


def basis_state(bits: str) -> np.ndarray:
    if not bits or any(bit not in "01" for bit in bits):
        raise ValueError("nonempty bit string required")
    vector = np.zeros(2 ** len(bits), dtype=complex)
    vector[int(bits, 2)] = 1
    return vector


def apply_single_qubit(state: np.ndarray, gate: np.ndarray, qubit: int, qubits: int) -> np.ndarray:
    if state.shape != (2 ** qubits,) or gate.shape != (2, 2) or not 0 <= qubit < qubits:
        raise ValueError("invalid dimensions")
    operator = np.array([[1]], dtype=complex)
    for index in range(qubits):
        operator = np.kron(operator, gate if index == qubit else I2)
    return operator @ state


def bell_state() -> np.ndarray:
    state = basis_state("00")
    state = apply_single_qubit(state, H, 0, 2)
    return CNOT @ state


def probabilities(state: np.ndarray) -> list[float]:
    values = np.abs(state) ** 2
    if not math.isclose(float(values.sum()), 1.0, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError("state is not normalized")
    return [float(value) for value in values]


def frame_lsp_message(payload: dict) -> bytes:
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def parse_lsp_messages(stream: bytes) -> list[dict]:
    messages = []
    position = 0
    while position < len(stream):
        marker = stream.find(b"\r\n\r\n", position)
        if marker < 0:
            raise ValueError("incomplete header")
        header = stream[position:marker].decode("ascii")
        fields = {}
        for line in header.split("\r\n"):
            name, value = line.split(":", 1)
            fields[name.strip().lower()] = value.strip()
        length = int(fields["content-length"])
        start = marker + 4
        end = start + length
        if end > len(stream):
            raise ValueError("incomplete body")
        messages.append(json.loads(stream[start:end].decode("utf-8")))
        position = end
    return messages


def line_column_to_offset(text: str, line: int, column: int) -> int:
    if line < 0 or column < 0:
        raise ValueError("negative position")
    lines = text.splitlines(keepends=True)
    if line >= len(lines):
        raise ValueError("line out of range")
    content = lines[line]
    visible = content.rstrip("\r\n")
    if column > len(visible):
        raise ValueError("column out of range")
    return sum(len(item) for item in lines[:line]) + column
'''


TESTS = r'''#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import random
from fractions import Fraction

import numpy as np

import implementation as w


def test_rank_and_solve():
    p = 257
    matrix = [[1, 1, 1], [1, 2, 4], [1, 3, 9]]
    rhs = [6, 17, 34]
    assert w.rank_mod_prime(matrix, p) == 3
    solution = w.solve_mod_prime(matrix, rhs, p)
    assert solution == [1, 2, 3]
    assert w.rank_mod_prime([[1, 2], [2, 4]], p) == 1


def test_continued_fractions():
    values = [Fraction(355, 113), Fraction(-22, 7), Fraction(0, 1), Fraction(1234567, 890123)]
    for value in values:
        terms = w.continued_fraction(value)
        assert w.fraction_from_continued_fraction(terms) == value


def test_graph_laplacian():
    path3 = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    spectrum = w.graph_laplacian_spectrum(path3)
    assert np.allclose(spectrum, [0, 1, 3], atol=1e-12)
    complete3 = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    assert np.allclose(w.graph_laplacian_spectrum(complete3), [0, 3, 3], atol=1e-12)


def test_expression_parser():
    examples = {
        "Plus[1,Times[2,x]]": "Plus[1,Times[2,x]]",
        "ListLike[{1,2,3},f[x]]": "ListLike[{1,2,3},f[x]]",
        "Empty[]": "Empty[]",
    }
    for source, expected in examples.items():
        assert w.canonical_expression(w.parse_expression(source)) == expected
    try:
        w.parse_expression("f[1,")
    except ValueError:
        pass
    else:
        raise AssertionError("malformed expression accepted")


def test_quantum():
    bell = w.bell_state()
    probs = w.probabilities(bell)
    assert np.allclose(probs, [0.5, 0, 0, 0.5], atol=1e-12)
    assert np.allclose(w.X @ w.X, w.I2)
    assert np.allclose(w.H @ w.H, w.I2)


def test_lsp():
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "method": "textDocument/didOpen", "params": {"text": "αβ"}},
    ]
    stream = b"".join(w.frame_lsp_message(message) for message in messages)
    assert w.parse_lsp_messages(stream) == messages
    text = "abc\ndef\r\nghi"
    assert w.line_column_to_offset(text, 0, 2) == 2
    assert w.line_column_to_offset(text, 1, 3) == 7
    assert w.line_column_to_offset(text, 2, 1) == 10


def main():
    tests = [test_rank_and_solve, test_continued_fractions, test_graph_laplacian,
             test_expression_parser, test_quantum, test_lsp]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(json.dumps({"tests": len(tests), "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
'''


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    spec_root = Path(args.spec_root)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    specs = []
    forbidden = []
    for path in spec_root.rglob("*"):
        if not path.is_file():
            continue
        if path.name not in {"white-room-spec.json", "shadow-cube.json", "shadow-cube.hbp", "SHA256SUMS"}:
            forbidden.append(str(path.relative_to(spec_root)))
        if path.name == "white-room-spec.json":
            specs.append(json.loads(path.read_text(encoding="utf-8")))
    if forbidden:
        raise RuntimeError(f"unexpected observer files crossed white-room boundary: {forbidden}")
    if len(specs) < 3:
        raise RuntimeError(f"expected three observer specs, got {len(specs)}")

    methods = sorted({method for spec in specs for method in spec.get("clean_room_methods", [])})
    requirements = sorted({item for spec in specs for item in spec.get("functional_requirements", [])})

    (out / "implementation.py").write_text(IMPLEMENTATION, encoding="utf-8")
    (out / "test_white_room.py").write_text(TESTS, encoding="utf-8")
    run = subprocess.run([sys.executable, "test_white_room.py"], cwd=out, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (out / "test.log").write_text(run.stdout, encoding="utf-8")
    result = {
        "schema": "WHITE-ROOM-BUILD-RESULT-v1",
        "observer_spec_count": len(specs),
        "methods_requested": methods,
        "requirements": requirements,
        "source_page_bodies_received": False,
        "third_party_source_checkouts_received": False,
        "unexpected_input_files": forbidden,
        "implementation_sha256": sha256((out / "implementation.py").read_bytes()),
        "tests_sha256": sha256((out / "test_white_room.py").read_bytes()),
        "test_exit_code": run.returncode,
        "test_output_sha256": sha256(run.stdout.encode("utf-8")),
        "status": "PASS" if run.returncode == 0 else "FAILED",
    }
    (out / "RESULT.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (out / "RESULT.hbp").write_text(
        "WHITEROOMv1"
        f"|specs={len(specs)}|methods={len(methods)}|source_bodies=0|source_checkouts=0"
        f"|implementation_sha256={result['implementation_sha256']}|tests_sha256={result['tests_sha256']}"
        f"|status={result['status']}|json=0\n",
        encoding="utf-8"
    )
    sums = []
    for name in ("implementation.py", "test_white_room.py", "test.log", "RESULT.json", "RESULT.hbp"):
        sums.append(f"{sha256((out / name).read_bytes())}  {name}")
    (out / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print(f"WHITEROOM|specs={len(specs)}|methods={len(methods)}|source_bodies=0|status={result['status']}|json=0")
    if run.returncode != 0:
        raise SystemExit(run.returncode)


if __name__ == "__main__":
    main()
