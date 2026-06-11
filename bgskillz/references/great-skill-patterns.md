# Great Skill Patterns

Patterns extracted from high-quality skills and research (teach, write-a-skill, grill-me, SkillOpt). Use when creating skills — pick the shape first, then apply the matching patterns.

## Pick Your Shape First

| Shape | Lines | Memory | Example pattern |
|-------|-------|--------|-----------------|
| **Behavioral prompt** | <20 | None | grill-me: interaction contract only |
| **Guided process** | 50–100 | Optional refs | write-a-skill: gather → draft → review |
| **Stateful workspace** | 100–200 + formats | Files persist | teach: MISSION, lessons, learning-records |
| **Orchestration** | 300–500 | Sub-agents | skill-creator: eval pipeline |

If the behavior fits in one paragraph, don't over-engineer. Match complexity to the problem.

## Pattern: Description as Selection Signal

The description is **the only thing the router sees** when choosing skills. The body loads only after activation.

**Two-sentence formula (default):**
1. What it does (third person)
2. `Use when [specific triggers].` Optional: `Do NOT use for [exclusions].`

**Shape-specific triggering:**
- **Auto-trigger skills:** Rich "Use when" + negative triggers. Be slightly pushy.
- **Manual-only skills:** `disable-model-invocation: true` + `argument-hint`
- **Phrase-embedded:** Include exact user phrases ("grill me", "stress-test my plan")

**Two-surface rule:** Description and body can quietly disagree. Test both separately, then end-to-end.

## Pattern: Quick Start → Workflows → Advanced

Default SKILL.md structure (guided process shape):

```markdown
## Quick start
[Minimal working example — one common path]

## Workflows
[Numbered steps for main use cases]

## Advanced
[Link: See `references/deep-topic.md`]
```

Front-load the 20% of instructions that cover 80% of cases.

## Pattern: Compactness (High Signal)

Targets from SkillOpt and production skills:
- **Ideal:** ~100 lines / ~900 tokens
- **Hard max:** 500 lines / 5000 words

Length is not effort. SkillOpt's best skills land at 300–2,000 tokens after 1–4 accepted edits. If your skill is long, you're hiding low signal.

## Pattern: User Review Gate

Before validate/package, present the draft and ask:
- Does this cover your use cases?
- Is anything missing or unclear?
- Should any section be more/less detailed?

Creation is not fire-and-forget. Human checkpoints prevent shipping slop.

## Pattern: Stateful Workspace

For multi-session skills, treat the directory as runtime state:

| Artifact | Role |
|----------|------|
| `MISSION.md` | Compass — why (slow, rarely changes) |
| `learning-records/` | ADR-style insights with evidence |
| Deliverables dir | Primary output unit (lessons, reports) |
| `reference/` | Compressed reuse material |
| `NOTES.md` | User preferences |

Use `*-FORMAT.md` files as contracts: template + rules + **negative criteria** ("coverage is not learning").

**Protected slow section** (optional, from SkillOpt):
```markdown
<!-- SLOW_UPDATE_START -->
Durable lessons — only update at major milestones
<!-- SLOW_UPDATE_END -->
```
Fast iteration must not overwrite slow compass.

## Pattern: Interaction Contract (Behavioral)

For minimal skills, encode how the agent relates to the user:
- One question at a time
- Explore codebase before asking when answer is discoverable
- Provide recommended answer with each question
- Walk decision tree branch by branch

## Pattern: Optimization Discipline (SkillOpt)

When iterating with evals:
- **Train / selection / test splits** — selection gates acceptance; test is report-only
- **Strict gate** — accept only strict improvement; ties rejected
- **Bounded edits** — 4–8 add/delete/replace edits per step, not full rewrites
- **Rejected-edit log** — record what failed and why
- **Expect 1–4 accepted edits** total for a mature skill

Without a verifier (writing, design, strategy): use human review, not auto-apply loops.

## Pattern: Verifier-Aware Paths

| Domain | Path |
|--------|------|
| Benchmarkable (code, QA, spreadsheets) | Full eval + strict validation gate |
| Open-ended (writing, design) | Exemplar patterns + human review |

Ask: "Do I have an auto-grader?" If no, don't pretend the LLM grader is enough.

## Anti-Patterns

- **Monolith SKILL.md** — 1000+ lines when references/ and agents/ would work
- **Vague description** — "Helps with documents" gives the router nothing
- **Coverage ≠ learning** — don't write learning records for material merely covered
- **Unbounded self-edit** — accepting most proposed changes in improvement loops
- **Harness coupling** — "use Codex tool X" instead of portable procedures

See `references/exemplar-notes.md` for full research notes.
