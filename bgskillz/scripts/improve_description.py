#!/usr/bin/env python3
"""Description optimization pipeline.

Generates trigger evaluation queries, tests them, and suggests improvements
to a skill's description for better triggering accuracy.

Usage:
    python improve_description.py /path/to/skill
    python improve_description.py /path/to/skill --queries queries.json
"""

import argparse
import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_skill import parse_frontmatter


def read_skill_description(skill_path: str) -> Tuple[str, str]:
    """Read the skill name and description from SKILL.md.

    Returns (name, description).
    """
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(skill_md):
        print(f"Error: SKILL.md not found at {skill_md}")
        sys.exit(1)

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    fm, _, _ = parse_frontmatter(content)
    if fm is None:
        print("Error: Could not parse frontmatter from SKILL.md")
        sys.exit(1)

    name = fm.get("name", "unknown")
    description = fm.get("description", "")
    return str(name), str(description)


def generate_default_queries(name: str, description: str) -> List[Dict[str, Any]]:
    """Generate a default set of trigger evaluation queries.

    Creates a mix of should-trigger and should-not-trigger queries
    based on the skill name and description.
    """
    queries = []

    # Extract key terms from description for generating queries
    desc_lower = description.lower()

    # Template for should-trigger queries
    trigger_templates = [
        {"query": f"Help me {name.replace('-', ' ')}", "should_trigger": True, "category": "exact"},
        {"query": f"I want to use {name.replace('-', ' ')}", "should_trigger": True, "category": "exact"},
        {"query": f"How do I {name.replace('-', ' ')}?", "should_trigger": True, "category": "paraphrase"},
    ]

    # Template for should-not-trigger queries
    no_trigger_templates = [
        {"query": "Write a hello world program", "should_trigger": False, "category": "unrelated"},
        {"query": "What's the weather like today?", "should_trigger": False, "category": "unrelated"},
        {"query": "Help me debug this error", "should_trigger": False, "category": "adjacent"},
    ]

    for i, t in enumerate(trigger_templates + no_trigger_templates):
        queries.append({
            "id": f"q-{i + 1}",
            "query": t["query"],
            "should_trigger": t["should_trigger"],
            "category": t["category"],
        })

    return queries


def load_queries(queries_path: str) -> List[Dict[str, Any]]:
    """Load trigger evaluation queries from a JSON file.

    Expected format:
    [
        {
            "id": "q-1",
            "query": "Help me create a new skill",
            "should_trigger": true,
            "category": "exact"
        }
    ]
    """
    with open(queries_path, "r", encoding="utf-8") as f:
        queries = json.load(f)

    if not isinstance(queries, list):
        print("Error: queries file must contain a JSON array")
        sys.exit(1)

    for i, q in enumerate(queries):
        if "query" not in q:
            print(f"Error: query {i} missing 'query' field")
            sys.exit(1)
        if "id" not in q:
            q["id"] = f"q-{i + 1}"
        if "should_trigger" not in q:
            print(f"Error: query {i} missing 'should_trigger' field (true/false)")
            sys.exit(1)
        if "category" not in q:
            q["category"] = "unknown"

    return queries


