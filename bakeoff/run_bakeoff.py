#!/usr/bin/env python3
"""BGSkillz v4 vs v5 bakeoff — verifiable comparison of created skill quality.

Phase 1 (create): Agent creates skills from fixed briefs using v4 or v5 BGSkillz guidance.
Phase 2 (score):  Deterministic rubric scoring — reproducible JSON, no LLM required.
Phase 3 (eval):   Optional functional eval via run_eval.py when Claude CLI is available.

Usage:
    # Score fixture skills (demonstrates rubric; v5 should win)
    python run_bakeoff.py --fixtures

    # Score artifact directories from a real bakeoff run
    python run_bakeoff.py --artifacts bakeoff/artifacts

    # Generate creation prompts for manual/agent runs
    python run_bakeoff.py --generate-prompts --output bakeoff/prompts/

Protocol: see bakeoff/PROTOCOL.md
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)


def load_briefs(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def git_info() -> Dict[str, str]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
        return {"commit": commit, "branch": branch}
    except subprocess.CalledProcessError:
        return {"commit": "unknown", "branch": "unknown"}


def score_one(skill_path: str, brief: Dict[str, Any], briefs_path: str) -> Dict[str, Any]:
    scorer = os.path.join(SCRIPT_DIR, "score_created_skill.py")
    result = subprocess.run(
        [
            sys.executable,
            scorer,
            skill_path,
            "--brief",
            briefs_path,
            "--brief-id",
            brief["id"],
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"Scorer failed: {result.stderr}")
    return json.loads(result.stdout)


def compare_versions(
    artifacts_root: str,
    briefs: List[Dict[str, Any]],
    briefs_path: str,
    versions: List[str],
) -> Dict[str, Any]:
    per_brief: List[Dict[str, Any]] = []
    version_totals: Dict[str, List[float]] = {v: [] for v in versions}

    for brief in briefs:
        bid = brief["id"]
        entry: Dict[str, Any] = {"brief_id": bid, "versions": {}}
        best_version = None
        best_score = -1.0

        for ver in versions:
            skill_path = os.path.join(artifacts_root, ver, bid, brief["skill_name"])
            if not os.path.isdir(skill_path):
                entry["versions"][ver] = {"error": f"Missing: {skill_path}"}
                continue
            score = score_one(skill_path, brief, briefs_path)
            entry["versions"][ver] = score
            version_totals[ver].append(score["total_score"])
            if score["total_score"] > best_score:
                best_score = score["total_score"]
                best_version = ver

        entry["winner"] = best_version
        entry["margin"] = None
        if len(versions) == 2 and all(v in entry["versions"] and "total_score" in entry["versions"][v] for v in versions):
            a, b = versions
            entry["margin"] = round(
                entry["versions"][b]["total_score"] - entry["versions"][a]["total_score"], 2
            )
        per_brief.append(entry)

    aggregates = {}
    for ver in versions:
        scores = version_totals[ver]
        if scores:
            aggregates[ver] = {
                "mean_score": round(sum(scores) / len(scores), 2),
                "min_score": round(min(scores), 2),
                "max_score": round(max(scores), 2),
                "briefs_scored": len(scores),
            }
        else:
            aggregates[ver] = {"error": "no scores"}

    wins = {v: 0 for v in versions}
    for entry in per_brief:
        w = entry.get("winner")
        if w in wins:
            wins[w] += 1

    overall_winner = max(wins, key=wins.get) if any(wins.values()) else None

    return {
        "timestamp": datetime.now().isoformat(),
        "git": git_info(),
        "briefs_path": os.path.abspath(briefs_path),
        "artifacts_root": os.path.abspath(artifacts_root),
        "versions": versions,
        "v4_baseline": {
            "path": os.path.join(REPO_ROOT, "versions", "v4"),
            "version": "4.0.0",
        },
        "v5_candidate": {
            "path": REPO_ROOT,
            "version": "5.0.0",
        },
        "per_brief": per_brief,
        "aggregates": aggregates,
        "head_to_head_wins": wins,
        "overall_winner": overall_winner,
        "verdict": _verdict(aggregates, wins, versions),
    }


def _verdict(
    aggregates: Dict[str, Any], wins: Dict[str, int], versions: List[str]
) -> str:
    if len(versions) < 2:
        return "insufficient_versions"
    a, b = versions[0], versions[1]
    if "mean_score" not in aggregates.get(a, {}) or "mean_score" not in aggregates.get(b, {}):
        return "incomplete_data"
    mean_delta = aggregates[b]["mean_score"] - aggregates[a]["mean_score"]
    if mean_delta > 5 and wins.get(b, 0) >= wins.get(a, 0):
        return f"{b}_wins"
    if mean_delta < -5 and wins.get(a, 0) >= wins.get(b, 0):
        return f"{a}_wins"
    return "tie_or_inconclusive"


def install_fixtures(artifacts_root: str) -> None:
    fixtures = os.path.join(SCRIPT_DIR, "fixtures")
    for ver in ("v4", "v5"):
        src = os.path.join(fixtures, ver)
        dst = os.path.join(artifacts_root, ver)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    print(f"Installed fixtures to {artifacts_root}")


def generate_prompts(output_dir: str, briefs: List[Dict[str, Any]]) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for ver in ("v4", "v5"):
        skill_md = os.path.join(REPO_ROOT, "versions", "v4", "SKILL.md") if ver == "v4" else os.path.join(REPO_ROOT, "SKILL.md")
        for brief in briefs:
            prompt = f"""You are creating a new agent skill. Follow the BGSkillz {ver.upper()} instructions below to create the skill.

