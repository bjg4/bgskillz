# Workflow Patterns

Six proven patterns for structuring skill and agent instructions. Choose the pattern that matches your skill's core behavior.

## Pattern 1: Sequential Workflow Orchestration

Use when your skill guides Claude through a multi-step process where each step depends on the previous one.

**Structure:**
```
## Workflow

### Step 1: [First action]
Do X. Verify Y before proceeding.

### Step 2: [Second action]
Using the result from Step 1, do Z.

### Step 3: [Final action]
Combine results and produce output.
```

**Key techniques:**
- Number steps explicitly so Claude follows the order
- Include verification gates: "Confirm X before moving to the next step"
- Specify what to do if a step fails: "If the API returns an error, report it and stop"
- Keep each step focused on one action

**Example use case:** Code review workflow (gather context → analyze → report findings → suggest fixes)

## Pattern 2: Multi-MCP Coordination

Use when your skill orchestrates multiple MCP servers or tools working together.

**Structure:**
```
## Tools Required

This skill uses:
- [MCP Server 1] for [purpose]
- [MCP Server 2] for [purpose]

## Workflow

1. Use [Server 1] to gather [data]
2. Process the data: [transformation logic]
3. Use [Server 2] to [action] with the processed data
4. Verify the result using [Server 1 or 2]
```

**Key techniques:**
- List required MCP servers upfront so Claude knows what's available
- Specify which server to use for each action
- Include fallback behavior if a server is unavailable: "If [server] is not connected, ask the user to enable it"
- Handle data format differences between servers

**Example use case:** Design-to-development handoff (Figma MCP → extract specs → filesystem MCP → generate component code)

## Pattern 3: Iterative Refinement

Use when the skill produces output that should improve through multiple passes.

**Structure:**
```
## Process

### Draft
Generate initial output based on user request.

### Review
Check the draft against these criteria:
- Criterion 1
- Criterion 2
- Criterion 3

### Refine
Fix any issues found in the review. Focus on [priority area].

### Final Check
Verify the output meets all criteria before presenting to the user.
```

**Key techniques:**
- Define clear quality criteria for the review step
- Limit iterations to prevent infinite loops: "Refine up to 2 times, then present the best version"
- Prioritize what to fix: "Address correctness issues first, then style"
- Show the user what changed between iterations (if significant)

**Example use case:** Report generation (draft → fact-check → improve clarity → format)

## Pattern 4: Context-Aware Tool Selection

Use when the skill needs to choose between different approaches or tools based on the user's situation.

**Structure:**
```
## Approach Selection

Determine the best approach based on context:

### If [condition A]
Use [approach/tool A] because [reason].
Steps: ...

### If [condition B]
Use [approach/tool B] because [reason].
Steps: ...

### Default
If conditions are unclear, use [default approach] and explain the choice.
```

**Key techniques:**
- Define conditions clearly so Claude can evaluate them
- Provide a default for ambiguous situations
- Explain *why* each approach is chosen (helps Claude make better decisions)
- Tell Claude to communicate its choice: "Tell the user which approach you selected and why"

**Example use case:** File storage selection (small files → local filesystem; large files → cloud storage; sensitive files → encrypted storage)

## Pattern 5: Domain-Specific Intelligence

Use when the skill embeds deep expertise in a specialized domain.

**Structure:**
```
## Domain Rules

### Core Principles
- Principle 1: [explanation]
- Principle 2: [explanation]

### Common Patterns
When you see [pattern], apply [solution].
When you see [pattern], apply [solution].

### Anti-Patterns
Never do [bad practice] because [consequence].
Instead, do [good practice].

### Edge Cases
If [unusual situation], handle it by [specific guidance].
```

**Key techniques:**
- Front-load the most important domain rules
- Use pattern-matching language: "When you see X, do Y"
- Include anti-patterns with explanations of *why* they're bad
- Cover edge cases that a non-expert would miss
- Link to reference files for exhaustive domain knowledge

**Example use case:** Compliance checking (HIPAA rules → scan code for violations → suggest fixes with regulatory references)

## Combining Patterns

Most real skills combine 2-3 patterns. A code review skill might use:
- **Sequential** for the overall workflow (gather → analyze → report)
- **Context-aware** for choosing review focus (security-heavy vs performance-heavy)
- **Domain-specific** for the actual review rules

Start with the primary pattern, then layer in secondary patterns as needed. Keep the overall structure readable — if it's getting complex, move detail into reference files.

## Pattern 6: Orchestrator-Workers (Multi-Agent)

Use when a skill needs specialized judgment at different stages, or when SKILL.md would exceed ~500 lines if all logic were inline.

**Structure:**
```
## Workflow

### Step 1: [Gather inputs]
Collect what the user needs. Validate before proceeding.

### Step 2: [Delegate to specialist]
Read `agents/specialist.md` and spawn a sub-agent with [specific input].
Wait for structured JSON output matching `references/schemas.md`.

### Step 3: [Deterministic processing]
Run `scripts/process.py` with the sub-agent output.

### Step 4: [Synthesize and present]
Combine results. Tell the user what happened.
```

**Key techniques:**
- SKILL.md describes *when, who, and what to delegate* — not how specialists do their work
- Each sub-agent gets one role with structured I/O (Input → Process → Output → Guidelines)
- Schema contracts in `references/schemas.md` stabilize handoffs between agents and scripts
- Push loops, aggregation, and file I/O into scripts — agents handle judgment
- Load sub-agent instructions only when spawning them (progressive disclosure)

**Combine with other patterns:**
- **Parallelization**: Run independent sub-agents concurrently (e.g., with_skill and baseline evals)
- **Evaluator-Optimizer**: Grade output → analyze patterns → apply fixes → re-run (see `run_loop.py`)

**Example use case:** Evaluation pipeline (orchestrator runs evals, delegates grading to grader agent, comparison to comparator agent, analysis to analyzer agent)

See `references/agent-lifecycle.md` for orchestration audit criteria and review layers.
