"""Run the deterministic theory-harness smoke test."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sua_lab.backends import MockBackend
from sua_lab.simulation import Config, Simulation, load_corpus, write_outputs


CONDITIONS = {
    "baseline": Config(
        ai_capability=0.45,
        quantity_weight=0.45,
        priority_premium=0.35,
    ),
    "high_ai_quantity": Config(
        ai_capability=0.85,
        quantity_weight=0.85,
        priority_premium=0.60,
    ),
    "high_ai_bestk": Config(
        ai_capability=0.85,
        quantity_weight=0.25,
        priority_premium=0.35,
        best_k=2,
    ),
}


def main() -> None:
    corpus = load_corpus(ROOT / "data" / "seed_corpus.jsonl")
    results = {}

    for name, config in CONDITIONS.items():
        projects, summary, traces = Simulation(
            config, MockBackend(), corpus
        ).run()
        write_outputs(
            projects,
            summary,
            traces,
            ROOT / "sample_results" / name,
            config=config,
        )
        results[name] = summary

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
