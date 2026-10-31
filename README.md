# Science Under Abundance (SUA) Lab

**A research instrument for varying the institutions of scientific discovery.**

Scientific ideas, code, and draft analyses can now be generated quickly. Deciding which ideas deserve attention, which results are credible, and which contributions are distinctive still takes scarce expert judgment. SUA Lab makes the rules around that judgment experimentally changeable.

The current research application is the *Organization Science* special issue, **AI-Enabled Frontiers in Organizational Science**. This repository contains the executable prototype and its reproducibility record. The associated Stage-1 proposal (revised after Mei Yang's feedback, V2) is a separate submission document, not a finished empirical paper.

## One experiment in concrete terms

Give two cohorts of AI-assisted researcher agents the **same synthetic knowledge base**.

- **Broad-output cohort:** additional publishable projects can improve the agent's evaluation.
- **Best-two cohort:** only the two strongest completed projects count.

Each agent is asked, in one structured LLM response, to generate four candidate questions, choose which to pursue, allocate a fixed 100-point verification budget across those projects, and react to a possible competing submission.

We can then examine which ideas are pursued, not just how many were proposed. A best-two rule might discourage marginal projects; it might also encourage agents to favor safe, familiar questions. The second possibility is an **alternative hypothesis**, not a finding.

This is the key distinction in the V2 research design: **candidate idea diversity and retained idea diversity are separate outcomes**. The analysis code reports both.

## What is implemented

- A **live-model protocol** for candidate generation, portfolio selection, verification allocation, and a priority response, using editable institutional prompts in [`configs/stage1_conditions.yaml`](configs/stage1_conditions.yaml).
- A separate **stylized theory harness** for portfolio costs, verification, and editorial congestion (`src/sua_lab/`).
- A lightweight publication layer with noisy screening, limited review capacity, and bounded resubmission.
- Ollama and OpenAI-compatible adapters, plus a deterministic backend for engineering checks.
- A frozen **two-family / three-regime pilot** with raw-trace artifacts and reproducibility metadata.

The prototype **does not yet contain LLM editor/reviewer agents, human-calibrated decisions, or validated measures of scientific novelty**. Those belong to the planned research program.

## What the October 2026 pilot did—and did not show

The first live pilot used Qwen2.5-1.5B-Instruct and SmolLM2-1.7B-Instruct: 2 models × 3 institutional regimes × 2 seeds × 3 agents = **36 trajectories**. Under the prototype parser, **34 records were structurally usable**.

Best-two evaluation was associated with smaller selected portfolios in both model families. The priority response was already near the "submit now" ceiling in the baseline, while lexical idea-overlap patterns differed across models. Neither result justifies a general claim about researchers.

**Important measurement boundary:** because agents were instructed to allocate a fixed 100-point verification budget, the average number of points per retained project is mechanically `100 / portfolio_size`. It is **not independent evidence that agents chose to verify more deeply**. The next study must measure verification *quality and content* separately.

See [`benchmark/stage1_quick_2026-10-22/`](benchmark/stage1_quick_2026-10-22/) and [`docs/RESEARCH_DESIGN_V2.md`](docs/RESEARCH_DESIGN_V2.md).

## Run locally

**Engineering smoke test (no model required):**

```bash
python tests/test_smoke.py
```

**One live-model experiment using the editable institutional rules:**

```bash
pip install -r requirements.txt
python scripts/run_stage1_benchmark.py \
  --base-url http://127.0.0.1:11434/v1 \
  --model YOUR_LOCAL_MODEL \
  --model-label your-model \
  --conditions-file configs/stage1_conditions.yaml \
  --n-seeds 2 --n-agents 3 \
  --out live_runs/my_experiment
```

The server must already be running and exposing an OpenAI-compatible `/v1/chat/completions` endpoint. For the stylized theory harness instead, run `python scripts/run_demo.py`.

## Reuse without adopting our theory

Fork the repository, replace [`data/seed_corpus.jsonl`](data/seed_corpus.jsonl), and edit [`configs/stage1_conditions.yaml`](configs/stage1_conditions.yaml) to compare a different institutional rule. The generation and trace-logging infrastructure does not require you to accept the project's workload or priority-race hypotheses.

The lab's most valuable output may be a counterexample: a selective evaluation rule that narrows exploration, or a priority signal that leads agents to abandon crowded topics rather than rush publication.

[Experiments and falsification](EXPERIMENTS.md) · [Reproducibility](REPRODUCIBILITY.md) · [Boundaries](BOUNDARIES.md) · [Artifact manifest](ARTIFACT_MANIFEST.md)

## License

Code is MIT licensed. The synthetic seed corpus and documentation are intended for reuse under CC BY 4.0.
