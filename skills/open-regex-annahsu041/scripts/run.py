#!/usr/bin/env python3
"""
open-regex skill — final output wrapper.

Reads a JSON payload from argv[1] containing {task_id, regex, rationale, confidence},
validates the contract minimally, and prints a single fenced JSON block matching
the Open Track output contract.
"""

from __future__ import annotations

import json
import sys


def emit_contract(obj: dict) -> int:
    out = {
        "task_id": str(obj.get("task_id", "")),
        "regex": str(obj.get("regex", "")).strip(),
        "rationale": str(obj.get("rationale", "")),
        "confidence": _clamp_confidence(obj.get("confidence", 0.5)),
    }
    sys.stdout.write("```json\n")
    sys.stdout.write(json.dumps(out, ensure_ascii=False, indent=2))
    sys.stdout.write("\n```\n")
    return 0


def _clamp_confidence(v) -> float:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0.0
    if f < 0.0:
        return 0.0
    if f > 1.0:
        return 1.0
    return f


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return emit_contract({
            "task_id": "",
            "regex": "",
            "rationale": "run.py invoked without argv payload",
            "confidence": 0.0,
        })

    try:
        payload = json.loads(argv[1])
        if not isinstance(payload, dict):
            raise ValueError("payload not an object")
    except (json.JSONDecodeError, ValueError) as e:
        return emit_contract({
            "task_id": "",
            "regex": "",
            "rationale": f"invalid argv JSON: {e}",
            "confidence": 0.0,
        })

    return emit_contract(payload)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