## Task brief
{brief['creation_brief']}

## Skill name
Folder and frontmatter name: `{brief['skill_name']}`

## Output location
Create the skill at: bakeoff/artifacts/{ver}/{brief['id']}/{brief['skill_name']}/

## Requirements
- Run validate_skill.py before finishing
- Keep SKILL.md focused; use references/ only if needed
- Include a strong description with "Use when" triggers

## BGSkillz instructions
Read and follow: {skill_md}

Create the skill now."""
            path = os.path.join(output_dir, f"{ver}-{brief['id']}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(prompt)
    print(f"Generated {len(briefs) * 2} creation prompts in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="BGSkillz v4 vs v5 bakeoff")
    parser.add_argument(
        "--briefs",
        default=os.path.join(SCRIPT_DIR, "briefs.json"),
        help="Path to briefs.json",
    )
    parser.add_argument(
        "--artifacts",
        default=os.path.join(SCRIPT_DIR, "artifacts"),
        help="Root directory with v4/ and v5/ subdirs",
    )
    parser.add_argument(
        "--fixtures",
        action="store_true",
        help="Copy fixture skills to artifacts and run scoring",
    )
    parser.add_argument(
        "--generate-prompts",
        action="store_true",
        help="Write creation prompts for agent runs",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.path.join(SCRIPT_DIR, "report.json"),
        help="Output report path",
    )
    parser.add_argument(
        "--prompts-dir",
        default=os.path.join(SCRIPT_DIR, "prompts"),
        help="Directory for generated prompts",
    )
    args = parser.parse_args()

    briefs = load_briefs(args.briefs)

    if args.generate_prompts:
        generate_prompts(args.prompts_dir, briefs)

    if args.fixtures:
        install_fixtures(args.artifacts)

    report = compare_versions(args.artifacts, briefs, args.briefs, ["v4", "v5"])

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\nBakeoff report: {args.output}")
    print(f"Verdict: {report['verdict']}")
    for ver, agg in report["aggregates"].items():
        if "mean_score" in agg:
            print(f"  {ver}: mean={agg['mean_score']} ({agg['briefs_scored']} briefs)")
    print(f"  Head-to-head wins: {report['head_to_head_wins']}")


if __name__ == "__main__":
    main()
