# BGSkillz v5.0

Build high-quality, portable agents and skills that trigger reliably and deliver real value. BGSkillz is a meta-skill that covers the full lifecycle from use case definition through automated evaluation, review, audit, iteration, and distribution.

## What's New in v5.0

- **Skill shape decision** — Behavioral / guided / stateful / orchestration (Step 0)
- **Simple vs rigorous paths** — Approachable creation vs full eval pipeline
- **Great skill patterns** — Patterns from teach, write-a-skill, grill-me, SkillOpt
- **Compactness target** — ~100 lines / ~900 tokens ideal (SkillOpt-aligned)
- **Two-surface testing** — Description (router) vs body (agent) tested separately
- **User review gate** — Confirm draft before validate/package
- **SkillOpt optimization discipline** — Bounded edits, strict validation gate, per-skill metrics
- **Bakeoff harness** — Verifiable v4 vs v5 comparison on fixed briefs (`bakeoff/`)

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
- **Creation workflow** from use case definition to packaged distribution (simple + rigorous paths)
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
- 9 guides including `great-skill-patterns.md`, agent lifecycle, descriptions, testing, quality checklist, schemas
- Audit checklist with 1-5 scoring rubric across 6 dimensions (S/A/B-tier thresholds)

## Installation

### Via skills.sh (recommended)

```bash
npx skills add bjg4/bgskillz
```

### Manual

```bash
git clone https://github.com/bjg4/bgskillz.git
cp -r bgskillz/bgskillz ~/.claude/skills/bgskillz
```

The skill directory is `bgskillz/` inside the repo. The repo root holds README, CHANGELOG, bakeoff harness, and version pins — not part of the installed skill.

## Quick Start

**Create a new skill:**
```
"I want to create a new skill"
```

**Validate the installed skill:**
```bash
python3 ~/.claude/skills/bgskillz/scripts/validate_skill.py ~/.claude/skills/bgskillz
```

**Package for distribution:**
```bash
python3 ~/.claude/skills/bgskillz/scripts/package_skill.py ~/.claude/skills/bgskillz
```

**Auto-improve a skill:**
```bash
python3 ~/.claude/skills/bgskillz/scripts/run_loop.py /path/to/skill --prompts tests/prompts.json --iterations 3 --auto-apply
```

**Run the v4 vs v5 bakeoff** (from cloned repo):
```bash
python3 bakeoff/run_bakeoff.py --fixtures
python3 bakeoff/run_live_bakeoff.py
```

**Release packaging** (from cloned repo):
```bash
./release.sh
```

See `bakeoff/PROTOCOL.md` for verifiable success criteria. See `CHANGELOG.md` for version history.

## Repository Structure

```
bgskillz/                    # GitHub repo root
├── README.md                # This file
├── CHANGELOG.md
├── LICENSE
├── release.sh               # Validate + zip bgskillz/
├── SELF-EVALUATION.md
├── bakeoff/                 # v4 vs v5 comparison harness
├── versions/                # Pinned v4/v5 snapshots
└── bgskillz/                # The installable skill
    ├── SKILL.md             # Main instructions (410 lines)
    ├── agents/              # grader, comparator, analyzer
    ├── scripts/             # init, validate, package, run_eval, run_loop, ...
    ├── references/          # 9 reference guides
    └── eval-viewer/
```

## Requirements

- Python 3.9+
- [PyYAML](https://pypi.org/project/PyYAML/) (`pip install pyyaml`)

## License

MIT
