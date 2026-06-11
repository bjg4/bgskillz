#!/usr/bin/env python3
"""Aggregate benchmark results across evaluation iterations.

Reads benchmark.json from each iteration-* directory in a workspace and
produces cross-iteration trend analysis.

Usage:
    python aggregate_benchmark.py /path/to/workspace
    python aggregate_benchmark.py /path/to/workspace --output trends.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional


def find_iterations(workspace: str) -> List[str]:
    """Find iteration directories sorted by number."""
    iterations = []
    if not os.path.isdir(workspace):
        return iterations

    for name in os.listdir(workspace):
        if name.startswith("iteration-"):
            path = os.path.join(workspace, name)
            if os.path.isdir(path):
                try:
                    num = int(name.split("-", 1)[1])
                    iterations.append((num, path))
                except ValueError:
                    continue

    iterations.sort(key=lambda x: x[0])
    return [path for _, path in iterations]


def load_benchmark(iter_dir: str) -> Optional[Dict[str, Any]]:
    """Load benchmark.json from an iteration directory."""
    path = os.path.join(iter_dir, "benchmark.json")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_trends(iterations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute trend metrics across iterations."""
    if not iterations:
        return {}

    first = iterations[0]
    last = iterations[-1]

    def delta(field: str, section: str) -> Optional[float]:
        a = first.get(section, {}).get(field)
        b = last.get(section, {}).get(field)
        if a is not None and b is not None:
            return round(b - a, 4)
        return None

    score_trend = []
    timing_trend = []
    for it in iterations:
        ws = it.get("with_skill", {})
        score_trend.append(ws.get("mean_score"))
        timing_trend.append(ws.get("mean_elapsed_seconds"))

    # Detect regression: last iteration worse than best
    scores = [s for s in score_trend if s is not None]
    best_score = max(scores) if scores else None
    last_score = score_trend[-1] if score_trend else None
    regression = (
        best_score is not None
        and last_score is not None
        and last_score < best_score - 0.05
    )

    return {
        "iteration_count": len(iterations),
        "first_iteration": first.get("iteration"),
        "last_iteration": last.get("iteration"),
        "score_trend": score_trend,
        "timing_trend_seconds": timing_trend,
        "delta": {
            "score_improvement": delta("mean_score", "with_skill"),
            "time_overhead_seconds": delta("mean_elapsed_seconds", "with_skill"),
            "baseline_score_change": delta("mean_score", "without_skill"),
        },
        "best_score": best_score,
        "last_score": last_score,
        "possible_regression": regression,
        "regression_note": (
            "Last iteration score is >5% below best iteration — check for overfitting"
            if regression
            else None
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate benchmark results across eval iterations"
    )
    parser.add_argument("workspace", help="Path to eval workspace directory")
    parser.add_argument(
        "--output",
        "-o",
        help="Write aggregate JSON to this path (default: workspace/aggregate.json)",
    )
    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)
    iter_dirs = find_iterations(workspace)

    if not iter_dirs:
        print(f"No iteration-* directories found in {workspace}")
        sys.exit(1)

    iterations = []
    for iter_dir in iter_dirs:
        benchmark = load_benchmark(iter_dir)
        if benchmark:
            benchmark["_dir"] = os.path.basename(iter_dir)
            iterations.append(benchmark)
        else:
            print(f"Warning: no benchmark.json in {iter_dir}")

    if not iterations:
        print("No benchmark.json files found")
        sys.exit(1)

    trends = compute_trends(iterations)
    aggregate = {
        "workspace": workspace,
        "timestamp": datetime.now().isoformat(),
        "iterations": iterations,
        "trends": trends,
    }

    output_path = args.output or os.path.join(workspace, "aggregate.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(aggregate, f, indent=2)

    print(f"Aggregated {len(iterations)} iterations → {output_path}")
    if trends.get("delta", {}).get("score_improvement") is not None:
        delta = trends["delta"]["score_improvement"]
        direction = "↑" if delta > 0 else "↓" if delta < 0 else "→"
        print(f"  Score change (first→last): {direction} {abs(delta):.2%}")
    if trends.get("possible_regression"):
        print(f"  ⚠ {trends['regression_note']}")


if __name__ == "__main__":
    main()
