#!/usr/bin/env python3
"""Package a skill into a distributable zip with validation gate."""

import argparse
import os
import sys
import zipfile
from typing import Optional

# Allow importing validate_skill from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_skill import validate_skill


EXCLUDED_DIRS = {".git", "__pycache__", "node_modules", ".env", ".venv"}
EXCLUDED_FILES = {".DS_Store", "Thumbs.db"}


def should_exclude(name: str) -> bool:
    """Check if a file or directory name should be excluded from the package."""
    if name in EXCLUDED_DIRS or name in EXCLUDED_FILES:
        return True
    if name.endswith(".pyc"):
        return True
    return False


def package_skill(skill_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """Validate and package a skill into a zip file.

    Returns the path to the zip file, or None if validation failed.
    """
    skill_path = os.path.expanduser(skill_path)
    skill_path = os.path.abspath(skill_path)
    skill_name = os.path.basename(skill_path)

    # Run validation first
    print(f"Validating skill: {skill_path}")
    print("=" * 60)
    result = validate_skill(skill_path)
    result.print_report()

    if not result.passed:
        print("\nPackaging aborted: fix validation errors first.")
        return None

    # Determine output path
    if output_path is None:
        output_path = os.path.join(os.path.dirname(skill_path), f"{skill_name}.zip")
    output_path = os.path.expanduser(output_path)

    # Create zip
    print(f"\nPackaging to: {output_path}")
    file_count = 0
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path, followlinks=False):
            # Filter directories in-place to prevent walking into excluded dirs
            dirs[:] = [d for d in dirs if not should_exclude(d)]

            for filename in files:
                if should_exclude(filename):
                    continue

                filepath = os.path.join(root, filename)
                if os.path.islink(filepath):
                    continue

                arcname = os.path.relpath(filepath, os.path.dirname(skill_path))
                zf.write(filepath, arcname)
                file_count += 1

    if file_count == 0:
        os.remove(output_path)
        print("\nError: No files to package (all files were excluded).")
        return None

    # Report size
    zip_size = os.path.getsize(output_path)
    if zip_size < 1024 * 1024:
        size_str = f"{zip_size / 1024:.1f} KB"
    else:
        size_str = f"{zip_size / (1024 * 1024):.1f} MB"

    print(f"\nPackaged {file_count} files ({size_str})")

    if zip_size > 1024 * 1024:
        print("Warning: Package is over 1MB. Consider reducing size for faster uploads.")

    print(f"Output: {output_path}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and package a Claude skill into a distributable zip.",
        epilog="Example: python package_skill.py ~/.claude/skills/my-skill",
    )
    parser.add_argument("skill_path", help="Path to the skill directory to package")
    parser.add_argument("output", nargs="?", default=None, help="Output zip path (default: <skill-name>.zip)")
    args = parser.parse_args()

    result = package_skill(args.skill_path, args.output)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
