# Generated engineering outputs (not research evidence)

This directory is used for local outputs from the deterministic smoke test:

```bash
python tests/test_smoke.py
# or: python scripts/run_demo.py
```

The test creates `baseline/`, `high_ai_quantity/`, and `high_ai_bestk/`, each with a `summary.json`, `projects.csv`, `traces.jsonl`, and `run_metadata.json` file.

The original tracked mock summaries were removed from the current branch because they were tied to an earlier implementation and could be mistaken for scientific findings. **The real two-family pilot is preserved separately** under `benchmark/stage1_quick_2026-10-22/` and its frozen snapshot.

The mock backend checks software plumbing only. Portfolio and verification effects in the stylized harness are coded assumptions and should not be reported as empirical effects of AI.
