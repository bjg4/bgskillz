---
name: bgskillz
description: Create S-tier portable skills with comprehensive quality guidance. This skill should be used when creating new skills, improving existing skills, auditing skill quality, or learning skill-building best practices. Covers the full lifecycle from use case definition through testing, distribution, and iteration. Do NOT use for general coding tasks, writing documentation unrelated to skills, or building applications.
license: MIT
metadata:
  author: Blake Graham
  version: "1.0.0"
---

# BGSkillz

Build high-quality, portable Claude skills that trigger reliably and deliver real value.

## Core Philosophy

1. **Skills are prompts** — SKILL.md is a prompt document. Everything in it shapes Claude's behavior when the skill activates.
2. **Progressive disclosure** — Keep SKILL.md lean (<500 lines). Put deep reference material in `references/` files and link to them.
3. **Composability** — Skills should do one thing well. Combine multiple skills for complex workflows rather than building monoliths.
4. **Portability** — Skills work across Claude.ai, Claude Code, and the API. Write for all surfaces unless you have a reason not to.
5. **Specificity wins** — Vague skills don't trigger. Specific skills with clear use cases and trigger phrases activate reliably.

## Skill Anatomy

```
my-skill/
├── SKILL.md              # Required. Main entry point. Contains frontmatter + instructions.
├── scripts/              # Optional. Executable helpers (Python, Bash, etc.)
├── references/           # Optional. Deep reference docs linked from SKILL.md.
└── assets/               # Optional. Templates, configs, examples bundled with the skill.
```

**SKILL.md** is the only required file. It must be exactly `SKILL.md` (not `skill.md`, not `README.md`).

Frontmatter fields:
- `name` (required): kebab-case, no spaces, no capitals, no "claude" or "anthropic"
- `description` (required): Under 1024 chars. Determines when the skill triggers.
- `license`, `metadata`, `compatibility`: Optional but recommended for distribution.

## Creation Workflow

Follow these 7 steps to build a skill from scratch.

### Step 1: Define 2-3 Concrete Use Cases

Before writing anything, articulate exactly who will use this skill and for what. Pick a category:

- **Document/Asset Creation** — Generate reports, code, configs, designs
- **Workflow Automation** — Multi-step processes with tools and decisions
- **MCP Enhancement** — Add intelligence on top of MCP server capabilities

Write 2-3 specific use case sentences: "A developer wants to... so they can..."

### Step 2: Define Success Criteria

Set measurable goals before building:

- **Quantitative**: Triggers correctly >90% of the time, reduces task time by X%, output matches template Y% of the time
- **Qualitative**: Users find output useful without heavy editing, skill integrates naturally into existing workflow

### Step 3: Choose Your Approach

- **Problem-first**: You have a pain point. Design the skill around solving it.
- **Tool-first**: You have an MCP server or API. Design the skill to make it more useful.

Problem-first skills tend to have better descriptions because the pain point *is* the trigger.

### Step 4: Plan Reusable Contents

Decide what goes into each directory:

