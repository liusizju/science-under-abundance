# Sample results: engineering only

These files come from the deterministic mock backend and exist to verify that the pipeline runs, writes complete traces, and responds to transparent theory-harness parameters.

They are **not substantive findings** about AI, scientists, or idea convergence. In particular, the mock backend does not encode an AI-induced semantic treatment effect.

Regenerate them with:

```bash
python scripts/run_demo.py
```

Each condition writes:

- `projects.csv`
- `summary.json`
- `traces.jsonl`
- `run_metadata.json`

The Stage-2 scientific tests require live model backends, cross-model replication, and human validation as described in `EXPERIMENTS.md`.
