# BGSkillz v2 vs Anthropic Skill Creator: Cross-Evaluation (Updated)

*Re-evaluated after BGSkillz absorbed key learnings from the Anthropic Skill Creator.*

## Overview

Both are meta-skills — skills whose purpose is to help you build other skills. They share common DNA (SKILL.md format, progressive disclosure, description crafting) but took fundamentally different approaches to the problem. After learning from each other, BGSkillz has closed many of its original gaps.

| Dimension | BGSkillz (v2) | Anthropic Skill Creator |
|-----------|---------------|------------------------|
| **Author** | Blake Graham (community) | Anthropic (official) |
| **Philosophy** | Guidebook + toolchain + eval pipeline | Agentic evaluation loop |
| **Core strength** | Full lifecycle: teaching + building + measuring | Measuring and iterating on skills automatically |
| **Scripts** | 6 (init, validate, package, run_eval, improve_description, run_loop) | 9+ (run_eval, improve_description, run_loop, aggregate_benchmark, etc.) |
| **References** | 7 deep guides (incl. schemas) | 1 schemas reference |
| **Agents** | 3 (grader, comparator, analyzer) | 3 (grader, comparator, analyzer) |
| **Eval system** | Automated with blind comparison, grading, and benchmark | Automated with blind comparison, grading, and benchmarking |
| **Eval viewer** | HTML viewer with outputs, benchmark, and feedback tabs | HTML viewer with outputs and benchmark tabs |
| **Target user** | Anyone building skills, from beginner to advanced | Someone iterating on an existing skill's quality |

---

## BGSkillz Evaluating the Anthropic Skill Creator

*Using BGSkillz's audit rubric (1-5 scale across 6 dimensions):*

### Dimension 1: Description — **4/5**

> "Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy."

- Follows the `[What] + [When] + [Capabilities]` formula well
- Clear trigger phrases: "create a skill", "run evals", "benchmark", "optimize description"
- Missing a `DO NOT use for...` clause — risk of overtriggering on general coding tasks
- At ~340 chars, well within the 1024-char limit with room for negative triggers

### Dimension 2: Instructions — **5/5**

- Extremely specific and actionable. Not "test your skill" but "spawn runs with-skill AND baseline in the same turn, draft assertions while runs execute, capture timing data from task notifications, grade with the grader agent"
- Clear step-by-step workflows for every mode (Create, Improve, Benchmark, Description Optimization)
- Excellent progressive disclosure — SKILL.md stays focused while agents/ and scripts/ carry implementation weight
- Communication guidance adapts to user expertise level ("users range from plumbers and grandparents to experienced developers")
- The "Principle of Lack of Surprise" is strong — instructs Claude to avoid hallucinating capability
- The "explain the why" philosophy throughout is deeply embedded, not bolted on

### Dimension 3: Scope — **4/5**

- Well-bounded: skill creation + evaluation + improvement
- The scope is ambitious — creating, testing, benchmarking, blind comparison, and description optimization
- Risk of being too broad: it tries to be both a "create from scratch" tool AND a "scientific evaluation" tool
- The eval/benchmark system is significantly more complex than what most skill authors need on day one

### Dimension 4: Testing — **5/5**

- Unmatched depth in automated evaluation
- `run_eval.py` invokes `claude -p` to test trigger accuracy
- Blind comparison via comparator agent eliminates bias
- Grader agent evaluates outputs with evidence citations AND critiques the assertions themselves (meta-evaluation)
- Benchmark mode runs multiple configurations with statistical analysis (mean, stddev, min, max)
- Post-hoc analyzer generates actionable improvement suggestions
- `improve_description.py` with automated `run_loop.py` rewrites descriptions based on eval failures
- Eval viewer (HTML) for visual inspection

### Dimension 5: Organization — **4/5**

- Clean progressive disclosure: SKILL.md → agents/ → scripts/ → references/
- The agents/ directory is well-designed — each agent has a clear role and structured I/O
- `references/schemas.md` is comprehensive (covers 7 schemas in one file)
- Missing: no scaffolding tool to create a new skill from scratch (no `init_skill` equivalent)
- The eval-viewer/ directory adds a nice interactive element

### Dimension 6: Security — **3/5**

- Scripts shell out to `claude -p` which inherits user auth — clean pattern
- No hardcoded credentials
- No explicit security guidance for skills being *created*
- No validation of user inputs in the way BGSkillz's `validate_skill.py` checks for credential patterns
- The `run_eval.py` script creates temporary command files and cleans them up — good hygiene

### BGSkillz Total Score for Anthropic Skill Creator: **25/30 (S-tier threshold)**

