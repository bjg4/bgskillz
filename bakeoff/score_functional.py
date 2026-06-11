#!/usr/bin/env python3
"""Functional proxy scoring for bakeoff created skills.

Simulates whether a skill's instructions would produce outputs passing eval assertions.
Uses deterministic keyword/phrase checks on skill-guided responses.

Usage:
    python score_functional.py /path/to/response.md --brief bakeoff/briefs.json --brief-id code-review
"""

import argparse
import json
import re
import sys
from typing import Any, Dict, List


def load_brief(briefs_path: str, brief_id: str) -> Dict[str, Any]:
    with open(briefs_path, "r", encoding="utf-8") as f:
        for b in json.load(f):
            if b["id"] == brief_id:
                return b
    raise ValueError(f"Brief not found: {brief_id}")


def score_assertion(assertion: str, response: str) -> Dict[str, Any]:
    """Heuristic PASS/FAIL based on assertion content."""
    resp = response.lower()
    a = assertion.lower()

    checks: List[tuple] = []

    if "sql injection" in a:
        checks.append(any(k in resp for k in ["sql injection", "injection", "parameterized", "prepared statement"]))
    if "parameterized" in a or "input validation" in a:
        checks.append(any(k in resp for k in ["parameterized", "prepared statement", "bind", "input validation", "sanitize"]))
    if "severity" in a or "priority" in a:
        checks.append(any(k in resp for k in ["critical", "major", "minor", "severity", "priority", "high", "medium", "low"]))
    if "conventional commit" in a:
        checks.append(any(k in resp for k in ["feat", "fix", "docs", "conventional", "type("]))
    if "72 character" in a or "length" in a:
        checks.append(any(k in resp for k in ["72", "50", "subject", "length", "chars"]))
    if "update code" in a:
        checks.append(not re.search(r"\bupdate code\b|\bfix stuff\b|\bupdate stuff\b", resp))
    if "one focused question" in a or "one question" in a:
        qmarks = resp.count("?")
        numbered_q = len(re.findall(r"^\s*\d+[\.)]", response, re.MULTILINE))
        checks.append(qmarks <= 2 and numbered_q <= 1)
    if "recommended answer" in a:
        checks.append(any(k in resp for k in ["recommend", "suggested", "i'd suggest", "consider", "direction"]))
    if "design decision" in a or "specific" in a:
        checks.append(any(k in resp for k in ["scale", "database", "websocket", "shard", "cache", "auth", "latency", "users"]))

    if not checks:
        # Generic: at least half of significant words from assertion appear
        words = [w for w in re.findall(r"[a-z]{4,}", a) if w not in {"that", "with", "this", "should", "rather", "than"}]
        if words:
            hits = sum(1 for w in words if w in resp)
            passed = hits >= max(1, len(words) // 2)
        else:
            passed = len(resp.strip()) > 50
    else:
        passed = all(checks)

    return {"assertion": assertion, "grade": "PASS" if passed else "FAIL", "checks_run": len(checks)}


def score_functional(response_path: str, brief: Dict[str, Any]) -> Dict[str, Any]:
    with open(response_path, "r", encoding="utf-8") as f:
        response = f.read()

    results = []
    for ep in brief.get("eval_prompts", []):
        for assertion in ep.get("assertions", []):
            results.append(score_assertion(assertion, response))

    passed = sum(1 for r in results if r["grade"] == "PASS")
    total = len(results) or 1
    return {
        "response_path": response_path,
        "assertions": results,
        "pass_rate": round(passed / total, 3),
        "passed": passed,
        "total": total,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score functional eval response")
    parser.add_argument("response_path")
    parser.add_argument("--brief", required=True)
    parser.add_argument("--brief-id", required=True)
    args = parser.parse_args()
    brief = load_brief(args.brief, args.brief_id)
    print(json.dumps(score_functional(args.response_path, brief), indent=2))


if __name__ == "__main__":
    main()
