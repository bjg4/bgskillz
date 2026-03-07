# BGSkillz vs Anthropic Skill Creator: Cross-Evaluation

## Overview

Both are meta-skills — skills whose purpose is to help you build other skills. They share a common DNA (SKILL.md format, progressive disclosure, description crafting) but take fundamentally different approaches to the problem.

| Dimension | BGSkillz | Anthropic Skill Creator |
|-----------|----------|------------------------|
| **Author** | Blake Graham (community) | Anthropic (official) |
| **Philosophy** | Guidebook + toolchain | Agentic evaluation loop |
| **Core strength** | Teaching you to write good skills | Measuring and iterating on skills automatically |
| **Scripts** | 3 (init, validate, package) | 9+ (run_eval, improve_description, run_loop, aggregate_benchmark, etc.) |
| **References** | 6 deep guides | 1 schemas reference |
| **Agents** | None | 3 (analyzer, comparator, grader) |
| **Eval system** | Manual testing guidance | Automated with blind comparison, grading, and benchmarking |
| **Target user** | Anyone learning to build skills | Someone iterating on an existing skill's quality |

---

## BGSkillz Evaluating the Anthropic Skill Creator

*Using BGSkillz's own audit rubric (1-5 scale across 6 dimensions):*

### Dimension 1: Description — **4/5**

> "Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy."

- Follows the `[What] + [When] + [Capabilities]` formula well
- Clear trigger phrases: "create a skill", "run evals", "benchmark", "optimize description"
- Could benefit from a `DO NOT use for...` clause to prevent overtriggering
- At ~340 chars, well within the 1024-char limit with room for negative triggers

### Dimension 2: Instructions — **5/5**

- Extremely specific and actionable. Not "test your skill" but "spawn runs with-skill AND baseline in the same turn, draft assertions while runs execute, capture timing data from task notifications, grade with the grader agent, launch the eval viewer"
- Clear step-by-step workflows for every mode (Create, Improve, Benchmark, Description Optimization)
- Excellent use of progressive disclosure — SKILL.md stays focused while agents/ and scripts/ carry the implementation weight
- Communication guidance adapts to user expertise level
- The "Principle of Lack of Surprise" section is particularly strong — it instructs Claude to avoid hallucinating capability

### Dimension 3: Scope — **4/5**

- Well-bounded: skill creation + evaluation + improvement
- The scope is ambitious — it covers creating, testing, benchmarking, blind comparison, and description optimization
- Risk of being too broad: it tries to be both a "create from scratch" tool AND a "scientific evaluation" tool
- The eval/benchmark system is significantly more complex than what most skill authors need on day one

### Dimension 4: Testing — **5/5**

- This is where the Anthropic skill creator is unmatched
- Automated eval system with `run_eval.py` that actually invokes `claude -p` to test trigger accuracy
- Blind comparison via the comparator agent eliminates bias
- Grader agent evaluates outputs against expectations with evidence citations
- Benchmark mode runs multiple configurations with statistical analysis (mean, stddev, min, max)
- Post-hoc analyzer generates actionable improvement suggestions
- `improve_description.py` automatically rewrites descriptions based on eval failures
- Eval viewer (HTML) lets users visually inspect results

### Dimension 5: Organization — **4/5**

