#!/usr/bin/env python3
"""
Deterministic regex validator for open-regex skill.

Usage:
    python validate_regex.py '{"regex":"...", "positive_examples":["..."], "negative_examples":["..."]}'

Prints a single fenced JSON block:
    {"ok": true|false, "error": "<error message or failed examples>"}
"""

from __future__ import annotations

import json
import re
import sys


def _emit(ok: bool, error: str = "") -> int:
    out = {"ok": bool(ok), "error": error}
    sys.stdout.write("```json\n")
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    sys.stdout.write("\n```\n")
    return 0 if ok else 1


def validate(regex_str: str, positive_examples: list[str], negative_examples: list[str]) -> tuple[bool, str]:
    if not regex_str:
        return False, "Empty regex"
        
    try:
        pattern = re.compile(regex_str)
    except re.error as e:
        return False, f"Invalid regex compilation error: {e}"
        
    failed_pos = []
    for pos in positive_examples:
        # Check if the pattern matches the positive example.
        # We use re.search. Usually positive examples expect the regex to match the whole string.
        # But we let re.search match.
        if not pattern.search(pos):
            failed_pos.append(pos)
            
    failed_neg = []
    for neg in negative_examples:
        # Check if the pattern incorrectly matches the negative example.
        if pattern.search(neg):
            failed_neg.append(neg)
            
    errors = []
    if failed_pos:
        errors.append(f"Failed to match positive examples: {failed_pos}")
    if failed_neg:
        errors.append(f"Incorrectly matched negative examples (should not match): {failed_neg}")
        
    if errors:
        return False, "; ".join(errors)
        
    return True, ""


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return _emit(False, "usage: validate_regex.py '<json payload>'")
    try:
        payload = json.loads(argv[1])
    except json.JSONDecodeError as e:
        return _emit(False, f"argv JSON invalid: {e}")
        
    regex_str = str(payload.get("regex", ""))
    positive_examples = payload.get("positive_examples", []) or []
    negative_examples = payload.get("negative_examples", []) or []
    
    ok, err = validate(regex_str, positive_examples, negative_examples)
    return _emit(ok, err)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
