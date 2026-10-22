# Artifact manifest

- `src/sua_lab/`: core simulation and backend adapters.
- `configs/`: transparent experiment configurations.
- `data/seed_corpus.jsonl`: synthetic, shareable seed corpus used for smoke tests.
- `scripts/run_demo.py`: deterministic three-condition smoke test.
- `scripts/run_experiment.py`: configurable run with mock, Ollama, or OpenAI-compatible backend.
- `sample_results/`: summary outputs from the deterministic smoke test; running the demo regenerates full project-level CSVs.

Stage-2 planned additions:
1. local open-weight LLM benchmark suite;
2. embedding-based idea overlap measurement;
3. model-family heterogeneity treatments;
4. reviewer-agent calibration and ablations;
5. optional human evaluation interface;
6. containerized reproducibility image.
