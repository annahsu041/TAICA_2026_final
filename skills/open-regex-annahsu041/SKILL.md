---
name: open-regex-annahsu041
description: Synthesize and verify regular expressions against natural language descriptions and positive/negative test cases.
version: 1.0.0
metadata:
  hermes:
    tags: [regex, logic, developer, aiase-2026]
    category: logic
---

# Regex Synthesis and Verification Skill

This skill translates a natural language pattern description and test examples into a robust, validated python regular expression.

## When to Use

When the user requests regular expression synthesis by sending a JSON payload containing:
- `task_id`: unique task identifier
- `description`: English/Chinese description of the regex pattern requirements
- `positive_examples`: List of strings that MUST match the regex
- `negative_examples`: List of strings that MUST NOT match the regex

Example trigger:
```
/open-regex-annahsu041 {
  "task_id": "regex_ip_01",
  "description": "Matches simple IPv4 address (4 numbers separated by dots, each 0-255)",
  "positive_examples": ["192.168.1.1", "0.0.0.0", "255.255.255.255"],
  "negative_examples": ["256.0.0.1", "1.2.3.4.5", "192.168.1", "abc.def.ghi.jkl"]
}
```

## Procedure

1. **Parse** the input payload to extract `task_id`, `description`, `positive_examples`, and `negative_examples`.
2. **Plan** the regular expression structure:
   - Identify anchors (typically `^` and `$`) to match the entire string if required.
   - Design subgroups or character classes based on description limits.
3. **Draft** the candidate regular expression.
4. **Validate** the candidate regex by running:
   ```bash
   python scripts/validate_regex.py '<payload>'
   ```
   Pass a JSON object with:
   - `regex`: candidate regular expression string
   - `positive_examples`: list of expected positive matches
   - `negative_examples`: list of expected negative matches
5. **Analyze validation feedback**:
   - The validator returns `{"ok": true}` or `{"ok": false, "error": "Reason description"}`.
   - If `ok` is `false`, **retry up to 3 times**, using the feedback (which tells you which positive examples failed to match or which negative examples were incorrectly matched) to fix the regex.
6. **Emit contract** by running:
   ```bash
   python scripts/run.py '<payload>'
   ```
   Pass a JSON object with:
   - `task_id`: exact input task_id
   - `regex`: final verified regex string
   - `rationale`: explanation of the regex components and design choices
   - `confidence`: confidence score in range [0.0, 1.0]

## Pitfalls

- **Unanchored regex**: If the description requires matching the entire string, make sure to anchor the pattern with `^` and `$`. Otherwise, substrings might match, causing negative examples to pass.
- **Escape characters**: Remember that regex characters like `.`, `+`, `*`, `?`, `^`, `$`, `(`, `)`, `[`, `]`, `{`, `}`, `|`, `\` have special meanings. If you want to match literal dots, escape them as `\.`.
- **JSON escaping**: When running Python scripts from command line, double-quotes and backslashes in JSON payloads must be escaped properly. The validator will fail if JSON is malformed.

## Verification

The output of `scripts/run.py` is a single fenced ```json``` block with:
- `task_id` (must match input)
- `regex` (string, valid python regex)
- `rationale` (string)
- `confidence` (float between 0.0 and 1.0)
This fenced JSON block is the final result.