- **scripts/**: Anything Claude should execute (scaffolders, validators, build tools)
- **references/**: Deep knowledge Claude should read when needed (style guides, API docs, patterns)
- **assets/**: Templates, example files, configs that get copied into user projects

Rule of thumb: If it's >50 lines and not needed on every invocation, it belongs in `references/`.

### Step 5: Initialize the Skill

Run the scaffolder to create your skill directory:

```bash
python ~/.claude/skills/bgskillz/scripts/init_skill.py my-skill-name --path ~/target/directory
```

This creates a well-structured starting point with TODO prompts to guide you.

### Step 6: Write the Skill

This is where quality is made or lost. Follow these rules:

**Description (most critical field):**
Use the formula: `[What it does] + [When to use it] + [Key capabilities]`

Good: "Generate production-ready database migrations from natural language descriptions. Use when adding tables, columns, indexes, or modifying schema. Handles rollbacks, data preservation, and index optimization."

Bad: "Helps with database stuff."

See `references/description-crafting.md` for 15+ examples and anti-patterns.

**Naming rules:**
- kebab-case only: `my-cool-skill` not `MyCoolSkill`
- No spaces or capital letters
- Never include "claude" or "anthropic" in the name
- Skill folder name must match the `name:` field in frontmatter

**Writing instructions:**
- Use imperative voice: "Generate a report" not "You should generate a report"
- Be specific and actionable: "Use 4-space indentation" not "Format code nicely"
- Front-load critical instructions — Claude may skim long documents
- Include examples of good output when possible
- Use markdown headings (##, ###) to organize sections — NOT XML tags
- Provide a "degrees of freedom" principle: tell Claude what it CAN vary, not just constraints
- Set defaults with escape hatches: "Use TypeScript by default. If the user specifies another language, use that instead."

**Error handling:**
- Tell Claude what to do when things go wrong
- Include fallback behaviors for missing tools or failed API calls
- Specify how to communicate errors to the user

**Security rules:**
- Never instruct Claude to bypass safety measures
- Don't hardcode credentials or API keys
- Don't reference external URLs that could change or be compromised
- Scripts should validate inputs before executing

### Step 7: Package and Distribute

Run the packager to validate and create a distributable zip:

```bash
python ~/.claude/skills/bgskillz/scripts/package_skill.py /path/to/my-skill
```

This runs full validation, then creates a zip ready for upload or sharing. See `references/distribution-guide.md` for hosting and positioning guidance.

## Critical Rules

These are hard requirements. Violating them causes failures.

1. **File must be named `SKILL.md`** — Exact casing. Not `skill.md`, not `Skill.md`.
2. **No `README.md` inside the skill folder** — It confuses the system. README goes in your GitHub repo root, outside the skill folder.
3. **Name must be kebab-case** — `my-skill` not `my_skill` or `MySkill` or `my skill`
4. **No XML tags in frontmatter** — No `<` or `>` characters anywhere in the YAML block.
5. **Name must match folder** — If folder is `my-skill/`, frontmatter name must be `my-skill`.
6. **No "claude" or "anthropic" in name** — Reserved terms.
7. **Description under 1024 characters** — Hard limit.
8. **SKILL.md under 5000 words** — Beyond this, Claude's attention degrades. Use references for depth.
9. **One level of nesting** — One level deep is fine. Nested subdirectories like bar/baz/ inside references are not.
10. **Forward slashes only** — Even on Windows. No backslash paths.

## Best Practices

**Be specific and actionable.** Every instruction should pass the "what would Claude actually do?" test. "Write good code" fails. "Use early returns to reduce nesting. Limit functions to 20 lines. Name variables descriptively." passes.

**Progressive disclosure.** Put the 20% of instructions that cover 80% of use cases in SKILL.md. Put the remaining detail in references. Link clearly: "For advanced configuration patterns, see `references/workflow-patterns.md`."

**Reference bundled resources clearly.** When pointing to a reference file, use the exact relative path. Claude will read the file when you reference it this way.

**Include error handling.** Tell Claude what to do when: the user's request is ambiguous, a required tool is missing, an API call fails, the output doesn't match expectations.

**Consistent terminology.** Pick one term and stick with it. Don't alternate between "skill", "plugin", and "extension" in the same document.

**Default + escape hatch.** "Generate TypeScript by default. If the user requests JavaScript or another language, adapt accordingly." This gives Claude a clear default while preserving flexibility.

**Show, don't just tell.** Include 1-2 examples of ideal output in your SKILL.md. Claude mimics examples more reliably than it follows abstract rules.

## Testing and Iteration

Test your skill in three ways:

1. **Trigger testing** — Does it activate when it should? Does it stay quiet when it shouldn't?
   - Test with exact phrases: "Create a new skill"
   - Test with paraphrases: "I want to build a plugin for Claude"
   - Test with non-triggers: "Write a Python script" (should NOT trigger a skill-building skill)

2. **Functional testing** — When triggered, does it produce correct output?
   - Test the happy path with a straightforward request
   - Test edge cases (empty input, unusual formats, missing context)
   - Test with different Claude models if possible (Haiku may need more explicit instructions)

3. **Baseline comparison** — Is the skill actually better than Claude without it?
   - Run the same task with and without the skill
   - The skill should produce noticeably better results

**Undertriggering signals**: Users have to explicitly invoke the skill; paraphrased requests don't activate it. Fix: Add more trigger phrases to the description. Be more specific about use cases.

**Overtriggering signals**: Skill activates on unrelated tasks. Fix: Add negative triggers. Narrow the description scope. Use more specific terminology.

For comprehensive testing methodology, read `references/testing-methodology.md`.

## Troubleshooting

**Skill won't upload**: Check that the file is named exactly `SKILL.md`. Verify frontmatter is valid YAML with `name` and `description`. Ensure the name is kebab-case with no spaces.

**Skill doesn't trigger**: Your description likely doesn't match how users phrase requests. Add more specific trigger phrases. Include the exact verbs and nouns users would say.

**Instructions not followed**: SKILL.md may be too long or instructions are buried. Front-load critical rules. Use bold for must-follow constraints. Reduce total word count.

For all troubleshooting scenarios, read `references/troubleshooting.md`.

## Audit Checklist

Quick pre-flight check before publishing:

- [ ] `SKILL.md` exists with exact casing
- [ ] Frontmatter has `name` (kebab-case) and `description` (under 1024 chars)
- [ ] Name matches folder name
- [ ] Description follows `[What] + [When] + [Capabilities]` formula
- [ ] No README.md inside the skill folder
- [ ] SKILL.md is under 500 lines / 5000 words
- [ ] All referenced files actually exist
- [ ] Scripts are executable and handle errors
- [ ] Tested with 3+ trigger phrases and 2+ non-trigger phrases
- [ ] Baseline comparison shows improvement over vanilla Claude

For the full audit rubric with scoring, read `references/quality-checklist.md`.

## What To Do

Choose what you need help with:

### Create a New Skill
"I want to create a new skill" — Walk through the 7-step creation workflow. Start by defining use cases and end with a packaged, validated skill.

### Audit an Existing Skill
"Audit my skill" or "Review this skill" — Run the full quality checklist against an existing skill. Identify issues and suggest fixes.

### Improve a Description
"Help me write a better description" — Apply the description formula and test trigger phrases. Rewrite for maximum activation reliability.

### Add a Component
"Add a script/reference/asset to my skill" — Help plan and implement a new component (validator, reference doc, template, etc.) for an existing skill.

### Validate a Skill
"Validate my skill" — Run the validation script to check structural correctness:
```bash
python ~/.claude/skills/bgskillz/scripts/validate_skill.py /path/to/skill
```

### Package for Distribution
"Package my skill" — Run validation + create a distributable zip:
```bash
python ~/.claude/skills/bgskillz/scripts/package_skill.py /path/to/skill
```

### Get Guidance
"How do I..." — Answer questions about skill building using the reference library. Topics: descriptions, workflows, testing, troubleshooting, distribution, quality.
