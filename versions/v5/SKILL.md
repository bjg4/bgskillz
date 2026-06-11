---
name: bgskillz
description: Create S-tier portable skills and agents with comprehensive quality guidance. Use when creating or improving skills, designing multi-agent orchestration workflows, auditing agent quality, running evals, or learning agent-building best practices. Covers the full lifecycle from use case definition through automated evaluation, review, and iteration. Do NOT use for general coding tasks, writing documentation unrelated to agents/skills, or building applications.
license: MIT
metadata:
  author: Blake Graham
  version: "5.0.0"
---

# BGSkillz

Build high-quality, portable agents and skills that trigger reliably and deliver real value. **Target ~100 lines / ~900 tokens** per skill — high signal, not high word count.

## Core Philosophy

1. **Skills are prompts** — SKILL.md is a prompt document. Everything in it shapes Claude's behavior when the skill activates.
2. **Explain the why, not just the what** — LLMs are smart. They respond better to understood rationale than rigid rules. Instead of "ALWAYS use 4-space indentation," explain *why* consistent indentation matters. If you find yourself writing MUST or NEVER in all caps, that's a yellow flag — reframe as reasoning.
3. **Progressive disclosure** — Target ~100 lines in SKILL.md (~900 tokens). Hard max 500 lines. Put depth in `references/`, judgment in `agents/`, determinism in `scripts/`.
4. **Composability** — Skills should do one thing well. Combine multiple skills for complex workflows rather than building monoliths.
5. **Portability** — Skills work across Claude.ai, Claude Code, and the API. Write for all surfaces unless you have a reason not to.
6. **Specificity wins** — Vague skills don't trigger. Specific skills with clear use cases and trigger phrases activate reliably. Make descriptions slightly "pushy" — Claude tends to undertrigger rather than overtrigger.
7. **Generalize, don't overfit** — A skill that works only for your test examples is useless. It will be invoked by diverse users with diverse needs. When iterating, resist fiddly overfitty changes. Instead, try different metaphors and explain reasoning. Lean toward fewer, higher-impact improvements.
8. **Evaluate end states, not processes** — Multi-agent paths are non-deterministic. Grade final outputs against rubrics, not specific tool-call sequences. Use a separate grading agent that hasn't seen the task agent's reasoning.
9. **Know your capability type** — Capability uplift skills may become obsolete as models improve (baseline passes without the skill). Encoded preference skills need fidelity testing against your actual workflow. Test and retire accordingly.
10. **Description and body are two surfaces** — The router only sees the description; the agent sees the body after activation. They can quietly disagree. Test triggers and behavior separately, then end-to-end.
11. **Right-size the skill** — Not every skill needs scripts, references, or eval pipelines. Match complexity to the behavior. See `references/great-skill-patterns.md`.

## Agent Architecture

Agents are harnesses combining **instructions + tools + model**. Skills, rules, commands, and sub-agents are all instruction surfaces — use the right one:

| Surface | Loads | Use for |
|---------|-------|---------|
| Rules (`.cursor/rules/`) | Always or on glob match | Conventions, commands, pointers to canonical files |
| Skills (`SKILL.md`) | On trigger | Domain workflows, bundled scripts |
| Commands (`.cursor/commands/`) | On `/invoke` | Repeatable team workflows |
| Sub-agents (`agents/`) | When spawned | Specialized judgment (grading, comparison) |

For orchestration skills that spawn sub-agents, make SKILL.md a flow-control orchestrator — delegate judgment to `agents/`, deterministic work to `scripts/`, and data contracts to `references/schemas.md`. See `references/agent-lifecycle.md` for the full create → review → audit → improve lifecycle.

## Skill Anatomy

