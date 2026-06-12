---
name: text2sql-annahsu041
description: Convert a natural-language question + SQLite schema into a verified read-only SQL query. AIASE 2026 Basic Track.
version: 0.1.0
metadata:
  hermes:
    tags: [sql, text2sql, data, aiase-2026]
    category: data
---

# Text2SQL Skill (Basic Track)

## When to Use

When the user sends a JSON payload with `question`, `db_schema` (SQLite DDL), and optional `task_id` + `dialect`. The skill must produce a single read-only SQLite query whose result on the hidden DB matches the gold answer under bag equality.

Trigger example:

```
/text2sql-annahsu041 {"task_id":"task_nl2sql_017",
  "question":"List the names of all students who scored above 90 ...",
  "db_schema":"CREATE TABLE Students(...); ...", "dialect":"sqlite"}
```

## Procedure

**IMPORTANT: You must complete this skill in exactly ONE terminal call.**

1. **Reason** about the input payload: extract `task_id`, `question`, `db_schema`, `dialect`. Identify the relevant tables, JOIN conditions, filters, and aggregations needed.
2. **Write** a single read-only SQLite SELECT statement answering the question. Check it mentally against the schema.
3. **Immediately emit** the result by running this single command:

```
python skills/text2sql-annahsu041/scripts/run.py '{"task_id":"<task_id>","sql":"<your_sql>","rationale":"<brief_reason>","confidence":0.85}'
```

Replace `<task_id>`, `<your_sql>`, and `<brief_reason>` with the actual values. This is the **only** terminal command you need to run — run it once and return the printed fenced JSON block unchanged as your final response.

**Do NOT call validate_sql.py. Do NOT make multiple calls. One call to run.py is sufficient.**

## SQL Writing Rules

- **Always SQLite dialect** — no CTEs (`WITH`), no window functions, no recursive queries.
- **Read-only**: only SELECT statements. No INSERT/UPDATE/DELETE/DDL.
- **Single statement**: no semicolons in the middle.
- **Use DISTINCT** when the question asks for a set ("list the students who …") to avoid duplicate rows from JOINs.
- **Column and table names** must exist verbatim in the given `db_schema`.
- **task_id** in your output must equal the input `task_id` exactly.

## Verification

The fenced JSON block printed by `scripts/run.py` has:
- `task_id` (must equal input)
- `sql` (single read-only SQLite query)
- `rationale` (string)
- `confidence` (number in `[0.0, 1.0]`)

Return that block verbatim as your final response. Do not add any text after it.

