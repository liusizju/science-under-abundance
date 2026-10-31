# Reproducing the SUA Lab pilot

SUA Lab has two execution paths. The deterministic model is useful for checking implementation details. The live-model protocol supplies the open-ended research choices used in the Stage-1 pilot. Their outputs should not be pooled or interpreted as equivalent evidence.

## Install and test

Python 3.11 or later is recommended.

\`\`\`bash
python -m pip install -r requirements.txt
python tests/test_smoke.py
python tests/test_stage1_v2.py
python tests/test_harness_quality.py
\`\`\`

The first test checks the stylized pipeline, the second checks the institutional-prompt interface and idea-overlap analysis, and the third checks parsing and selected simulation assumptions.

## Run the live protocol

Start a local model server with an OpenAI-compatible \`/v1/chat/completions\` endpoint:

\`\`\`bash
python scripts/run_stage1_benchmark.py \
  --base-url http://127.0.0.1:11434/v1 \
  --model YOUR_MODEL_ID \
  --model-label local-model \
  --conditions-file configs/stage1_conditions.yaml \
  --n-seeds 2 --n-agents 3 \
  --out live_runs/local_run
\`\`\`

The runner saves:

- \`raw_traces.jsonl\`: prompt, full model output, parsed object, treatment, seed, and protocol warnings.
- \`manifest.json\`: number of attempts, valid parses, model identifier, and commit ID.

The parser normalizes reported point allocations to 100 for comparison, but it also records the total originally reported by the model and flags deviations. Use the original raw response when evaluating protocol compliance.

To summarize two runs:

\`\`\`bash
python scripts/analyze_stage1_benchmark.py \
  live_runs/model_a/raw_traces.jsonl \
  live_runs/model_b/raw_traces.jsonl \
  --out live_runs/comparison
\`\`\`

The report separates lexical similarity among all proposed ideas from similarity among selected ideas. These metrics are exploratory until compared with semantic models and independent human ratings.

## Run the stylized theory harness

\`\`\`bash
python scripts/run_demo.py
python scripts/run_grid.py --backend mock
\`\`\`

The YAML files describing the theory scenarios contain \`ai_capability\`. Institutional prompt settings use a separate YAML schema and are excluded from the theory grid. Scenario results are written to \`sample_results/\` and should be described as simulated outputs.

## Frozen October 2026 pilot

The original reference run used GitHub Actions run **39708296202**, code commit \`da51fe69e6ddaacbd7f8cde57216d718c552e231\`, and Q4_K_M variants of Qwen2.5-1.5B-Instruct and SmolLM2-1.7B-Instruct.

There were 36 attempted trajectories and 34 structurally usable records. Historical summaries, original scripts at that commit, and artifact digests are documented in [benchmark/stage1_quick_2026-10-22/](benchmark/stage1_quick_2026-10-22/).

GitHub Actions artifacts expire. Preserve the separately frozen raw-trace snapshot when sharing or submitting the project. A new run on the current branch may differ because the software, runtime, or model weights have changed. Do not replace the historical results with new outputs under the same run identifier.

## Reporting limits

- The 100-point verification budget makes points per retained project an accounting measure, not a quality measure.
- A structurally usable JSON response may violate other experimental instructions. Review the recorded protocol warnings and source text.
- Lexical/Jaccard overlap is not equivalent to a scientifically duplicated idea.
- Model family, prompt wording, and corpus selection are possible sources of heterogeneity.
- No synthetic result in this repository estimates a causal effect on human researchers.

The benchmark is intended to generate questions and reveal conditions for later human or archival validation.
