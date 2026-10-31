# Repository inventory

| Location | Contents |
|---|---|
| \`src/sua_lab/\` | Model adapters, single-project prompts, lexical diagnostics, and the stylized simulation |
| \`scripts/run_stage1_benchmark.py\` | Live researcher-agent protocol; editable evaluation conditions and raw trace logging |
| \`scripts/analyze_stage1_benchmark.py\` | Descriptive comparison by model and treatment, including selected-idea overlap |
| \`configs/stage1_conditions.yaml\` | Three institutional rules used by the live protocol |
| \`data/seed_corpus.jsonl\` | Synthetic literature-like prompts; no confidential documents |
| \`scripts/run_demo.py\` | Deterministic engineering demonstration |
| \`scripts/run_experiment.py\` | Single stylized theory scenario with a chosen backend |
| \`scripts/run_grid.py\` | Theory-scenario grid (excludes institutional-prompt YAML) |
| \`configs/baseline.yaml\` and \`configs/high_ai_*.yaml\` | Parameters for the stylized theory harness |
| \`tests/\` | Offline checks for reproducibility, parsers, scenario configuration, and calculations |
| \`benchmark/stage1_quick_2026-10-22/\` | Historical two-family pilot metadata, descriptive results, and reanalysis notes |
| \`docs/RESEARCH_DESIGN_V2.md\` | Scientific questions and planned discriminating tests |

The original pilot is tied to its historical commit. The current branch contains a code-quality refactor; updated analyses should be labeled separately from that pilot.

## Planned additions

The current prototype does not yet have LLM editor or reviewer agents, validated verification-quality metrics, or blinded novelty ratings. These remain necessary for more substantive claims about scientific competition and evaluation.

An independent researcher should be able to replace the source corpus or evaluation YAML and rerun a treatment comparison without editing the logging infrastructure. See [README.md](README.md) and [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

**Licenses:** MIT for code; CC BY 4.0 is the stated reuse intention for the synthetic data and documentation.
