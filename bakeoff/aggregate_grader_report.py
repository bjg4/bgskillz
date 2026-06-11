#!/usr/bin/env python3
"""Aggregate per-response grading.json files into bakeoff/report-grader.json."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_briefs(path: str) -> Dict[str, Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return {b["id"]: b for b in json.load(f)}


def aggregate(live_dir: str, briefs_path: str, grader: str) -> Dict[str, Any]:
    briefs = load_briefs(briefs_path)
    entries: List[Dict[str, Any]] = []

    for version in ("v4", "v5"):
        version_dir = os.path.join(live_dir, version)
        if not os.path.isdir(version_dir):
            continue
        for brief_id in sorted(os.listdir(version_dir)):
            brief = briefs.get(brief_id)
            if not brief:
                continue
            skill_name = brief["skill_name"]
            grade_path = os.path.join(
                version_dir, brief_id, skill_name, "eval", "grading.json"
            )
            if not os.path.isfile(grade_path):
                continue
            with open(grade_path, "r", encoding="utf-8") as f:
                entry = json.load(f)
            entry["version"] = version
            entry["brief_id"] = brief_id
            grading = entry.get("grading") or {}
            grades = grading.get("grades", [])
            passed = sum(1 for g in grades if g.get("grade") == "PASS")
            entry["pass_rate"] = round(passed / len(grades), 3) if grades else None
            entries.append(entry)

    aggregates: Dict[str, Any] = {}
    for ver in ("v4", "v5"):
        rates = [e["pass_rate"] for e in entries if e.get("version") == ver and e.get("pass_rate") is not None]
        aggregates[ver] = {
            "mean_pass_rate": round(sum(rates) / len(rates), 3) if rates else None,
            "count": len(rates),
        }

    v4_mean = aggregates.get("v4", {}).get("mean_pass_rate")
    v5_mean = aggregates.get("v5", {}).get("mean_pass_rate")
    if v4_mean is not None and v5_mean is not None:
        verdict = "v5_wins" if v5_mean > v4_mean else ("v4_wins" if v4_mean > v5_mean else "tie")
    else:
        verdict = "inconclusive"

    return {
        "timestamp": datetime.now().isoformat(),
        "grader": grader,
        "grader_instructions": os.path.join(os.path.dirname(SCRIPT_DIR), "bgskillz", "agents", "grader.md"),
        "live_dir": os.path.abspath(live_dir),
        "entries": entries,
        "aggregates": aggregates,
        "verdict": verdict,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate agent grader results")
    parser.add_argument("--live-dir", default=os.path.join(SCRIPT_DIR, "live"))
    parser.add_argument("--briefs", default=os.path.join(SCRIPT_DIR, "briefs.json"))
    parser.add_argument("--output", "-o", default=os.path.join(SCRIPT_DIR, "report-grader.json"))
    parser.add_argument("--grader", default="cursor-agent")
    args = parser.parse_args()

    report = aggregate(args.live_dir, args.briefs, args.grader)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    v4 = report["aggregates"].get("v4", {}).get("mean_pass_rate")
    v5 = report["aggregates"].get("v5", {}).get("mean_pass_rate")
    print(f"Grader report: {args.output}")
    print(f"Agent grader: v4={v4} v5={v5} verdict={report['verdict']}")


if __name__ == "__main__":
    main()
