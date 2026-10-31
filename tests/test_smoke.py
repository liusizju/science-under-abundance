"""Offline checks for the deterministic research-production harness."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    path = ROOT / "sample_results" / name / "summary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_demo.py")],
        check=True,
        capture_output=True,
        text=True,
    )

    baseline = load("baseline")
    quantity = load("high_ai_quantity")
    best_two = load("high_ai_bestk")

    # These are checks on prescribed simulation equations, not behavioral tests.
    assert quantity["primary_projects"] > baseline["primary_projects"]
    assert quantity["avg_verification"] < baseline["avg_verification"]
    assert quantity["total_submissions"] > baseline["total_submissions"]
    assert best_two["primary_projects"] < quantity["primary_projects"]
    assert best_two["avg_verification"] > quantity["avg_verification"]

    for name in ("baseline", "high_ai_quantity", "high_ai_bestk"):
        output = ROOT / "sample_results" / name
        for filename in (
            "summary.json", "projects.csv", "traces.jsonl", "run_metadata.json"
        ):
            assert (output / filename).is_file()

    print("Deterministic harness checks passed")


if __name__ == "__main__":
    main()
