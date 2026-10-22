from pathlib import Path
import argparse, csv, json, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from sua_lab.backends import make_backend
from sua_lab.simulation import Config, Simulation, load_corpus, write_outputs

try:
    import yaml
except ImportError as e:
    raise SystemExit("PyYAML is required: pip install PyYAML") from e

p=argparse.ArgumentParser(description="Run every YAML config in configs/ and collect a summary table.")
p.add_argument("--backend", choices=["mock","ollama","openai-compatible"], default="mock")
p.add_argument("--model", default="deterministic-mock-v2")
p.add_argument("--out", default=str(ROOT/"sample_results"/"grid_run"))
a=p.parse_args()
out=Path(a.out); out.mkdir(parents=True, exist_ok=True)
corpus=load_corpus(ROOT/"data"/"seed_corpus.jsonl")
rows=[]
for path in sorted((ROOT/"configs").glob("*.yaml")):
    obj=yaml.safe_load(path.read_text())
    obj.pop("backend", None); obj.pop("model", None)
    cfg=Config(**obj)
    backend=make_backend(a.backend, a.model)
    projects, summary, traces=Simulation(cfg, backend, corpus).run()
    write_outputs(projects, summary, traces, out/path.stem, config=cfg)
    rows.append({"condition":path.stem, **summary})
(out/"grid_summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
with (out/"grid_summary.csv").open("w", newline="", encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(json.dumps(rows, indent=2))
