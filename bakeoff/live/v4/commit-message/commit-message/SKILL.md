---
name: commit-message
description: Assists developers with writing high-quality commit messages for version control. Use when committing changes, summarizing staged diffs, or preparing changelog entries. Supports conventional commits and descriptive subject lines.
license: MIT
metadata:
  author: bakeoff-v4
  version: "1.0.0"
---

# Commit Message Skill

## Purpose

Good commit messages document *what* changed and *why*. Future readers (including future you) rely on history to understand decisions. This skill guides message writing so commits are searchable and meaningful.

## Use Cases

- A developer wants to commit staged changes and needs a clear message.
- A team uses conventional commits and wants consistent formatting.
- Someone needs to summarize a complex diff in a readable subject and body.

## Why Conventional Commits Help

Standard prefixes (`feat`, `fix`, `docs`, etc.) make history scannable and enable automated tooling. They are not mandatory for every repo but are a strong default when the team adopts them.

## Guidelines

Write in imperative mood ("Add feature" not "Added feature") because each commit is a instruction to the repository: "if applied, this commit will..."

Keep the subject line concise — many teams aim for 50–72 characters. Add a body when the *why* is not obvious from the subject.

Reference issue trackers when the team uses them (e.g., `Fixes #123`).

## Conventional Commit Types

| Type | Purpose |
|------|---------|
| feat | New user-facing capability |
| fix | Bug fix |
| docs | Documentation only |
| refactor | Code change without behavior change |
| test | Tests only |
| chore | Maintenance, deps, tooling |

## Process

1. Read the diff or change summary the user provides.
2. Identify the primary intent (feature, fix, docs, etc.).
3. Draft subject line; add body if needed.
4. Confirm format matches team conventions if known.

## Error Handling

If no diff or summary is provided, ask for `git diff --staged` or a short description of changes.

## Examples

Subject: `feat(auth): add JWT login endpoint`

Subject: `fix(api): handle null user in profile lookup`

Weak: `update stuff` — too vague for history search.
