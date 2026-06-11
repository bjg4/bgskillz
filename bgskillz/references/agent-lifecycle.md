# Agent Lifecycle Guide

How to create, review, audit, and improve agents — skills, sub-agents, rules, and orchestration workflows — using patterns from Anthropic's skill-creator, Cursor's agent harness, and production multi-agent systems.

## The Agent Stack

An agent is not one thing. It is a **harness** combining three layers:

| Layer | What it is | Examples |
|-------|-----------|----------|
| **Instructions** | Persistent or on-demand guidance that shapes behavior | Rules (`.cursor/rules/`), Skills (`SKILL.md`), Commands (`.cursor/commands/`), sub-agent prompts (`agents/`) |
| **Tools** | Capabilities the agent can invoke | File editing, terminal, grep, MCP servers, browser, hooks |
| **Model** | The LLM running the loop | Sonnet for balance, Opus for depth, Haiku for speed, cheaper models for sub-agents |

Design decisions at each layer interact. A skill with excellent instructions but no access to the right MCP server will fail. A sub-agent on a fast model with vague instructions will produce inconsistent grades. Audit all three layers, not just the prompt text.

### Rules vs Skills vs Commands vs Sub-Agents

These are the four primary instruction surfaces. Most agent quality problems come from putting the wrong content in the wrong surface.

| Surface | When it loads | Best for | Avoid |
|---------|--------------|----------|-------|
| **Rules** | Always (or when glob matches) | Project conventions, commands to run, pointers to canonical files | Full style guides, edge-case instructions, domain workflows |
| **Skills** | When triggered by description match | Domain workflows, multi-step processes, bundled scripts | Always-on constraints that apply to every task |
| **Commands** | When user invokes `/command` | Repeatable team workflows (PR, review, deploy) | General guidance that should trigger automatically |
| **Sub-agents** | When parent spawns them | Specialized judgment (grading, comparison, analysis) | Deterministic loops, file I/O, aggregation |

**Progressive disclosure applies at every level.** Rules stay lean and reference files instead of copying them. Skills keep SKILL.md under 500 lines and push depth into `references/`. Orchestration skills push specialized judgment into `agents/` and deterministic work into `scripts/`.

## Two Kinds of Capabilities

Before building, classify what you're creating. The type determines how you test and when you retire it.

### Capability Uplift

Teaches the model something it cannot do consistently without help. Examples: PDF form filling at exact coordinates, proprietary API patterns, domain-specific output formats.

**Testing focus:** Does the skill produce measurably better output than baseline? Run evals after every model update.

**Retirement signal:** When baseline Claude passes your evals *without* the skill loaded, the uplift may have been absorbed into the base model. The skill isn't broken — it may no longer be necessary. Archive it rather than endlessly patching.

### Encoded Preference

Documents a workflow the model could do piecemeal, but sequences according to your team's process. Examples: NDA review checklist, weekly status report format, release train steps.

**Testing focus:** Does the skill follow your process faithfully? Fidelity to the actual workflow matters more than beating baseline on raw quality.

**Retirement signal:** When the underlying process changes. These skills are durable across model updates but fragile to organizational change.

Most real skills blend both types. Tag each test assertion with which type it validates so you know what a regression means.

## Creating Agents

### Standard Skill (Single Agent)

Follow the 7-step creation workflow in SKILL.md. This is the default path for skills that guide one agent through a task.

### Orchestration Skill (Multi-Agent)

When a workflow needs specialized judgment at different stages, make SKILL.md an **orchestrator** and delegate to sub-agents and scripts.

```
SKILL.md (~300-500 lines): flow control only
  ├── agents/grader.md      — specialized judgment (loaded only during grading)
  ├── agents/comparator.md  — blind comparison (loaded only during comparison)
  ├── agents/analyzer.md    — pattern analysis (loaded only during analysis)
  ├── references/schemas.md — data contracts between agents and scripts
  └── scripts/              — deterministic work (parallel runs, aggregation, packaging)
```

**Why this structure works:**
- Each sub-agent loads only when needed — progressive disclosure inside the skill itself
- Judgment stays with LLMs; loops and math stay with scripts
- Schema contracts in `references/` stabilize handoffs between non-deterministic agents and deterministic scripts

### Orchestration Patterns

Real orchestration skills combine multiple patterns. Name which ones you're using so reviewers can evaluate the design.

