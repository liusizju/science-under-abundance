"""Run one theory-harness configuration with a selected model backend."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sua_lab.backends import make_backend
from sua_lab.simulation import Config, Simulation, load_corpus, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(ROOT / "configs" / "baseline.yaml"))
    parser.add_argument(
        "--backend", choices=("mock", "ollama", "openai-compatible")
    )
    parser.add_argument("--model")
    parser.add_argument(
        "--out", default=str(ROOT / "sample_results" / "live_run")
    )
    args = parser.parse_args()

    settings = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    if not isinstance(settings, dict) or "ai_capability" not in settings:
        parser.error("--config must reference a theory-harness YAML file")

    backend_name = args.backend or settings.pop("backend", "mock")
    model = args.model or settings.pop("model", "deterministic-mock-v2")
    config = Config(**settings)

    corpus = load_corpus(ROOT / "data" / "seed_corpus.jsonl")
    projects, summary, traces = Simulation(
        config, make_backend(backend_name, model), corpus
    ).run()
    write_outputs(projects, summary, traces, args.out, config=config)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
