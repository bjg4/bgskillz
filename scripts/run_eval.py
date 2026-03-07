#!/usr/bin/env python3
"""Automated skill evaluation pipeline.

Runs test prompts with and without a skill, then grades and compares outputs
using the grader and comparator agent instructions.

Usage:
    python run_eval.py /path/to/skill --prompts prompts.json
    python run_eval.py /path/to/skill --prompts prompts.json --iteration 2
"""

import argparse
import json
import math
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional


def load_prompts(prompts_path: str) -> List[Dict[str, Any]]:
    """Load test prompts from a JSON file.

    Expected format:
    [
        {
            "id": "test-1",
            "prompt": "Help me create a new skill for code review",
            "assertions": [
                "Output includes a SKILL.md template",
                "Description follows the [What] + [When] + [Capabilities] formula"
            ]
        }
    ]
    """
    with open(prompts_path, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    if not isinstance(prompts, list):
        print("Error: prompts file must contain a JSON array")
        sys.exit(1)

    for i, p in enumerate(prompts):
        if "prompt" not in p:
            print(f"Error: prompt {i} missing 'prompt' field")
            sys.exit(1)
        if "id" not in p:
            p["id"] = f"test-{i + 1}"
        if "assertions" not in p:
            p["assertions"] = []

    return prompts


def run_claude(prompt: str, skill_path: Optional[str] = None, timeout: int = 120) -> Dict[str, Any]:
    """Run a prompt through Claude Code CLI and capture output.

    Returns dict with output text, timing, and success status.
    """
    cmd = ["claude", "--print"]
    if skill_path:
        cmd.extend(["--skill", skill_path])

    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.time() - start_time
        return {
            "output": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "elapsed_seconds": round(elapsed, 2),
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        return {
            "output": "",
            "stderr": "Timeout expired",
            "exit_code": -1,
            "elapsed_seconds": round(elapsed, 2),
            "success": False,
        }
    except FileNotFoundError:
        return {
            "output": "",
            "stderr": "claude CLI not found. Install Claude Code first.",
            "exit_code": -1,
            "elapsed_seconds": 0,
            "success": False,
        }


def create_workspace(skill_path: str, iteration: int) -> str:
    """Create the workspace directory structure for this evaluation run."""
    skill_name = os.path.basename(os.path.abspath(skill_path))
    workspace = os.path.join(os.getcwd(), f"{skill_name}-workspace")
    iter_dir = os.path.join(workspace, f"iteration-{iteration}")
    os.makedirs(iter_dir, exist_ok=True)
    return iter_dir


def run_evaluation(
    skill_path: str,
    prompts: List[Dict[str, Any]],
    iteration: int,
    timeout: int = 120,
) -> Dict[str, Any]:
    """Run the full evaluation pipeline.

    For each test prompt:
    1. Run with the skill
    2. Run without the skill (baseline)
    3. Save outputs for later grading
    """
    iter_dir = create_workspace(skill_path, iteration)
    results = []

    print(f"\nEvaluation workspace: {iter_dir}")
    print(f"Running {len(prompts)} test prompts (with + without skill each)")
    print("=" * 60)

    for i, test in enumerate(prompts):
        test_id = test["id"]
        prompt_text = test["prompt"]
        eval_dir = os.path.join(iter_dir, f"eval-{test_id}")
        os.makedirs(os.path.join(eval_dir, "with_skill", "outputs"), exist_ok=True)
        os.makedirs(os.path.join(eval_dir, "without_skill", "outputs"), exist_ok=True)

        print(f"\n[{i + 1}/{len(prompts)}] Running: {test_id}")
        print(f"  Prompt: {prompt_text[:80]}{'...' if len(prompt_text) > 80 else ''}")

        # Run with skill
        print("  Running WITH skill...", end="", flush=True)
        with_result = run_claude(prompt_text, skill_path, timeout)
        print(f" done ({with_result['elapsed_seconds']}s)")

        # Save with-skill output
        with open(os.path.join(eval_dir, "with_skill", "outputs", "response.md"), "w") as f:
            f.write(with_result["output"])
        with open(os.path.join(eval_dir, "with_skill", "timing.json"), "w") as f:
            json.dump({
                "elapsed_seconds": with_result["elapsed_seconds"],
                "success": with_result["success"],
            }, f, indent=2)

        # Run without skill (baseline)
        print("  Running WITHOUT skill (baseline)...", end="", flush=True)
        without_result = run_claude(prompt_text, None, timeout)
        print(f" done ({without_result['elapsed_seconds']}s)")

        # Save baseline output
        with open(os.path.join(eval_dir, "without_skill", "outputs", "response.md"), "w") as f:
            f.write(without_result["output"])
        with open(os.path.join(eval_dir, "without_skill", "timing.json"), "w") as f:
            json.dump({
                "elapsed_seconds": without_result["elapsed_seconds"],
                "success": without_result["success"],
            }, f, indent=2)

        test_result = {
            "id": test_id,
            "prompt": prompt_text,
            "assertions": test.get("assertions", []),
            "with_skill": {
                "output_path": os.path.join(eval_dir, "with_skill", "outputs", "response.md"),
                "elapsed_seconds": with_result["elapsed_seconds"],
                "success": with_result["success"],
            },
            "without_skill": {
                "output_path": os.path.join(eval_dir, "without_skill", "outputs", "response.md"),
                "elapsed_seconds": without_result["elapsed_seconds"],
                "success": without_result["success"],
            },
        }
        results.append(test_result)

    # Compute benchmark statistics
    benchmark = compute_benchmark(results, iteration)

    # Save evaluation manifest
    manifest = {
        "skill_path": os.path.abspath(skill_path),
        "iteration": iteration,
        "timestamp": datetime.now().isoformat(),
        "test_count": len(prompts),
        "results": results,
        "benchmark": benchmark,
    }

    manifest_path = os.path.join(iter_dir, "evals.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Save benchmark separately for easy access
    benchmark_path = os.path.join(iter_dir, "benchmark.json")
    with open(benchmark_path, "w") as f:
        json.dump(benchmark, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Evaluation complete. Results saved to: {iter_dir}")
    print(f"Manifest: {manifest_path}")
    print_benchmark_summary(benchmark)
    print()
    print("Next steps:")
    print("  1. Review outputs in the eval directories")
    print("  2. Ask Claude to grade the results using agents/grader.md")
    print("  3. Ask Claude to compare outputs using agents/comparator.md")
    print("  4. Ask Claude to analyze patterns using agents/analyzer.md")
    print("  5. Or open the eval viewer for a visual review")
    print(f"  6. Or run: python generate_review.py {manifest_path}")

    return manifest


def _stats(values: List[float]) -> Dict[str, Any]:
    """Compute mean, stddev, min, max for a list of values."""
    if not values:
        return {"mean": 0, "stddev": 0, "min": 0, "max": 0, "count": 0}
    n = len(values)
    mean = sum(values) / n
    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        stddev = 0
    return {
        "mean": round(mean, 3),
        "stddev": round(stddev, 3),
        "min": round(min(values), 3),
        "max": round(max(values), 3),
        "count": n,
    }


def compute_benchmark(results: List[Dict[str, Any]], iteration: int) -> Dict[str, Any]:
    """Compute aggregate benchmark statistics from evaluation results."""
    with_times = [r["with_skill"]["elapsed_seconds"] for r in results]
    without_times = [r["without_skill"]["elapsed_seconds"] for r in results]
    with_success = sum(1 for r in results if r["with_skill"]["success"])
    without_success = sum(1 for r in results if r["without_skill"]["success"])

    benchmark = {
        "iteration": iteration,
        "timestamp": datetime.now().isoformat(),
        "test_count": len(results),
        "with_skill": {
            "elapsed_seconds": _stats(with_times),
            "success_count": with_success,
            "success_rate": round(with_success / len(results), 3) if results else 0,
        },
        "without_skill": {
            "elapsed_seconds": _stats(without_times),
            "success_count": without_success,
            "success_rate": round(without_success / len(results), 3) if results else 0,
        },
    }

    if with_times and without_times:
        mean_with = sum(with_times) / len(with_times)
        mean_without = sum(without_times) / len(without_times)
        benchmark["delta"] = {
            "time_overhead_seconds": round(mean_with - mean_without, 3),
        }

    return benchmark


def print_benchmark_summary(benchmark: Dict[str, Any]) -> None:
    """Print a human-readable benchmark summary."""
    print("\nBenchmark Summary")
    print("-" * 40)

    ws = benchmark.get("with_skill", {})
    wos = benchmark.get("without_skill", {})

    ws_time = ws.get("elapsed_seconds", {})
    wos_time = wos.get("elapsed_seconds", {})

    if ws_time.get("count"):
        print(f"  With skill:    {ws_time['mean']:.1f}s avg "
              f"(stddev={ws_time['stddev']:.1f}, min={ws_time['min']:.1f}, max={ws_time['max']:.1f}) "
              f"[{ws.get('success_count', 0)}/{ws_time['count']} success]")
    if wos_time.get("count"):
        print(f"  Without skill: {wos_time['mean']:.1f}s avg "
              f"(stddev={wos_time['stddev']:.1f}, min={wos_time['min']:.1f}, max={wos_time['max']:.1f}) "
              f"[{wos.get('success_count', 0)}/{wos_time['count']} success]")

    delta = benchmark.get("delta", {})
    if "time_overhead_seconds" in delta:
        overhead = delta["time_overhead_seconds"]
        sign = "+" if overhead > 0 else ""
        print(f"  Time delta:    {sign}{overhead:.1f}s")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run automated skill evaluation with baseline comparison.",
        epilog="Example: python run_eval.py ~/.claude/skills/my-skill --prompts tests/prompts.json",
    )
    parser.add_argument("skill_path", help="Path to the skill directory to evaluate")
    parser.add_argument(
        "--prompts",
        required=True,
        help="Path to JSON file containing test prompts and assertions",
    )
    parser.add_argument(
        "--iteration",
        type=int,
        default=1,
        help="Iteration number for this eval run (default: 1)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Timeout in seconds per Claude invocation (default: 120)",
    )

    args = parser.parse_args()

    # Validate inputs
    if not os.path.isdir(args.skill_path):
        print(f"Error: Skill directory not found: {args.skill_path}")
        sys.exit(1)

    if not os.path.isfile(args.prompts):
        print(f"Error: Prompts file not found: {args.prompts}")
        sys.exit(1)

    prompts = load_prompts(args.prompts)
    run_evaluation(args.skill_path, prompts, args.iteration, args.timeout)


if __name__ == "__main__":
    main()