- Clean progressive disclosure: SKILL.md → agents/ → scripts/ → references/
- The agents/ directory is novel and well-designed — each agent has a clear role and structured I/O
- `references/schemas.md` is comprehensive but could be split (it's one big file covering 7 schemas)
- Missing: no scaffolding tool to create a new skill from scratch (init_skill equivalent)
- The eval-viewer/ directory adds a nice interactive element

### Dimension 6: Security — **3/5**

- Scripts shell out to `claude -p` which inherits the user's auth — clean pattern
- No hardcoded credentials
- However: no explicit security guidance in the SKILL.md for skills being *created*
- No validation of user inputs in the same way BGSkillz's validate_skill.py checks for credential patterns
- The `run_eval.py` script creates temporary command files in `.claude/commands/` and cleans them up — good hygiene

### BGSkillz Total Score: **25/30 (S-tier threshold)**

**Summary from BGSkillz's perspective:**

The Anthropic Skill Creator is an engineering marvel for skill evaluation. Its automated eval loop — spawn runs, grade blindly, analyze differences, improve description, repeat — is something BGSkillz can only dream about. The blind comparator agent is brilliant: it eliminates bias by hiding which output came from which skill version.

**What BGSkillz would steal:**
- The entire eval automation pipeline (run_eval.py, improve_description.py, run_loop.py)
- The blind comparison pattern for A/B testing skill versions
- The eval viewer for visual result inspection
- The concept of specialized agents (analyzer, comparator, grader) as reusable components

**What BGSkillz finds lacking:**
- No getting-started guidance for beginners. The skill assumes you already have a SKILL.md to improve
- No scaffolding tool (no `init_skill.py` equivalent)
- No validation tool for structural correctness
- No packaging/distribution tooling
- No troubleshooting guide — what do you do when things go wrong outside the eval loop?
- The reference library is thin (1 file vs BGSkillz's 6)
- No description-crafting guide with examples and anti-patterns
- No audit checklist for manual review

---

## Anthropic Skill Creator Evaluating BGSkillz

*Using the Anthropic Skill Creator's evaluation methodology (blind comparison rubric + expectation grading):*

### Content Assessment

#### Correctness — **5/5**
- All structural rules are accurate and match Anthropic's skill format specification
- The description formula `[What] + [When] + [Capabilities]` is battle-tested and correct
- Validation rules in `validate_skill.py` enforce real constraints (1024-char description limit, 5000-word body limit, kebab-case naming, no "claude"/"anthropic" in names)
- The 10 Critical Rules are all legitimate requirements

#### Completeness — **4/5**
- Covers the full lifecycle: define → plan → scaffold → write → validate → test → package → distribute
- 6 reference guides provide depth on every major topic
- Missing: automated evaluation. The testing section describes *what* to test but leaves execution to the user
- Missing: baseline comparison tooling. BGSkillz says "run the same task with and without the skill" but provides no infrastructure to do this

#### Accuracy — **5/5**
- Examples are well-chosen and illustrative
- Good/bad description examples clearly demonstrate the principle
- The audit rubric scoring (1-5 across 6 dimensions, 25-30 = S-tier) is internally consistent
- Workflow patterns in references match real Claude behavior

### Structure Assessment

#### Organization — **5/5**
- Textbook progressive disclosure: SKILL.md is 248 lines (well under 500), with 6 reference files for depth
- Clear hierarchy: Core Philosophy → Anatomy → Workflow → Rules → Best Practices → Testing → Troubleshooting → Audit
- Each reference file covers one topic thoroughly
- The "What To Do" section at the end provides clear entry points for different user goals

#### Formatting — **4/5**
- Clean markdown throughout
- Good use of bold for emphasis, code blocks for examples, checklists for audit
- The 7-step creation workflow is well-structured
- Minor: some sections could use more examples inline (the "Writing Instructions" section lists principles but only has one inline example)

#### Usability — **4/5**
- The scaffolder (`init_skill.py`) gives users a concrete starting point
- The validator (`validate_skill.py`) catches mistakes before they become problems
- The packager (`package_skill.py`) handles distribution logistics
- However: all three scripts require Python + PyYAML, which is a dependency hurdle
- The testing section tells users *what* to test but doesn't automate any of it

### Expectation Results

| Expectation | Pass? | Evidence |
|-------------|-------|----------|
| Teaches users to write effective skill descriptions | PASS | Description formula + 15+ examples in references/description-crafting.md |
| Provides structural validation | PASS | validate_skill.py checks 30+ rules |
| Enables skill scaffolding | PASS | init_skill.py creates well-structured templates |
| Automates quality measurement | FAIL | No automated eval, no blind comparison, no grading |
| Handles skill iteration/improvement | PARTIAL | Guides manual iteration but doesn't automate the loop |
| Works without external dependencies | FAIL | Requires PyYAML |

### Anthropic Skill Creator's Verdict

**Content Score: 4.7/5 | Structure Score: 4.3/5 | Overall: 9.0/10**

**Winner determination: Each skill wins in its domain.**

BGSkillz is the superior *teaching tool*. If you've never built a skill before, BGSkillz will walk you from zero to a published, validated skill faster than the Anthropic Skill Creator. Its description-crafting guide alone is worth the install — the examples and anti-patterns are immediately actionable. The validation tooling catches structural mistakes that would otherwise require trial-and-error to discover.

The Anthropic Skill Creator is the superior *engineering tool*. Once you have a working skill, it provides the infrastructure to systematically measure and improve it. The blind comparison, automated grading, and description optimization loop are genuinely novel capabilities that don't exist in BGSkillz.

**Improvement suggestions for BGSkillz:**

| Priority | Category | Suggestion |
|----------|----------|------------|
| **High** | tools | Add automated eval infrastructure — even a simple "run with skill / run without / compare" script |
| **High** | tools | Add trigger eval testing (test whether descriptions cause correct activation) |
| **Medium** | instructions | Add guidance on writing quantitative assertions/expectations for skill outputs |
| **Medium** | tools | Add a blind comparison mode for A/B testing skill versions |
| **Low** | references | Add a schemas reference documenting eval/grading JSON formats |
| **Low** | tools | Remove PyYAML dependency — parse YAML frontmatter with simple string parsing (like the Anthropic skill creator's utils.py does) |

---

## Head-to-Head Summary

```
                        BGSkillz    Anthropic Skill Creator
                        ────────    ───────────────────────
Getting started         ★★★★★       ★★☆☆☆
Description guidance    ★★★★★       ★★★☆☆
Structural validation   ★★★★★       ★★☆☆☆
Scaffolding             ★★★★☆       ☆☆☆☆☆
Reference depth         ★★★★★       ★★☆☆☆
Automated testing       ★☆☆☆☆       ★★★★★
Eval infrastructure     ☆☆☆☆☆       ★★★★★
Blind comparison        ☆☆☆☆☆       ★★★★★
Description optimization ☆☆☆☆☆     ★★★★★
Benchmarking            ☆☆☆☆☆       ★★★★★
Packaging/distribution  ★★★★★       ★★★☆☆
Troubleshooting         ★★★★★       ★☆☆☆☆
```

## Conclusion

These skills are **complementary, not competitive**. The ideal workflow is:

1. **Use BGSkillz** to design, scaffold, write, validate, and publish your skill
2. **Use the Anthropic Skill Creator** to measure, benchmark, and iteratively improve it

BGSkillz gives you the knowledge to build a good skill. The Anthropic Skill Creator gives you the tools to prove it's good — and make it better.

The most interesting gap: BGSkillz has no automated testing, and the Anthropic Skill Creator has no beginner guidance. A merger of the two would be the definitive skill-building toolkit.
