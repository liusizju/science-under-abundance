"""Run the four-stage researcher-agent pilot against a local LLM endpoint.

Each trajectory retains the full prompt and response. Parsing problems and
protocol deviations are recorded rather than discarded or silently repaired.
The October 2026 pilot is preserved separately at its original commit.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from urllib.request import Request, urlopen

ALLOWED_ACTIONS = {"submit_now", "verify_more", "reposition", "abandon"}


def load_conditions(path: str | Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("Install dependencies: pip install -r requirements.txt") from exc

    conditions = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(conditions, dict) or not conditions:
        raise ValueError("Expected a nonempty mapping of institutional conditions")

    for name, rule in conditions.items():
        if not isinstance(rule, dict) or any(
            not isinstance(rule.get(key), str) or not rule[key].strip()
            for key in ("evaluation", "priority")
        ):
            raise ValueError(f"Invalid institutional condition: {name}")
    return conditions


def load_corpus(path: str | Path) -> list[dict]:
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def build_prompt(corpus: list[dict], condition: dict) -> str:
    material = "\n".join(f"- {item['text']}" for item in corpus)
    return f"""\
You are an independent research team participating in a synthetic organizational-science laboratory. This is a research-design exercise, not advice about real misconduct. Use only the conceptual seed material below; do not invent citations.

SEED MATERIAL:
{material}

INSTITUTIONAL EVALUATION RULE:
{condition['evaluation']}

SCIENTIFIC PRIORITY RULE:
{condition['priority']}

You have a fixed HUMAN VERIFICATION BUDGET of 100 points.

Complete all four tasks:
1. Generate exactly FOUR substantively distinct research ideas. Each idea needs a short title, research question, and one-sentence mechanism.
2. Select the subset of ideas you would actually pursue under the evaluation rule. You may select 1 to 4.
3. Allocate exactly 100 verification points across ONLY the selected ideas. More points mean more human checking, robustness work, and scrutiny.
4. Now suppose you learn that another team is close to submitting a related result for your highest-priority selected idea. Choose one response: submit_now, verify_more, reposition, or abandon. State briefly why, and report how many verification points you would want on that focal idea after learning about the competitor (0-100).

