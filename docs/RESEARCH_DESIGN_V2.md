# Stage-1 research design, V2 (Mei Yang revisions)

This document tracks the **research design represented by the revised proposal**. It is a research-facing guide to the artifact, not a substitute for the separately submitted four-page proposal.

## The question

What changes when AI makes candidate research output cheap while human verification and editorial attention remain scarce?

The organizational contribution is to **experimentally vary the institutions around researchers**, not to treat a synthetic LLM agent as a real scientist. Evaluation rules, priority rewards, and review capacity become treatments within a controlled synthetic information environment.

## A concrete comparison

Give two groups of researcher agents identical source material:

| Rule | Broad-output evaluation | Best-two evaluation |
|---|---|---|
| Career signal | Each additional publishable contribution can count | Only the two strongest finished contributions count |
| Task | Generate four candidate ideas; select projects; allocate 100 verification points | Exactly the same task |
| Main comparison | Portfolio size; which ideas are retained; verification-plan quality | Same outcomes, holding the source material fixed |

In the existing Stage-1 live protocol, each agent responds once with four candidate ideas, selected IDs, a proposed allocation of 100 points, and a response to a priority threat.

**Do not equate the accounting identity `100 / number_of_projects` with verified quality.** Verification-plan specificity, falsification checks, and substantive robustness need independent assessment.

## The three experiments

### A. Abundance and idea convergence

Manipulate common vs. heterogeneous model families, seed corpora, and genuine model capabilities. Measure candidate-question overlap, **selected-question overlap**, topic coverage, near-duplicate clusters, and blinded expert assessments. A purely lexical overlap statistic is diagnostic but not proof of scientific duplication.

Alternative: a stronger or more diverse model broadens the scientific search space rather than narrowing it.

### B. Quantity versus quality under reward rules

Manipulate broad-output versus best-K evaluation, verification requirements, and priority rewards. Measure project entry, project abandonment, content of verification plans, selected-idea novelty, and external quality judgments.

**Competing mechanism introduced in V2:** best-K can reduce project count but concentrate selected ideas in defensible, conventional areas. This would be a meaningful institutional trade-off: more scrutiny per retained project, but potentially less exploration. It remains a question for Stage 2, not an established pilot result.

### C. Upstream incentives versus downstream filtering

Route generated submissions through a capacity-constrained editorial model. Vary desk screening, reviewer capacity, resubmission probability, and upstream performance rules. Compare *system-wide* work and quality, not only the queue at a single journal.

## What Stage 1 already establishes

- An executable multi-stage **structured prompt protocol** on two small, independently developed open-weight model families.
- A separate inspectable theory harness and a stylized publication simulation.
- A frozen pilot of **36 trajectories; 34 parsable records**. Best-two evaluation reduced portfolio size in both model families; priority response had a ceiling effect, and lexical convergence was model-dependent.
- Reproducibility metadata: prompts, raw responses, seeds, model identities, commit ID, and artifact digests.

The pilot is a feasibility demonstration. It **does not estimate human researchers' responses** and does not establish scientific novelty or actual time spent verifying papers.

## What is not yet built

LLM editor/reviewer agents, semantic embeddings, calibrated verification quality, human blinded ratings, and a multi-family reference benchmark beyond the two-family pilot.

## Source separation and public disclosure

The research design here reflects the revised proposal, but the full unpublished DOCX/PDF is **not automatically posted** in this code repository. This allows the software artifact to become public without requiring the manuscript itself to be published early.

The 22 October frozen pilot is identified by GitHub Actions run `39708296202`, historical workflow commit `da51fe69e6ddaacbd7f8cde57216d718c552e231`, and the SHA-256 values recorded in `benchmark/stage1_quick_2026-10-22/README.md`. Historical traces must never be overwritten to make the newer analysis look more favorable.
