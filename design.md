1. the review function should return a list of pydantic findings.
2. nope if an error comes it should add it and then continue to see for more such errors so that we can tell that them at once.
3. We should merge them

Return type: list[Finding], with every item validated by Pydantic.

Syntax errors: report the error and skip AST-dependent analysis; continue independent checks where appropriate.

Deduplication: merge findings that represent the same underlying issue, preserving their evidence and sources.

Execution status: track success, partial completion, or failure separately from the findings list.

## Finding Schema

Field | Type | Required? | Allowed values / constraints
title str Yes Non-empty, short description
severity str Yes low, medium, high, critical
confidence str Yes low, medium, high
line_number int \| None Yes Positive integer or None if unknown
explanation str Yes Non-empty explanation of the bug
impact str Yes What could break or go wrong
suggested_fix str \| None Yes Proposed fix or None if no safe fix is known
sources list[str] Yes Values such as ruff, bandit, llm
status str Yes confirmed, likely, needs_review, unsupported
