# Troubleshooting Guide

Common problems with skills and how to fix them.

## Skill Won't Upload

### File naming
The file MUST be named exactly `SKILL.md`. Not `skill.md`, not `Skill.md`, not `SKILL.MD`.

Check: `ls -la` in your skill directory and verify the exact casing.

### Frontmatter format
Frontmatter must be valid YAML between `---` delimiters:

```yaml
---
name: my-skill
description: What it does. When to use it. What it covers.
---
```

Common YAML errors:
- Missing quotes around descriptions with colons: `description: "Use for: testing"` (needs quotes because of the colon)
- Tabs instead of spaces (YAML requires spaces)
- Missing the closing `---`

### Skill name issues
- Must be kebab-case: `my-skill` not `my_skill` or `MySkill`
- No spaces
- Must start with a letter
- Cannot contain "claude" or "anthropic"
- Must match the folder name

### File too large
If the skill has many files or large assets, the upload may fail silently. Keep the total package under 1MB.

## Skill Doesn't Trigger

This is the most common problem. It almost always comes down to the description.

### Debugging checklist

1. **Read your description aloud.** Does it contain the words a user would say? If a user says "help me write tests" and your description says "quality assurance automation," there's a vocabulary mismatch.

2. **Check for the 'when' clause.** A description without "Use when..." or equivalent gives Claude no trigger context. Add explicit trigger phrases.

3. **Test with exact description words.** Try a prompt that uses the exact words from your description. If it triggers with exact words but not paraphrases, your description is too narrow.

4. **Check for competition.** If another skill has a similar description, Claude may activate the other skill instead. Make your description more specific to differentiate.

5. **Check skill is actually installed.** In Claude Code, verify with the /skills command. In Claude.ai, check the skills panel.

### Quick fixes

- Add 2-3 more trigger phrases: "Use when creating X, building Y, or setting up Z"
- Include verbs users actually say: "write", "create", "build", "set up", "fix", "debug"
- Mention file types if relevant: ".py files", "Dockerfile", "YAML configs"
- Include the domain noun: "React components", "SQL queries", "API endpoints"

## Skill Triggers Too Often

### Symptoms
- Activates on unrelated tasks
- Interferes with other skills
- Users see skill behavior when they didn't ask for it

### Fixes

**Add negative triggers:**
Append to your description: "Do NOT use for [adjacent task 1] or [adjacent task 2]."

**Narrow the scope:**
Instead of "Helps with JavaScript development" try "Generate and optimize Webpack configurations for JavaScript bundling."

**Use specific terminology:**
Replace broad words with precise ones. "Code" → "React components". "Testing" → "Jest unit tests". "Database" → "PostgreSQL migrations".

**Check for overly common words:**
If your description contains "help", "code", "write", "create" without qualification, it may match too broadly. Always pair these verbs with specific nouns.

## Instructions Not Followed

### Symptoms
- Claude activates the skill but ignores key instructions
- Output format doesn't match the spec
- Important rules are skipped

### Causes and fixes

**Instructions are buried.** Claude processes SKILL.md like a prompt — early content gets more weight. Move critical rules to the top of the file, not the bottom.

**Too much text.** If SKILL.md is over 3000 words, Claude may skim. Cut aggressively. Move detail to reference files. Keep the core instructions under 2000 words.

**Ambiguous instructions.** "Format the output nicely" means nothing. "Use H2 headings for sections, bullet points for lists, and code fences for code blocks" is actionable.

**Contradictory instructions.** If you say "be concise" in one section and "include comprehensive detail" in another, Claude will pick one unpredictably. Resolve contradictions.

**Model limitations.** Haiku follows simpler instructions better than complex ones. If targeting Haiku, keep instructions direct and explicit. Test on the model your users will actually use.

**Lacking examples.** Claude mimics examples more reliably than it follows abstract rules. Add 1-2 concrete examples of ideal output.

## MCP Connection Issues

### Server not available
If your skill depends on an MCP server and it's not connected:

1. **Include fallback instructions:** "If [MCP tool] is not available, inform the user and suggest they enable it."
2. **Don't assume tools exist:** Check tool availability and handle gracefully.

### Authentication failures
MCP servers may require authentication. Your skill should:
- Not hardcode credentials
- Instruct Claude to ask the user for credentials if needed
- Specify which environment variables to check

### Tool name changes
If an MCP server updates its tool names, your skill breaks. Mitigate by:
- Referencing tools by purpose, not just name
- Including the expected tool name but with fallback guidance
- Noting which MCP server version you tested against

### Debugging MCP issues
Tell Claude to test the MCP server independently:
"Before using [tool], verify it works by calling [simple test command]. If it fails, report the error to the user."

## Large Context Issues

### Symptoms
- Claude seems to forget parts of the skill instructions
- Output quality degrades on complex tasks
- Claude mixes up skill instructions with other context

### Causes and fixes

**SKILL.md is too large.** Over 5000 words, and Claude's attention to specific instructions drops. Split into SKILL.md (core rules) + reference files (depth).

**Too many skills enabled.** If the user has many skills installed, the combined context may be too large. Your skill should be self-contained enough to work even when other skills are present.

**Progressive disclosure not used.** Don't dump everything into SKILL.md. Use `references/` files and instruct Claude: "Read `references/detail.md` only when the user asks about [topic]." This keeps the default context lean.

**Reference files are too large.** Even reference files should be focused. A 2000-line reference file is an encyclopedia, not a reference. Split into focused files.

## Skill Works Locally But Not After Upload

### Check for local-only paths
If your skill references `/Users/yourname/...` or other absolute paths, it won't work for anyone else. Use relative paths from the skill root.

### Check for local-only dependencies
If scripts require packages not in the standard library, document the requirements or bundle them.

### Check for platform-specific commands
Bash scripts with `pbcopy`, `open`, or other macOS-specific commands won't work on Linux. Either handle both platforms or document the requirement.
