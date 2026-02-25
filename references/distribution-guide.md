# Distribution Guide

How to share, host, and position your skill for maximum adoption.

## Distribution Methods

### Direct Install

Users place the skill folder directly in their skills directory:

```bash
# Claude Code
cp -r my-skill ~/.claude/skills/my-skill

# Or for project-level skills
cp -r my-skill .claude/skills/my-skill
```

**Best for:** Personal skills, team-internal tools, quick sharing.

### Zip Upload

Package the skill as a zip and upload via Claude.ai or share for manual installation:

```bash
python ~/.claude/skills/bgskillz/scripts/package_skill.py /path/to/my-skill
# Creates my-skill.zip
```

**Best for:** Sharing with individuals, uploading to Claude.ai.

### GitHub Hosting

Host the skill in a GitHub repository. This is the recommended approach for public skills.

**Repository structure:**
```
my-skill-repo/
├── README.md              # Installation instructions, screenshots, examples
├── LICENSE
├── my-skill/              # The actual skill directory
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
└── tests/                 # Your test prompts and validation scripts
```

Important: `README.md` goes in the repo root, NOT inside the skill folder. The skill folder should only contain `SKILL.md` and its supporting files.

**Installation instructions in your README:**
```markdown
## Installation

### Claude Code
git clone https://github.com/you/my-skill-repo.git
cp -r my-skill-repo/my-skill ~/.claude/skills/

### Manual
Download the latest release zip and extract to ~/.claude/skills/
```

### Organization Deployment

For teams using Claude at scale:
- Place skills in a shared directory or internal package registry
- Use version tags for controlled rollouts
- Include a changelog with each version
- Consider skill composition — multiple focused skills vs one large skill

## API Usage

Skills can be loaded via the Anthropic API for programmatic use:

```python
import anthropic

client = anthropic.Anthropic()

# Skills are provided in the request
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Review this code for security issues"}],
    # Skill loading depends on your deployment method
)
```

This enables:
- Automated workflows that leverage skills
- Batch processing with skill-enhanced Claude
- Integration into existing toolchains

## Positioning Your Skill

### Lead with Outcomes, Not Features

**Bad:** "A skill with 15 validation rules and 3 output formats."
**Good:** "Ship database migrations without breaking production. Catches missing rollbacks, unsafe data transformations, and index gaps."

Users care about what they can accomplish, not what the skill contains.

### Tell the MCP + Skills Story

If your skill enhances an MCP server, explain the combined value:

"This skill turns the GitHub MCP server from a raw API interface into an intelligent project manager. Instead of manually calling GitHub API endpoints, describe what you want ('triage this week's issues by priority') and the skill orchestrates the right API calls."

### Explain Portability

Skills work across surfaces. Mention this:

"Works in Claude.ai, Claude Code, and via the API. Same skill, every environment."

### Show Before/After

The most compelling pitch is a side-by-side comparison:

**Without the skill:** [Show Claude's generic response]
**With the skill:** [Show the enhanced, structured, expert-level response]

## Versioning

Include version in your frontmatter metadata:

```yaml
metadata:
  version: "1.2.0"
```

Follow semantic versioning:
- **Patch** (1.0.x): Bug fixes, typo corrections, minor wording improvements
- **Minor** (1.x.0): New features, additional reference files, expanded instructions
- **Major** (x.0.0): Breaking changes to behavior, restructured output format, removed capabilities

## Quality Signals

Skills that get adopted share these traits:

1. **Specific scope** — Does one thing well. Not "helps with development" but "generates React component tests with Testing Library."
2. **Immediate value** — Works on the first try without configuration.
3. **Procedural knowledge** — Contains expert-level instructions that save the user from figuring it out themselves.
4. **Well-tested** — The author has clearly used it and refined it.
5. **Good documentation** — The README explains what it does, shows examples, and has clear installation steps.

## Maintenance

After publishing:
- Monitor user feedback for trigger issues
- Update descriptions based on real usage patterns
- Keep reference files current with API/tool changes
- Test with new Claude model releases (behavior can shift)
- Increment version numbers with each update
