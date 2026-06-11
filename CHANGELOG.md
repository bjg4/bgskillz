# Changelog

All notable changes to BGSkillz are documented here.

## [5.0.0] - 2026-06-11

### Added

- **Skill shape picker (Step 0)** — Behavioral / guided / stateful / orchestration
- **Simple vs rigorous creation paths** — Approachable first skill vs full eval pipeline
- **`references/great-skill-patterns.md`** — Patterns from teach, write-a-skill, grill-me, SkillOpt
- **Compactness target** — ~100 lines / ~900 tokens ideal for downstream skills
- **Two-surface testing** — Description (router) vs body (agent) tested separately
- **User review gate** — Confirm draft before validate/package
- **SkillOpt optimization discipline** — Bounded edits, strict validation gate
- **Bakeoff harness** (`bakeoff/`) — Verifiable v4 vs v5 comparison on fixed briefs
- **Agent grader** — Grade eval outputs via `bgskillz/agents/grader.md` without external CLI auth

### Changed

- **Repo layout** — Skill lives in `bgskillz/` subfolder; README and dev tooling at repo root
- **Creation workflow** — Shape-first, compactness-aware, with explicit path selection
- **Philosophy** — Added principles for two-surface testing, right-sizing, and SkillOpt discipline

### Bakeoff results (v4 vs v5)

- Structural rubric: v5 **89.6** vs v4 **81.3** (+8.3 mean)
- Agent grader pass rate: v5 **100%** vs v4 **88.9%**
- Head-to-head brief wins: v5 **3/3**
- Key differentiator: grill-me-clone — v5 produces behavioral one-question skills; v4 over-engineers

## [4.0.0]

- Agent lifecycle guide, orchestration patterns, end-state evaluation
- Cross-iteration aggregation (`aggregate_benchmark.py`)
- Capability uplift vs encoded preference framework

## [2.0.0]

- Automated evaluation pipeline (`run_eval.py`, grader/comparator/analyzer agents)
- Improvement loop (`run_loop.py`), description optimizer, eval viewer

## [1.0.0]

- Initial release: 7-step workflow, scaffolder, validator, packager, reference library

[5.0.0]: https://github.com/bjg4/bgskillz/releases/tag/v5.0.0
