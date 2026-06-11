# Quality Checklist

Comprehensive pre-flight, development, and post-launch checklist for skills.

## Before You Start

- [ ] **Use cases defined**: Written 2-3 specific "A [user] wants to [action] so they can [outcome]" statements
- [ ] **Category identified**: Document/Asset Creation, Workflow Automation, or MCP Enhancement
- [ ] **Success criteria set**: At least 1 quantitative and 1 qualitative metric defined
- [ ] **Approach chosen**: Problem-first or Tool-first, with reasoning documented
- [ ] **Scope bounded**: Clear statement of what the skill does NOT do
- [ ] **Existing skills checked**: Verified no existing skill already covers this use case

## During Development

### SKILL.md Structure

- [ ] File is named exactly `SKILL.md` (not `skill.md` or `Skill.md`)
- [ ] Frontmatter is valid YAML between `---` delimiters
- [ ] `name` field is kebab-case, matches folder name
- [ ] `name` does not contain "claude" or "anthropic"
- [ ] `description` follows [What] + [When] + [Capabilities] formula
- [ ] `description` is under 1024 characters
- [ ] `description` includes 2+ trigger phrases users would actually say
- [ ] No XML tags (`<` or `>`) in frontmatter
- [ ] No `README.md` inside the skill folder
- [ ] Body is under 500 lines / 5000 words
- [ ] Uses markdown headings (## and ###), not XML tags
- [ ] All paths use forward slashes (no backslashes)

### Instruction Quality

- [ ] Instructions are in imperative voice ("Generate X" not "You should generate X")
- [ ] Critical rules are front-loaded (first 30% of the document)
- [ ] Each instruction passes the "what would Claude actually do?" test
- [ ] Defaults are set with escape hatches ("Use X by default. If user specifies Y, use that.")
- [ ] 1-2 examples of ideal output included
- [ ] Error handling instructions present (what to do when things go wrong)
- [ ] Terminology is consistent throughout (no synonym cycling)
- [ ] No contradictory instructions

### File Organization

- [ ] References are one level deep (no nested subdirectories)
- [ ] All referenced files actually exist
- [ ] No empty directories (scripts/, references/, assets/)
- [ ] Reference files are focused (under 500 lines each)
- [ ] Scripts validate inputs before executing
- [ ] Scripts don't hardcode credentials or API keys
- [ ] Scripts handle errors gracefully

### Security

- [ ] No hardcoded credentials or API keys
- [ ] No instructions to bypass safety measures
- [ ] No external URL references that could change or be compromised
- [ ] Scripts validate and sanitize inputs
- [ ] No instructions that could cause data loss without confirmation

## Before Upload / Publishing

### Trigger Testing

- [ ] Tested with 3+ exact trigger phrases — all activate the skill
- [ ] Tested with 3+ paraphrased trigger phrases — most activate the skill
- [ ] Tested with 3+ non-trigger phrases — none activate the skill
- [ ] Trigger accuracy is >90% on should-trigger prompts
- [ ] False positive rate is <10% on should-not-trigger prompts

### Functional Testing

- [ ] Happy path tested with 2+ straightforward requests
- [ ] Edge case tested (minimal input, unusual format)
- [ ] Error handling tested (missing tool, invalid input)
- [ ] Output format matches specifications
- [ ] Scripts execute correctly (`python scripts/*.py`)

### Baseline Comparison

- [ ] Ran same task with and without the skill
- [ ] Skill produces noticeably better results on target tasks
- [ ] Skill doesn't degrade performance on non-target tasks

### Validation

- [ ] `python validate_skill.py /path/to/skill` passes with 0 errors
- [ ] All warnings reviewed and addressed or accepted

### Packaging

- [ ] Package is under 1MB
- [ ] No `.git`, `__pycache__`, `.DS_Store` in package
- [ ] Package extracts to correct directory structure

## After Upload / Publishing

### Documentation (for public skills)

- [ ] README.md in repo root (not in skill folder) with:
  - [ ] What the skill does (1-2 sentences)
  - [ ] Installation instructions
  - [ ] 1-2 usage examples
  - [ ] Requirements (MCP servers, dependencies)
- [ ] License specified in both frontmatter and LICENSE file
- [ ] Version number set in metadata

### Monitoring

- [ ] Collected feedback from first 3 users
- [ ] Identified any trigger issues from real usage
- [ ] Updated description based on actual user language
- [ ] Noted any instructions that Claude doesn't follow consistently
- [ ] Planned iteration based on feedback

## Audit Rubric

Score your skill on each dimension (1-5 scale):

| Dimension | 1 (Poor) | 3 (Good) | 5 (Excellent) |
|-----------|----------|----------|----------------|
| **Description** | Vague, no trigger phrases | Formula used, some triggers | Precise formula, rich triggers, negative triggers |
| **Instructions** | Generic, abstract | Specific, some examples | Actionable, exemplified, error-handled |
| **Scope** | Too broad or too narrow | Reasonable scope | Perfectly bounded with clear exclusions |
| **Testing** | Untested | Basic trigger + happy path | Full trigger, functional, baseline, blind comparison, model testing |
| **Organization** | Everything in SKILL.md | Some use of references | Clean progressive disclosure, focused files |
| **Security** | Hardcoded secrets or unsafe | No obvious issues | Explicit security guidance, input validation |

**Score guide:**
- 25-30: S-tier — ready for public distribution
- 18-24: A-tier — solid, minor improvements possible
- 12-17: B-tier — functional, needs refinement
- Below 12: Needs significant work before publishing

## Agent-Specific Audit (Orchestration Skills)

For skills that spawn sub-agents or orchestrate multi-stage workflows, also check:

### Orchestration Design

- [ ] SKILL.md is flow control only — specialized judgment lives in `agents/`
- [ ] Each sub-agent has one clear role with structured I/O (Input → Process → Output → Guidelines)
- [ ] Deterministic work (loops, aggregation, file ops) is in scripts, not agent prompts
- [ ] Schema contracts documented in `references/schemas.md` for all agent→script handoffs
- [ ] Sub-agents load only when needed (progressive disclosure within the skill)

### Evaluation Infrastructure

- [ ] Evals test end states (outputs), not specific tool-call sequences
- [ ] Baseline comparison included (with and without skill on every test)
- [ ] Blind A/B comparison used for quality judgments (comparator agent)
- [ ] Grader runs meta-evaluation on assertion quality (flags trivially-satisfied tests)
- [ ] Parallel eval runs use clean context per test (no cross-contamination)
- [ ] Capability type identified (uplift vs encoded preference) with appropriate test strategy
- [ ] Obsolescence check: if baseline passes most evals, skill uplift may no longer be needed

### Autonomy & Safety (Tool-Using Agents)

- [ ] Tool scope is minimal (`allowed-tools` or permissions match actual needs)
- [ ] Destructive actions require confirmation or are blocked
- [ ] Agent has escalation path (when to ask user vs proceed autonomously)
- [ ] Scripts validate inputs; no hardcoded credentials

See `references/agent-lifecycle.md` for the full agent lifecycle framework.
