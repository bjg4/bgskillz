#!/usr/bin/env python3
"""Automated improvement loop: eval -> grade -> analyze -> improve -> re-eval.

Runs multiple iterations of the evaluation pipeline, using Claude to analyze
results and suggest improvements between each iteration.

Usage:
    python run_loop.py /path/to/skill --prompts prompts.json --iterations 3
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_eval import load_prompts, run_claude, create_workspace, run_evaluation


def load_agent_instructions(agent_name: str) -> str:
    """Load agent instructions from the agents/ directory."""
    agents_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "agents",
    )
    agent_path = os.path.join(agents_dir, f"{agent_name}.md")
    if not os.path.isfile(agent_path):
        print(f"Warning: Agent file not found: {agent_path}")
        return ""
    with open(agent_path, "r", encoding="utf-8") as f:
        return f.read()


def grade_outputs(iter_dir: str, manifest: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
    """Grade all outputs in an iteration using the grader agent."""
    grader_instructions = load_agent_instructions("grader")
    if not grader_instructions:
        return {"error": "Grader agent not found"}

    grading_results = {}

    for result in manifest.get("results", []):
        test_id = result["id"]
        prompt_text = result["prompt"]
        assertions = result.get("assertions", [])

        if not assertions:
            continue

        for label in ["with_skill", "without_skill"]:
            output_path = result[label].get("output_path", "")
            if not os.path.isfile(output_path):
                continue

            with open(output_path, "r") as f:
                output_text = f.read()

            assertions_text = "\n".join(f"- {a}" for a in assertions)
            grading_prompt = f"""{grader_instructions}

---

**Test Prompt:** {prompt_text}

**Output to Grade:**
{output_text[:4000]}

**Assertions:**
{assertions_text}

Grade each assertion and produce the JSON output as specified."""

            print(f"  Grading {test_id} ({label})...", end="", flush=True)
            grade_result = run_claude(grading_prompt, timeout=timeout)
            print(" done")

            # Try to parse JSON from output
            parsed = None
            if grade_result["success"]:
                try:
                    text = grade_result["output"]
                    json_start = text.find("{")
                    json_end = text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        parsed = json.loads(text[json_start:json_end])
                except json.JSONDecodeError:
                    pass

            key = f"{test_id}_{label}"
            grading_results[key] = parsed or {"raw_output": grade_result["output"][:2000]}

    # Save grading results
    grading_path = os.path.join(iter_dir, "grading.json")
    with open(grading_path, "w") as f:
        json.dump(grading_results, f, indent=2)

    return grading_results


def analyze_results(iter_dir: str, manifest: Dict[str, Any],
                    grading_results: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
    """Run the analyzer agent on grading results to get improvement suggestions."""
    analyzer_instructions = load_agent_instructions("analyzer")
    if not analyzer_instructions:
        return {"error": "Analyzer agent not found"}

    skill_path = manifest.get("skill_path", "")
    skill_name = os.path.basename(skill_path)

    # Read current SKILL.md for context
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    skill_content = ""
    if os.path.isfile(skill_md_path):
        with open(skill_md_path, "r") as f:
            skill_content = f.read()[:3000]

    # Build analysis prompt
    grading_summary = json.dumps(grading_results, indent=2)[:4000]

    analysis_prompt = f"""{analyzer_instructions}

---

**Skill Name:** {skill_name}
**Skill Content (truncated):**
{skill_content}

**Grading Results:**
{grading_summary}

Analyze the patterns and produce the JSON output as specified."""

    print("  Running analyzer...", end="", flush=True)
    analysis_result = run_claude(analysis_prompt, timeout=timeout)
    print(" done")

    parsed = None
    if analysis_result["success"]:
        try:
            text = analysis_result["output"]
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                parsed = json.loads(text[json_start:json_end])
        except json.JSONDecodeError:
            pass

    analysis = parsed or {"raw_output": analysis_result["output"][:2000]}

    # Save analysis
    analysis_path = os.path.join(iter_dir, "analysis.json")
    with open(analysis_path, "w") as f:
        json.dump(analysis, f, indent=2)

    return analysis


def apply_suggestions(skill_path: str, analysis: Dict[str, Any],
                      iteration: int, timeout: int = 120) -> bool:
    """Use Claude to apply improvement suggestions to the skill.

    Returns True if changes were made.
    """
    suggestions = analysis.get("suggestions", [])
    if not suggestions:
        print("  No improvement suggestions to apply.")
        return False

    # Read current SKILL.md
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    with open(skill_md_path, "r") as f:
        current_content = f.read()

    # Build improvement prompt
    suggestions_text = json.dumps(suggestions, indent=2)

    improve_prompt = f"""You are improving a Claude skill based on evaluation feedback.

Here is the current SKILL.md:

```markdown
{current_content}
```

Here are the improvement suggestions from the analyzer (ordered by priority):

{suggestions_text}

Apply the suggestions that have priority P0 or P1. Skip P2 suggestions.

Important rules:
- Keep the frontmatter (name, description) unchanged unless a suggestion specifically targets it
- Maintain the existing structure and formatting style
- Do not add instructions that would overfit to specific test cases
- Explain reasoning in the instructions rather than adding rigid rules
- Keep SKILL.md under 500 lines

