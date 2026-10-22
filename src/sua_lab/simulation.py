from __future__ import annotations
import csv, json, random
from dataclasses import dataclass, asdict
from pathlib import Path
from .prompts import idea_prompt
from .metrics import pairwise_overlap, mean

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
        self.cfg, self.backend, self.corpus = cfg, backend, corpus
        self.rng = random.Random(cfg.seed)

    def _portfolio_size(self, researcher: int) -> int:
        base = 1.2 + 1.8*self.cfg.ai_capability
        incentive = 1.0 + 1.4*self.cfg.quantity_weight
        if self.cfg.best_k is not None:
            incentive *= 0.70
        noise = self.rng.uniform(0.85, 1.15)
        return max(1, int(round(base*incentive*noise)))

    def _verification(self, n: int, local_overlap: float) -> float:
        attention_dilution = 1.0 / (1.0 + 0.35*(n-1))
        priority_compression = 1.0 / (1.0 + self.cfg.priority_premium*(0.6+local_overlap))
        ai_substitution = 1.0 / (1.0 + 0.35*self.cfg.ai_capability)
        return max(0.05, attention_dilution*priority_compression*ai_substitution)

    def run(self):
        projects: list[Project] = []
        corpus_text = "\n".join(x["text"] for x in self.corpus)
        prior_questions: list[str] = []
        for r in range(self.cfg.n_researchers):
            n = self._portfolio_size(r)
            for p in range(n):
                reward_rule = ("Only the best outputs count." if self.cfg.best_k is not None
                               else "More publishable outputs improve evaluated performance.")
                priority_note = ("Being first is strongly rewarded." if self.cfg.priority_premium > .5
                                 else "Priority matters, but independent follow-on contributions retain value.")
                raw = self.backend.generate(idea_prompt(corpus_text, reward_rule, priority_note, self.cfg.ai_capability), seed=self.cfg.seed+r*100+p)
                try:
                    obj = json.loads(raw)
                except json.JSONDecodeError:
                    obj = {"question": raw[:240], "mechanism": "unparsed", "keywords": [], "verification_plan": ""}
                overlap = pairwise_overlap(prior_questions + [obj["question"]]) if prior_questions else 0.0
                v = self._verification(n, overlap)
                quality = max(0.0, min(1.0, 0.35 + 0.55*v + self.rng.uniform(-0.08,0.08)))
                pr = Project(r, f"R{r+1}P{p+1}", obj["question"], obj.get("mechanism",""), v, quality)
                projects.append(pr); prior_questions.append(pr.question)

        queue = list(projects)
        total_submissions = 0; external_reviews = 0; desk_rejections = 0
        while queue:
            manuscript = queue.pop(0)
            manuscript.attempts += 1; total_submissions += 1
            load = total_submissions / max(1, self.cfg.review_capacity)
            threshold = min(0.80, 0.34 + 0.18*max(0.0, load-1.0))
            signal = manuscript.quality + self.rng.uniform(-0.18,0.18)
            if signal < threshold:
                manuscript.desk_rejected = True; desk_rejections += 1
                if manuscript.attempts <= self.cfg.max_resubmissions:
                    queue.append(manuscript)
            else:
                manuscript.externally_reviewed = True; external_reviews += 1

        questions = [p.question for p in projects]
        summary = {
            "n_researchers": self.cfg.n_researchers,
            "primary_projects": len(projects),
            "avg_projects_per_researcher": len(projects)/self.cfg.n_researchers,
            "avg_verification": mean([p.verification for p in projects]),
            "avg_quality_proxy": mean([p.quality for p in projects]),
            "idea_overlap_jaccard": pairwise_overlap(questions),
            "total_submissions": total_submissions,
            "desk_rejections": desk_rejections,
            "external_reviews": external_reviews,
            "review_load_ratio": external_reviews/max(1,self.cfg.review_capacity),
            "avg_attempts": mean([p.attempts for p in projects]),
        }
        return projects, summary

def load_corpus(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

def write_outputs(projects, summary, out_dir):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    with (out/"projects.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(projects[0]).keys()))
        w.writeheader(); w.writerows(asdict(x) for x in projects)
    (out/"summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
