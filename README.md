# BGSkillz v4.0

Build high-quality, portable agents and skills that trigger reliably and deliver real value. BGSkillz is a meta-skill that covers the full lifecycle from use case definition through automated evaluation, review, audit, iteration, and distribution.

## What's New in v4.0

- **Agent lifecycle guide** — Comprehensive framework for creating, reviewing, auditing, and improving agents (not just skills)
- **Agent architecture** — Rules vs Skills vs Commands vs Sub-agents; instructions + tools + model harness model
- **Two capability types** — Capability uplift vs encoded preference, with different testing and retirement strategies
- **End-state evaluation** — Grade outcomes, not tool-call sequences, for non-deterministic multi-agent paths
- **Review layers** — Self-review → during-generation → dedicated review → blind comparison → CI → autonomy governance
- **Orchestration patterns** — Parallelization, Orchestrator-Workers, Evaluator-Optimizer with audit criteria
- **Cross-iteration aggregation** — `aggregate_benchmark.py` for trend analysis across eval iterations
- **Capability obsolescence detection** — When baseline passes without the skill, the uplift may no longer be needed

## What's New in v2.0

- **Automated evaluation pipeline** — Run prompts with and without your skill, grade outputs, blind-compare them, and analyze patterns
- **3 evaluation agents** — Grader (claim extraction + binary grading), Comparator (blind A/B with quality profiles), Analyzer (benchmark analysis + instruction adherence scoring)
- **Automated improvement loop** — `run_loop.py --auto-apply` runs eval → grade → analyze → improve → re-eval automatically
- **Statistical benchmarking** — Mean, stddev, min, max timing stats with success rates
- **Description optimizer** — Test and improve trigger accuracy with `improve_description.py`
- **Visual review** — HTML eval viewer + `generate_review.py` for self-contained review pages
- **Anti-overfitting philosophy** — Generalize from feedback, explain reasoning over rigid rules

## Features

### Building
- **7-step creation workflow** from use case definition to packaged distribution
- **Description crafting** with the `[What] + [When] + [Capabilities]` formula and 15+ examples
- **Scaffold generator** (`init_skill.py`) with best-practice templates
- **Comprehensive validator** (`validate_skill.py`) enforcing 30+ rules
- **Packager** (`package_skill.py`) with validation gate and size reporting

### Evaluating
- **Eval runner** (`run_eval.py`) — Baseline comparison with statistical benchmarking
- **Grader agent** — Claim extraction/verification, binary PASS/FAIL grading, execution metrics, meta-evaluation
- **Comparator agent** — Blind A/B comparison with prompt analysis, expectation checking, quality profiles
- **Analyzer agent** — Benchmark analysis, instruction adherence scoring, prioritized improvement suggestions
- **Improvement loop** (`run_loop.py`) — Automated eval→grade→analyze→improve cycle with backups
- **Description optimizer** (`improve_description.py`) — Trigger accuracy testing and rewriting
- **Eval viewer** — Interactive HTML viewer + `generate_review.py` for shareable reports

### Reference Library
- 8 guides: agent lifecycle, descriptions, workflow patterns, testing methodology, troubleshooting, distribution, quality checklist, data schemas
- Audit checklist with 1-5 scoring rubric across 6 dimensions (S/A/B-tier thresholds)
- Agent-specific audit criteria for orchestration skills and tool-using agents

## Installation

### Via skills.sh (recommended)

```bash
npx skills add bjg4/bgskillz
```

### Manual

```bash
git clone https://github.com/bjg4/bgskillz.git ~/.claude/skills/bgskillz
```

## Quick Start

**Create a new skill:**
```
"I want to create a new skill"
```
Walks you through the 7-step workflow: define use cases, set success criteria, choose approach, plan contents, scaffold, write, and package.

**Audit an existing skill:**
```
"Audit my skill at ~/.claude/skills/my-skill"
```
Runs the full quality checklist and scores the skill across 6 dimensions.

**Evaluate a skill:**
```
"Run evals on my skill at ~/.claude/skills/my-skill"
```
Runs the automated evaluation pipeline with baseline comparison, grading, and analysis.

**Auto-improve a skill:**
```bash
python3 ~/.claude/skills/bgskillz/scripts/run_loop.py /path/to/skill --prompts tests/prompts.json --iterations 3 --auto-apply
```
Runs the full improvement loop: evaluate, grade, analyze, apply suggestions, repeat.

**Audit an agent or orchestration skill:**
```
"Audit my agent at ~/.claude/skills/my-skill"
```
Runs the full quality checklist plus agent-specific audits (orchestration, eval coverage, autonomy).

**Design multi-agent orchestration:**
```
"I want to build an orchestration skill with sub-agents"
```
Walks through orchestration patterns, sub-agent design, schema contracts, and the eval pipeline.

**Aggregate eval trends:**
```bash
python3 ~/.claude/skills/bgskillz/scripts/aggregate_benchmark.py /path/to/workspace
```
Compares pass rates and timing across eval iterations.

**Validate a skill:**
```bash
python3 ~/.claude/skills/bgskillz/scripts/validate_skill.py /path/to/my-skill
```

## File Structure

```
bgskillz/
├── SKILL.md                          # Main skill instructions (308 lines)
├── agents/
│   ├── grader.md                     # Assertion grading with claim verification
│   ├── comparator.md                 # Blind A/B comparison
│   └── analyzer.md                   # Pattern analysis + improvement suggestions
├── scripts/
│   ├── init_skill.py                 # Scaffold a new skill
│   ├── validate_skill.py             # Structural validation (30+ rules)
│   ├── package_skill.py              # Package for distribution
│   ├── run_eval.py                   # Automated evaluation with benchmarking
│   ├── run_loop.py                   # Eval→grade→analyze→improve loop
│   ├── aggregate_benchmark.py        # Cross-iteration trend analysis
│   └── improve_description.py        # Trigger accuracy optimization
├── references/
│   ├── agent-lifecycle.md            # Create, review, audit, improve agents
│   ├── description-crafting.md       # 15+ examples and anti-patterns
│   ├── workflow-patterns.md          # Common skill patterns
│   ├── testing-methodology.md        # Testing approaches and methodology
│   ├── troubleshooting.md            # Common issues and fixes
│   ├── distribution-guide.md         # Hosting and positioning
│   ├── quality-checklist.md          # Audit rubric with scoring
│   └── schemas.md                    # JSON schemas for 8 data types
└── eval-viewer/
    ├── viewer.html                   # Interactive HTML eval viewer
    └── generate_review.py            # Generate self-contained review pages
```

## Requirements

- Python 3.9+
- [PyYAML](https://pypi.org/project/PyYAML/) (`pip install pyyaml`)

## License

MIT
