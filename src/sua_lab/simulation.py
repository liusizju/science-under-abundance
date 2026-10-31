"""Stylized research-production and editorial-capacity simulation.

The rules in this module are modeling assumptions. Outputs from the mock
backend are software checks, not observations about working scientists.
"""

from __future__ import annotations

import csv
import json
import random
from collections import deque
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from .metrics import jaccard, mean, pairwise_overlap
from .prompts import idea_prompt


@dataclass
class Config:
    seed: int = 20261021
    n_researchers: int = 8
    ai_capability: float = 0.5
    quantity_weight: float = 0.5
    priority_premium: float = 0.4
    review_capacity: int = 14
    best_k: int | None = None
    max_resubmissions: int = 2

    def __post_init__(self) -> None:
        if self.n_researchers < 1 or self.review_capacity < 1:
            raise ValueError("Researchers and review capacity must be positive")
        if self.max_resubmissions < 0:
            raise ValueError("max_resubmissions cannot be negative")
        if self.best_k is not None and self.best_k < 1:
            raise ValueError("best_k must be positive when specified")
        if min(self.ai_capability, self.quantity_weight, self.priority_premium) < 0:
            raise ValueError("Capability and incentive parameters cannot be negative")


@dataclass
class Project:
    researcher: int
    project_id: str
    question: str
    mechanism: str
    verification: float
    quality: float
    attempts: int = 0
    desk_rejected: bool = False
    externally_reviewed: bool = False


class Simulation:
    def __init__(self, cfg: Config, backend, corpus: list[dict]):
        self.cfg = cfg
        self.backend = backend
        self.corpus = corpus
        self.rng = random.Random(cfg.seed)

    def _portfolio_size(self) -> int:
        production = 1.2 + 1.8 * self.cfg.ai_capability
        incentive = 1.0 + 1.4 * self.cfg.quantity_weight
        if self.cfg.best_k is not None:
            incentive *= 0.70
        variation = self.rng.uniform(0.85, 1.15)
        return max(1, round(production * incentive * variation))

    def _verification(self, portfolio_size: int, overlap: float) -> float:
        attention = 1.0 / (1.0 + 0.35 * (portfolio_size - 1))
        priority = 1.0 / (
            1.0 + self.cfg.priority_premium * (0.6 + overlap)
        )
        return max(0.05, attention * priority)

    @staticmethod
    def _idea_record(raw: str) -> dict:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = None

        if isinstance(parsed, dict) and isinstance(parsed.get("question"), str):
            return parsed
        return {
            "question": raw[:240],
            "mechanism": "unparsed",
            "keywords": [],
            "verification_plan": "",
        }

    @staticmethod
    def _overlap_with_prior(question: str, prior: list[str]) -> float:
        if not prior:
            return 0.0
        return mean([jaccard(question, earlier) for earlier in prior])

    def _screen_manuscripts(self, projects: list[Project]) -> tuple[int, int, int]:
        queue = deque(projects)
        submissions = desk_rejections = external_reviews = 0

        while queue:
            manuscript = queue.popleft()
            manuscript.attempts += 1
            submissions += 1

            load = submissions / self.cfg.review_capacity
            threshold = min(0.80, 0.34 + 0.18 * max(0.0, load - 1.0))
            editorial_signal = manuscript.quality + self.rng.uniform(-0.18, 0.18)

            if editorial_signal < threshold:
                manuscript.desk_rejected = True
                desk_rejections += 1
                if manuscript.attempts <= self.cfg.max_resubmissions:
                    queue.append(manuscript)
            else:
                manuscript.externally_reviewed = True
                external_reviews += 1

        return submissions, desk_rejections, external_reviews

    def run(self) -> tuple[list[Project], dict, list[dict]]:
        projects: list[Project] = []
        traces: list[dict] = []
        prior_questions: list[str] = []
        corpus_text = "\n".join(item["text"] for item in self.corpus)

        reward_rule = (
            "Only the best outputs count."
            if self.cfg.best_k is not None
            else "More publishable outputs improve evaluated performance."
        )
        priority_note = (
            "Being first is strongly rewarded."
            if self.cfg.priority_premium > 0.5
            else "Priority matters, but independent follow-on contributions retain value."
        )
        backend_name = getattr(self.backend, "name", type(self.backend).__name__)

        for researcher in range(self.cfg.n_researchers):
            portfolio_size = self._portfolio_size()

            for index in range(portfolio_size):
                project_id = f"R{researcher + 1}P{index + 1}"
                seed = self.cfg.seed + researcher * 100 + index
                prompt = idea_prompt(corpus_text, reward_rule, priority_note)
                raw_response = self.backend.generate(prompt, seed=seed)
                record = self._idea_record(raw_response)

                # Compare this proposal with prior proposals, not all prior pairs.
                overlap = self._overlap_with_prior(record["question"], prior_questions)
                verification = self._verification(portfolio_size, overlap)
                quality_proxy = max(
                    0.0,
                    min(
                        1.0,
                        0.35 + 0.55 * verification + self.rng.uniform(-0.08, 0.08),
                    ),
                )

                projects.append(
                    Project(
                        researcher=researcher,
                        project_id=project_id,
                        question=record["question"],
                        mechanism=record.get("mechanism", ""),
                        verification=verification,
                        quality=quality_proxy,
                    )
                )
                prior_questions.append(record["question"])
                traces.append(
                    {
                        "researcher": researcher,
                        "project_id": project_id,
                        "seed": seed,
                        "backend": backend_name,
                        "prompt": prompt,
                        "raw_response": raw_response,
                        "parsed": record,
                    }
                )

        submissions, desk_rejections, external_reviews = self._screen_manuscripts(
            projects
        )
        summary = {
            "backend": backend_name,
            "n_researchers": self.cfg.n_researchers,
            "primary_projects": len(projects),
            "avg_projects_per_researcher": len(projects) / self.cfg.n_researchers,
            "avg_verification": mean([p.verification for p in projects]),
            "avg_quality_proxy": mean([p.quality for p in projects]),
            "idea_overlap_jaccard": pairwise_overlap(
                [p.question for p in projects]
            ),
            "total_submissions": submissions,
            "desk_rejections": desk_rejections,
            "external_reviews": external_reviews,
            "review_load_ratio": external_reviews / self.cfg.review_capacity,
            "avg_attempts": mean([p.attempts for p in projects]),
        }
        return projects, summary, traces


def load_corpus(path: str | Path) -> list[dict]:
    corpus = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            corpus.append(json.loads(line))
    return corpus


def write_outputs(
    projects: list[Project],
    summary: dict,
    traces: list[dict],
    out_dir: str | Path,
    config: Config | None = None,
) -> None:
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)

    with (output / "projects.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=[field.name for field in fields(Project)]
        )
        writer.writeheader()
        writer.writerows(asdict(project) for project in projects)

    (output / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    with (output / "traces.jsonl").open("w", encoding="utf-8") as handle:
        for trace in traces:
            handle.write(json.dumps(trace, ensure_ascii=False) + "\n")
    if config is not None:
        (output / "run_metadata.json").write_text(
            json.dumps(asdict(config), indent=2), encoding="utf-8"
        )
