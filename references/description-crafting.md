# Description Crafting Guide

The `description` field in your SKILL.md frontmatter is the single most important factor determining whether your skill works. It controls trigger matching (when Claude activates your skill), user discovery (what users see when browsing), and install decisions.

## The Formula

**[What it does] + [When to use it] + [Key capabilities]**

Every description should answer three questions:
1. What does this skill do? (the outcome)
2. When should Claude use it? (the trigger context)
3. What specific things can it handle? (capabilities that refine matching)

## Good Examples

### Document/Asset Creation Skills

**Code review skill:**
"Perform thorough code reviews with security, performance, and maintainability analysis. Use when reviewing pull requests, auditing code quality, or preparing for code review meetings. Covers OWASP vulnerabilities, N+1 queries, error handling gaps, and naming conventions."

**API documentation skill:**
"Generate OpenAPI-compliant API documentation from source code. Use when documenting REST endpoints, creating API references, or updating endpoint specifications. Handles path parameters, request bodies, response schemas, authentication, and error codes."

**Migration skill:**
"Generate production-ready database migrations from natural language descriptions. Use when adding tables, columns, indexes, or modifying schema. Handles rollbacks, data preservation, and index optimization."

### Workflow Automation Skills

**Deployment skill:**
"Orchestrate multi-environment deployments with safety checks and rollback capability. Use when deploying to staging or production, running blue-green deployments, or managing release trains. Integrates with Docker, Kubernetes, and major CI/CD platforms."

**Incident response skill:**
"Guide structured incident response from detection through post-mortem. Use when investigating production issues, coordinating incident communication, or writing post-mortems. Covers triage, escalation, mitigation, and root cause analysis."

**Data pipeline skill:**
"Build and validate ETL pipelines with schema enforcement and error recovery. Use when setting up data ingestion, transforming datasets, or debugging pipeline failures. Supports CSV, JSON, Parquet, and database sources."

### MCP Enhancement Skills

**GitHub project management skill:**
"Manage GitHub projects with intelligent issue triage, sprint planning, and progress tracking. Use when organizing issues, planning sprints, generating status reports, or triaging incoming bug reports. Works with GitHub MCP server for direct API access."

**Database assistant skill:**
"Write and optimize SQL queries with performance analysis and index recommendations. Use when writing complex queries, debugging slow queries, or designing database schemas. Connects to PostgreSQL and MySQL via MCP database servers."

**File organization skill:**
"Organize project files with consistent naming, directory structure, and cleanup automation. Use when restructuring a project, enforcing naming conventions, or cleaning up build artifacts. Works with filesystem MCP server for safe batch operations."

## Bad Examples (and Why)

**Too vague:**
"Helps with coding stuff."
— No trigger phrases. No specificity. Claude won't know when to activate this.

**Too broad:**
"A comprehensive development assistant for all programming tasks."
— Triggers on everything, which means it helps with nothing. Skills must be specific.

**Missing the 'when':**
"Generates TypeScript interfaces from JSON schemas."
— Good 'what', but no 'when'. Add: "Use when converting API responses to TypeScript types, creating form validation schemas, or generating type-safe API clients."

**Feature list without context:**
"Supports React, Vue, Angular, Svelte, Solid, Preact, and Lit."
— Lists capabilities but doesn't explain the use case. What does it *do* with these frameworks?

**Too technical:**
"Implements AST-based transpilation for ECMAScript modules with tree-shaking support."
— Users don't say "I need AST-based transpilation." They say "Help me optimize my bundle size."

## Negative Trigger Patterns

If your skill triggers too broadly, add negative triggers to the description:

"Create S-tier portable skills with comprehensive quality guidance. This skill should be used when creating new skills, improving existing skills, auditing skill quality, or learning skill-building best practices. Do NOT use for general coding tasks, writing documentation, or building applications."

Common negative trigger patterns:
- "Do NOT use for [adjacent but different task]"
- "This is specifically for [X], not [Y]"
- "Only applies to [narrow scope]"

Use negative triggers sparingly — they're a band-aid for a description that's too broad. Prefer narrowing the positive description first.

## Trigger Phrase Strategy

Include the exact words and phrases users will say:

If users will say "help me write tests", include "writing tests" in your description.
If users will say "review my PR", include "reviewing pull requests" in your description.
If users will say "set up CI/CD", include "CI/CD" in your description.

Also include paraphrases:
- "write tests" / "create test suite" / "add unit tests"
- "review PR" / "code review" / "audit code"
- "deploy" / "ship to production" / "release"

## File Type Mentions

If your skill is specific to certain file types, mention them:

"Generate and validate Terraform configurations. Use when creating .tf files, planning infrastructure changes, or reviewing Terraform plans."

"Optimize Docker images for production. Use when writing Dockerfiles, reducing image size, or debugging container builds."

## Length Guidance

- **Minimum**: 50 characters — enough for basic what + when
- **Sweet spot**: 100-200 characters — covers the full formula
- **Maximum**: 1024 characters — hard limit
- **Front-load**: Put the most important information in the first 100 characters, as some UIs may truncate

## Self-Check

Before finalizing your description, verify:

1. Would you know what this skill does from the description alone?
2. Does it include at least 2 trigger phrases users would actually say?
3. Is the scope narrow enough that it won't trigger on unrelated tasks?
4. Would someone browsing a skill directory pick this one for the right reason?
5. Is it under 1024 characters?
