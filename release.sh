#!/usr/bin/env bash
# Validate and package BGSkillz for distribution.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$ROOT/bgskillz"
OUT_DIR="$ROOT/dist"
VERSION="$(grep -m1 'version:' "$SKILL_DIR/SKILL.md" | sed 's/.*"\(.*\)".*/\1/')"
ZIP="$OUT_DIR/bgskillz-${VERSION}.zip"

mkdir -p "$OUT_DIR"
python3 "$SKILL_DIR/scripts/validate_skill.py" "$SKILL_DIR"
python3 "$SKILL_DIR/scripts/package_skill.py" "$SKILL_DIR" "$ZIP"
echo "Release artifact: $ZIP"
