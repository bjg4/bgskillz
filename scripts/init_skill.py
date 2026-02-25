#!/usr/bin/env python3
"""Initialize a new skill scaffold with best-practice structure and TODO prompts."""

import argparse
import os
import sys

# Import canonical name validation from validate_skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_skill import validate_skill_name


def create_skill_md(name: str) -> str:
    """Generate SKILL.md content with TODO prompts."""
    return f"""---
name: "{name}"
description: "TODO: Write your description using the formula: [What it does] + [When to use it] + [Key capabilities]. Aim for 100-200 chars. Max 1024. Include trigger phrases users would actually say."
license: MIT
metadata:
  author: "TODO: Your name"
  version: "0.1.0"
---

# {name.replace('-', ' ').title()}

TODO: One sentence explaining what this skill does and why it exists.

## Quick Start

TODO: Show the simplest possible usage. What does the user say to trigger this skill, and what happens?

## Instructions

TODO: Write specific, actionable instructions in imperative voice. Front-load the most important rules.

Key principles:
- Be specific: "Use 4-space indentation" not "Format code nicely"
- Set defaults with escape hatches: "Use X by default. If the user specifies Y, use that instead."
- Include examples of good output
- Tell Claude what to do when things go wrong

## Examples

TODO: Show 1-2 examples of ideal input/output pairs.

### Example 1: [Scenario Name]

**User says**: "..."

**Skill produces**: ...

## Guidelines

TODO: Add constraints, style rules, or domain-specific knowledge.

- Guideline 1
- Guideline 2
- Guideline 3
"""


def create_example_reference(name: str) -> str:
    """Generate a starter reference file."""
    return f"""# {name.replace('-', ' ').title()} -- Reference Guide

TODO: Add deep reference material here that supports the main SKILL.md.

This file is read by Claude when referenced from SKILL.md. Keep SKILL.md lean
and put detailed knowledge here.

## Section 1

TODO: Add content.

## Section 2

TODO: Add content.
"""


def init_skill(name: str, path: str, include_scripts: bool = False, include_references: bool = True) -> None:
    """Create the full skill scaffold."""
    # Validate name even when called as a library function
    errors = validate_skill_name(name)
    if errors:
        raise ValueError(f"Invalid skill name: {'; '.join(errors)}")

    skill_dir = os.path.join(path, name)

    try:
        os.makedirs(skill_dir, exist_ok=False)
    except FileExistsError:
        print(f"Error: Directory already exists: {skill_dir}")
        sys.exit(1)

    print(f"Created: {skill_dir}/")

    # SKILL.md
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write(create_skill_md(name))
    print(f"Created: {skill_md_path}")

    # References directory
    if include_references:
        refs_dir = os.path.join(skill_dir, "references")
        os.makedirs(refs_dir, exist_ok=True)
        ref_path = os.path.join(refs_dir, "guide.md")
        with open(ref_path, "w", encoding="utf-8") as f:
            f.write(create_example_reference(name))
        print(f"Created: {ref_path}")

    # Scripts directory
    if include_scripts:
        scripts_dir = os.path.join(skill_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        script_path = os.path.join(scripts_dir, "example.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env python3\n")
            f.write(f'"""Example script for {name}."""\n\n')
            f.write("# TODO: Implement your script logic here\n")
            f.write(f'print("Hello from {name}")\n')
        os.chmod(script_path, 0o755)
        print(f"Created: {script_path}")

    print()
    print(f"Skill '{name}' initialized at {skill_dir}")
    print()
    print("Next steps:")
    print(f"  1. Edit {skill_md_path} -- fill in the TODO sections")
    print("  2. Write your description using: [What] + [When] + [Capabilities]")
    print("  3. Add specific, actionable instructions in imperative voice")
    print("  4. Test trigger phrases: does Claude activate when expected?")
    print(f"  5. Validate: python ~/.claude/skills/bgskillz/scripts/validate_skill.py {skill_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude skill scaffold.",
        epilog="Example: python init_skill.py my-awesome-skill --path ~/skills",
    )
    parser.add_argument("name", help="Skill name in kebab-case (e.g., 'my-skill')")
    parser.add_argument(
        "--path",
        default=os.path.expanduser("~/.claude/skills"),
        help="Parent directory for the skill (default: ~/.claude/skills)",
    )
    parser.add_argument(
        "--scripts",
        action="store_true",
        help="Include a scripts/ directory with an example script",
    )
    parser.add_argument(
        "--no-references",
        action="store_true",
        help="Skip creating the references/ directory",
    )

    args = parser.parse_args()

    # Validate name
    errors = validate_skill_name(args.name)
    if errors:
        print("Invalid skill name:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    # Expand and normalize path
    path = os.path.abspath(os.path.expanduser(args.path))
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

    init_skill(
        name=args.name,
        path=path,
        include_scripts=args.scripts,
        include_references=not args.no_references,
    )


if __name__ == "__main__":
    main()
