---
name: code-author-annahsu041
description: Implement a Python function from a natural-language task description, self-test, and emit the AIASE 2026 Pairwise Code Author contract.
version: 0.1.0
metadata:
  hermes:
    tags: [code, python, aiase-2026]
    category: code
---

# Code Author Skill (Pairwise Track)

> **TODO for student**: rename folder + frontmatter `name` to include your github_id;
> fill in the LLM-side planning in the Procedure; strengthen the harness in `scripts/`.

## When to Use

When the user sends a JSON payload with `task_description`, `constraints` (entry_function, max_loc, imports_forbidden), and `task_id`. The skill must produce a Python implementation that:

- defines exactly the entry function named in `constraints.entry_function`,
- does not exceed `constraints.max_loc` source lines (measured by `radon raw`),
- does not import anything in `constraints.imports_forbidden`,
- handles realistic edge cases (empty input, single element, extremes — see Pitfalls).

Trigger example:

```
/code-author-annahsu041 {"task_id":"task_042",
  "task_description":"Implement merge_intervals(intervals): merge overlapping intervals, empty input returns [].",
  "constraints":{"entry_function":"merge_intervals","max_loc":500,"imports_forbidden":["os","sys"]}}
```

## Procedure

**Complete this skill in exactly 3 terminal calls. Do NOT reason between calls.**

1. **Write** a Python implementation of `constraints.entry_function` mentally (no intermediate files).

2. **Selftest** — run exactly once with your code and 3–5 edge cases. Use key `sample_inputs` (not `test_cases`):

   ```
   python scripts/selftest.py '{"code":"<your_code_as_one_line_with_\\n>","constraints":<constraints_json>,"sample_inputs":[{"input":[<arg1>],"expected":<expected>},...]}'
   ```

   Edge cases to always include: empty input (`[]` or `""`), single element, and the standard example from the description.

3. **Emit immediately** — do NOT retry selftest even if some tests fail. Run:

   ```
   python scripts/run.py '{"task_id":"<task_id>","code":"<your_code_as_one_line_with_\\n>","loc":<sloc_from_selftest>,"self_test_results":{"passed":<n>,"failed":<m>},"rationale":"<one_sentence>","confidence":<0.0-1.0>}'
   ```

   Output the resulting fenced JSON block **unchanged** as your final response.

## Pitfalls

- **Missing empty-input handling** — always test `[]` / `""` / `0`.
- **Wrong selftest key** — selftest.py uses `sample_inputs`, NOT `test_cases`.
- **Forbidden imports** — do not import `os`, `sys`, `subprocess` or anything in `imports_forbidden`.
- **LoC limit** — `radon raw` counts source lines (excludes blank + pure-comment). Keep code lean.
- **No intermediate files** — do not `printf` or write code to disk. Pass code directly as JSON string.

## Verification

The output of `scripts/run.py` is a single fenced ```json``` block with:

- `task_id` (must equal input)
- `code` (string, valid Python defining `entry_function`)
- `loc` (integer — what your harness measured)
- `self_test_results` (object with `passed` and `failed` counts at minimum)
- `rationale` (string)
- `confidence` (number in `[0.0, 1.0]`)

