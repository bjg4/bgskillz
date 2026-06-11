# Exemplar Skill Notes

Research notes from studying popular skills to extract patterns for BGSkillz.
Goal: make BGSkillz the best skill at *creating* skills — not just measuring them.

Sources (mattpocock/skills):
- [teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach)
- [write-a-skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/write-a-skill)
- [grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)

---

## Three Skill Shapes

These exemplars suggest skills fall into distinct shapes. Pick the shape before writing.

| Shape | Exemplar | SKILL.md size | Memory | Best for |
|-------|----------|---------------|--------|----------|
| **Behavioral prompt** | grill-me | ~10 lines | None (chat only) | Simple interaction contracts |
| **Guided process** | write-a-skill | ~100 lines | Optional files | Teaching a workflow, scaffolding output |
| **Stateful workspace** | teach | ~200 lines + format files | Workspace files persist | Multi-session work that accumulates artifacts |

BGSkillz today optimizes for **guided process** and **orchestration**. It undercovers **behavioral prompt** ("when is less more?") and **stateful workspace** patterns.

---

## teach — Stateful Workspace

### What it does
Multi-session teaching. The user's workspace becomes the runtime — lessons, learning records, mission, references all persist as files.

### Patterns to steal

**1. Declare statefulness upfront**
> "This is a stateful request — they intend to learn over multiple sessions."

BGSkillz should ask during creation: "Is this one-shot or multi-session?" and route to different patterns.

**2. Workspace as memory**
Artifact taxonomy with clear roles:
- `MISSION.md` — compass (why)
- `learning-records/` — decision-grade insights (ADR-style)
- `lessons/` — primary deliverable
- `reference/` — compressed reuse
- `RESOURCES.md` — external grounding
- `NOTES.md` — user preferences

**3. Format files as contracts (`*-FORMAT.md`)**
Not eval schemas — contracts for *user-facing artifacts*. Each includes template, rules, and **negative criteria** ("coverage is not learning").

**4. Spec the unit of output precisely**
A "lesson" is not vague. It's: one HTML file, Tufte-style, one win, linked, cited, opens via CLI, ends with "ask followup questions."

BGSkillz creation step: **"Define your unit of output."**

**5. Domain philosophy IS the product**
Learning science (fluency vs storage strength, retrieval practice, ZPD) — not generic rules. The skill's value is *how Matt thinks about teaching*.

**6. Epistemic humility**
> "Never trust your parametric knowledge."

For knowledge-heavy skills: populate external sources before generating content.

**7. Manual invocation**
`disable-model-invocation: true` — accidental trigger would be harmful for multi-session workflows.

**8. Gates before proceeding**
Don't teach until `MISSION.md` is concrete. Interview first, write second.

### BGSkillz gaps
- No "stateful workspace" creation pattern
- No `*-FORMAT.md` recommendation for artifact-producing skills
- No "define unit of output" step
- No skill-shape decision (one-shot vs stateful)

---

## write-a-skill — Guided Process (Direct Competitor)

### What it does
Minimal meta-skill for creating skills. 3 steps: gather requirements → draft → review with user.

### Patterns to steal

**1. "Description is the only thing your agent sees"**
Best framing we've seen for why descriptions matter. Surfaces the selection problem explicitly — the agent picks from a list of description strings.

BGSkillz should use this exact framing in description-crafting guidance.

**2. Three-step process with user review built in**
```
Gather → Draft → Review with user
```
Step 3 is not optional QA — it's part of creation. BGSkillz jumps from write to validate/package; explicit human review loop is lighter and more approachable.

**3. SKILL.md structure template**
```md
## Quick start      — minimal working example
## Workflows        — step-by-step with checklists
## Advanced features — link out
```
Simpler and more scannable than BGSkillz's current anatomy sections. Consider as default scaffold template.

**4. Aggressive brevity target**
- write-a-skill: **100 lines** ideal, split beyond that
- BGSkillz: **500 lines** max

The 100-line target forces better progressive disclosure. Consider: "Target 100 lines. Hard max 500."

**5. Inline review checklist**
6 items at the end of the skill itself — no separate reference file needed for basic skills:
- Description includes triggers
- Under 100 lines
- No time-sensitive info
- Consistent terminology
- Concrete examples
- References one level deep

BGSkillz has a comprehensive checklist in references/ — but a **micro-checklist inline** for simple skills would help beginners.

**6. When-to decision trees (compact)**
"When to add scripts" and "When to split files" — short bullet criteria, not essays.

**7. Description format: two sentences**
- Sentence 1: what it does
- Sentence 2: "Use when [specific triggers]"
Third person. Max 1024 chars. Good/bad example inline.

### Where BGSkillz already wins
- Eval pipeline, blind comparison, improvement loop
- Scaffolder, validator, packager
- 7 reference guides, agent orchestration
- Anti-overfitting, capability types, audit rubric

### Where write-a-skill wins
- Approachability (3 steps vs 7)
- Brevity discipline (100 lines)
- User review as core step
- "Description is the only thing your agent sees"

### BGSkillz gaps
- Too heavy for beginners who just want to write their first skill
- No "simple path" vs "rigorous path" fork in creation workflow
- Missing the selection-problem framing for descriptions

