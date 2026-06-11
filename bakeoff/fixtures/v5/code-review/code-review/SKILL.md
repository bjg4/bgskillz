---
name: code-review
description: Review pull requests for bugs, security issues, and maintainability problems with structured findings. Use when reviewing PRs, diffs, or code changes. Do NOT use for writing new features from scratch.
---

# Code Review

## Quick start

Read the diff or code snippet. Produce findings grouped by severity (critical, major, minor). Each finding: location, issue, suggested fix.

## Workflow

1. Scan for security issues first (injection, auth, secrets, unsafe defaults).
2. Check correctness and error handling paths.
3. Assess maintainability (naming, duplication, missing tests).
4. Output structured review — not a rewrite unless asked.

## Output format

```markdown
## Critical
- [file:line] Issue — suggested fix

## Major
...

## Minor
...
```

## Error handling

If code context is missing, ask for the diff or file. If outside review scope, say so and suggest the right skill.
