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

---

# SkillOpt Research (arxiv 2605.23904)

Paper: [SkillOpt: Executive Strategy for Self-Evolving Agent Skills](https://arxiv.org/pdf/2605.23904) (Microsoft, May 2026)
Community synthesis: [@koylanai thread](https://x.com/koylanai) + Context Engineering Agent Skills v2.3.0 shipping lessons

SkillOpt treats `SKILL.md` as **trainable external state** for a frozen model — textual gradient descent with deep-learning discipline. This validates the core BGSkillz thesis (skills are the adaptation layer) but exposes gaps in how BGSkillz teaches *optimization* and *compactness*.

## Paper mechanics (what actually works)

| Mechanism | What it does | Paper evidence |
|-----------|-------------|----------------|
| **Held-out validation gate** | Candidate skill accepted only if selection-split score **strictly improves** (ties rejected) | Prevents harmful "plausible" edits from accumulating |
| **Bounded edits (learning rate)** | Max L_t add/delete/replace edits per step (default L=4, cosine decay to 2) | Unbounded rewrite collapses performance; lr=4 beats lr=1,8,16 on spreadsheets |
| **Rejected-edit buffer** | Failed proposals + score drops fed back to optimizer | -1.6 to -4.6 points when removed |
| **Slow/meta update** | Protected section updated only at epoch boundary | -22.5 points on SpreadsheetBench when removed |
| **Minibatch reflection** | Failures and successes analyzed separately, merged with failure priority | Filters anecdotal fixes |
| **Separate optimizer model** | Frontier model proposes edits; frozen target model executes | Zero inference-time optimizer cost at deploy |

**Output profile:** Final skills are 300–2,000 tokens after only **1–4 accepted edits** total across training.

## Koylan's distilled lessons (shipping reality)

1. **Validation gate is the only thing that matters** in self-editing loops. If you're accepting most proposed edits, you're shipping slop. Best runs: 1–4 accepted edits total.

2. **Bounded edits > full rewrites.** 4–8 edits/step is the sweet spot. Textual learning rate — applies to any LLM-as-author loop (docs, prompts, skills).

3. **Compactness wins.** Median ~920 tokens. Length ≠ effort. High signal density.

4. **Harness < skill.** Codex-trained skill → Claude Code: +59.7 on SpreadsheetBench. Procedural knowledge transfers; runtime doesn't own the value.

5. **Frozen model + trained context** = practical domain adaptation for everyone not training weights. Portable, inspectable, zero inference overhead.

6. **Verifier is the bottleneck.** Auto-graders work for benchmarks; open-ended work (writing, design, strategy) still needs human or better verifiers.

7. **Description ≠ body (two surfaces).** Router sees description only; agent sees body once activated. They can quietly disagree — only end-to-end task tests catch this.

8. **Per-skill effect size > corpus average.** Rewriting 3 descriptions moved corpus ~1pp but individual skills 23–25pp. Measure per skill, not aggregate.

9. **Fast/slow state split** (Personal Brain OS → SkillOpt):
   - Slow-state: voice-guide, tone-of-voice.md (rarely touched)
   - Fast-state: posts.jsonl, bookmarks.jsonl (frequent updates)
   - **Protected section invariant**: fast edits cannot overwrite slow lessons (`<!-- SLOW_UPDATE_START/END -->`). Removing it: -22 points.

## Implications for BGSkillz (skill-creation skill)

These are **creation and optimization** lessons, not eval-only.

### 1. Teach compactness as a first-class goal

| Source | Target |
|--------|--------|
| SkillOpt | 300–2,000 tokens final; ~920 median |
| write-a-skill | 100 lines ideal |
| BGSkillz today | 500 lines / 5000 words max |

**Change:** Reframe limits. **Target ~100 lines / ~900 tokens.** Hard max 500 lines. "If your skill is long, you're probably hiding low signal."

### 2. Teach optimization discipline, not just "iterate"

BGSkillz `run_loop.py --auto-apply` is philosophically closer to *uncontrolled self-revision* (what SkillOpt argues against) than SkillOpt's loop.

**Creation guidance should teach:**
- Train / selection / test splits (selection gates acceptance; test is report-only)
- Strict improvement gate (ties rejected)
- Bounded edits per iteration (4–8, not full rewrites)
- Rejected-edit log (what was tried and why it failed)
- Expect **1–4 accepted edits** total for a mature skill, not 20

### 3. Protected sections for stateful skills

Borrow from SkillOpt + Koylan's fast/slow split:

```markdown
<!-- SLOW_UPDATE_START -->
Durable domain lessons — epoch-level, rarely changed
<!-- SLOW_UPDATE_END -->

## Fast procedures
(iteration-level edits allowed here)
```

For teach-style workspace skills: MISSION.md = slow; lessons = fast. Explicit invariant: fast edits must not contradict slow compass.

BGSkillz should recommend this when skill shape = **stateful workspace**.

### 4. Description/body as two test surfaces

New creation checklist item:
- [ ] Description accurately previews what the body delivers
- [ ] End-to-end test: does the skill activate AND behave as description promises?
- [ ] Test description and body **separately** (trigger eval vs functional eval)

Koylan: only E2E catches quiet disagreement. BGSkillz already has trigger + functional testing — make the **two-surface problem** explicit in creation workflow.

### 5. Per-skill measurement, not portfolio averages

When improving descriptions or running evals across a skill library:
- Report Δ per skill
- Flag skills with high variance (23pp moves hidden in 1pp average)
- Don't declare victory on corpus averages

Add to testing-methodology.md and analyzer agent guidance.

### 6. Verifier-aware creation paths

SkillOpt only works where auto-graders exist. BGSkillz should fork:

| Domain | Optimization path |
|--------|-------------------|
| Benchmarkable (code, spreadsheets, QA) | Full eval loop + strict gate (SkillOpt-style) |
| Open-ended (writing, design, strategy) | Human review gate; exemplar patterns; no false confidence from LLM grader |

Creation step: **"Do you have a verifier?"** If no → simple path + user review, not auto-apply loop.

### 7. Portability as design goal

SkillOpt transfer results support BGSkillz portability principle — but make it concrete:
- Write harness-agnostic procedures ("verify output format") not harness-specific ("use Codex tool X")
- Test skill on 2+ models or harnesses before shipping
- Procedural knowledge > runtime coupling

### 8. Skills as trainable parameters (philosophy upgrade)

Koylan's arc: Personal Brain OS (files as state) → SkillOpt (files as **measured, optimizable** state).

BGSkillz v4 agent-lifecycle + v5 direction:
- **Static:** hand-written skill
- **Measured:** eval pipeline (what we have)
- **Optimized:** SkillOpt-style bounded edits with validation gate (what we should teach)

Position BGSkillz as the guide for static → measured → optimized maturity.

## BGSkillz gaps exposed by SkillOpt

| Gap | Severity | Fix direction |
|-----|----------|---------------|
| `--auto-apply` lacks strict held-out gate | High | Document gate requirements; optionally implement selection split |
| No bounded edit cap in improvement loop | High | Max 4–8 edits per iteration in run_loop |
| No rejected-edit buffer | Medium | Log rejected proposals + score delta |
| No protected slow/fast sections | Medium | Pattern in stateful skills + scaffold |
| Compactness target too loose (500 lines) | Medium | Target 100 lines / ~900 tokens |
| Description/body mismatch not explicit | Medium | Two-surface testing in creation workflow |
| Corpus-level metrics emphasized | Low | Per-skill effect size reporting |
| Open-ended verifier gap unacknowledged | Medium | Verifier-aware creation fork |

## Synthesis: three research streams converging

```
Exemplar skills (teach, write-a-skill, grill-me)
  → HOW to shape skills (behavioral / guided / stateful)
  → Right-size, domain depth, artifact contracts

SkillOpt paper
  → HOW to OPTIMIZE skills (gate, bounded edits, compact output)
  → Skills as trainable external state

Koylan shipping lessons
  → HOW to MEASURE skills (two surfaces, per-skill Δ, fast/slow split)
  → Verifier limits, portability in production
```

BGSkillz should integrate all three into the **creation workflow**, not just the eval pipeline.

## References

- Paper: https://arxiv.org/pdf/2605.23904
- Project: https://microsoft.github.io/SkillOpt/
- Code: https://github.com/microsoft/SkillOpt
- Koylan Context Engineering Skills: referenced in thread (composer-2, claude-opus-4-7, gpt-5.5, gemini-3.1-pro cross-model testing)
