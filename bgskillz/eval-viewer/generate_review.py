#!/usr/bin/env python3
"""Generate a self-contained HTML review page with evaluation data embedded.

Takes an evals.json manifest and optional grading/analysis files, embeds all
data into the viewer HTML template, and produces a single HTML file that can
be opened directly in a browser.

Usage:
    python generate_review.py /path/to/iteration-1/evals.json
    python generate_review.py /path/to/iteration-1/evals.json --output review.html
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional


def load_json(path: str) -> Optional[Dict[str, Any]]:
    """Load a JSON file, returning None if it doesn't exist."""
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def load_output_text(path: str) -> str:
    """Load output text from a response file."""
    if not os.path.isfile(path):
        return "[Output file not found]"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return "[Error reading output file]"


def collect_data(evals_path: str) -> Dict[str, Any]:
    """Collect all evaluation data from the iteration directory.

    Loads evals.json, grading.json, analysis.json, comparison results,
    and the actual output text from response files.
    """
    iter_dir = os.path.dirname(os.path.abspath(evals_path))

    manifest = load_json(evals_path)
    if manifest is None:
        print(f"Error: Could not load {evals_path}")
        sys.exit(1)

    # Load grading results
    grading = load_json(os.path.join(iter_dir, "grading.json"))

    # Load analysis results
    analysis = load_json(os.path.join(iter_dir, "analysis.json"))

    # Load output text for each test case
    for result in manifest.get("results", []):
        for label in ["with_skill", "without_skill"]:
            output_path = result.get(label, {}).get("output_path", "")
            if output_path:
                # Handle both absolute and relative paths
                if not os.path.isabs(output_path):
                    output_path = os.path.join(iter_dir, output_path)
                result[label]["output_text"] = load_output_text(output_path)
            else:
                result[label]["output_text"] = "[No output path]"

    # Load comparison results per test case
    for result in manifest.get("results", []):
        test_id = result["id"]
        eval_dir = os.path.join(iter_dir, f"eval-{test_id}")
        comparison = load_json(os.path.join(eval_dir, "comparison.json"))
        if comparison:
            result["comparison"] = comparison

    return {
        "manifest": manifest,
        "grading": grading,
        "analysis": analysis,
    }


def generate_html(data: Dict[str, Any]) -> str:
    """Generate a self-contained HTML review page with data embedded."""
    viewer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "viewer.html")
    if not os.path.isfile(viewer_path):
        print(f"Error: viewer.html not found at {viewer_path}")
        sys.exit(1)

    with open(viewer_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Serialize data as JSON for embedding
    manifest_json = json.dumps(data["manifest"], indent=2)
    grading_json = json.dumps(data.get("grading") or {}, indent=2)
    analysis_json = json.dumps(data.get("analysis") or {}, indent=2)

    # Inject data and auto-load script before closing </body>
    inject_script = f"""
<script>
  // Auto-loaded evaluation data
  (function() {{
    const embeddedData = {manifest_json};
    const embeddedGrading = {grading_json};
    const embeddedAnalysis = {analysis_json};

    // Override loadFile to use embedded data
    evalData = embeddedData;
    window._grading = embeddedGrading;
    window._analysis = embeddedAnalysis;

    // Render on load
    document.addEventListener('DOMContentLoaded', function() {{
      renderAll();

      // Update output panels with actual text
      if (evalData && evalData.results) {{
        evalData.results.forEach(function(result, i) {{
          var withEl = document.getElementById('with-' + i);
          var withoutEl = document.getElementById('without-' + i);
          if (withEl && result.with_skill && result.with_skill.output_text) {{
            withEl.textContent = result.with_skill.output_text;
          }}
          if (withoutEl && result.without_skill && result.without_skill.output_text) {{
            withoutEl.textContent = result.without_skill.output_text;
          }}
        }});
      }}

      // Hide load section
      var ls = document.getElementById('loadSection');
      if (ls) ls.style.display = 'none';
    }});
  }})();
</script>
"""

    # Insert before </body>
    html = template.replace("</body>", inject_script + "</body>")

    return html


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a self-contained HTML review page from evaluation data.",
        epilog="Example: python generate_review.py iteration-1/evals.json",
    )
    parser.add_argument(
        "evals_path",
        help="Path to evals.json manifest from an evaluation run",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output HTML file path (default: review-<iteration>.html)",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.evals_path):
        print(f"Error: evals.json not found: {args.evals_path}")
        sys.exit(1)

    # Collect all data
    print(f"Loading evaluation data from: {args.evals_path}")
    data = collect_data(args.evals_path)

    manifest = data["manifest"]
    iteration = manifest.get("iteration", "?")
    test_count = manifest.get("test_count", 0)

    print(f"  Iteration: {iteration}")
    print(f"  Test cases: {test_count}")
    print(f"  Grading data: {'yes' if data.get('grading') else 'no'}")
    print(f"  Analysis data: {'yes' if data.get('analysis') else 'no'}")

    # Generate HTML
    html = generate_html(data)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(
            os.path.dirname(args.evals_path),
            f"review-iteration-{iteration}.html",
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"\nGenerated: {output_path} ({size_kb:.1f} KB)")
    print(f"Open in a browser to review results.")


if __name__ == "__main__":
    main()
