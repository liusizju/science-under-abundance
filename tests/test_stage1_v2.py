"""Offline checks of the Stage-1 institutional interface and analysis."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_runner():
    script = ROOT / "scripts" / "run_stage1_benchmark.py"
    spec = importlib.util.spec_from_file_location("stage1_runner", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_trajectory(runner, agent: int, selected_ids: list[int]) -> dict:
    ideas = [
        {
            "id": 1,
            "title": "Quality standards",
            "question": "When does verification improve research quality?",
            "mechanism": "Attention shapes validity.",
        },
        {
            "id": 2,
            "title": "Peer review",
            "question": "How does congestion slow journal review?",
            "mechanism": "Capacity limits screening.",
        },
        {
            "id": 3,
            "title": "Research priority",
            "question": "Does priority pressure increase rushing?",
            "mechanism": "Speed competes with checking.",
        },
        {
            "id": 4,
            "title": "Novelty",
            "question": "Do output rewards reduce topic diversity?",
            "mechanism": "Rules change selection.",
        },
    ]
    record = {
        "ideas": ideas,
        "selected_ids": selected_ids,
        "verification": {
            str(idea_id): 100 / len(selected_ids)
            for idea_id in selected_ids
        },
        "priority_response": {
            "focal_id": selected_ids[0],
            "action": "verify_more",
            "reason": "The mechanism needs another robustness check.",
            "revised_verification": 55,
        },
    }
    normalized = runner.normalize(record)
    assert normalized is not None
    return {
        "model_label": "fixture",
        "condition": "quantity",
        "agent": agent,
        "normalized": normalized,
    }


def main() -> None:
    runner = load_runner()
    conditions = runner.load_conditions(
        ROOT / "configs" / "stage1_conditions.yaml"
    )
    assert list(conditions) == ["quantity", "best_k", "high_priority"]

    corpus = [{"text": "Research choices respond to institutional evaluation."}]
    prompt = runner.build_prompt(corpus, conditions["best_k"])
    assert "FOUR substantively distinct" in prompt
    assert "100 points" in prompt
    assert "TWO strongest" in prompt

    with tempfile.TemporaryDirectory() as temporary:
        workdir = Path(temporary)
        raw_path = workdir / "raw_traces.jsonl"
        trajectories = [
            sample_trajectory(runner, 0, [1]),
            sample_trajectory(runner, 1, [1, 2]),
        ]
        raw_path.write_text(
            "\n".join(json.dumps(record) for record in trajectories) + "\n",
            encoding="utf-8",
        )
        output = workdir / "analysis"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "analyze_stage1_benchmark.py"),
                str(raw_path),
                "--out",
                str(output),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(
            (output / "benchmark_summary.json").read_text(encoding="utf-8")
        )
        summary = result["summaries"][0]
        assert summary["n"] == 2
        assert 0 <= summary["idea_jaccard"] <= 1
        assert 0 <= summary["selected_idea_jaccard"] <= 1
        assert summary["selected_idea_jaccard"] != summary["idea_jaccard"]

    print("Stage-1 institutional interface checks passed")


if __name__ == "__main__":
    main()
