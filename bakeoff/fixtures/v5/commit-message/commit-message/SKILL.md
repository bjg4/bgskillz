---
name: commit-message
description: Write clear conventional commit messages from git diffs or change descriptions. Use when committing, writing commit messages, or summarizing staged changes. Do NOT use for PR descriptions or release notes.
---

# Commit Message

## Quick start

From the diff or change summary, produce:
- Subject: imperative, ≤72 chars, conventional type if clear (`feat:`, `fix:`, `docs:`)
- Body (optional): what and why, wrapped at 72 chars

## Conventional commits

| Type | When |
|------|------|
| feat | New capability |
| fix | Bug fix |
| docs | Documentation only |
| refactor | Behavior-preserving restructure |

Default to `feat` or `fix` when obvious; otherwise omit prefix and write a clear subject.

## Error handling

If no diff or summary provided, ask for `git diff --staged` output or a one-line change description.
