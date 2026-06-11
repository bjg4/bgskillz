#!/usr/bin/env python3
"""Run live bakeoff: structural scores + agent grader (or functional proxy fallback)."""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)


def run_bakeoff_report(artifacts: str, output: str) -> Dict[str, Any]:
    subprocess.run(
        [sys.executable, os.path.join(SCRIPT_DIR, "run_bakeoff.py"),
         "--artifacts", artifacts, "--output", output],
        check=True,
    )
    with open(output, "r", encoding="utf-8") as f:
        return json.load(f)


def has_agent_grades(live_dir: str, briefs: List[Dict[str, Any]]) -> bool:
    for brief in briefs:
        skill_name = brief["skill_name"]
        for ver in ("v4", "v5"):
            grade_path = os.path.join(
                live_dir, ver, brief["id"], skill_name, "eval", "grading.json"
            )
            if os.path.isfile(grade_path):
                return True
    return False


def score_functional_proxy(
    artifacts: str, briefs: List[Dict[str, Any]], briefs_path: str
) -> Dict[str, Any]:
    functional: Dict[str, Any] = {"v4": {}, "v5": {}}
    for brief in briefs:
        bid = brief["id"]
        skill_name = brief["skill_name"]
        for ver in ("v4", "v5"):
            resp_path = os.path.join(artifacts, ver, bid, skill_name, "eval", "response.md")
            if os.path.isfile(resp_path):
                result = subprocess.run(
                    [sys.executable, os.path.join(SCRIPT_DIR, "score_functional.py"),
                     resp_path, "--brief", briefs_path, "--brief-id", bid],
                    capture_output=True, text=True, check=True,
                )
                functional[ver][bid] = json.loads(result.stdout)
    return functional


def main() -> None:
    parser = argparse.ArgumentParser(description="Run live bakeoff report")
    parser.add_argument(
        "--artifacts",
        default=os.path.join(SCRIPT_DIR, "live"),
        help="Directory with v4/v5 created skills (default: bakeoff/live)",
    )
    args = parser.parse_args()

    artifacts = args.artifacts
    briefs_path = os.path.join(SCRIPT_DIR, "briefs.json")
    with open(briefs_path, "r", encoding="utf-8") as f:
        briefs = json.load(f)

    structural_path = os.path.join(SCRIPT_DIR, "report-live.json")
    report = run_bakeoff_report(artifacts, structural_path)

    grader_path = os.path.join(SCRIPT_DIR, "report-grader.json")
    if has_agent_grades(artifacts, briefs):
        subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "aggregate_grader_report.py"),
             "--live-dir", artifacts, "--briefs", briefs_path, "-o", grader_path],
            check=True,
        )
        with open(grader_path, "r", encoding="utf-8") as f:
            grader_report = json.load(f)
        report["agent_grader"] = grader_report.get("aggregates", {})
        report["agent_grader_verdict"] = grader_report.get("verdict")
        report["agent_grader_entries"] = grader_report.get("entries", [])
    else:
        functional = score_functional_proxy(artifacts, briefs, briefs_path)
        for ver in ("v4", "v5"):
            rates = [v["pass_rate"] for v in functional[ver].values()]
            report["functional_proxy"] = report.get("functional_proxy", {})
            report["functional_proxy"][ver] = {
                "per_brief": functional[ver],
                "mean_pass_rate": round(sum(rates) / len(rates), 3) if rates else None,
            }
        if functional.get("v4") and functional.get("v5"):
            v4_mean = report["functional_proxy"]["v4"]["mean_pass_rate"] or 0
            v5_mean = report["functional_proxy"]["v5"]["mean_pass_rate"] or 0
            report["functional_verdict"] = "v5_wins" if v5_mean > v4_mean else (
                "v4_wins" if v4_mean > v5_mean else "tie"
            )

    report["bakeoff_type"] = "live"
    report["artifacts_root"] = os.path.abspath(artifacts)
    report["timestamp"] = datetime.now().isoformat()

    with open(structural_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    summary: Dict[str, Any] = {
        "report": structural_path,
        "structural_verdict": report.get("verdict"),
        "v4_structural_mean": report["aggregates"]["v4"].get("mean_score"),
        "v5_structural_mean": report["aggregates"]["v5"].get("mean_score"),
    }
    if report.get("agent_grader_verdict"):
        summary["agent_grader_verdict"] = report["agent_grader_verdict"]
        summary["v4_agent_grader_mean"] = report.get("agent_grader", {}).get("v4", {}).get("mean_pass_rate")
        summary["v5_agent_grader_mean"] = report.get("agent_grader", {}).get("v5", {}).get("mean_pass_rate")
    else:
        summary["functional_verdict"] = report.get("functional_verdict")
        summary["v4_functional_mean"] = report.get("functional_proxy", {}).get("v4", {}).get("mean_pass_rate")
        summary["v5_functional_mean"] = report.get("functional_proxy", {}).get("v5", {}).get("mean_pass_rate")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
