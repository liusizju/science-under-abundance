# Experimental agenda

SUA Lab is meant to make the institutions around AI-enabled knowledge production experimentally manipulable. The experiments below are the Stage-2 agenda, not claims already established by the Stage-1 smoke test.

## 1. Abundance and convergence

**Question.** Does AI assistance expand the number of plausible research directions while also making independent search paths more similar?

**Manipulations.** Common vs. heterogeneous model families; common vs. heterogeneous seed corpora; model capability.

**Primary outcomes.** Number of viable ideas; semantic similarity; topical coverage; near-duplicate clusters; blinded novelty ratings.

**Evidence against the mechanism.** If common-model assistance does not raise overlap relative to heterogeneous-model assistance after controlling for output volume, the idea-convergence channel is weakened. If stronger models expand coverage rather than concentrate it, the theory should be revised rather than re-labeled as support.

## 2. Evaluation rules and verification

**Question.** Do broad output rewards turn AI productivity into project proliferation, while selective evaluation shifts attention back toward fewer projects?

**Manipulations.** Output-count reward vs. best-K reward; verification requirement; priority premium.

**Primary outcomes.** Portfolio size; verification-plan depth; project abandonment; time-to-submit proxy; quality and distinctiveness ratings.

**Evidence against the mechanism.** If evaluation breadth does not change project entry or verification under the same AI environment, the institutional channel is not doing the work the theory assigns to it.

## 3. Where should the system intervene?

**Question.** When generation scales faster than review capacity, is it more effective to filter harder downstream or to change incentives upstream?

**Manipulations.** Reviewer capacity; desk threshold; editor-signal noise; resubmission probability; upstream evaluation rule.

**Primary outcomes.** Manuscript traffic; desk rejection; external-review load; repeated submissions; accepted-output quality; delay.

**Evidence against the mechanism.** If upstream evaluation changes manuscript traffic only trivially while downstream screening absorbs the shock without meaningful displacement, the proposed upstream-downstream substitution is weak.

## Validation strategy

- Replicate across multiple open-weight model families and prompt variants.
- Treat model family as a design factor rather than nuisance infrastructure.
- Use lexical, embedding, cluster, and blinded human ratings for idea similarity.
- Pre-specify primary outcomes and null/falsification patterns before the main grid runs.
- Release raw prompts, responses, parsed traces, and analysis code where provider terms permit.
