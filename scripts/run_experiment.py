from pathlib import Path
import argparse, sys, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from sua_lab.backends import make_backend
from sua_lab.simulation import Config, Simulation, load_corpus, write_outputs

try:
    import yaml
except ImportError as e:
    raise SystemExit("PyYAML is required for config files: pip install PyYAML") from e

p=argparse.ArgumentParser()
p.add_argument("--config", default=str(ROOT/"configs"/"baseline.yaml"))
p.add_argument("--backend", choices=["mock","ollama","openai-compatible"], default=None)
p.add_argument("--model", default=None)
p.add_argument("--out", default=str(ROOT/"sample_results"/"live_run"))
a=p.parse_args()
obj=yaml.safe_load(Path(a.config).read_text())
backend_name=a.backend or obj.pop("backend", "mock")
model=a.model or obj.pop("model", "deterministic-mock-v2")
cfg=Config(**obj)
backend=make_backend(backend_name, model)
corpus=load_corpus(ROOT/"data"/"seed_corpus.jsonl")
projects, summary, traces=Simulation(cfg, backend, corpus).run()
write_outputs(projects, summary, traces, a.out, config=cfg)
print(json.dumps(summary, indent=2))