Output ONLY the complete updated SKILL.md content, nothing else."""

    print("  Applying improvements...", end="", flush=True)
    result = run_claude(improve_prompt, timeout=timeout)
    print(" done")

    if not result["success"] or not result["output"].strip():
        print("  Warning: Failed to generate improvements.")
        return False

    new_content = result["output"].strip()

    # Basic sanity checks
    if "---" not in new_content:
        print("  Warning: Generated content missing frontmatter. Skipping.")
        return False

    if len(new_content) < len(current_content) * 0.5:
        print("  Warning: Generated content is suspiciously short. Skipping.")
        return False

    # Backup and write
    backup_path = os.path.join(skill_path, f"SKILL.md.backup-iter{iteration}")
    with open(backup_path, "w") as f:
        f.write(current_content)

    with open(skill_md_path, "w") as f:
        f.write(new_content)

    print(f"  SKILL.md updated. Backup saved to {backup_path}")
    return True


def run_loop(
    skill_path: str,
    prompts_path: str,
    max_iterations: int = 3,
    timeout: int = 120,
    auto_apply: bool = False,
) -> None:
    """Run the full improvement loop.

    For each iteration:
    1. Run evaluation (with/without skill)
    2. Grade outputs against assertions
    3. Analyze patterns and generate suggestions
    4. Optionally apply suggestions to SKILL.md
    5. Repeat
    """
    skill_path = os.path.abspath(os.path.expanduser(skill_path))
    prompts = load_prompts(prompts_path)

    print(f"Starting improvement loop for: {os.path.basename(skill_path)}")
    print(f"Max iterations: {max_iterations}")
    print(f"Auto-apply: {auto_apply}")
    print(f"Test prompts: {len(prompts)}")

    for iteration in range(1, max_iterations + 1):
        print(f"\n{'=' * 60}")
        print(f"ITERATION {iteration}/{max_iterations}")
        print(f"{'=' * 60}")

        # Step 1: Run evaluation
        print("\n[Step 1] Running evaluation...")
        manifest = run_evaluation(skill_path, prompts, iteration, timeout)

        # Step 2: Grade outputs
        print("\n[Step 2] Grading outputs...")
        iter_dir = os.path.join(
            os.getcwd(),
            f"{os.path.basename(skill_path)}-workspace",
            f"iteration-{iteration}",
        )
        grading_results = grade_outputs(iter_dir, manifest, timeout)

        # Step 3: Analyze and suggest improvements
        print("\n[Step 3] Analyzing results...")
        analysis = analyze_results(iter_dir, manifest, grading_results, timeout)

        # Print summary
        suggestions = analysis.get("suggestions", [])
        if suggestions:
            print(f"\n  Found {len(suggestions)} improvement suggestions:")
            for s in suggestions:
                priority = s.get("priority", "?")
                action = s.get("action", "?")
                rationale = s.get("rationale", "no rationale")[:80]
                print(f"    [{priority}] {action}: {rationale}")
        else:
            print("\n  No improvement suggestions. Skill may be converged.")

        assessment = analysis.get("overall_assessment", "")
        if assessment:
            print(f"\n  Assessment: {assessment[:200]}")

        # Step 4: Apply improvements (if auto_apply or last iteration)
        if iteration < max_iterations:
            if auto_apply:
                print("\n[Step 4] Applying improvements...")
                changed = apply_suggestions(skill_path, analysis, iteration, timeout)
                if not changed:
                    print("  No changes applied. Stopping loop early.")
                    break
            else:
                print(f"\n[Step 4] Skipped (auto-apply disabled).")
                print(f"  Review suggestions in: {os.path.join(iter_dir, 'analysis.json')}")
                print(f"  To apply manually, review and edit SKILL.md, then re-run with --iteration {iteration + 1}")
                break

    # Final summary
    print(f"\n{'=' * 60}")
    print("LOOP COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Iterations run: {iteration}")
    workspace = os.path.join(os.getcwd(), f"{os.path.basename(skill_path)}-workspace")
    print(f"  Workspace: {workspace}")
    print(f"  Review results with: eval-viewer/viewer.html")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run automated eval->analyze->improve loop for a skill.",
        epilog="Example: python run_loop.py ~/.claude/skills/my-skill --prompts tests/prompts.json --iterations 3 --auto-apply",
    )
    parser.add_argument("skill_path", help="Path to the skill directory")
    parser.add_argument(
        "--prompts", required=True,
        help="Path to JSON file with test prompts and assertions",
    )
    parser.add_argument(
        "--iterations", type=int, default=3,
        help="Maximum number of improvement iterations (default: 3)",
    )
    parser.add_argument(
        "--timeout", type=int, default=120,
        help="Timeout per Claude invocation in seconds (default: 120)",
    )
    parser.add_argument(
        "--auto-apply", action="store_true",
        help="Automatically apply improvement suggestions between iterations. "
             "Without this flag, the loop runs one iteration and stops for manual review.",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.skill_path):
        print(f"Error: Skill directory not found: {args.skill_path}")
        sys.exit(1)

    if not os.path.isfile(args.prompts):
        print(f"Error: Prompts file not found: {args.prompts}")
        sys.exit(1)

    run_loop(
        skill_path=args.skill_path,
        prompts_path=args.prompts,
        max_iterations=args.iterations,
        timeout=args.timeout,
        auto_apply=args.auto_apply,
    )


if __name__ == "__main__":
    main()
