#!/usr/bin/env python3
"""Comprehensive skill validator implementing the full quality checklist."""

import argparse
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

# Compiled once at module level
_REF_PATTERN = re.compile(r'`((?:references|scripts|assets)/[^`]+)`')
_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


class ValidationResult:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.info.append(msg)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def print_report(self) -> None:
        if self.errors:
            print("\nErrors (must fix):")
            for e in self.errors:
                print(f"  [ERROR] {e}")

        if self.warnings:
            print("\nWarnings (should fix):")
            for w in self.warnings:
                print(f"  [WARN]  {w}")

        if self.info:
            print("\nInfo:")
            for i in self.info:
                print(f"  [INFO]  {i}")

        print()
        if self.passed:
            print(f"Result: PASSED ({len(self.warnings)} warnings)")
        else:
            print(f"Result: FAILED ({len(self.errors)} errors, {len(self.warnings)} warnings)")


def validate_skill_name(name: str) -> List[str]:
    """Validate a skill name against all rules. Returns list of error strings.

    This is the canonical name validation used by both init_skill.py and
    validate_skill.py. Keep rules in sync by importing from here.
    """
    errors = []
    if name != name.lower():
        errors.append(f"Name must be lowercase: '{name}' -> '{name.lower()}'")
    if " " in name:
        errors.append("Name must not contain spaces. Use kebab-case: 'my-skill'")
    if "_" in name:
        errors.append(f"Use hyphens, not underscores: '{name}' -> '{name.replace('_', '-')}'")
    # Only fire the generic regex error if no specific formatting errors above
    if not errors and not _NAME_PATTERN.match(name):
        errors.append("Name must start with a letter and contain only lowercase letters, numbers, and hyphens")
    if "claude" in name.lower():
        errors.append("Name must not contain 'claude' (reserved)")
    if "anthropic" in name.lower():
        errors.append("Name must not contain 'anthropic' (reserved)")
    if len(name) > 64:
        errors.append(f"Name is too long ({len(name)} chars). Keep under 64.")
    return errors


def parse_frontmatter(content: str) -> Tuple[Optional[Dict], str, str]:
    """Extract YAML frontmatter, raw frontmatter text, and body from SKILL.md.

    Returns (parsed_dict, raw_frontmatter_text, body).
    Returns (None, "", content) if frontmatter is missing or malformed.
    """
    if not content.startswith("---"):
        return None, "", content

    # Find the closing --- on its own line (not inside a YAML value)
    match = re.search(r'\n---\s*\n', content[3:])
    if not match:
        # Try matching closing --- at end of file
        match = re.search(r'\n---\s*$', content[3:])
        if not match:
            return None, "", content

    fm_start = 3  # skip opening ---
    fm_end = fm_start + match.start()
    fm_text = content[fm_start:fm_end]
    body = content[fm_start + match.end():]

    try:
        fm = yaml.safe_load(fm_text)
        return fm, fm_text, body
    except yaml.YAMLError:
        return None, fm_text, content


