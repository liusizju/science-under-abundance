# Science Under Abundance (SUA Lab)

SUA Lab is an experimental environment for studying how research evaluation rules affect AI-assisted knowledge production. It combines open-ended idea generation with an inspectable model of portfolio decisions and editorial capacity.

A motivating question is whether cheaper idea generation leads researchers to pursue more projects than they can adequately assess. We also study competing explanations: selective evaluation might reduce marginal projects yet favor familiar topics, while priority competition might prompt researchers to rush, reframe, or abandon work.

This repository contains the Stage-1 prototype prepared for the *Organization Science* special issue **AI-Enabled Frontiers in Organizational Science**.

## Try the institutional comparison

The initial live-model experiment gives research agents the same synthetic literature and asks them to:

1. Propose four candidate research questions.
2. Select projects under a specified evaluation rule.
3. Allocate a fixed 100-point verification budget.
4. Respond to news of a competing submission.

The evaluation treatments are in [configs/stage1_conditions.yaml](configs/stage1_conditions.yaml):

| Treatment | Evaluation rule |
|---|---|
| Broad output | Each additional publishable project can contribute to evaluation |
| Best-two | Only the two strongest completed projects count |
| High priority | Broad-output evaluation with a larger reward for publishing first |

The primary comparisons concern portfolio selection, proposed verification activities, and the diversity of **retained** ideas as distinct from all generated candidates.

## Current implementation

The repository has two components with different purposes.

**Researcher-agent pilot.** [scripts/run_stage1_benchmark.py](scripts/run_stage1_benchmark.py) calls an OpenAI-compatible local inference server, records each prompt and raw response, and parses the project choices. The analysis script reports candidate and retained idea overlap, portfolio size, and priority-response frequencies. Parsing or protocol problems are retained in the trace.

**Stylized theory harness.** [src/sua_lab/](src/sua_lab/) models portfolio expansion, verification allocation, and screening under limited editorial capacity. Its equations and thresholds are assumptions, not behavioral estimates. The deterministic backend checks software plumbing only.

LLM-based editor and reviewer agents, validated novelty measures, and human calibration are not yet implemented.

## Installation and quick checks

Python 3.11 or later is recommended.

\`\`\`bash
python -m pip install -r requirements.txt
python tests/test_smoke.py
python tests/test_stage1_v2.py
python tests/test_harness_quality.py
\`\`\`

For the deterministic theory-harness example:

\`\`\`bash
python scripts/run_demo.py
\`\`\`

For a live researcher-agent run, start a local model server that supports the OpenAI-compatible chat-completions endpoint, then run:

\`\`\`bash
python scripts/run_stage1_benchmark.py \
  --base-url http://127.0.0.1:11434/v1 \
  --model YOUR_MODEL_ID \
  --model-label local-model \
  --conditions-file configs/stage1_conditions.yaml \
  --n-seeds 2 --n-agents 3 \
  --out live_runs/local_run
\`\`\`

The local server must already be running. Examples and methodological details appear in [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## Stage-1 pilot

The frozen October 2026 run used Qwen2.5-1.5B-Instruct and SmolLM2-1.7B-Instruct, with three institutional regimes, two seeds, and three agents per cell. There were **36 attempted trajectories and 34 structurally usable outputs**.

Both model families selected fewer projects under best-two evaluation in this small sample. Priority-action responses were near ceiling and lexical idea-overlap patterns differed between models. These observations motivate follow-up experiments; they do not estimate how human researchers behave.

A measurement caution matters here: under the fixed 100-point allocation, mean verification points per selected project equal \`100 / portfolio_size\` by construction. The figure is not an independent measure of verification quality.

Original results and run identifiers are in [benchmark/stage1_quick_2026-10-22/](benchmark/stage1_quick_2026-10-22/). This repository does not rewrite the frozen pilot when the software changes.

## Reuse

To examine another institutional mechanism, replace the [synthetic seed corpus](data/seed_corpus.jsonl) and edit [the YAML evaluation rules](configs/stage1_conditions.yaml). Researchers can replace the portfolio or screening equations without changing the model adapters or trace format.

The design, planned tests, and limitations are described in:

[Research design](docs/RESEARCH_DESIGN_V2.md) ·
[Experiments](EXPERIMENTS.md) ·
[Reproducibility](REPRODUCIBILITY.md) ·
[Interpretation limits](BOUNDARIES.md) ·
[File inventory](ARTIFACT_MANIFEST.md)

**License:** Code is MIT licensed. The synthetic corpus and documentation are intended for reuse under CC BY 4.0.
