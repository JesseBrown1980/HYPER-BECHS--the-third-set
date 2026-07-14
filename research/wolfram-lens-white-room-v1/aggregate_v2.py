#!/usr/bin/env python3
"""Compatibility wrapper that verifies original cube bodies before aggregate metadata."""
from __future__ import annotations

import hashlib
import json

import aggregate


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def verify_lens(cube):
    claimed = cube.get("cube_sha256")
    body = dict(cube)
    for key in ("cube_sha256", "artifact_path", "digest_verified"):
        body.pop(key, None)
    return claimed == hashlib.sha256(canonical(body)).hexdigest()


def verify_open_cube(cube):
    claimed = cube.get("cube_manifest_sha256")
    body = dict(cube)
    for key in ("cube_manifest_sha256", "artifact_path", "digest_verified"):
        body.pop(key, None)
    return claimed == hashlib.sha256(canonical(body)).hexdigest()


aggregate.verify_lens = verify_lens
aggregate.verify_open_cube = verify_open_cube
aggregate.main()
