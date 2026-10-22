# Science Under Abundance (SUA) Lab

SUA Lab is an early research prototype for a simple question: **what happens to a knowledge system when producing candidate work becomes cheap before the capacity to verify and evaluate it scales?**

The scientific setting is useful because the bottleneck is visible. AI can help generate questions, code, analyses, and prose quickly, while researchers, editors, and reviewers still have finite attention. SUA Lab turns that mismatch into an experimental object. It lets researchers vary the production technology and the institutions around it in the same environment.

This is deliberately a prototype rather than a synthetic claim about how scientists behave.

## What is implemented now

The Stage-1 repository contains:

- LLM-backed generation of structured research ideas and verification plans;
- transparent theory-harness rules for portfolio size, scarce verification, priority pressure, desk screening, and bounded resubmission;
- experiment configurations for broad output incentives and best-K evaluation;
- adapters for a deterministic plumbing test, local Ollama models, and OpenAI-compatible endpoints;
- run-level logging of configuration, prompts, raw responses, parsed records, and derived metrics;
- a synthetic, redistributable seed corpus;
- smoke tests that verify the pipeline without treating mock outputs as scientific findings.

LLM-based editor and reviewer agents, human validation, and cross-model benchmark runs are **Stage-2 work**, not completed Stage-1 features.

## Three questions for the lab

1. **Abundance and convergence.** Can AI increase the number of plausible ideas while making independent search paths more correlated?
2. **Evaluation and verification.** Does broad output-based evaluation convert AI productivity into more projects and thinner scrutiny, while best-K evaluation changes that allocation?
3. **Where to intervene.** When manuscript generation outruns expert review, is the better response to screen harder downstream or to change incentives upstream?

See [`EXPERIMENTS.md`](EXPERIMENTS.md) for planned tests and explicit falsification patterns.

## Quick start: deterministic plumbing test

```bash
python scripts/run_demo.py
```

The deterministic backend is an engineering fixture. It does **not** encode an AI-induced semantic convergence effect and its outputs are not evidence for the substantive theory.

## Live model mode

### Ollama

```bash
python scripts/run_experiment.py --backend ollama --model llama3.1:8b --config configs/baseline.yaml --out sample_results/ollama_baseline
```

### OpenAI-compatible endpoint

```bash
export SUA_BASE_URL="http://localhost:8000/v1"
export SUA_API_KEY="optional"
python scripts/run_experiment.py --backend openai-compatible --model your-model --config configs/baseline.yaml --out sample_results/compatible_baseline
```

### Run the configuration grid

```bash
python scripts/run_grid.py --backend mock
```

For substantive experiments, replace `mock` with an accessible live backend.

## Stage-1 live-model pilot

A frozen 36-trajectory open-weight pilot has now been run with Qwen2.5-1.5B-Instruct and SmolLM2-1.7B-Instruct across three institutional regimes. The pilot produced 34 valid structured trajectories. Best-K evaluation reduced selected portfolio size in both model families; the priority-action and idea-convergence margins were mixed or uninformative at this scale. We treat that mixture as evidence that the lab can return null and model-specific patterns rather than as confirmatory evidence.

See [`benchmark/stage1_quick_2026-10-22/`](benchmark/stage1_quick_2026-10-22/) for the frozen design, descriptive summary, workflow identifiers, and artifact digests. Raw prompts and responses are preserved in the GitHub Actions artifacts and the submission snapshot.

## Reproducibility

Each run writes the complete configuration, random seed, prompt, raw model response, parsed record, and summary metrics. See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Boundaries

LLM agents are computational probes, not estimates of human behavior. A failed replication across models or a mismatch with human judgments is scientifically informative. See [`BOUNDARIES.md`](BOUNDARIES.md).

## Stage-1 proposal

Prepared for the *Organization Science* special issue **AI-Enabled Frontiers in Organizational Science**.

## License

Code: MIT License. Synthetic seed corpus and documentation: CC BY 4.0.
