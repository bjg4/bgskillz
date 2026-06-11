#!/usr/bin/env python3
"""Grade bakeoff eval outputs using Codex CLI + grader agent instructions.

Uses `codex exec` in read-only mode with agents/grader.md. Falls back to
OPENAI_API_KEY or saved Codex login auth.

Usage:
    python grade_with_codex.py --live-dir bakeoff/live --briefs bakeoff/briefs.json
    python grade_with_codex.py --response path/to/response.md --brief-id code-review --version v5
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRADER_PATH = os.path.join(REPO_ROOT, "bgskillz", "agents", "grader.md")


def load_grader_instructions() -> str:
    with open(GRADER_PATH, "r", encoding="utf-8") as f:
        return f.read()


def load_briefs(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_brief(briefs: List[Dict[str, Any]], brief_id: str) -> Dict[str, Any]:
    for b in briefs:
        if b["id"] == brief_id:
            return b
    raise ValueError(f"Brief not found: {brief_id}")


def build_grading_prompt(test_prompt: str, output_text: str, assertions: List[str]) -> str:
    grader = load_grader_instructions()
    assertions_text = "\n".join(f"- {a}" for a in assertions)
    return f"""{grader}

---

**Test Prompt:**
{test_prompt}

**Output to Grade:**
{output_text[:8000]}

**Assertions:**
{assertions_text}

Grade each assertion with binary PASS or FAIL. Produce ONLY valid JSON matching the grader output format. No markdown fences."""


def parse_grader_json(text: str) -> Optional[Dict[str, Any]]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}") + 1
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(text[start:end])
    except json.JSONDecodeError:
        return None


def run_codex_exec(prompt: str, timeout: int = 180) -> Dict[str, Any]:
    """Run codex exec in read-only sandbox; return stdout and metadata."""
    codex_bin = os.environ.get("CODEX_BIN", "codex")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        out_path = tmp.name

    cmd = [
        codex_bin,
        "exec",
        "--sandbox",
        "read-only",
        "--ephemeral",
        "-o",
        out_path,
        prompt,
    ]

    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=REPO_ROOT,
        )
        elapsed = round(time.time() - start, 2)
        stdout = result.stdout
        if os.path.isfile(out_path):
            with open(out_path, "r", encoding="utf-8") as f:
                last = f.read()
            if last.strip():
                stdout = last
        return {
            "output": stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "elapsed_seconds": elapsed,
            "success": result.returncode == 0,
            "backend": "codex",
        }
    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "stderr": "Timeout",
            "exit_code": -1,
            "elapsed_seconds": timeout,
            "success": False,
            "backend": "codex",
        }
    except FileNotFoundError:
        return {
            "output": "",
            "stderr": f"{codex_bin} not found. Install: npm install -g @openai/codex",
            "exit_code": -1,
            "elapsed_seconds": 0,
            "success": False,
            "backend": "codex",
        }
    finally:
        if os.path.isfile(out_path):
            os.unlink(out_path)


def grade_response(
    response_path: str,
    brief: Dict[str, Any],
    timeout: int = 180,
) -> Dict[str, Any]:
    with open(response_path, "r", encoding="utf-8") as f:
        output_text = f.read()

    eval_prompts = brief.get("eval_prompts", [])
    if not eval_prompts:
        return {"error": "no eval_prompts in brief"}

    ep = eval_prompts[0]
    prompt = build_grading_prompt(ep["prompt"], output_text, ep.get("assertions", []))
    result = run_codex_exec(prompt, timeout=timeout)
    parsed = parse_grader_json(result["output"]) if result["output"] else None

    return {
        "response_path": response_path,
        "brief_id": brief["id"],
        "backend": result["backend"],
        "elapsed_seconds": result["elapsed_seconds"],
        "success": result["success"] and parsed is not None,
        "stderr": result["stderr"][:500] if result["stderr"] else None,
        "grading": parsed,
        "raw_output": result["output"][:2000] if not parsed else None,
    }


def grade_live_tree(live_dir: str, briefs_path: str, timeout: int = 180) -> Dict[str, Any]:
    briefs = load_briefs(briefs_path)
    brief_by_id = {b["id"]: b for b in briefs}
    results: Dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "grader": "codex-exec",
        "grader_instructions": GRADER_PATH,
        "live_dir": os.path.abspath(live_dir),
        "entries": [],
    }

    for version in ("v4", "v5"):
        version_dir = os.path.join(live_dir, version)
        if not os.path.isdir(version_dir):
            continue
        for brief_id in os.listdir(version_dir):
            brief = brief_by_id.get(brief_id)
            if not brief:
                continue
            skill_name = brief["skill_name"]
            resp_path = os.path.join(version_dir, brief_id, skill_name, "eval", "response.md")
            if not os.path.isfile(resp_path):
                continue

            print(f"Grading {version}/{brief_id}...", flush=True)
            entry = grade_response(resp_path, brief, timeout=timeout)
            entry["version"] = version
            entry["brief_id"] = brief_id

            grade_path = os.path.join(
                version_dir, brief_id, skill_name, "eval", "grading.json"
            )
            with open(grade_path, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2)

            if entry.get("grading"):
                grades = entry["grading"].get("grades", [])
                passed = sum(1 for g in grades if g.get("grade") == "PASS")
                entry["pass_rate"] = round(passed / len(grades), 3) if grades else 0.0
            else:
                entry["pass_rate"] = None

            results["entries"].append(entry)
            status = "OK" if entry.get("success") else "FAIL"
            print(f"  {status} pass_rate={entry.get('pass_rate')}", flush=True)

    # Aggregate by version
    for ver in ("v4", "v5"):
        rates = [e["pass_rate"] for e in results["entries"] if e.get("version") == ver and e.get("pass_rate") is not None]
        results.setdefault("aggregates", {})[ver] = {
            "mean_pass_rate": round(sum(rates) / len(rates), 3) if rates else None,
            "count": len(rates),
        }

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Grade bakeoff outputs with Codex CLI grader")
    parser.add_argument("--live-dir", default=os.path.join(REPO_ROOT, "bakeoff", "live"))
    parser.add_argument("--briefs", default=os.path.join(REPO_ROOT, "bakeoff", "briefs.json"))
    parser.add_argument("--output", "-o", default=os.path.join(REPO_ROOT, "bakeoff", "report-grader.json"))
    parser.add_argument("--response", help="Grade single response file")
    parser.add_argument("--brief-id", help="Brief id for single response")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    if args.response:
        if not args.brief_id:
            print("Error: --brief-id required with --response")
            sys.exit(1)
        brief = find_brief(load_briefs(args.briefs), args.brief_id)
        result = grade_response(args.response, brief, timeout=args.timeout)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("success") else 1)

    report = grade_live_tree(args.live_dir, args.briefs, timeout=args.timeout)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\nGrader report: {args.output}")

    v4 = report.get("aggregates", {}).get("v4", {}).get("mean_pass_rate")
    v5 = report.get("aggregates", {}).get("v5", {}).get("mean_pass_rate")
    if v4 is not None and v5 is not None:
        winner = "v5" if v5 > v4 else ("v4" if v4 > v5 else "tie")
        print(f"Codex grader: v4={v4} v5={v5} winner={winner}")

    any_success = any(e.get("success") for e in report.get("entries", []))
    sys.exit(0 if any_success else 1)


if __name__ == "__main__":
    main()
