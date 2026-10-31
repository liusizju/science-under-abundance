# Interpretation limits

SUA Lab offers controlled comparisons between synthetic research environments. An LLM's choice in this environment is not a measurement of what an academic researcher would do.

## What the prototype demonstrates

- A live model can generate proposed research ideas, choose projects, allocate a stated budget, and respond to a priority prompt.
- Those tasks can be repeated across evaluation conditions with the same seed material.
- Prompts, raw responses, and analysis settings can be preserved for audit and reanalysis.
- A small two-family pilot produced both directional and uninformative comparisons.

## What remains unresolved

The pilot does not show whether AI increases human workload, causes plagiarism, reduces real verification quality, or leads researchers to pursue less novel work. The editorial-capacity model is stylized and cannot identify the best actual tenure or journal policy.

Two measurement issues are especially important.

**Verification budget.** The protocol requires agents to allocate 100 points. Accordingly, the mean allocation per retained project is always \`100 / n\`. A higher value after selecting fewer projects cannot independently support a claim about research quality. Assessing the substance of verification plans requires other measures.

**Idea similarity.** Shared vocabulary is not equivalent to the same contribution. Lexical overlap should be treated as a screening statistic until it is compared with semantic and blinded human judgments.

The original structured-output parser accepted some deviations from the instructions. The current runner records protocol warnings so these can be distinguished from parsing failures. We do not retroactively change the frozen October 2026 pilot.

## Competing explanations

Best-K evaluation could produce smaller portfolios while favoring conventional, easy-to-defend ideas. A priority threat could cause project abandonment instead of rushed submission. Different model families may respond in opposite directions.

These outcomes are relevant findings, not software failures. The purpose of the lab is to make such comparisons inspectable before drawing conclusions about real organizations.

All inputs are synthetic or shareable. Do not add confidential manuscripts, grant applications, reviews, or unpublished work belonging to others without the appropriate authorization.
