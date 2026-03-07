# BGSkillz v2.0

Build high-quality, portable Claude skills that trigger reliably and deliver real value. BGSkillz is a meta-skill that covers the full lifecycle from use case definition through automated evaluation, iteration, and distribution.

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
- 7 guides: descriptions, workflow patterns, testing methodology, troubleshooting, distribution, quality checklist, data schemas
- Audit checklist with 1-5 scoring rubric across 6 dimensions (S/A/B-tier thresholds)

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
│   └── improve_description.py        # Trigger accuracy optimization
├── references/
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
