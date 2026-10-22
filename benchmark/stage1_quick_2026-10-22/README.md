# Frozen Stage-1 open-weight pilot (2026-10-22)

This folder documents the first live-model proof-of-execution for SUA Lab.

## Design

- **Model families:** Qwen2.5-1.5B-Instruct and SmolLM2-1.7B-Instruct, Q4_K_M GGUF
- **Institutional conditions:** broad output evaluation (`quantity`), best-two evaluation (`best_k`), and broad output evaluation with a high priority premium (`high_priority`)
- **Replications:** 2 seeds × 3 independent agents per condition and model
- **Total trajectories:** 36
- **Valid structured trajectories:** 34 (94.4%)
- **Workflow commit:** `da51fe69e6ddaacbd7f8cde57216d718c552e231`
- **GitHub Actions run:** 39708296202

Each trajectory asked a live open-weight model to generate four candidate research ideas, choose which projects to pursue under the institutional rule, allocate a fixed 100-point human-verification budget, and respond to a priority shock.

## Descriptive traction, not confirmation

Two results are useful at Stage 1.

First, best-K evaluation moved project selection in the same direction in both model families. Relative to broad output evaluation, Qwen carried 2.17 rather than 2.83 projects on average; SmolLM2 carried 1.83 rather than 2.00. Because the verification budget was fixed, this also concentrated verification on retained projects.

Second, the pilot did **not** give blanket support to the other mechanisms. The priority shock produced a near-ceiling submit-now response even without the high-priority treatment, so the treatment did not generate an informative action contrast. Lexical idea-overlap patterns also differed across model families rather than showing a uniform convergence effect.

That mixture is the point of the pilot: the artifact can produce predicted, null, and model-specific patterns rather than mechanically replaying the analytical model.

## Frozen traces

The raw prompts and responses are preserved in the GitHub Actions artifacts for run 39708296202 and in the Stage-1 submission snapshot.

- `quick-qwen25-1.5b`: artifact 12395499859; SHA-256 `4f971eaa3ed005a24176d6f445aa6071980aaf82adb507b3cfc318225b848e38`
- `quick-smollm2-1.7b`: artifact 12396077772; SHA-256 `74c52b074a812e9b9da8c4716b540d83c8299d736749b2cc8aabd13db452e506`
- `stage1-quick-combined`: artifact 12396467583; SHA-256 `e265f883384b532fea074672633b02f4da39fd9aa18ce260d6fd0d5f01d640ad`

The pilot is intentionally too small for statistical inference and is not evidence about human researchers.
