---
name: bug-hunter-annahsu041
description: Audit a Python function for bugs against its task description, emit a structured bug report per the AIASE 2026 Pairwise Bug Hunter contract.
version: 0.1.0
metadata:
  hermes:
    tags: [code, audit, aiase-2026]
    category: code
---

# Bug Hunter Skill (Pairwise Track)

## When to Use

When the user sends a JSON payload with `code` (Python source), `task_description`, and `task_id`. The skill must produce a structured bug report whose `bugs[]` matches actual bugs (Jaccard-ish line+type overlap), with low false-positive rate on clean code.

## Procedure

**Complete this skill in exactly 3 terminal calls (or using equivalent file operations). Do NOT reason between steps.**

### Call 1 — Write code and edge inputs to files

Write the received `code` to `_bh_code.py`, and the probe inputs (derived from `task_description` function signature) to `_bh_edge_inputs.json`. 
*Note: Prefer using built-in file tools (e.g. `write_file` or `create_file`) if available. Otherwise, use shell redirection.*

```json
// _bh_edge_inputs.json format:
[
  {"input": [<arg1>, <arg2>...], "label": "empty"},
  {"input": [<arg1>, <arg2>...], "label": "normal"},
  {"input": [<arg1>, <arg2>...], "label": "feature"}
]
```

> **Rules for `_bh_edge_inputs.json`:**
> - Match the function's ACTUAL argument count: `binary_search(arr, target)` -> 2 args per probe.
> - Always include: empty/null input, single element, normal case, AND the spec's special feature.
> - Example for `merge_intervals(intervals)` (1-arg): `[{"input":[[]],"label":"empty"},{"input":[[[1,3]]],"label":"single"},{"input":[[[1,2],[2,3]]],"label":"touching"}]`
> - Example for `binary_search(arr, target)` (2-arg): `[{"input":[[],5],"label":"empty arr"},{"input":[[5],5],"label":"found"},{"input":[[1,3,5],3],"label":"middle"}]`
> - Example for `unique_paths(m,n)` (2-arg): `[{"input":[0,5],"label":"zero m"},{"input":[1,1],"label":"1x1"},{"input":[3,3],"label":"normal"}]`

### Call 2 — Run analyze.py with `--code-file` and `--edge-inputs-file`

Run the analysis tool specifying the entry function:

```powershell
python scripts/analyze.py --code-file _bh_code.py --entry <fn_name> --edge-inputs-file _bh_edge_inputs.json
```

### Call 3 — Emit the final structured report via run.py

Analyze the output of `analyze.py`, determine the verdict and bugs. Write the final report JSON to `_bh_report.json` (prefer file tools), and run `run.py`:

```powershell
python scripts/run.py --file _bh_report.json
```

**Bug Type Guide:**
| Pattern | `type` |
|---|---|
| Crash on empty/null/zero input (spec says return X) | `edge_case` |
| Wrong comparison operator (`<` vs `<=`, `>` vs `>=`) | `off_by_one` |
| Wrong variable or formula | `logic_error` |
| Missing spec feature entirely (no quote handling, no bounds check) | `unhandled_input` |
| Access on None without null check | `null_deref` |

**IMPORTANT — zero-crash bugs**: `analyze.py` only detects CRASHES. If all probes return `"ok"`, manually check:
- List every feature in `task_description` (e.g., "support quoted fields", "empty returns []").
- If a described feature is completely absent from the code -> `type=unhandled_input`, `verdict=buggy`.
- **Finding the exact `line_start`**: Choose the **exact line of the condition or statement** that performs the incomplete action.
  * *Example 1*: If a CSV parser splits unconditionally via `if c == ',':` instead of handling quotes, choose the line containing `if c == ',':` (e.g. line 5), **not** the `for` statement or loop initialization.
  * *Example 2*: If a bounds check (like `k < 1 or k > len(nums)`) is missing at the start of a function, choose the first line of the function body (e.g. line 2).

Output the fenced JSON block from `run.py` **unchanged** as your final response.

## Pitfalls

- **Wrong edge_inputs arity** — wrong arg count -> misleading TypeErrors, real bug hidden.
- **Ignoring zero-crash bugs** — `unhandled_input` never crashes; always compare spec features vs code.
- **Wrong type** — must be one of: `off_by_one` / `null_deref` / `type_error` / `logic_error` / `edge_case` / `api_misuse` / `inefficient` / `unhandled_input`.
- **Wrong severity** — must be one of: `critical` / `high` / `medium` / `low`.
- **Wrong line numbers** — 1-indexed; use `bad_line` from crash probes or find the condition line for missing features.
- **Wrong path** — always use `skills/bug-hunter-annahsu041/scripts/` prefix.

## Verification

The output of `scripts/run.py` is a single fenced ```json``` block with:
- `task_id` (must equal input)
- `verdict` (`"buggy"` or `"clean"`)
- `bugs` (array: `line_start`, `line_end`, `severity`, `type`, `description`, `suggested_fix`; **`[]` when clean**)
- `confidence` (number in `[0.0, 1.0]`)