| Pattern | What it does | Example in skill-creator |
|---------|-------------|-------------------------|
| **Parallelization** | Run independent work concurrently | with_skill and baseline evals in parallel |
| **Orchestrator-Workers** | Parent delegates to specialists | SKILL.md spawns grader, comparator, analyzer |
| **Evaluator-Optimizer** | Grade output, suggest fixes, re-run | eval → grade → analyze → improve → re-eval loop |

**Agent/Skill frontmatter options** (Claude Code):

| Field | Purpose |
|-------|---------|
| `context: fork` | Run skill in isolated sub-agent context |
| `agent` | Specify sub-agent type when forked |
| `allowed-tools` | Tools permitted without approval prompts |
| `model` | Override model for this skill |
| `disable-model-invocation` | Manual-only via `/name` |

Use `context: fork` when a skill does exploratory work that would pollute the main conversation. Use cheaper models for sub-agents doing structured grading or extraction.

### Creation Checklist for Orchestration Skills

- [ ] SKILL.md contains flow control only — no specialized judgment inline
- [ ] Each sub-agent has one clear role with structured I/O (Input → Process → Output → Guidelines)
- [ ] Schema contracts documented in `references/schemas.md`
- [ ] Deterministic work (loops, aggregation, file ops) lives in scripts, not agent instructions
- [ ] Test cases written before first eval run (2-3 realistic prompts minimum)
- [ ] Parallel eval runs use clean context per test (no cross-contamination)

## Reviewing Agents

Review happens at multiple layers. Use the right layer for the question you're asking.

### Layer 1: During Generation

Watch the agent work. Stop and redirect early if it heads wrong — this is faster than fixing through follow-up prompts. For coding agents, revert and refine the plan rather than patching a bad implementation.

### Layer 2: Self-Review Checklists

Embed verification steps at the end of agent instructions or rules. Phrase them as must-pass conditions the agent runs before responding:

- Are all imports present?
- Do types check?
- Are error paths covered?
- Does output match the schema contract?

This catches issues before human review without adding a separate agent pass.

### Layer 3: Dedicated Review Pass

After the agent finishes, run a separate review focused on the diff:

- **Cursor Agent Review:** line-by-line analysis of proposed edits
- **Source Control review:** compare local changes against main branch
- **Architecture review:** ask for Mermaid diagrams on significant changes

The review agent should evaluate the **output**, not re-litigate the process that produced it. Separating task agent from review agent prevents anchoring bias.

### Layer 4: Blind Comparison

For skills and agent configurations, use the comparator agent (`agents/comparator.md`):

- Random A/B assignment so the judge doesn't know which output is skill vs baseline
- Score on content dimensions (correctness, completeness, specificity, depth) and structure dimensions (organization, clarity, format)
- Check expectations from the prompt, not just assertions

Blind comparison answers: "Is this change actually better?" — the question that subjective review often gets wrong.

### Layer 5: Automated PR Review

Push to source control for CI-integrated review (Bugbot, linters, type checkers). Agents can't fix what they can't detect — typed languages, linters, and tests give agents verifiable success signals.

### Layer 6: Autonomy Governance

For agents with tool access, define what they may do without asking:

- **Auto-review classifiers** evaluate actions in context before execution — autonomy as a dial, not a switch
- **Permissions files** (`.cursor/permissions.json`) define allowed and blocked instructions
- Blocked actions return explanation to the parent agent, which can choose a safer path without interrupting the user

Audit autonomy boundaries explicitly. An agent that can run arbitrary shell commands needs different review than one that only edits markdown.

## Auditing Agents

Use the standard 6-dimension rubric from `references/quality-checklist.md`, plus these agent-specific checks.

### Orchestration Audit

| Check | Pass criteria |
|-------|--------------|
| Single responsibility | Each sub-agent does one thing; SKILL.md orchestrates |
| Context isolation | Sub-agents load only when needed; no 1000-line monolith |
| Clean handoffs | Schema contracts exist for all agent→script and agent→agent data |
| Deterministic boundary | Loops, aggregation, and file I/O are in scripts, not agent prompts |
| Failure handling | Each stage defines what happens when upstream fails |

### Evaluation Audit

| Check | Pass criteria |
|-------|--------------|
| End-state coverage | Evals check outcomes, not specific tool-call sequences |
| Assertion quality | No trivially-satisfied assertions; meta-evaluation run on assertion set |
| Blind comparison | A/B tests use random assignment; judge doesn't see labels |
| Baseline included | Every eval runs with and without the skill/agent config |
| Obsolescence check | Baseline pass rate tracked — high baseline pass may mean skill is unnecessary |
| Parallel isolation | Each test run gets clean context (no bleed between runs) |