def test_trigger(query: str, skill_path: str, timeout: int = 30) -> bool:
    """Test whether a query triggers the skill.

    Returns True if the skill appears to have triggered.
    This is a heuristic based on checking if the skill's patterns
    appear in the output.
    """
    try:
        # Run with the skill and check if skill-specific content appears
        result = subprocess.run(
            ["claude", "--print"],
            input=query,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def analyze_results(
    name: str,
    description: str,
    queries: List[Dict[str, Any]],
    results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Analyze trigger test results and generate improvement suggestions."""
    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    accuracy = correct / total if total > 0 else 0

    # Categorize failures
    false_negatives = [r for r in results if r["should_trigger"] and not r["triggered"]]
    false_positives = [r for r in results if not r["should_trigger"] and r["triggered"]]

    suggestions = []

    if false_negatives:
        missed_queries = [r["query"] for r in false_negatives]
        suggestions.append({
            "type": "undertriggering",
            "severity": "high" if len(false_negatives) > len(queries) * 0.2 else "medium",
            "description": f"Skill failed to trigger on {len(false_negatives)} queries that should have activated it.",
            "missed_queries": missed_queries,
            "fix": "Add more trigger phrases to the description. Include the verbs and nouns from the missed queries.",
        })

    if false_positives:
        unwanted_queries = [r["query"] for r in false_positives]
        suggestions.append({
            "type": "overtriggering",
            "severity": "high" if len(false_positives) > len(queries) * 0.1 else "medium",
            "description": f"Skill triggered on {len(false_positives)} queries that should NOT have activated it.",
            "unwanted_queries": unwanted_queries,
            "fix": "Add negative trigger patterns to the description. Use 'Do NOT use for...' clauses.",
        })

    # Check description quality
    if len(description) < 50:
        suggestions.append({
            "type": "description_too_short",
            "severity": "high",
            "description": "Description is under 50 characters. Too short for reliable triggering.",
            "fix": "Expand using the formula: [What it does] + [When to use it] + [Key capabilities]",
        })

    if "use when" not in description.lower() and "use for" not in description.lower():
        suggestions.append({
            "type": "missing_trigger_context",
            "severity": "medium",
            "description": "Description lacks a 'Use when...' clause.",
            "fix": "Add explicit trigger context: 'Use when [specific situations].'",
        })

    return {
        "skill_name": name,
        "description": description,
        "total_queries": total,
        "correct": correct,
        "accuracy": round(accuracy, 3),
        "false_negatives": len(false_negatives),
        "false_positives": len(false_positives),
        "suggestions": suggestions,
    }


def run_trigger_eval(
    skill_path: str,
    queries: List[Dict[str, Any]],
    timeout: int = 30,
) -> List[Dict[str, Any]]:
    """Run trigger evaluation for all queries."""
    results = []

    print(f"\nTesting {len(queries)} trigger queries...")
    print("=" * 60)

    for i, q in enumerate(queries):
        query_text = q["query"]
        should_trigger = q["should_trigger"]

        print(f"  [{i + 1}/{len(queries)}] {'SHOULD' if should_trigger else 'SHOULD NOT'} trigger: {query_text[:60]}", end="", flush=True)
        triggered = test_trigger(query_text, skill_path, timeout)
        correct = triggered == should_trigger

        status = "PASS" if correct else "FAIL"
        print(f" -> {status}")

        results.append({
            "id": q["id"],
            "query": query_text,
            "should_trigger": should_trigger,
            "triggered": triggered,
            "correct": correct,
            "category": q.get("category", "unknown"),
        })

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimize a skill's description for better triggering accuracy.",
        epilog="Example: python improve_description.py ~/.claude/skills/my-skill",
    )
    parser.add_argument("skill_path", help="Path to the skill directory")
    parser.add_argument(
        "--queries",
        help="Path to JSON file with trigger evaluation queries. If not provided, default queries are generated.",
    )
    parser.add_argument(
        "--output",
        help="Path to save results JSON (default: <skill>-trigger-eval.json)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout in seconds per query test (default: 30)",
    )
    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Only generate default queries file without running tests",
    )

    args = parser.parse_args()

    skill_path = os.path.abspath(os.path.expanduser(args.skill_path))
    if not os.path.isdir(skill_path):
        print(f"Error: Skill directory not found: {skill_path}")
        sys.exit(1)

    name, description = read_skill_description(skill_path)
    print(f"Skill: {name}")
    print(f"Description: {description[:100]}{'...' if len(description) > 100 else ''}")

    # Load or generate queries
    if args.queries:
        queries = load_queries(args.queries)
    else:
        queries = generate_default_queries(name, description)
        print(f"\nGenerated {len(queries)} default trigger queries.")
        print("For better results, create a custom queries file. See references/schemas.md for format.")

    # Generate-only mode: save queries and exit
    if args.generate_only:
        output_path = args.output or f"{name}-trigger-queries.json"
        with open(output_path, "w") as f:
            json.dump(queries, f, indent=2)
        print(f"\nQueries saved to: {output_path}")
        print("Edit the file to add domain-specific queries, then re-run without --generate-only.")
        return

    # Run trigger evaluation
    results = run_trigger_eval(skill_path, queries, args.timeout)

    # Analyze results
    analysis = analyze_results(name, description, queries, results)

    # Print summary
    print("\n" + "=" * 60)
    print(f"Trigger Accuracy: {analysis['accuracy'] * 100:.1f}%")
    print(f"  Correct: {analysis['correct']}/{analysis['total_queries']}")
    print(f"  False negatives (undertriggering): {analysis['false_negatives']}")
    print(f"  False positives (overtriggering): {analysis['false_positives']}")

    if analysis["suggestions"]:
        print("\nSuggestions:")
        for s in analysis["suggestions"]:
            severity = s["severity"].upper()
            print(f"  [{severity}] {s['description']}")
            print(f"         Fix: {s['fix']}")

    # Save results
    output_path = args.output or f"{name}-trigger-eval.json"
    full_output = {
        "analysis": analysis,
        "results": results,
        "queries": queries,
    }
    with open(output_path, "w") as f:
        json.dump(full_output, f, indent=2)
    print(f"\nFull results saved to: {output_path}")


if __name__ == "__main__":
    main()
