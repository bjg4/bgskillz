---
name: code-review
description: Provides comprehensive code review assistance for developers analyzing pull requests and code changes. Use when performing code reviews, examining diffs, or evaluating code quality before merge. Covers bugs, security vulnerabilities, performance concerns, and maintainability with structured feedback and severity levels.
license: MIT
metadata:
  author: bakeoff-v4
  version: "1.0.0"
---

# Code Review Skill

## Purpose and Use Cases

This skill helps developers review code effectively. Code review is a collaborative process where experienced developers examine changes to catch issues before they reach production.

Use cases:
- A developer wants to review a pull request before approving it so they can catch bugs early.
- A team lead wants consistent review quality across the team so feedback is actionable.
- A security-conscious developer wants to scan changes for vulnerabilities so the codebase stays safe.

## Why Structured Reviews Matter

Unstructured reviews miss critical issues because reviewers jump around without a system. Structured findings with severity levels help authors prioritize fixes. Explaining *why* something is a problem teaches the team and reduces repeat mistakes.

## Review Process

When reviewing code, work through these areas in order because security and correctness issues outweigh style nits:

### 1. Correctness and Logic

Look for off-by-one errors, null handling, race conditions, and missing edge cases. Ask whether the change handles failure paths.

### 2. Security

Examine input validation, authentication, authorization, secrets handling, and injection risks (SQL, XSS, command injection). Security issues should be flagged as high severity because they can cause real harm.

### 3. Maintainability

Consider naming clarity, function length, duplication, test coverage, and whether the change fits existing patterns. Maintainability affects long-term velocity.

### 4. Performance

Note obvious inefficiencies — N+1 queries, unnecessary allocations, blocking calls in hot paths — when relevant to the change.

## Output Format

Produce structured findings grouped by severity:

- **Critical** — must fix before merge (security, data loss, broken behavior)
- **Major** — should fix (logic bugs, missing error handling)
- **Minor** — nice to fix (style, naming, small refactors)

Each finding should include: location (file/line if available), description of the issue, and a suggested fix or direction.

## Communication Style

Be constructive. Explain reasoning so the author learns. Avoid vague comments like "this is wrong" without saying why.

## When Things Go Wrong

If the diff or code context is missing, ask the user to provide it. If the request is outside review scope (e.g., writing new features from scratch), explain that and offer to switch tasks.

## Degrees of Freedom

Adapt review depth to the change size — a one-line typo fix needs a lighter pass than a new auth module. Match the user's stated priorities (security-heavy vs speed-heavy) when they indicate them.

## Examples

Good finding: "Line 42: SQL query uses string interpolation with user input — SQL injection risk. Use parameterized queries."

Weak finding: "Security could be better."
