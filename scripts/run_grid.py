"""Run the stylized production model over configured scenarios."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sua_lab.backends import make_backend
from sua_lab.simulation import Config, Simulation, load_corpus, write_outputs


def load_scenarios():
    """Skip institutional prompt settings, which use a different schema."""
    for path in sorted((ROOT / "configs").glob("*.yaml")):
        values = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(values, dict) or "ai_capability" not in values:
            continue
        values.pop("backend", None)
        values.pop("model", None)
        yield path.stem, Config(**values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--backend",
        choices=("mock", "ollama", "openai-compatible"),
        default="mock",
    )
    parser.add_argument("--model", default="deterministic-mock-v2")
    parser.add_argument(
        "--out", default=str(ROOT / "sample_results" / "grid_run")
    )
    args = parser.parse_args()

    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    corpus = load_corpus(ROOT / "data" / "seed_corpus.jsonl")
    backend = make_backend(args.backend, args.model)
    rows = []

    for name, config in load_scenarios():
        projects, summary, traces = Simulation(config, backend, corpus).run()
        write_outputs(projects, summary, traces, output / name, config=config)
        rows.append({"condition": name, **summary})

    if not rows:
        raise SystemExit("No theory-harness configurations found in configs/")

    (output / "grid_summary.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )
    with (output / "grid_summary.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