```
my-skill/
├── SKILL.md              # Required. Main entry point. Contains frontmatter + instructions.
├── agents/               # Optional. Sub-agent instruction files for multi-agent workflows.
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

Choose a path first:
- **Simple path** — Shape → use cases → draft → **user review** → validate → package. For first skills or behavioral prompts.
- **Rigorous path** — Simple path + eval pipeline + bounded improvement loop. When you have a verifier (benchmarkable domain).

See `references/great-skill-patterns.md` for patterns from teach, write-a-skill, grill-me, and SkillOpt.

### Step 0: Pick Skill Shape

| Shape | When | SKILL.md size |
|-------|------|---------------|
| Behavioral prompt | One interaction behavior | <20 lines |
| Guided process | Workflow + optional refs | 50–100 lines |
| Stateful workspace | Multi-session, files persist | 100–200 + `*-FORMAT.md` |
| Orchestration | Sub-agents for specialized judgment | 300–500, flow control only |

Also ask: **Do I have a verifier?** Benchmarkable → rigorous path. Open-ended → human review, not auto-apply loops.

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
- **Orchestration**: You need multi-stage judgment (eval, grade, compare, analyze). Design SKILL.md as orchestrator with sub-agents in `agents/`.

Also classify the capability type:
- **Capability uplift**: Teaches something the base model can't do consistently. Test against baseline; watch for obsolescence as models improve.
- **Encoded preference**: Sequences a workflow the model could do piecemeal. Test for fidelity to your actual process.

Problem-first skills tend to have better descriptions because the pain point *is* the trigger.

### Step 4: Plan Reusable Contents

Decide what goes into each directory:

- **agents/**: Sub-agent instruction files loaded only when spawning specialized agents (graders, comparators, analyzers). These keep SKILL.md lean while enabling multi-agent workflows.
- **scripts/**: Anything Claude should execute (scaffolders, validators, eval runners, build tools)
- **references/**: Deep knowledge Claude should read when needed (style guides, API docs, patterns, schemas)
- **assets/**: Templates, example files, configs that get copied into user projects

Rule of thumb: If it's >50 lines and not needed on every invocation, it belongs in `references/`. If it's instructions for a sub-agent, it belongs in `agents/`.

### Step 5: Initialize the Skill

Run the scaffolder to create your skill directory:

```bash
python ~/.claude/skills/bgskillz/scripts/init_skill.py my-skill-name --path ~/target/directory
```

This creates a well-structured starting point with TODO prompts to guide you.

### Step 6: Write the Skill

Use structure: **Quick start → Workflows → Advanced** (link out). See `references/great-skill-patterns.md`.

**Description (most critical field):**
The description is **the only thing the router sees** when selecting skills. The body loads only after activation.

Two-sentence formula:
1. What it does (third person)
2. `Use when [triggers].` Optional: `Do NOT use for [exclusions].`

Good: "Review pull requests for bugs, security, and maintainability with structured findings. Use when reviewing PRs or diffs. Do NOT use for writing new features."

Bad: "Helps with code review."

See `references/description-crafting.md` for 15+ examples.

**Naming rules:**
- kebab-case only: `my-cool-skill` not `MyCoolSkill`
- No spaces or capital letters
- Never include "claude" or "anthropic" in the name
- Skill folder name must match the `name:` field in frontmatter

**Writing instructions:**
- Use imperative voice: "Generate a report" not "You should generate a report"
- Be specific and actionable: "Use 4-space indentation" not "Format code nicely"
- Explain reasoning over rigid rules: "Use early returns because deeply nested code is harder to debug" is more effective than "ALWAYS use early returns"
- Front-load critical instructions — Claude may skim long documents
- Include examples of good output when possible — Claude mimics examples more reliably than it follows abstract rules
- Use markdown headings (##, ###) to organize sections — NOT XML tags
- Provide a "degrees of freedom" principle: tell Claude what it CAN vary, not just constraints
- Set defaults with escape hatches: "Use TypeScript by default. If the user specifies another language, use that instead."
- Calibrate your tone to your audience — users range from non-technical to expert developers. Use context cues from the user's message to adapt jargon level.

**Error handling:**
- Tell Claude what to do when things go wrong
- Include fallback behaviors for missing tools or failed API calls
- Specify how to communicate errors to the user

**Security rules:**
- Never instruct Claude to bypass safety measures
- Don't hardcode credentials or API keys
- Don't reference external URLs that could change or be compromised
- Scripts should validate inputs before executing

### Step 7: Review With User

Before validating, present the draft:
- Does this cover your use cases?
- Anything missing or unclear?
- Should any section be more or less detailed?

Do not package until the user confirms or explicitly skips review.

### Step 8: Validate, Test, Package

Run validation:
```bash
python ~/.claude/skills/bgskillz/scripts/validate_skill.py /path/to/my-skill
```

**Two-surface check:**
- Trigger test: does the description activate on 3+ should-trigger phrases?
- Body test: when activated, does behavior match what the description promises?
- E2E: run one real task end-to-end

If benchmarkable, run evals. If open-ended, stop at human review.

### Step 9: Package and Distribute

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
8. **SKILL.md under 5000 words** — Target ~900 tokens (~100 lines). Beyond 5000 words, attention degrades.
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

**Look for repeated work.** If you run tests and notice Claude independently writes similar boilerplate or setup code each time, bundle that code into the skill as a script or template. Don't make Claude reinvent the wheel on every invocation.

**Keep the prompt lean.** After each iteration, review the full SKILL.md and remove instructions that aren't pulling their weight. Read transcripts to identify instructions that Claude ignores or that cause unproductive behavior. A shorter, focused skill outperforms a comprehensive but bloated one.

## Testing and Iteration

Test your skill in three ways, from manual to fully automated:

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
   - If baseline passes evals without the skill, the uplift may be obsolete — consider retiring it

4. **Review layers** — Match review depth to risk:
   - Self-review checklists in instructions (must-pass before responding)
   - Dedicated review pass on diffs (Agent Review, PR review)
   - Blind A/B comparison via comparator agent (eliminates evaluator bias)
   - Autonomy governance for tool-using agents (permissions, auto-review classifiers)

See `references/agent-lifecycle.md` for the full review and audit framework.

### Automated Evaluation Pipeline

For rigorous testing, use the automated eval pipeline:

```bash
# Run evaluation with baseline comparison
python ~/.claude/skills/bgskillz/scripts/run_eval.py /path/to/skill --prompts tests/prompts.json

