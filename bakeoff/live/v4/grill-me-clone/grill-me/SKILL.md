---
name: grill-me
description: Helps users stress-test plans and designs through detailed questioning. Use when discussing architecture, project plans, or design documents. Supports Socratic dialogue and recommended answers.
license: MIT
metadata:
  author: bakeoff-v4
  version: "1.0.0"
---

# Plan and Design Review (Grill Me)

## Purpose

Plans fail when unstated assumptions stay hidden. This skill uses questioning to surface gaps in scalability, security, data modeling, operations, and edge cases before implementation.

## Use Cases

- A developer has an architecture proposal and wants critical feedback.
- A team is planning a launch and needs to stress-test dependencies.
- Someone says "grill me" on a design doc.

## Approach

Cover the design systematically:

1. **Requirements** — Who uses it? What scale? What SLAs?
2. **Architecture** — Components, data flow, failure modes.
3. **Security** — Threat model, auth, data protection.
4. **Operations** — Deploy, monitor, rollback, on-call.
5. **Tradeoffs** — What are you optimizing for? What are you deferring?

For each area, ask probing questions and provide your recommended answer or direction so the user can compare their thinking.

## Interaction Style

Be thorough. It is acceptable to ask several related questions in one turn when exploring a subsystem, then summarize recommended paths.

If the codebase holds answers (e.g., existing auth pattern), read the codebase before asking the user.

## Error Handling

If the plan is too vague, ask for a one-paragraph summary of goal and constraints before deep questioning.

## Output

End sections with a short "recommended direction" when you have a strong opinion based on common practice.
