# Agent Grader Instructions

Use this when grading bakeoff eval responses. **You are the grader** — no external CLI required.

## When to use

After live bakeoff skills are created and eval responses exist at:

```
bakeoff/live/{v4|v5}/{brief-id}/{skill-name}/eval/response.md
```

## Process

1. Read `bgskillz/agents/grader.md` — follow its grading process exactly.
2. Read `bakeoff/briefs.json` — get eval prompts and assertions per brief.
3. For each response in `bakeoff/live/`, grade against that brief's assertions.
4. Write `eval/grading.json` next to each `response.md` using the JSON format from `grader.md`.
5. Aggregate:

```bash
python bakeoff/aggregate_grader_report.py -o bakeoff/report-grader.json
```

## Parallel subagents (optional)

For faster grading, launch one subagent per response. Each subagent receives:
- `bgskillz/agents/grader.md`
- The test prompt and assertions from `briefs.json`
- The response text from `eval/response.md`

Each subagent writes its `eval/grading.json`. Then run the aggregate script once.

## Output

- Per-response: `bakeoff/live/{version}/{brief}/{skill}/eval/grading.json`
- Aggregate: `bakeoff/report-grader.json` with v4 vs v5 pass rates and verdict

## Optional: Codex CLI

If `OPENAI_API_KEY` is available, `bakeoff/grade_with_codex.py` can grade via `codex exec`.
Agent grading (this doc) is the default — same grader instructions, no auth required.
