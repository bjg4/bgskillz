# BGSkillz

Build high-quality, portable Claude skills that trigger reliably and deliver real value. BGSkillz is the definitive skill-building skill — a meta-skill that walks you through the full lifecycle from use case definition through testing, distribution, and iteration.

## Why BGSkillz?

Most skills fail because their descriptions are vague, their instructions are buried, or they trigger on the wrong requests. BGSkillz combines Anthropic's official guide, ecosystem patterns from 72K+ indexed skills, and battle-tested tooling into a single comprehensive workflow.

## Features

- **7-step creation workflow** from use case definition to packaged distribution
- **Description crafting** with the `[What] + [When] + [Capabilities]` formula
- **Scaffold generator** (`init_skill.py`) with best-practice templates
- **Comprehensive validator** (`validate_skill.py`) enforcing all official rules
- **Packager** (`package_skill.py`) with validation gate and size reporting
- **6 reference guides** covering descriptions, workflow patterns, testing, troubleshooting, distribution, and quality
- **Audit checklist** with 1-5 scoring rubric across 6 dimensions

## Installation

### Via skills.sh (recommended)

```bash
npx skills add bjg4/bgskillz
```

### Manual

```bash
git clone https://github.com/bjg4/bgskillz.git ~/.claude/skills/bgskillz
```

## Quick Start

**Create a new skill:**
```
"I want to create a new skill"
```
BGSkillz walks you through the 7-step workflow: define use cases, set success criteria, choose approach, plan contents, scaffold, write, and package.

**Audit an existing skill:**
```
"Audit my skill at ~/.claude/skills/my-skill"
```
Runs the full quality checklist and scores the skill on a 1-5 rubric across 6 dimensions.

**Validate a skill:**
```bash
python3 ~/.claude/skills/bgskillz/scripts/validate_skill.py /path/to/my-skill
```
Checks structure, frontmatter, naming, description quality, referenced files, and more.

## Requirements

- Python 3.9+
- [PyYAML](https://pypi.org/project/PyYAML/) (`pip install pyyaml`)

## License

MIT
