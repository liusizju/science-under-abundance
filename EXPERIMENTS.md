# Experimental plan

The central comparison is between the behavior of researcher agents under different institutional rules, holding their starting information constant. The following experiments are proposals for Stage 2; the frozen 36-trajectory pilot demonstrates feasibility, not the outcomes of these tests.

## 1. Idea generation and selection

**Question.** Does using the same model make research trajectories more similar? Does an evaluation rule subsequently amplify or reduce that similarity?

Vary model family, whether agents share a model or use different models, and the seed corpus. Count distinct ideas and measure overlap separately for all generated candidates and the subset chosen for development.

The lexical Jaccard metric in the prototype is only a first diagnostic. Planned measures include embeddings, clustering, and blinded expert assessments of whether two ideas are substantively distinct.

A stronger model or shared model could broaden search rather than narrow it. That outcome would challenge the proposed convergence mechanism.

## 2. Evaluation breadth and research choices

**Question.** Does limiting evaluation to a researcher's best outputs encourage deeper investigation, or does it steer project selection toward safer questions?

Compare broad-output rewards with best-K evaluation, keeping the task and corpus the same. Record which ideas agents retain, which they abandon, and what checking and falsification activities their plans specify. Vary priority rewards independently.

Because the initial protocol fixes a total budget of 100 verification points, more points per project follow automatically when fewer projects are retained. Verification *quality* must instead be assessed from the planned checks and, subsequently, by independent raters.

An important alternative is that best-K decreases project count while increasing concentration on familiar research topics. Smaller portfolios would then involve a trade-off with exploration rather than an unqualified improvement.

## 3. Research volume and editorial capacity

**Question.** When submissions grow, does stricter desk screening conserve scarce reviewer attention or mainly displace work into repeated submissions?

Within the stylized publication environment, vary review capacity, editorial signal noise, desk thresholds, and resubmission behavior. Compare these changes with earlier interventions in researcher evaluation.

The outcomes of interest are total submission attempts, external reviews, delayed decisions, erroneous rejections, and workload displaced across journals. The first version uses transparent screening equations; LLM editor and reviewer roles remain planned work.

A finding that strict screening protects reviewer capacity with little resubmission burden would weaken the case for upstream incentive reform.

## Evidence and safeguards

Runs will retain prompts, raw responses, model details, seeds, and analysis parameters. The main comparisons should be checked across model families and prompt variants rather than interpreted from a single LLM.

Human experts will evaluate selected idea pairs and verification plans without seeing the agents' treatment labels. We will report failed parses, protocol violations, null comparisons, and model-specific effects alongside successful runs.

No confidential submissions, referee reports, or private research conversations are used as inputs.
