# Reproducibility notes

The repository separates three layers that should not be conflated.

1. **Theory harness.** Portfolio, verification, and publication-capacity rules implement transparent stylized mechanisms. These are inspectable assumptions.
2. **Language-model layer.** In live runs, models generate semantic research objects (questions, mechanisms, and verification plans). Model identity is an experimental factor.
3. **Measurement layer.** Similarity, quality proxies, screening outcomes, and human ratings are analyzed separately from the generation process.

Every run writes:

- the configuration and random seed (`run_metadata.json`);
- the full prompt and raw response for each project (`traces.jsonl`);
- parsed project-level records (`projects.csv`);
- a compact run summary (`summary.json`).

The deterministic mock backend exists only to test plumbing. It does not encode semantic treatment effects and should never be cited as substantive evidence.

For the main experiments, the intended reference setup is an open-weight model available through a local runtime such as Ollama. Additional model families can be used as robustness treatments. If a commercial endpoint is used, raw traces will be cached when terms permit so downstream analysis does not depend on the model remaining unchanged.
