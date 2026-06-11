# Live Bakeoff Manifest

**Run:** 2026-06-11  
**Branch:** `cursor/bgskillz-v5-bakeoff-24b5`  
**Commit:** `d204d13` (pre-live-run; see `report-live.json` for exact git hash)

## Method

For each brief in `briefs.json`, an agent created a skill following:
- **v4:** `versions/v4/SKILL.md` (7-step workflow, comprehensive guidance)
- **v5:** root `SKILL.md` v5.0.0 (shape-first, compactness, two-surface, great-skill-patterns)

Skills saved under `bakeoff/live/{v4|v5}/{brief-id}/{skill-name}/`.

Functional eval: agent applied each created skill to the brief's eval prompt; responses in `eval/response.md`. Scored with `score_functional.py` (deterministic assertion checks).

## Results (`report-live.json`)

| Metric | v4 | v5 | Winner |
|--------|----|----|--------|
| Structural mean | 81.33 | 89.61 | **v5** |
| Functional pass rate | 0.778 | 0.889 | **v5** |
| Head-to-head briefs | 0/3 | 3/3 | **v5** |

**Verdict: v5_wins** (structural + functional)

## Per-brief highlights

| Brief | Structural Δ (v5−v4) | Functional v4 / v5 |
|-------|---------------------|---------------------|
| code-review | +8.4 | 1.0 / 1.0 |
| commit-message | +7.8 | 1.0 / 1.0 |
| grill-me-clone | +11.4 | 0.33 / 0.67 |

v5's shape-first guidance produced a 10-line behavioral skill for grill-me; v4 over-engineered it (multi-question dump), failing the "one question at a time" assertion.

## Reproduce

```bash
python bakeoff/run_live_bakeoff.py   # after artifacts populated
python bakeoff/run_bakeoff.py --artifacts bakeoff/live -o bakeoff/report-live.json
```
