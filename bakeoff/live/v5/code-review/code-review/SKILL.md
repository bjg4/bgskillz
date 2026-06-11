---
name: code-review
description: Review pull requests for bugs, security issues, and maintainability with severity-grouped findings. Use when reviewing PRs, diffs, or code changes before merge. Do NOT use for implementing features or writing new code.
license: MIT
metadata:
  author: bakeoff-v5
  version: "1.0.0"
---

# Code Review

## Quick start

Read the diff or snippet. Output findings in three buckets: **Critical**, **Major**, **Minor**. Each item: location, issue, suggested fix.

## Workflow

1. **Security first** — injection, auth, secrets, unsafe defaults.
2. **Correctness** — logic, null/edge cases, error paths.
3. **Maintainability** — naming, duplication, tests, fit with codebase patterns.
4. **Performance** — only when the change suggests a real concern.

## Output template

```markdown
## Critical
- [file:line] Issue — fix

## Major
...

## Minor
...
```

## Error handling

Missing diff? Ask for `git diff` output or the file. Out of scope? Say so and stop.