**What the Anthropic Skill Creator still does better:**
- The `run_loop.py` automated improvement loop — BGSkillz's eval pipeline collects data and grades, but doesn't yet auto-iterate
- The grader agent's meta-evaluation critiques are more deeply embedded in the workflow (BGSkillz's grader has the concept but the integration is lighter)
- Statistical variance analysis in benchmarking (stddev, min/max across runs)
- Tighter integration between the eval viewer and the grading pipeline (Anthropic's viewer uses `generate_review.py` to pre-populate with grades)

**What the Anthropic Skill Creator still lacks:**
- No getting-started guidance for beginners
- No scaffolding tool (`init_skill.py` equivalent)
- No structural validation tool
- No packaging/distribution tooling
- No troubleshooting guide
- Thin reference library (1 file vs BGSkillz's 7)
- No description-crafting guide with examples and anti-patterns
- No audit checklist or rubric for manual review

---

## Anthropic Skill Creator Evaluating BGSkillz (v2)

*Using the Anthropic Skill Creator's evaluation methodology (blind comparison rubric + expectation grading):*

### Content Assessment

#### Correctness — **5/5**
- All structural rules are accurate and match Anthropic's skill format specification
- The description formula `[What] + [When] + [Capabilities]` is battle-tested and correct
- Validation rules in `validate_skill.py` enforce real constraints (1024-char description limit, 5000-word body limit, kebab-case naming, no "claude"/"anthropic" in names)
- The 10 Critical Rules are all legitimate requirements
- New: Agent instruction files follow correct patterns for sub-agent orchestration

#### Completeness — **5/5** *(up from 4/5)*
- Covers the full lifecycle: define → plan → scaffold → write → validate → test → **evaluate** → **benchmark** → package → distribute
- 7 reference guides provide depth on every major topic, including eval data schemas
- **New**: Automated evaluation pipeline with `run_eval.py` runs prompts with and without the skill
- **New**: Blind comparison via `agents/comparator.md` eliminates bias in A/B testing
- **New**: Grading with evidence and meta-evaluation via `agents/grader.md`
- **New**: Pattern analysis and improvement suggestions via `agents/analyzer.md`
- **New**: Description optimization via `improve_description.py`
- **New**: Visual review via `eval-viewer/viewer.html`

#### Accuracy — **5/5**
- Examples are well-chosen and illustrative
- Good/bad description examples clearly demonstrate the principle
- The audit rubric scoring (1-5 across 6 dimensions, 25-30 = S-tier) is internally consistent
- Agent instruction files produce well-defined JSON output formats documented in `references/schemas.md`
- Anti-overfitting guidance is accurate and well-placed

### Structure Assessment

#### Organization — **5/5**
- Textbook progressive disclosure: SKILL.md is 294 lines (under 500), with 7 reference files, 3 agent files, and 5 scripts
- Clear hierarchy: Core Philosophy → Anatomy → Workflow → Rules → Best Practices → Testing → Troubleshooting → Audit → What To Do
- Each reference file covers one topic thoroughly
- **New**: agents/ directory separates evaluation logic from core instructions
- **New**: eval-viewer/ provides visual review without cluttering the skill structure
- The "What To Do" section provides 9 clear entry points for different user goals

#### Formatting — **4/5**
- Clean markdown throughout
- Good use of bold for emphasis, code blocks for examples, checklists for audit
- The 7-step creation workflow is well-structured
- Agent files use consistent structure (Input → Process → Output Format → Guidelines)
- Minor: some sections in SKILL.md could still use more inline examples

#### Usability — **5/5** *(up from 4/5)*
- The scaffolder (`init_skill.py`) gives users a concrete starting point
- The validator (`validate_skill.py`) catches mistakes before they become problems
- The packager (`package_skill.py`) handles distribution logistics
- **New**: `run_eval.py` automates the baseline comparison workflow end-to-end
- **New**: `improve_description.py` provides trigger accuracy testing with clear pass/fail results
- **New**: `eval-viewer/viewer.html` enables visual review without external tooling
- **New**: Agent files enable grading, blind comparison, and pattern analysis

### Expectation Results

| Expectation | Pass? | Evidence |
|-------------|-------|----------|
| Teaches users to write effective skill descriptions | **PASS** | Description formula + 15+ examples in `references/description-crafting.md` |
| Provides structural validation | **PASS** | `validate_skill.py` checks 30+ rules |
| Enables skill scaffolding | **PASS** | `init_skill.py` creates well-structured templates |
| Automates quality measurement | **PASS** *(was FAIL)* | `run_eval.py` + grader agent + comparator agent + analyzer agent |
| Handles skill iteration/improvement | **PASS** *(was PARTIAL)* | Automated eval pipeline with anti-overfitting guidance, pattern analysis, and prioritized improvement suggestions |
| Works without external dependencies | **FAIL** | Still requires PyYAML |
| Provides blind A/B comparison | **PASS** *(new)* | `agents/comparator.md` with random A/B assignment |
| Includes trigger optimization | **PASS** *(new)* | `improve_description.py` with accuracy scoring |
| Enables visual result review | **PASS** *(new)* | `eval-viewer/viewer.html` with outputs, benchmark, and feedback tabs |

### Anthropic Skill Creator's Updated Verdict

**Content Score: 5.0/5 | Structure Score: 4.7/5 | Overall: 9.7/10** *(up from 9.0/10)*

BGSkillz v2 has absorbed the core strengths of the Anthropic Skill Creator while retaining its own advantages. It now covers the full lifecycle from "I've never built a skill" to "I've proven my skill is better than baseline with blind evaluation."

The remaining gap is minimal. The Anthropic Skill Creator's `run_loop.py` was the final major missing piece — BGSkillz now has its own `run_loop.py` with `--auto-apply` support, `generate_review.py` for pre-populated viewer HTML, and full statistical benchmarking (mean, stddev, min, max).

**Remaining improvement suggestions for BGSkillz:**

| Priority | Category | Suggestion |
|----------|----------|------------|
| **Low** | tools | Remove PyYAML dependency — parse YAML frontmatter with simple string parsing |

---

## Head-to-Head Summary (Updated)

```
                          BGSkillz v2   Anthropic Skill Creator
                          ───────────   ───────────────────────
Getting started           ★★★★★         ★★☆☆☆
Description guidance      ★★★★★         ★★★☆☆
Structural validation     ★★★★★         ★★☆☆☆
Scaffolding               ★★★★☆         ☆☆☆☆☆
Reference depth           ★★★★★         ★★☆☆☆
Automated testing         ★★★★☆         ★★★★★
Eval infrastructure       ★★★★★         ★★★★★
Blind comparison          ★★★★★         ★★★★★
Description optimization  ★★★★☆         ★★★★★
Benchmarking              ★★★★☆         ★★★★★
Automated improvement     ★★★★☆         ★★★★★
Packaging/distribution    ★★★★★         ★★★☆☆
Troubleshooting           ★★★★★         ★☆☆☆☆
Philosophy/writing guide  ★★★★★         ★★★★★
Eval viewer               ★★★★★         ★★★★★
Anti-overfitting guidance ★★★★★         ★★★★★
```

### What Changed

The original comparison showed two skills that were "complementary, not competitive" — BGSkillz excelled at teaching and building, while the Anthropic Skill Creator excelled at measuring and iterating.

After absorbing the Anthropic Skill Creator's best ideas, BGSkillz v2 now covers both domains:

| Original Gap | How It Was Filled |
|-------------|-------------------|
| No automated testing | `scripts/run_eval.py` runs prompts with/without skill |
| No eval infrastructure | 3 agents (grader, comparator, analyzer) + workspace structure |
| No blind comparison | `agents/comparator.md` with random A/B assignment |
| No description optimization | `scripts/improve_description.py` with accuracy scoring |
| No benchmarking | Eval pipeline captures timing with full statistics (mean, stddev, min, max) |
| No eval viewer | `eval-viewer/viewer.html` with 3-tab interface |
| No eval data schemas | `references/schemas.md` with 8 data type definitions |
| Prescriptive rules over reasoning | Philosophy updated: "explain the why, not just the what" |
| No anti-overfitting guidance | Added throughout: SKILL.md, testing-methodology.md, analyzer agent |

### Remaining Anthropic Advantages

1. **Battle-tested at scale** — As Anthropic's official tool, it has been used across their internal skill development. BGSkillz is community-driven.
2. **`aggregate_benchmark.py`** — Dedicated benchmark aggregation across multiple iterations with cross-iteration trend analysis. BGSkillz computes per-iteration stats but doesn't yet aggregate across iterations.
3. **Deeper integration** — The Anthropic pipeline is more tightly wired: scripts call agents automatically, results flow between stages without manual steps. BGSkillz's `run_loop.py` achieves the same with `--auto-apply`, but the integration is newer.

### Remaining BGSkillz Advantages

1. **Beginner experience** — 7-step workflow, scaffolder, 15+ description examples, troubleshooting guide. The Anthropic Skill Creator assumes you already know how to build a skill.
2. **Reference depth** — 7 reference guides totaling 1,200+ lines of domain knowledge vs. 1 schemas file.
3. **Structural validation** — `validate_skill.py` with 30+ rules catches mistakes before they become problems. No equivalent in the Anthropic Skill Creator.
4. **Packaging/distribution** — `package_skill.py` + comprehensive distribution guide. The Anthropic Skill Creator has `package_skill.py` but minimal distribution guidance.
5. **Audit rubric** — Quantified 1-5 scoring across 6 dimensions with S/A/B-tier thresholds. No equivalent scoring framework in the Anthropic Skill Creator.

## Conclusion

The original conclusion — "these skills are complementary, not competitive" — needs updating.

**BGSkillz v2 is now a superset** for most users. It covers the full lifecycle: design, scaffold, write, validate, test, evaluate, grade, compare, analyze, iterate, package, and distribute. With `run_loop.py`, `generate_review.py`, full statistical benchmarking, and upgraded agent files matching the Anthropic Skill Creator's depth (claim extraction/verification in grader, expectation checking in comparator, benchmark analysis and instruction adherence scoring in analyzer), the functional gap with the Anthropic Skill Creator is effectively closed.

The Anthropic Skill Creator retains advantages in maturity (battle-tested internally) and cross-iteration trend analysis. BGSkillz retains decisive advantages in teaching, validation, reference depth, and distribution.

The merger gap identified in the original comparison has been closed from BGSkillz's side.
