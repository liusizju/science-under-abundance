# Experiments: what would the SUA Lab help us learn?

The Stage-1 study is a **synthetic research instrument**, not a field experiment on actual scientists. Institutional rules are manipulated while the knowledge environment is held fixed. The three experiments below also state plausible outcomes that would challenge the original theory.

## 1. Does a common AI system narrow scientific search?

**Treatment:** common versus heterogeneous model families, different knowledge corpora, and actual capability differences (not merely a prompt saying "high AI").

**Unit:** independent agent-generated research ideas under the same assignment.

**Outcomes:** number of viable candidates, pairwise semantic and lexical similarity, near-duplicate clusters, topical coverage, and blind ratings of conceptual novelty.

Measure **all candidate ideas** separately from **ideas the agent elects to pursue**. Choosing which idea survives may create convergence even when initial ideation is diverse.

**Possible counterexample:** common-model assistance increases diversity or has no effect once output count is controlled.

## 2. Does selective evaluation improve scrutiny at the expense of exploration?

**Treatment:** broad-output evaluation versus best-two / best-K evaluation; separately manipulate verification demands and priority premiums.

**Stage-1 task:** generate four questions from a fixed synthetic corpus, choose a portfolio, allocate 100 verification points, respond to a possible competitor submission. See `configs/stage1_conditions.yaml`.

**Outcomes:** selected portfolio size, idea abandonment, candidate-versus-selected idea overlap, *substantive* quality of verification plans, falsification strategies, blinded novelty and quality ratings.

A useful rival mechanism in the V2 proposal is that a best-K rule can lower portfolio size while **funneling researchers toward safe questions**, thereby reducing exploration. We should not treat "fewer projects" as unconditionally better.

**Measurement warning:** 100 points are required by the prompt. Average budget/project is therefore algebraically `100/n`. It cannot independently establish that more checking occurred, nor does it establish more reliable science.

**Possible counterexamples:** best-K leaves project selection unchanged, produces greater convergence, or reduces scrutiny of nonselected but scientifically valuable directions.

## 3. Is stronger desk rejection preferable to upstream reform?

**Treatment:** reviewer capacity, desk threshold, noisy screening, resubmission probabilities, upstream publication rewards, and verification requirements.

**Outcomes:** primary projects and total submission attempts, editor/reviewer load, false negatives, resubmission displacement, and decision delay.

The stylized publication queue is currently **coded as inspectable rules**; genuine LLM editor and reviewer roles are a future extension.

**Possible counterexample:** higher desk-rejection thresholds protect scarce reviewers at low total social cost, with negligible resubmission displacement.

## Cross-cutting safeguards

- Compare actual model families and prompt variants. Preserve negative results.
- Pre-register measurement choices for the main study before interpreting semantic convergence.
- Use both embeddings and blinded human judgments to validate idea similarity and scientific distinctiveness.
- Validate the decision protocol itself: completion, violations of best-K rewards, allocation sums, and the share of generic or malformed outputs.
- Do not use confidential manuscripts or real peer-review material.
- Freeze complete prompts/responses and publish enough metadata for independent reruns, subject to model licensing.

The October 2026 two-family pilot demonstrates that the workflow runs and can exhibit model-specific outcomes. Its 36 trajectories are not confirmatory evidence or population estimates.
