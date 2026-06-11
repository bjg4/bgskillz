# Testing Methodology

Systematic approaches for verifying that your skill triggers correctly, produces good output, and actually improves on vanilla Claude.

## Testing Approaches

### Manual Testing (Claude.ai / Claude Code)

The simplest approach. Upload or install your skill, then interact with Claude.

**Good for:** Initial development, trigger testing, quick iteration
**Limitation:** Time-consuming, hard to reproduce exactly

### Scripted Testing (Claude Code CLI)

Use Claude Code's CLI mode to run repeatable test prompts:

```bash
# Test a trigger phrase
echo "Help me create a new skill" | claude --print

# Test a non-trigger phrase
echo "Write a Python script to parse CSV" | claude --print
```

**Good for:** Regression testing, batch trigger testing
**Limitation:** Can't easily verify nuanced output quality

### Programmatic Testing (API)

Use the Anthropic API with the `container.skills` parameter to test skills programmatically:

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Help me create a new skill"}],
    # Skills are loaded via the API skill parameter
)
```

**Good for:** Automated test suites, CI integration, A/B testing
**Limitation:** Requires API access, costs money per test

## Two Kinds of Capabilities

Before writing tests, classify what your skill does. The type determines what regressions mean and when to retire the skill.

### Capability Uplift

Teaches the model something it cannot do consistently without help (proprietary formats, exact coordinate placement, domain-specific techniques).

**Test for:** Measurable improvement over baseline on target tasks.
**Run evals:** After every model update.
**Retire when:** Baseline passes your evals without the skill — the uplift may have been absorbed into the base model.

### Encoded Preference

Sequences a workflow the model could do piecemeal, but according to your team's process (review checklists, report formats, release steps).

**Test for:** Fidelity to the actual workflow, not raw quality vs baseline.
**Run evals:** When the underlying process changes.
**Retire when:** The process itself changes — update the skill to match.

Tag test assertions with capability type so you interpret failures correctly.

## End-State Evaluation for Multi-Agent Systems

Multi-agent paths are non-deterministic — the same skill may take different tool-call sequences across runs. Evaluate **outcomes**, not processes.

**Evaluate:**
- Final output correctness and completeness
- Whether the user's request was fulfilled
- Schema compliance of structured outputs
- Timing and cost aggregates

**Don't evaluate:**
- Specific tool-call order (unless order is a safety requirement)
- Exact reasoning chains
- Number of intermediate steps

Use a **separate grading agent** that sees only the output and rubric — not the task agent's reasoning. This prevents anchoring bias where a flawed process accidentally produces a good result.

## Trigger Testing

The most critical test category. If your skill doesn't trigger, nothing else matters.

### Should-Trigger Tests

Write 5-10 prompts that SHOULD activate your skill:

1. **Exact match**: Use the exact words from your description
2. **Paraphrase**: Same intent, different words
3. **Implicit**: The task implies your skill without naming it
4. **With context**: A longer message where the skill-relevant part is embedded

Example for a skill-building skill:
- "Create a new skill" (exact)
- "I want to build a Claude plugin" (paraphrase)
- "How do I extend Claude's capabilities with custom instructions?" (implicit)
- "I've been working on this project and I think it would be useful to package it as a skill. Can you help?" (context-embedded)

### Should-NOT-Trigger Tests

Write 3-5 prompts that should NOT activate your skill:

- Prompts in adjacent domains
- Prompts with similar keywords but different intent
- Completely unrelated prompts

Example:
- "Write a Python script" (adjacent — coding, but not skill-building)
- "Explain how Claude's context window works" (similar keywords, different intent)
- "What's the weather like?" (unrelated)

### Trigger Test Scorecard

Track results in a simple table:

| Prompt | Expected | Actual | Pass? |
|--------|----------|--------|-------|
| "Create a new skill" | Trigger | Trigger | Yes |
| "Build a Claude plugin" | Trigger | No trigger | No |
| "Write a Python script" | No trigger | No trigger | Yes |

**Target:** >90% correct on should-trigger, >95% correct on should-not-trigger.

## Functional Testing

Once the skill triggers, verify it produces correct output.

### Happy Path Tests

Test the most common use cases with straightforward inputs:
- Does the skill follow its own instructions?
- Is the output format correct?
- Are all required sections/elements present?

### Edge Case Tests

Test unusual inputs:
- Empty or minimal input: "Create a skill" (no details provided)
- Very specific input: "Create a skill called my-cool-tool that does X, Y, Z with these exact requirements..."
- Conflicting input: "Create a skill that does everything" (impossible scope)
- Wrong domain: The skill triggers but the user's actual need is outside its scope

### Error Handling Tests

Test failure scenarios:
- Missing required tools/MCP servers
- Invalid user input
- API failures (if applicable)

Verify the skill fails gracefully with helpful messages, not silently or with confusing errors.

## Baseline Comparison

The most overlooked test: Is your skill actually better than Claude without it?

### Method

1. Run the same task WITHOUT the skill installed
2. Run the same task WITH the skill installed
3. Compare outputs on these dimensions:
   - **Correctness**: Are there fewer errors with the skill?
   - **Completeness**: Does the skill produce more thorough output?
   - **Consistency**: Does the skill produce more predictable output?
   - **Efficiency**: Does the skill reduce back-and-forth?

If the skill doesn't meaningfully improve on vanilla Claude, reconsider whether it's needed.

If the skill doesn't meaningfully improve on vanilla Claude, reconsider whether it's needed. If baseline *matches or beats* the skill, the capability uplift may be obsolete.

## Parallel Evaluation with Clean Context

Running evals sequentially causes two problems: slow results and context bleed between test runs. Best practice:

- Run each test prompt in an **isolated context** (separate agent session or `context: fork`)
- Run with_skill and baseline **in parallel** when possible
- Capture per-run timing and token metrics independently
- Never let grading results from test-1 influence test-2's execution

The eval pipeline in `scripts/run_eval.py` handles this. For manual testing, start a fresh conversation per test case.

## Review Layers

Testing measures quality; review catches issues before they ship. Use the right layer:

| Layer | When | What it catches |
|-------|------|----------------|
| Self-review checklists | Before agent responds | Missing imports, schema violations, incomplete output |
| During-generation observation | While agent works | Wrong direction early — stop and redirect |
| Dedicated review pass | After agent finishes | Line-by-line issues in diffs |
| Blind comparison | After eval runs | Whether skill version is actually better than baseline |
| CI/PR review | Before merge | Regressions, lint errors, type failures |
| Autonomy governance | Before tool execution | Actions that exceed permitted scope |

See `references/agent-lifecycle.md` for the full review framework.

## Model Testing

Different Claude models respond differently to skill instructions.

### Haiku
- Follows explicit, simple instructions well
- May miss nuanced or implicit guidance
- Needs more explicit step numbering
- Test critical paths to ensure they work

### Sonnet
- Good balance of instruction following and creativity
- Handles moderate complexity well
- The primary target for most skills

### Opus
- Handles complex, nuanced instructions well
- May add more than requested (can be good or bad)
- Test that the skill doesn't over-constrain Opus

**Recommendation:** Develop primarily on Sonnet. Test critical paths on Haiku to ensure robustness. Test on Opus to verify the skill doesn't limit Claude's capabilities unnecessarily.

## Iteration Signals

### Undertriggering
**Symptoms:** Users have to explicitly name or invoke the skill. Paraphrased requests don't activate it.

**Fixes:**
- Add more trigger phrases to the description
- Include common synonyms and verbs users would use
- Broaden the "when to use" clause slightly
- Add file type mentions if relevant

### Overtriggering
**Symptoms:** Skill activates on unrelated tasks. Users complain about unwanted behavior.

**Fixes:**
- Add negative trigger clauses: "Do NOT use for..."
- Narrow the description scope
- Use more specific, less common terminology
- Remove overly broad keywords

### Partial Following
**Symptoms:** Claude activates the skill but doesn't follow all instructions.

**Fixes:**
- Front-load critical instructions (put them first, not last)
- Use bold or headers for must-follow rules
- Reduce total word count — Claude may skim long documents
- Add explicit examples of correct output
- Check that instructions aren't contradictory

## Success Metrics

### Quantitative
- Trigger accuracy: >90% correct activation on test prompts
- Output correctness: >85% of outputs need no manual correction
- Time savings: Task completion X% faster than without the skill
- Consistency: Output format matches template >90% of the time

### Qualitative
- Users find the output useful without heavy editing
- The skill integrates naturally into the user's workflow
- Claude's explanations and reasoning align with the skill's domain
- Error messages are helpful and actionable

## Automated Evaluation Pipeline

For rigorous, reproducible testing, use the automated evaluation pipeline. This runs test prompts through Claude with and without the skill, then uses specialized sub-agents for grading and comparison.

### Setup

Create a prompts file (`tests/prompts.json`):

```json
[
  {
    "id": "test-1",
    "prompt": "Help me create a skill for code review",
    "assertions": [
      "Output includes a SKILL.md template",
      "Description follows the [What] + [When] + [Capabilities] formula",
      "Includes at least one example"
    ]
  }
]
```

### Running Evaluations

```bash
# Run eval with baseline comparison
python ~/.claude/skills/bgskillz/scripts/run_eval.py /path/to/skill --prompts tests/prompts.json

