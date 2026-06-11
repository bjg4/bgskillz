#!/usr/bin/env python3
"""Run live bakeoff: structural scores + functional proxy on agent-created skills."""

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


def main() -> None:
    artifacts = os.path.join(SCRIPT_DIR, "artifacts")
    briefs_path = os.path.join(SCRIPT_DIR, "briefs.json")
    with open(briefs_path, "r", encoding="utf-8") as f:
        briefs = json.load(f)

    structural_path = os.path.join(SCRIPT_DIR, "report-live.json")
    report = run_bakeoff_report(artifacts, structural_path)

    functional: Dict[str, Any] = {"v4": {}, "v5": {}}
    for brief in briefs:
        bid = brief["id"]
        skill_name = brief["skill_name"]
        for ver in ("v4", "v5"):
            eval_dir = os.path.join(artifacts, ver, bid, skill_name, "eval")
            resp_path = os.path.join(eval_dir, "response.md")
            if os.path.isfile(resp_path):
                result = subprocess.run(
                    [sys.executable, os.path.join(SCRIPT_DIR, "score_functional.py"),
                     resp_path, "--brief", briefs_path, "--brief-id", bid],
                    capture_output=True, text=True, check=True,
                )
                functional[ver][bid] = json.loads(result.stdout)

    # Aggregate functional pass rates
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
    report["timestamp"] = datetime.now().isoformat()

    with open(structural_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps({
        "report": structural_path,
        "structural_verdict": report.get("verdict"),
        "functional_verdict": report.get("functional_verdict"),
        "v4_structural_mean": report["aggregates"]["v4"].get("mean_score"),
        "v5_structural_mean": report["aggregates"]["v5"].get("mean_score"),
        "v4_functional_mean": report.get("functional_proxy", {}).get("v4", {}).get("mean_pass_rate"),
        "v5_functional_mean": report.get("functional_proxy", {}).get("v5", {}).get("mean_pass_rate"),
    }, indent=2))


if __name__ == "__main__":
    main()
