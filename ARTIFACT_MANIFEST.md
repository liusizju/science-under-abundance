# SUA Lab repository manifest — Stage-1 proposal V2 alignment

The repository contains a **research instrument**, not the complete unpublished proposal DOCX/PDF. Its code and supporting documentation are aligned with the Mei Yang V2 revision.

## Current components

| Path | Status | Purpose |
|---|---|---|
| `docs/RESEARCH_DESIGN_V2.md` | V2 | Concrete broad-output vs. best-two experiment; counterhypotheses |
| `configs/stage1_conditions.yaml` | V2 | Editable institutional treatments for the live benchmark |
| `scripts/run_stage1_benchmark.py` | V2 | Live four-part structured agent protocol; raw response logging |
| `scripts/analyze_stage1_benchmark.py` | V2 | Candidate versus selected idea similarity; descriptive contrasts |
| `src/sua_lab/` | Stage 1 | Backend adapters, prompts, lexical metrics, and stylized theory harness |
| `scripts/run_demo.py` | Stage 1 | Deterministic engineering smoke-test pipeline |
| `scripts/run_experiment.py` / `scripts/run_grid.py` | Stage 1 | Stylized theory-harness runs |
| `data/seed_corpus.jsonl` | Stage 1 | Synthetic, redistributable information environment |
| `benchmark/stage1_quick_2026-10-22/` | Frozen | Original two-family live-model pilot metadata and summaries |
| `sample_results/` | Engineering | Mock-only summaries; not scientific evidence |
| `tests/test_smoke.py` | Stage 1 | Pipeline and harness smoke tests |
| `EXPERIMENTS.md` / `BOUNDARIES.md` / `REPRODUCIBILITY.md` | V2 | Design, limits, reproducibility and falsification |

## What has been superseded

- The failed, oversized first benchmark workflow and the one-off SmolLM2 retry workflow are historical attempts. Their code is no longer the recommended entry point.
- The successful **Stage-1 quick open-weight pilot** workflow remains the reference workflow; its GitHub Actions run is separately recorded.
- No historical raw traces or benchmark results have been rewritten to fit the revised theory.

## Stage-2 development targets

1. Test idea convergence under shared vs heterogeneous model and corpus environments;
2. measure both initial candidates and *selected research ideas* using semantic embeddings and blinded human ratings;
3. isolate best-K's project-reduction effect from any potential narrowing of exploration;
4. incorporate LLM editor/reviewer roles and institution-level congestion experiments;
5. conduct systematic protocol-compliance and cross-model/prompt robustness audits;
6. create an independently replicable snapshot beyond temporary Actions artifact retention.

For access to the full Stage-1 research proposal, use the separately maintained submission document.
