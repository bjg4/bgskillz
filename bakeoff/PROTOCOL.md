# BGSkillz Bakeoff Protocol

Verifiable comparison: does BGSkillz v5 produce **better downstream skills** than v4?

## Hypothesis

Skills created following v5 guidance (shape-first, compactness, two-surface descriptions, user review) score higher on a deterministic rubric and functional evals than skills created following v4.

## Fixed inputs (committed, reproducible)

| Artifact | Purpose |
|----------|---------|
| `bakeoff/briefs.json` | Skill creation briefs + eval assertions |
| `versions/v4/` | Pinned v4 BGSkillz (SKILL.md + references) |
| Root `SKILL.md` v5 | Candidate BGSkillz |
| `bakeoff/score_created_skill.py` | Deterministic 100-point rubric |
| `bakeoff/fixtures/` | Reference v4-style vs v5-style outputs for rubric validation |

## Scoring rubric (0–100, no LLM required)

| Dimension | Points | Verifiable how |
|-----------|--------|----------------|
| Validation | 20 | `validate_skill.py` pass/fail |
| Compactness | 20 | Line count + token estimate vs brief ideal |
| Description | 20 | "Use when", negative triggers, length, not TODO |
| Structure | 15 | Quick start, error handling, imperative voice |
| Brief alignment | 20 | Required terms in description/body |
| Two-surface coherence | 10 | Description terms appear in body |

Report **per-brief** scores and **per-version** aggregates. Head-to-head wins count briefs where one version wins outright.

## Protocol

### Phase 1: Create (requires Claude/agent)

```bash
python bakeoff/run_bakeoff.py --generate-prompts
```

Run each prompt in `bakeoff/prompts/` twice — once with v4 BGSkillz loaded, once with v5. Output:

```
bakeoff/artifacts/v4/{brief-id}/{skill-name}/SKILL.md
bakeoff/artifacts/v5/{brief-id}/{skill-name}/SKILL.md
```

Or use fixtures to validate the scoring pipeline without Claude:

```bash
python bakeoff/run_bakeoff.py --fixtures
```

### Phase 2: Score (deterministic)

```bash
python bakeoff/run_bakeoff.py --artifacts bakeoff/artifacts -o bakeoff/report.json
```

Produces `report.json` with:
- Git commit + branch
- Per-brief scores for v4 and v5
- Mean/min/max per version
- Head-to-head wins
- Verdict: `v5_wins`, `v4_wins`, or `tie_or_inconclusive`

### Phase 3: Functional eval (optional, requires Claude CLI)

For each created skill, run brief eval prompts:

```bash
python scripts/run_eval.py bakeoff/artifacts/v5/code-review/code-review \
  --prompts bakeoff/briefs/code-review-eval.json
```

Grade with `agents/grader.md`. Compare pass rates v4 vs v5 per brief.

## Success criteria

v5 wins the bakeoff if:
1. **Mean rubric score** ≥ 5 points higher than v4 across all briefs
2. **Head-to-head wins** ≥ 2 of 3 briefs (for current corpus)
3. **Functional eval** (when run): v5 pass rate ≥ v4 on same prompts

## Anti-gaming rules

- Briefs and rubric weights are committed before creation runs
- Scorer is deterministic — same skill always gets same score
- v4 baseline pinned in `versions/v4/` with git commit hash
- Fixture run must show v5 > v5 before trusting live bakeoff results
- Report includes git commit for reproducibility

## Current fixture baseline

Run `python bakeoff/run_bakeoff.py --fixtures` — expected verdict: **v5_wins** (fixtures encode v4-style bloat vs v5-style compact skills).

Live bakeoff with agent-created skills is the real proof; fixtures prove the measurement works.
