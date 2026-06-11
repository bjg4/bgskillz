#!/usr/bin/env python3
"""Deterministic scoring rubric for skills created during BGSkillz bakeoff.

Produces verifiable JSON scores — no LLM required for structural metrics.
Functional eval scores require separate run_eval + grader pass.

Usage:
    python score_created_skill.py /path/to/skill --brief bakeoff/briefs.json --brief-id code-review
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from validate_skill import parse_frontmatter, validate_skill  # noqa: E402


def estimate_tokens(text: str) -> int:
    """Rough token estimate (~0.75 words per token for English prose)."""
    words = len(text.split())
    return max(1, int(words / 0.75))


def load_brief(briefs_path: str, brief_id: str) -> Dict[str, Any]:
    with open(briefs_path, "r", encoding="utf-8") as f:
        briefs = json.load(f)
    for b in briefs:
        if b["id"] == brief_id:
            return b
    raise ValueError(f"Brief not found: {brief_id}")


def score_compactness(lines: int, tokens: int, max_ideal: int) -> Tuple[float, Dict[str, Any]]:
    """0-20 points for compactness."""
    detail: Dict[str, Any] = {"lines": lines, "tokens": tokens, "max_ideal_lines": max_ideal}
    line_score = 0.0
    if lines <= max_ideal:
        line_score = 10.0
    elif lines <= max_ideal * 1.5:
        line_score = 6.0
    elif lines <= 200:
        line_score = 3.0
    else:
        line_score = 0.0

    token_score = 0.0
    if tokens <= 900:
        token_score = 10.0
    elif tokens <= 1500:
        token_score = 6.0
    elif tokens <= 2500:
        token_score = 3.0
    else:
        token_score = 0.0

    detail["line_score"] = line_score
    detail["token_score"] = token_score
    return line_score + token_score, detail


def score_description(description: str) -> Tuple[float, Dict[str, Any]]:
    """0-20 points for description quality."""
    desc = description or ""
    lower = desc.lower()
    detail: Dict[str, Any] = {"length": len(desc)}
    points = 0.0

    if any(p in lower for p in ["use when", "use for", "should be used when"]):
        points += 5
        detail["has_use_when"] = True
    else:
        detail["has_use_when"] = False

    if any(p in lower for p in ["do not use", "don't use", "not for"]):
        points += 5
        detail["has_negative_trigger"] = True
    else:
        detail["has_negative_trigger"] = False

    if 50 <= len(desc) <= 400:
        points += 5
        detail["length_ok"] = True
    else:
        detail["length_ok"] = False

    if not desc.strip().upper().startswith("TODO"):
        points += 5
        detail["not_todo"] = True
    else:
        detail["not_todo"] = False

    detail["points"] = points
    return points, detail


def score_structure(body: str, preferred_sections: List[str]) -> Tuple[float, Dict[str, Any]]:
    """0-15 points for structure."""
    lower = body.lower()
    detail: Dict[str, Any] = {}
    points = 0.0

    if "quick start" in lower or "## quick" in lower:
        points += 5
        detail["has_quick_start"] = True
    else:
        detail["has_quick_start"] = False

    if any(w in lower for w in ["error", "fail", "missing tool", "when things go wrong"]):
        points += 5
        detail["has_error_handling"] = True
    else:
        detail["has_error_handling"] = False

    you_should = len(re.findall(r"\byou should\b", lower))
    imperatives = len(re.findall(r"\n(?:generate|run|use|create|review|check|write|validate)\b", lower))
    if imperatives >= 3 and you_should <= 2:
        points += 5
        detail["imperative_voice"] = True
    else:
        detail["imperative_voice"] = False
        detail["you_should_count"] = you_should
        detail["imperative_count"] = imperatives

    if preferred_sections:
        found = sum(1 for s in preferred_sections if s.lower() in lower)
        detail["preferred_sections_found"] = found
        detail["preferred_sections_total"] = len(preferred_sections)

    detail["points"] = points
    return points, detail


def score_brief_alignment(
    description: str, body: str, brief: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """0-20 points for brief-specific requirements."""
    combined = (description + " " + body).lower()
    detail: Dict[str, Any] = {}
    points = 0.0

    desc_terms = brief.get("required_description_terms", [])
    body_terms = brief.get("required_body_terms", [])

    desc_hits = sum(1 for t in desc_terms if t.lower() in description.lower())
    body_hits = sum(1 for t in body_terms if t.lower() in body.lower())

    if desc_terms:
        desc_ratio = desc_hits / len(desc_terms)
        points += desc_ratio * 10
        detail["description_term_hits"] = desc_hits
        detail["description_term_total"] = len(desc_terms)

    if body_terms:
        body_ratio = body_hits / len(body_terms)
        points += body_ratio * 10
        detail["body_term_hits"] = body_hits
        detail["body_term_total"] = len(body_terms)

    detail["points"] = round(points, 2)
    return points, detail


def score_two_surface_coherence(description: str, body: str) -> Tuple[float, Dict[str, Any]]:
    """0-10: description promises should appear in body."""
    desc_words = set(re.findall(r"[a-z]{4,}", description.lower()))
    stop = {"when", "this", "that", "with", "from", "should", "skill", "use", "user", "help", "does", "not"}
    desc_words -= stop
    if not desc_words:
        return 5.0, {"note": "no significant description terms"}

    body_lower = body.lower()
    hits = sum(1 for w in desc_words if w in body_lower)
    ratio = hits / len(desc_words)
    points = round(ratio * 10, 2)
    return points, {"desc_terms_checked": len(desc_words), "hits_in_body": hits, "ratio": round(ratio, 3)}


def score_skill(skill_path: str, brief: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Score a created skill directory. Returns verifiable JSON."""
    skill_path = os.path.abspath(os.path.expanduser(skill_path))
    validation = validate_skill(skill_path)

    skill_md = os.path.join(skill_path, "SKILL.md")
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    fm, _, body = parse_frontmatter(content)
    description = str(fm.get("description", "")) if fm else ""
    lines = len(content.splitlines())
    tokens = estimate_tokens(content)
    max_ideal = brief.get("max_ideal_lines", 120) if brief else 120

    validation_points = 20.0 if validation.passed else 0.0
    compact_pts, compact_detail = score_compactness(lines, tokens, max_ideal)
    desc_pts, desc_detail = score_description(description)
    struct_pts, struct_detail = score_structure(body, brief.get("preferred_sections", []) if brief else [])
    brief_pts, brief_detail = (
        score_brief_alignment(description, body, brief) if brief else (0.0, {})
    )
    coherence_pts, coherence_detail = score_two_surface_coherence(description, body)

    total = validation_points + compact_pts + desc_pts + struct_pts + brief_pts + coherence_pts

    return {
        "skill_path": skill_path,
        "total_score": round(total, 2),
        "max_score": 100.0,
        "breakdown": {
            "validation": {"points": validation_points, "passed": validation.passed, "errors": len(validation.errors)},
            "compactness": {"points": round(compact_pts, 2), **compact_detail},
            "description": {"points": round(desc_pts, 2), **desc_detail},
            "structure": {"points": round(struct_pts, 2), **struct_detail},
            "brief_alignment": {"points": round(brief_pts, 2), **brief_detail},
            "two_surface_coherence": {"points": round(coherence_pts, 2), **coherence_detail},
        },
        "metrics": {
            "lines": lines,
            "tokens_estimate": tokens,
            "validation_errors": validation.errors,
            "validation_warnings": validation.warnings,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score a created skill for bakeoff")
    parser.add_argument("skill_path", help="Path to created skill directory")
    parser.add_argument("--brief", help="Path to briefs.json")
    parser.add_argument("--brief-id", help="Brief id for alignment scoring")
    parser.add_argument("--output", "-o", help="Write JSON to file")
    args = parser.parse_args()

    brief = None
    if args.brief and args.brief_id:
        brief = load_brief(args.brief, args.brief_id)

    result = score_skill(args.skill_path, brief)
    out = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Wrote {args.output}")
    else:
        print(out)

    sys.exit(0 if result["breakdown"]["validation"]["passed"] else 1)


if __name__ == "__main__":
    main()