---

## grill-me — Behavioral Prompt

### What it does
Relentless Socratic interview about a plan/design. Entire skill is ~10 lines.

### Patterns to steal

**1. When the behavior is simple, don't over-engineer**
No scripts, references, agents, checklists, or philosophy sections. The skill *is* the prompt. If you can state the behavior in one paragraph, do.

BGSkillz should teach: **"Not every skill needs references/ and scripts/. Match complexity to the behavior."**

**2. Interaction contract in the body**
Specific interaction rules encoded minimally:
- One question at a time
- Provide recommended answer with each question
- Explore codebase instead of asking when the answer is discoverable
- Walk decision tree branch by branch

This is an **interaction pattern** — how the agent relates to the user — distinct from workflow or domain patterns.

**3. Trigger phrases in description**
"grill me", "stress-test a plan" — exact phrases users would say, embedded in description.

**4. Body can be the instruction**
Frontmatter description + body that's essentially the system prompt. No headings needed when structure adds nothing.

### Skill shape decision
If the skill is:
- One behavior
- No bundled resources
- No persistent state
- No multi-step artifact production

→ **Behavioral prompt**. Keep it under 20 lines. Don't run the 7-step workflow.

### BGSkillz gaps
- No "minimal skill" path
- Creation workflow assumes all skills need full anatomy
- No interaction-pattern category (interviewer, coach, reviewer, executor)

---

## Cross-Exemplar Patterns

### Pattern: Match shape to problem

```
Is it multi-session with accumulating files?  → Stateful workspace (teach)
Is it a multi-step creation/teaching flow?    → Guided process (write-a-skill)
Is it a single interaction behavior?          → Behavioral prompt (grill-me)
Does it need specialized sub-agents?          → Orchestration (skill-creator, BGSkillz)
```

BGSkillz should make this the **first creation decision** — before use cases, before description.

### Pattern: Description as selection signal

All three nail descriptions differently:
- **teach**: short + manual invocation (triggering handled by `/teach`)
- **write-a-skill**: two-sentence formula with "Use when"
- **grill-me**: embeds exact trigger phrases ("grill me")

Common thread: description matches how the skill is invoked and what shape it is.

### Pattern: Negative space

teach: "coverage is not learning", "don't duplicate glossary"
grill-me: implicit — don't ask what codebase can answer
write-a-skill: "bad example" for descriptions

Skills need **anti-patterns** and **stop conditions**, not just positive instructions.

### Pattern: User-in-the-loop

- write-a-skill: explicit review step
- teach: confirm before changing mission
- grill-me: one question at a time (user-paced)

Creation skills should not assume fire-and-forget. Human checkpoints are a feature.

### Pattern: Right-size the skill

| Skill | Files | Lines (SKILL.md) | Scripts | References |
|-------|-------|-------------------|---------|------------|
| grill-me | 1 | ~10 | 0 | 0 |
| write-a-skill | 1 | ~100 | 0 | 0 |
| teach | 6 | ~200 | 0 | 5 format files |
| BGSkillz | 20+ | ~350 | 7 | 8 |

**Intuition:** Popularity ≠ complexity. grill-me and write-a-skill have no eval infrastructure. teach has no scripts. Right-sizing is a skill.

---

## Proposed BGSkillz Additions (from this research)

### Creation workflow changes
1. **Step 0: Pick skill shape** (behavioral / guided / stateful / orchestration)
2. **Step 1b: Define unit of output** (what artifact, what format, what "done" looks like)
3. **Fork paths**: "Simple path" (write-a-skill style) vs "Rigorous path" (full eval pipeline)
4. **User review step** before validate/package (from write-a-skill)

### New reference content
- `great-skill-patterns.md` — codified patterns from exemplars (this doc is the seed)
- Interaction patterns: interviewer, coach, executor, orchestrator
- Stateful workspace template (MISSION, records, deliverables)
- `*-FORMAT.md` convention for artifact-producing skills

### Description guidance update
- Add "description is the only thing your agent sees" framing
- Two-sentence formula as default for simple skills
- Shape-specific trigger strategy (manual vs auto vs phrase-embedded)

### Quality checklist update
- Right-sizing check: "Is this skill over-engineered for its behavior?"
- Artifact quality (for stateful skills)
- Interaction contract defined (one-at-a-time? review loop? gates?)

### Scaffold update
- `init_skill.py` templates per shape (minimal / standard / stateful / orchestration)
- Default SKILL.md structure: Quick start → Workflows → Advanced (from write-a-skill)

---

## Open Questions

- Should BGSkillz explicitly acknowledge write-a-skill as the "simple path" and position itself as "when you're ready for rigor"?
- How many exemplars before codifying into `great-skill-patterns.md`? (Currently 3)
- Do we study Anthropic official skills next, or more mattpocock productivity skills?
- Can we run BGSkillz's audit rubric on teach / write-a-skill / grill-me and see what scores they get? (Hypothesis: teach scores high on Instructions/Scope, grill-me scores high on right-sizing despite minimal Testing infrastructure)

---

## Next exemplars to study

- [ ] Other mattpocock/skills productivity skills
- [ ] Anthropic official skills (document skills, skill-creator)
- [ ] Community skills on skills.sh with high install counts