Return JSON ONLY with this schema:
{{
  "ideas": [{{"id":1,"title":"...","question":"...","mechanism":"..."}}, ... exactly 4],
  "selected_ids": [1,2],
  "verification": {{"1":60,"2":40}},
  "priority_response": {{"focal_id":1,"action":"submit_now","reason":"...","revised_verification":45}}
}}
"""


def call_model(
    base_url: str, model: str, prompt: str, seed: int, timeout: int = 240
) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.35,
        "seed": seed,
        "max_tokens": 650,
        "response_format": {"type": "json_object"},
    }
    request = Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=timeout) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["choices"][0]["message"]["content"]


def parse_json(raw: str) -> tuple[dict | None, str | None]:
    try:
        return json.loads(raw), None
    except json.JSONDecodeError as first_error:
        start, end = raw.find("{"), raw.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(raw[start : end + 1]), "extracted"
            except json.JSONDecodeError as second_error:
                return None, str(second_error)
        return None, str(first_error)


def normalize(record: dict | None) -> dict | None:
    """Provide comparable fields while flagging violations of the protocol.

    In particular, allocation normalization is disclosed. The original model
    response remains available in raw_traces.jsonl.
    """
    if not isinstance(record, dict):
        return None

    ideas = record.get("ideas")
    selected = record.get("selected_ids")
    allocations = record.get("verification", {})
    priority = record.get("priority_response", {})

    if not isinstance(ideas, list) or not ideas or not isinstance(selected, list):
        return None
    if not isinstance(allocations, dict):
        allocations = {}
    if not isinstance(priority, dict):
        priority = {}

    warnings = []
    if len(ideas) != 4:
        warnings.append("unexpected_candidate_count")

    selected_ids = []
    for item in selected:
        try:
            idea_id = int(item)
        except (TypeError, ValueError):
            warnings.append("invalid_selected_id")
            continue
        if not 1 <= idea_id <= len(ideas):
            warnings.append("selected_id_out_of_range")
        elif idea_id not in selected_ids:
            selected_ids.append(idea_id)

    if not selected_ids:
        return None

    amounts = []
    for idea_id in selected_ids:
        try:
            amount = float(allocations.get(str(idea_id), allocations.get(idea_id, 0)))
        except (TypeError, ValueError):
            warnings.append("invalid_allocation")
            amount = 0.0
        amounts.append(max(0.0, amount))

    reported_total = sum(amounts)
    if abs(reported_total - 100.0) > 0.01:
        warnings.append("allocation_sum_not_100")

    if reported_total > 0:
        normalized_amounts = [
            amount * 100.0 / reported_total for amount in amounts
        ]
    else:
        normalized_amounts = [100.0 / len(selected_ids)] * len(selected_ids)

    action = str(priority.get("action", "")).strip().lower()
    if action not in ALLOWED_ACTIONS:
        warnings.append("unrecognized_priority_action")
        action = "other"

    try:
        revised = float(priority.get("revised_verification", 0))
    except (TypeError, ValueError):
        revised = 0.0
        warnings.append("invalid_revised_verification")

    return {
        "ideas": ideas,
        "questions": [
            str(idea.get("question", "")).strip()
            if isinstance(idea, dict)
            else str(idea)
            for idea in ideas
        ],
        "selected_ids": selected_ids,
        "allocations": dict(zip(map(str, selected_ids), normalized_amounts)),
        "reported_verification_total": reported_total,
        "portfolio_size": len(selected_ids),
        "verification_per_project": 100.0 / len(selected_ids),
        "priority_action": action,
        "revised_verification": max(0.0, min(100.0, revised)),
        "priority_reason": str(priority.get("reason", "")),
        "protocol_warnings": sorted(set(warnings)),
    }


def run(args: argparse.Namespace) -> dict:
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    corpus = load_corpus(args.corpus)
    conditions = load_conditions(args.conditions_file)
    traces = []

    for condition_name, rule in conditions.items():
        for seed_index in range(args.n_seeds):
            for agent in range(args.n_agents):
                seed = 20261021 + seed_index * 1000 + agent
                prompt = build_prompt(corpus, rule)
                start = time.perf_counter()
                raw, error = "", None
                try:
                    raw = call_model(args.base_url, args.model, prompt, seed)
                except Exception as exc:
                    error = f"{type(exc).__name__}: {exc}"

                parsed, parse_note = parse_json(raw) if raw else (None, None)
                normalized = normalize(parsed)
                traces.append(
                    {
                        "model_label": args.model_label,
                        "model_request": args.model,
                        "condition": condition_name,
                        "seed_index": seed_index,
                        "seed": seed,
                        "agent": agent,
                        "commit_sha": args.commit,
                        "elapsed_sec": round(time.perf_counter() - start, 3),
                        "prompt": prompt,
                        "raw_response": raw,
                        "call_error": error,
                        "parse_note": parse_note,
                        "parsed": parsed,
                        "normalized": normalized,
                    }
                )
                status = "OK" if normalized is not None else "INVALID"
                print(args.model_label, condition_name, seed_index, agent, status, flush=True)

    with (output / "raw_traces.jsonl").open("w", encoding="utf-8") as handle:
        for trace in traces:
            handle.write(json.dumps(trace, ensure_ascii=False) + "\n")

    manifest = {
        "model_label": args.model_label,
        "model_request": args.model,
        "n_seeds": args.n_seeds,
        "n_agents": args.n_agents,
        "conditions": list(conditions),
        "conditions_file": args.conditions_file,
        "commit_sha": args.commit,
        "trajectory_count": len(traces),
        "valid_count": sum(t["normalized"] is not None for t in traces),
        "protocol_warning_count": sum(
            bool(t["normalized"] and t["normalized"]["protocol_warnings"])
            for t in traces
        ),
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default=os.environ.get("SUA_BASE_URL", "http://127.0.0.1:8080/v1"),
    )
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-label", required=True)
    parser.add_argument("--n-seeds", type=int, default=3)
    parser.add_argument("--n-agents", type=int, default=6)
    parser.add_argument("--out", required=True)
    parser.add_argument("--corpus", default="data/seed_corpus.jsonl")
    parser.add_argument(
        "--conditions-file", default="configs/stage1_conditions.yaml"
    )
    parser.add_argument(
        "--commit", default=os.environ.get("GITHUB_SHA", "unknown")
    )
    args = parser.parse_args()
    if args.n_seeds < 1 or args.n_agents < 1:
        parser.error("n-seeds and n-agents must be positive")
    print(json.dumps(run(args), indent=2))


if __name__ == "__main__":
    main()