def validate_skill(skill_path: str) -> ValidationResult:
    """Run all validation checks on a skill directory."""
    result = ValidationResult()
    skill_path = os.path.expanduser(skill_path)
    skill_path = os.path.abspath(skill_path)

    # Check directory exists
    if not os.path.isdir(skill_path):
        result.error(f"Skill directory not found: {skill_path}")
        return result

    folder_name = os.path.basename(skill_path)

    # --- SKILL.md existence and casing ---
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(skill_md_path):
        result.error("SKILL.md not found in skill directory")
        return result

    # --- No README.md inside skill folder ---
    readme_path = os.path.join(skill_path, "README.md")
    if os.path.isfile(readme_path):
        result.error("README.md found inside skill folder. Remove it — only SKILL.md belongs here. Put README.md in your repo root, outside the skill folder.")

    # --- Read and parse SKILL.md ---
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter, fm_text, body = parse_frontmatter(content)

    if frontmatter is None:
        if content.startswith("---"):
            result.error("Frontmatter YAML is malformed (could not parse)")
        else:
            result.error("SKILL.md must start with YAML frontmatter (--- block)")
        return result

    # --- Frontmatter: no XML tags (check the raw text, covers all fields) ---
    if "<" in fm_text or ">" in fm_text:
        result.error("Frontmatter contains XML tag characters (< or >). Remove all < and > from the YAML block.")

    # --- Frontmatter: name ---
    name = frontmatter.get("name")
    if not name:
        result.error("Frontmatter missing required field: 'name'")
    else:
        name = str(name)
        name_errors = validate_skill_name(name)
        for e in name_errors:
            result.error(e)
        if name != folder_name:
            result.error(f"Name '{name}' does not match folder name '{folder_name}'")

    # --- Frontmatter: description ---
    description = frontmatter.get("description")
    if not description:
        result.error("Frontmatter missing required field: 'description'")
    else:
        description = str(description)
        if len(description) > 1024:
            result.error(f"Description is {len(description)} chars (max 1024)")
        if len(description) < 20:
            result.warn(f"Description is very short ({len(description)} chars). Aim for 100-200 chars with [What] + [When] + [Capabilities].")
        if description.startswith("TODO"):
            result.warn("Description still contains TODO placeholder")

        # Check for trigger context
        desc_lower = description.lower()
        has_trigger_context = any(phrase in desc_lower for phrase in [
            "use when", "use this when", "should be used when", "use for",
            "invoke when", "triggers on", "applies when",
        ])
        if len(description) > 30 and not has_trigger_context:
            result.warn("Description may be missing a 'when to use' clause. Include trigger context like 'Use when...'")

    # --- Body size checks ---
    body_word_count = len(body.split())

    if body_word_count > 5000:
        result.error(f"SKILL.md body is {body_word_count} words (max 5000). Move content to references/.")
    elif body_word_count > 3000:
        result.warn(f"SKILL.md body is {body_word_count} words. Consider moving some content to references/.")

    total_lines = len(content.split("\n"))
    if total_lines > 500:
        result.warn(f"SKILL.md is {total_lines} lines. Aim for under 500 lines; use references/ for depth.")

    # --- Check for backslash paths ---
    if "\\" in body:
        result.warn("SKILL.md contains backslash characters. Use forward slashes for all paths.")

    # --- Check referenced files exist ---
    referenced_files = _REF_PATTERN.findall(content)
    for ref in referenced_files:
        ref_path = os.path.join(skill_path, ref)
        if not os.path.exists(ref_path):
            result.error(f"Referenced file does not exist: {ref}")

    # --- Check subdirectories ---
    for subdir in ["scripts", "references", "assets"]:
        subdir_path = os.path.join(skill_path, subdir)
        if os.path.isdir(subdir_path):
            contents = [c for c in os.listdir(subdir_path) if not c.startswith(".")]
            if not contents:
                result.warn(f"Directory '{subdir}/' exists but is empty. Remove it or add content.")

    # --- Check nesting depth in references ---
    refs_dir = os.path.join(skill_path, "references")
    if os.path.isdir(refs_dir):
        for item in os.listdir(refs_dir):
            item_path = os.path.join(refs_dir, item)
            if os.path.isdir(item_path):
                result.error(f"Nested directory found: references/{item}/. References must be one level deep (no subdirectories).")

    # --- Optional frontmatter fields ---
    if "license" not in frontmatter:
        result.note("No 'license' field in frontmatter. Recommended for distribution.")
    if "metadata" not in frontmatter:
        result.note("No 'metadata' field in frontmatter. Consider adding author and version.")
    elif isinstance(frontmatter.get("metadata"), dict):
        meta = frontmatter["metadata"]
        if "version" not in meta:
            result.note("No 'version' in metadata. Recommended for tracking changes.")

    # --- Summary ---
    result.note(f"SKILL.md: {total_lines} lines, {body_word_count} words")
    if referenced_files:
        result.note(f"References {len(referenced_files)} external files")

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a Claude skill directory against quality rules.",
        epilog="Example: python validate_skill.py ~/.claude/skills/my-skill",
    )
    parser.add_argument("skill_path", help="Path to the skill directory to validate")
    args = parser.parse_args()

    print(f"Validating skill: {args.skill_path}")
    print("=" * 60)

    result = validate_skill(args.skill_path)
    result.print_report()

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