# Run automated improvement loop (eval -> grade -> analyze -> improve -> repeat)
python ~/.claude/skills/bgskillz/scripts/run_loop.py /path/to/skill --prompts tests/prompts.json --iterations 3 --auto-apply

# Optimize description triggering
python ~/.claude/skills/bgskillz/scripts/improve_description.py /path/to/skill

# Generate a self-contained HTML review page
python ~/.claude/skills/bgskillz/eval-viewer/generate_review.py /path/to/workspace/iteration-1/evals.json

# Aggregate trends across iterations
python ~/.claude/skills/bgskillz/scripts/aggregate_benchmark.py /path/to/workspace
```

The eval pipeline runs each test prompt through Claude with and without the skill in **clean, isolated contexts** (no cross-contamination between runs), computing benchmark statistics (mean, stddev, min, max) and saving outputs for grading. Use the sub-agents in `agents/` to grade outputs, blind-compare them, and analyze patterns:

- `agents/grader.md` — Grades outputs against assertions with evidence and meta-evaluation
- `agents/comparator.md` — Blind A/B comparison (doesn't know which output is skill vs. baseline)
- `agents/analyzer.md` — Unblinded pattern analysis with prioritized improvement suggestions

The `run_loop.py` script automates the full cycle: eval → grade → analyze → apply suggestions → re-eval.

**SkillOpt discipline when iterating:**
- Hold out a selection split — accept edits only on strict improvement (ties rejected)
- Cap at **4–8 bounded edits** per iteration, not full rewrites
- Log rejected edits; expect **1–4 accepted edits** total for a mature skill
- Report **per-skill** effect size, not portfolio averages

Use `--auto-apply` cautiously — only when you have a verifier. Backups are saved.

Review results visually with `eval-viewer/viewer.html`, or generate a self-contained review page with `eval-viewer/generate_review.py`. See `references/schemas.md` for all data formats.

### Iteration Signals

**Undertriggering**: Users have to explicitly invoke the skill; paraphrased requests don't activate it. Fix: Add more trigger phrases to the description. Be more specific about use cases.

**Overtriggering**: Skill activates on unrelated tasks. Fix: Add negative triggers. Narrow the description scope. Use more specific terminology.

**Anti-overfitting warning**: When iterating, read the actual transcripts. Look for unproductive behavior the skill causes and look for repeated work across test runs (if all runs independently write similar scripts, bundle that script into the skill). Resist adding fiddly constraints — generalize from the feedback instead.

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
- [ ] SKILL.md is under 100 lines (ideal) or 500 lines (max)
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

### Evaluate a Skill
"Evaluate my skill" or "Run evals" — Run the automated evaluation pipeline with baseline comparison:
```bash
python ~/.claude/skills/bgskillz/scripts/run_eval.py /path/to/skill --prompts tests/prompts.json
```
Then grade and analyze results using the agents in `agents/`. Review visually with `eval-viewer/viewer.html` or generate a self-contained review page with `eval-viewer/generate_review.py`.

### Run Improvement Loop
"Iterate on my skill" or "Auto-improve my skill" — Run the full automated cycle (eval → grade → analyze → improve → re-eval):
```bash
python ~/.claude/skills/bgskillz/scripts/run_loop.py /path/to/skill --prompts tests/prompts.json --iterations 3 --auto-apply
```

### Optimize Triggering
"Improve my skill's triggering" — Run the description optimization pipeline:
```bash
python ~/.claude/skills/bgskillz/scripts/improve_description.py /path/to/skill
```

### Audit an Agent or Orchestration Skill
"Audit my agent" or "Review this orchestration skill" — Run the quality checklist plus agent-specific audits (orchestration clarity, eval coverage, autonomy boundaries). See `references/agent-lifecycle.md` and `references/quality-checklist.md`.

### Design Multi-Agent Orchestration
"I want to build an orchestration skill" — Walk through orchestration patterns (Parallelization, Orchestrator-Workers, Evaluator-Optimizer), sub-agent design, schema contracts, and the eval pipeline. See `references/agent-lifecycle.md` and `references/workflow-patterns.md`.

### Create a New Skill
"I want to create a new skill" — Step 0: pick shape. Simple or rigorous path. End with validated, reviewed skill.

### Run BGSkillz Bakeoff
Compare v4 vs v5 skill-creation quality on fixed briefs:
```bash
python bakeoff/run_bakeoff.py --fixtures
python bakeoff/run_bakeoff.py --generate-prompts
```
See `bakeoff/PROTOCOL.md` for the full verifiable bakeoff protocol.

### Get Guidance
"How do I..." — Topics: great skill patterns, agent lifecycle, descriptions, workflows, testing, evaluation, SkillOpt optimization, distribution, quality.
