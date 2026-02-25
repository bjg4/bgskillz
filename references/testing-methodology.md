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