### Autonomy Audit

| Check | Pass criteria |
|-------|--------------|
| Tool scope | `allowed-tools` or permissions match actual needs — not "all tools" |
| Escalation path | Agent knows when to ask the user vs proceed |
| Destructive action guard | Data loss, force push, credential exposure require confirmation |
| Sandbox awareness | Scripts validate inputs; no hardcoded secrets |

**Scoring:** Add orchestration and evaluation audits as subsections under Testing (dimension 4). A skill with perfect instructions but no eval infrastructure caps at 3/5 on Testing.

## Improving Agents

### The Improvement Loop

```
eval → grade → compare → analyze → apply → re-eval
```

Run via `scripts/run_loop.py --auto-apply` or manually with the agents in `agents/`. Each iteration should produce measurable delta in pass rate, comparison wins, or timing.

### Cross-Iteration Analysis

Use `scripts/aggregate_benchmark.py` to compare trends across iterations:

```bash
python ~/.claude/skills/bgskillz/scripts/aggregate_benchmark.py /path/to/workspace
```

Track pass rate, timing, and comparison win rate per iteration. A skill that improves on iteration 1 but regresses on iteration 3 is overfitting to specific test cases.

### Anti-Overfitting Principles

When the analyzer suggests changes, apply these filters before editing:

1. **Would this generalize?** If the fix only helps test-2, it's overfitting.
2. **Read transcripts, not just grades.** Look for behavioral patterns the grader missed.
3. **Bundle repeated work.** If every run independently writes the same setup script, add it to the skill.
4. **Fewer, higher-impact changes.** One reasoning explanation beats five fiddly constraints.
5. **Protect what works.** The analyzer flags consistent wins — don't break them while fixing losses.

### Why-Driven Over Must-Driven

When improving agent instructions, explain reasoning instead of adding ALWAYS/NEVER rules:

| Must-driven (avoid) | Why-driven (prefer) |
|---------------------|---------------------|
| "ALWAYS validate before submission" | "Validation prevents API errors that waste tokens and frustrate users" |
| "NEVER skip the formatting step" | "Consistent formatting ensures downstream scripts can parse results" |

Reserve hard constraints for narrow bridges — schema field names, security boundaries, irreversible actions. Use reasoning everywhere else so the model handles novel cases.

### Pruning Stale Instructions

After each iteration, review the full instruction set:

- Which instructions did Claude ignore across all test runs? Remove or rewrite them.
- Which instructions caused unproductive behavior? Remove them.
- Which instructions are redundant with model defaults? The model may have caught up — test without them.

A shorter, focused agent outperforms a comprehensive but bloated one. Same principle as pruning stale rules in `.cursor/rules/`.

### Description Optimization

Output quality only matters if the agent triggers correctly. Run `scripts/improve_description.py` to test trigger accuracy:

- Target >90% on should-trigger, <10% false positives on should-not-trigger
- Add negative triggers ("Do NOT use for...") to prevent overtriggering
- Be slightly "pushy" in descriptions — models undertrigger more than overtrigger

## Evaluation Philosophy for Multi-Agent Systems

Multi-agent paths are non-deterministic. The same skill may take different tool-call sequences across runs. Evaluate **end states**, not processes.

**Do evaluate:**
- Final output correctness and completeness
- Whether the user's request was fulfilled
- Schema compliance of structured outputs
- Timing and token cost aggregates

**Don't evaluate:**
- Specific tool-call order (unless order is a safety requirement)
- Exact reasoning chain (unless auditing for compliance)
- Number of intermediate steps

For complex workflows, use a **separate grading agent** that sees only the output and rubric — not the task agent's reasoning. This prevents the judge from being anchored to a flawed process that accidentally produced a good result.

## Quick Reference: Which Tool When

| Goal | Tool |
|------|------|
| Create a new skill from scratch | 7-step workflow + `init_skill.py` |
| Create an orchestration skill | This guide + orchestration patterns in `workflow-patterns.md` |
| Validate structure | `validate_skill.py` |
| Run evals with baseline | `run_eval.py` |
| Grade outputs | `agents/grader.md` |
| Blind A/B compare | `agents/comparator.md` |
| Analyze patterns + suggest fixes | `agents/analyzer.md` |
| Auto-improve loop | `run_loop.py --auto-apply` |
| Cross-iteration trends | `aggregate_benchmark.py` |
| Optimize triggering | `improve_description.py` |
| Visual review | `eval-viewer/viewer.html` or `generate_review.py` |
| Full quality audit | `references/quality-checklist.md` |
