# Research design: Science Under Abundance

*October 2026 Stage-1 proposal, revised after feedback from Mei Yang.*

The scientific setting is a useful case of a broader organizational problem: technology reduces the cost of generating candidate work more rapidly than the cost of evaluating it.

We study that gap by holding a synthetic knowledge environment fixed while varying evaluation rules, priority rewards, and editorial capacity. LLMs supply open-ended research proposals; a separate, inspectable simulation supplies portfolio and publication-system mechanisms. The two parts are deliberately distinguished.

## A testable comparison

Give agents the same seed material and ask each to propose four questions, select a portfolio, allocate a fixed 100-point verification budget, and respond to a competing submission.

Under **broad-output evaluation**, additional publishable projects may improve career standing. Under **best-two evaluation**, only the two strongest completed projects count. The experiment records which questions are retained, not just how many are produced.

The initial idea was that selective evaluation would dampen portfolio proliferation. An equally important alternative is that agents might select familiar, lower-risk topics when only a few outputs count. Both explanations should be evaluated, rather than declaring smaller portfolios a desirable result by definition.

## Three experimental lines

**Idea overlap.** Compare shared versus heterogeneous model families and information sources. Measure overlap among candidate ideas and among retained ideas separately. Check lexical results against semantic comparisons and blinded expert assessments.

**Evaluation and verification.** Compare broad-output with best-K assessment while varying priority rewards and verification demands. Inspect the *content* of checking and falsification plans. Because the initial budget is fixed at 100 points, allocations per project are not independent evidence of diligence.

**Publication capacity.** Pass candidate work through a stylized editorial layer. Compare increased review capacity or stricter screening against upstream changes in researcher evaluation. Account for resubmission work rather than observing a single journal's queue only.

## What the first pilot provides

Two small open-weight model families completed a 36-trajectory pilot in October 2026, with 34 usable structured outputs. Best-two evaluation was associated with smaller portfolios in both models. Priority responses were near ceiling, while idea similarity was not uniform across models.

These are feasibility observations. There is no evidence here about actual working hours, misconduct, or real publication outcomes. LLM-based editors and reviewers have not been built, and measures of research quality still require human validation.

The original pilot outputs, model identifiers, and run metadata remain frozen. Later exploratory reanalysis distinguishing candidate and retained ideas is kept separate from the original results.

## What would change the interpretation?

An evaluation rule that produces fewer projects but more concentrated research directions would reveal a different trade-off from the original workload story. A priority prompt that leads agents to abandon crowded topics would similarly challenge a pure racing mechanism. Results that disappear across models or after blind human review would indicate the limit of this synthetic approach.

A successful research instrument should make those counterexamples visible and reproducible, even when they weaken its initial theory.
