#!/usr/bin/env python3
"""Corrected wrapper for aggregate_wolfram_cubes.py.

Attempt 1 added aggregate-only fields before verifying the lane receipt, causing all
20 otherwise valid receipts to be reported invalid. This wrapper ignores those
aggregate annotations during digest recomputation and then runs the same aggregator.
"""
from __future__ import annotations

import hashlib
import json

import aggregate_wolfram_cubes as aggregate


def verify_receipt(result):
    claimed = result.get("receipt_sha256")
    body = dict(result)
    for key in ("receipt_sha256", "artifact_path", "receipt_verified"):
        body.pop(key, None)
    actual = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    return claimed == actual


aggregate.verify_receipt = verify_receipt
aggregate.main()
