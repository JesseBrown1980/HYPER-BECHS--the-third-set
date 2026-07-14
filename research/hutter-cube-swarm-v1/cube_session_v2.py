#!/usr/bin/env python3
"""Compatibility wrapper for cube_session.py.

The first swarm attempt proved the 30-job fan-out but exposed one receipt-rendering
bug: research-only lanes store ``training: null``, while the original HBP renderer
called ``.get`` on that null value. This wrapper fixes only the renderer and then
executes the original source-pinned session logic unchanged.
"""
from __future__ import annotations

import cube_session


def hbp_summary(cube):
    def esc(value):
        return str(value).replace("\\", "\\\\").replace("|", "\\p").replace("\n", "\\n")

    training = cube.get("training") or {}
    research = cube.get("research") or {}
    fields = {
        "lane": cube["lane_id"],
        "family": cube["family"],
        "kind": cube["kind"],
        "status": cube["status"],
        "cube_sha256": cube["cube_sha256"],
        "source_sha256": research.get("text_sha256", "none"),
        "algorithms": len(research.get("algorithm_hits", [])),
        "formulas": len(research.get("formula_candidates", [])),
        "people": len(research.get("people_candidates", [])),
        "training_status": training.get("status", "not-run"),
        "restore": int(bool(training.get("all_restore", False))),
        "started_at": cube["runtime"]["started_at"],
        "ended_at": cube["runtime"]["ended_at"],
        "json": 0,
    }
    return "CUBESESSIONv1" + "".join(f"|{k}={esc(v)}" for k, v in fields.items()) + "\n"


cube_session.hbp_summary = hbp_summary
cube_session.main()
