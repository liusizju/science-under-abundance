from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from sua_lab.backends import MockBackend
from sua_lab.simulation import Config, Simulation, load_corpus, write_outputs

corpus = load_corpus(ROOT / "data" / "seed_corpus.jsonl")
conditions = {
    "baseline": Config(seed=20261021, n_researchers=8, ai_capability=.45, quantity_weight=.45, priority_premium=.35, review_capacity=14),
    "high_ai_quantity": Config(seed=20261021, n_researchers=8, ai_capability=.85, quantity_weight=.85, priority_premium=.60, review_capacity=14),
    "high_ai_bestk": Config(seed=20261021, n_researchers=8, ai_capability=.85, quantity_weight=.25, priority_premium=.35, review_capacity=14, best_k=2),
}
all_summaries = {}
for name, cfg in conditions.items():
    sim = Simulation(cfg, MockBackend(), corpus)
    projects, summary = sim.run()
    write_outputs(projects, summary, ROOT / "sample_results" / name)
    all_summaries[name] = summary
print(json.dumps(all_summaries, indent=2))
