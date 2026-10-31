"""Descriptive analysis of frozen or newly generated researcher trajectories."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "src"))

from sua_lab.metrics import jaccard, pairwise_overlap


def average(values: list[float]) -> float | None:
    return mean(values) if values else None


def load_traces(paths: list[str]) -> list[dict]:
    records = []
    for filename in paths:
        with Path(filename).open(encoding="utf-8") as handle:
            records.extend(
                json.loads(line) for line in handle if line.strip()
            )
    return records


def selected_questions(record: dict) -> list[str]:
    ideas = record.get("ideas", [])
    questions = []
    for idea_id in record.get("selected_ids", []):
        if not isinstance(idea_id, int) or not 1 <= idea_id <= len(ideas):
            continue
        idea = ideas[idea_id - 1]
        if isinstance(idea, dict) and idea.get("question"):
            questions.append(str(idea["question"]))
    return questions


def summarize_cells(records: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for record in records:
        if record.get("normalized") is not None:
            groups[(record["model_label"], record["condition"])].append(record)

    summaries = []
    for (model, condition), group in sorted(groups.items()):
        decisions = [record["normalized"] for record in group]
        candidates = [
            question
            for decision in decisions
            for question in decision["questions"]
            if question
        ]
        retained = [
            question
            for decision in decisions
            for question in selected_questions(decision)
        ]
        actions = Counter(
            decision["priority_action"] for decision in decisions
        )
        attempted = sum(
            record.get("model_label") == model
            and record.get("condition") == condition
            for record in records
        )
        n = len(decisions)
        summaries.append(
            {
                "model": model,
                "condition": condition,
                "n": n,
                "valid_rate": n / attempted,
                "mean_portfolio": average(
                    [d["portfolio_size"] for d in decisions]
                ),
                "mean_verification_per_project": average(
                    [d["verification_per_project"] for d in decisions]
                ),
                "idea_jaccard": pairwise_overlap(candidates),
                "selected_idea_jaccard": pairwise_overlap(retained),
                "submit_now_rate": actions["submit_now"] / n,
                "verify_more_rate": actions["verify_more"] / n,
                "reposition_rate": actions["reposition"] / n,
                "abandon_rate": actions["abandon"] / n,
                "mean_revised_verification": average(
                    [d["revised_verification"] for d in decisions]
                ),
                "protocol_warning_rate": sum(
                    bool(d.get("protocol_warnings")) for d in decisions
                ) / n,
            }
        )
    return summaries


def compare_families(records: list[dict]) -> list[dict]:
    valid = [record for record in records if record.get("normalized")]
    models = sorted({record["model_label"] for record in valid})
    conditions = sorted({record["condition"] for record in valid})
    comparisons = []

    for model_a, model_b in combinations(models, 2):
        for condition in conditions:
            questions_a = [
                question
                for record in valid
                if record["model_label"] == model_a
                and record["condition"] == condition
                for question in record["normalized"]["questions"]
                if question
            ]
            questions_b = [
                question
                for record in valid
                if record["model_label"] == model_b
                and record["condition"] == condition
                for question in record["normalized"]["questions"]
                if question
            ]
            scores = [
                jaccard(a, b) for a in questions_a for b in questions_b
            ]
            if scores:
                comparisons.append(
                    {
                        "condition": condition,
                        "model_a": model_a,
                        "model_b": model_b,
                        "cross_family_jaccard": average(scores),
                    }
                )
    return comparisons


def institutional_contrasts(summaries: list[dict]) -> list[dict]:
    contrasts = []
    models = sorted({row["model"] for row in summaries})
    for model in models:
        rows = {
            row["condition"]: row
            for row in summaries
            if row["model"] == model
        }
        if {"best_k", "quantity"} <= rows.keys():
            best, broad = rows["best_k"], rows["quantity"]
            contrasts.append(
                {
                    "model": model,
                    "contrast": "best_k-minus-quantity",
                    "portfolio_diff": (
                        best["mean_portfolio"] - broad["mean_portfolio"]
                    ),
                    "verification_diff": (
                        best["mean_verification_per_project"]
                        - broad["mean_verification_per_project"]
                    ),
                    "idea_overlap_diff": (
                        best["idea_jaccard"] - broad["idea_jaccard"]
                    ),
                    "selected_overlap_diff": (
                        best["selected_idea_jaccard"]
                        - broad["selected_idea_jaccard"]
                    ),
                }
            )
        if {"high_priority", "quantity"} <= rows.keys():
            high, broad = rows["high_priority"], rows["quantity"]
            contrasts.append(
                {
                    "model": model,
                    "contrast": "high_priority-minus-quantity",
                    "submit_now_diff": (
                        high["submit_now_rate"] - broad["submit_now_rate"]
                    ),
                    "verify_more_diff": (
                        high["verify_more_rate"] - broad["verify_more_rate"]
                    ),
                    "revised_verification_diff": (
                        high["mean_revised_verification"]
                        - broad["mean_revised_verification"]
                    ),
                }
            )
    return contrasts


def completion_by_cell(records: list[dict]) -> list[dict]:
    """Keep cells visible even when every model response is unusable."""
    groups = defaultdict(list)
    for record in records:
        groups[(record["model_label"], record["condition"])].append(record)

    return [
        {
            "model": model,
            "condition": condition,
            "attempted": len(group),
            "usable": sum(record.get("normalized") is not None for record in group),
            "invalid": sum(record.get("normalized") is None for record in group),
        }
        for (model, condition), group in sorted(groups.items())
    ]

def write_report(output: Path, records: list[dict], results: dict) -> None:
    summaries = results["summaries"]
    coverage = results["completion_by_cell"]
    usable = sum(record.get("normalized") is not None for record in records)
    total = len(records)
    lines = [
        "# Researcher-agent pilot: descriptive report",
        "",
        f"Trajectories: {total}; structurally usable: {usable}"
        + (f" ({usable / total:.1%})." if total else "."),
        "",
        "## Structured-output coverage",
        "",
        "| Model | Condition | Attempted | Usable | Invalid |",
        "|---|---|---:|---:|---:|",
    ]
    for row in coverage:
        lines.append(
            f"| {row['model']} | {row['condition']} | {row['attempted']} "
            f"| {row['usable']} | {row['invalid']} |"
        )
    lines.extend([
        "",
        "## Results by model and institutional condition",
        "",
        "| Model | Condition | Valid | Portfolio | Points/project | Candidate overlap | Selected overlap | Submit now |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ])
    for row in summaries:
        lines.append(
            f"| {row['model']} | {row['condition']} | {row['n']} "
            f"| {row['mean_portfolio']:.2f} "
            f"| {row['mean_verification_per_project']:.1f} "
            f"| {row['idea_jaccard']:.3f} "
            f"| {row['selected_idea_jaccard']:.3f} "
            f"| {row['submit_now_rate']:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A fixed 100-point verification budget makes points per project "
            "an accounting identity, not an independently measured quality gain.",
            "Candidate and retained idea overlap are lexical diagnostics. "
            "Neither establishes conceptual novelty.",
            "This small synthetic pilot is not evidence about how human "
            "researchers would respond to these institutions.",
        ]
    )
    (output / "BENCHMARK_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traces", nargs="+")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    records = load_traces(args.traces)
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)

    results = {
        "summaries": summarize_cells(records),
        "completion_by_cell": completion_by_cell(records),
        "cross_family": compare_families(records),
        "contrasts": [],
    }
    results["contrasts"] = institutional_contrasts(results["summaries"])
    (output / "benchmark_summary.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )

    if results["summaries"]:
        with (output / "benchmark_summary.csv").open(
            "w", newline="", encoding="utf-8"
        ) as handle:
            writer = csv.DictWriter(
                handle, fieldnames=list(results["summaries"][0])
            )
            writer.writeheader()
            writer.writerows(results["summaries"])

    write_report(output, records, results)
    print((output / "BENCHMARK_REPORT.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
