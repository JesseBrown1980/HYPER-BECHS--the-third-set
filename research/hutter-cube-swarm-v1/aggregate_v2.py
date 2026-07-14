#!/usr/bin/env python3
"""Run aggregate.py with cube digest verification before aggregate-only metadata."""
from __future__ import annotations
import hashlib
import json
import aggregate


def verify_cube(cube):
    claimed = cube.get("cube_sha256")
    body = dict(cube)
    body.pop("cube_sha256", None)
    body.pop("artifact_path", None)
    body.pop("digest_verified", None)
    actual = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    return claimed == actual


aggregate.verify_cube = verify_cube
aggregate.main()