# Run iteration 2 after improvements
python ~/.claude/skills/bgskillz/scripts/run_eval.py /path/to/skill --prompts tests/prompts.json --iteration 2
```

### Grading with Sub-Agents

Use the agents in `agents/` to evaluate outputs:

1. **Grader** (`agents/grader.md`): Evaluates outputs against assertions with binary PASS/FAIL grades and evidence. Extracts and verifies claims (catches hallucinations assertions miss). Runs meta-evaluation on the assertion set itself.

2. **Blind Comparator** (`agents/comparator.md`): Compares skill vs. baseline outputs without knowing which is which. Scores on content and structure dimensions. Prevents evaluator bias.

3. **Post-Hoc Analyzer** (`agents/analyzer.md`): After unblinding, analyzes patterns across all test cases. Identifies consistent wins/losses, instruction adherence, and benchmark trends. Produces prioritized improvement suggestions (P0/P1/P2) with overfitting risk assessment.

### Cross-Iteration Trends

```bash
python ~/.claude/skills/bgskillz/scripts/aggregate_benchmark.py /path/to/workspace
```

Compares pass rates, timing, and scores across iterations. A skill that improves on iteration 1 but regresses on iteration 3 is likely overfitting to specific test cases.

### Review Workflow

1. Run the eval pipeline to collect outputs
2. Grade each test case with the grader agent
3. Run blind comparisons with the comparator agent
4. Unblind and analyze with the analyzer agent
5. Open `eval-viewer/viewer.html` for visual review
6. Provide per-test-case feedback, export as `feedback.json`
7. Apply improvements and run the next iteration

### Description Optimization

```bash
# Generate default trigger queries
python ~/.claude/skills/bgskillz/scripts/improve_description.py /path/to/skill --generate-only

# Run trigger accuracy tests
python ~/.claude/skills/bgskillz/scripts/improve_description.py /path/to/skill --queries queries.json
```

### Anti-Overfitting

When iterating on eval results:

- **Ask "would this generalize?"** before every change
- **Read transcripts**, not just grades — look for behavioral patterns
- **Look for repeated work** across runs (if Claude writes similar setup each time, bundle it)
- **Fewer, higher-impact changes** over many small tweaks
- **Explain reasoning** over adding rigid constraints

See `references/schemas.md` for all data format specifications.
