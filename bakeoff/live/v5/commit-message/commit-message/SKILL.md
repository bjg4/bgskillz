---
name: commit-message
description: Write conventional commit messages from git diffs or change summaries. Use when committing, drafting commit messages, or summarizing staged changes. Do NOT use for PR bodies or release notes.
license: MIT
metadata:
  author: bakeoff-v5
  version: "1.0.0"
---

# Commit Message

## Quick start

From diff or summary, output:
```
<type>(<scope>): <subject ≤72 chars>

<body: what and why, wrap at 72>
```

## Conventional types

| Type | When |
|------|------|
| feat | New capability |
| fix | Bug fix |
| docs | Docs only |
| refactor | No behavior change |

Pick the closest type; omit scope if unclear.

## Error handling

No diff? Request `git diff --staged` or a one-line change summary.

## Example

```
feat(auth): add JWT login endpoint

Add POST /login issuing tokens; validate credentials against user store.
```
