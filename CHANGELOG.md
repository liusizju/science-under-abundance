# Development notes

## October 2026: code and documentation review

This revision focuses on readability, reproducibility, and clearer separation between simulation assumptions and measured LLM outputs.

- Organized the Python code into smaller functions with consistent names, argument validation, and explicit output formats.
- Corrected the stylized simulator's overlap calculation to compare each new idea with earlier ideas rather than averaging unrelated historical pairs. This changes future mock outputs; it does not change the frozen live-model pilot.
- Updated the benchmark prompt with a valid four-idea JSON example and improved numeric-allocation checks. The raw response remains available; normalization and protocol warnings are separate fields.
- Made the analysis report include all attempted model-by-condition cells, including cells with zero usable responses.
- Clarified the accounting nature of the 100-point verification allocation. Work on validation quality remains an open research task.
- Simplified the repository documentation and added tests for protocol compliance and key implementation details.
- Removed an unused HTTP dependency and excluded generated local outputs from version control.

### Historical results

The Stage-1 live-model pilot recorded on October 22, 2026 is tied to commit \`da51fe69e6ddaacbd7f8cde57216d718c552e231\` and GitHub Actions run \`39708296202\`. Its recorded outputs and digests have not been rewritten.

Any analysis produced with the current code should be labeled as a new run or an exploratory reanalysis. Differences between versions should not be interpreted as additional evidence for the underlying theory.

### Research integrity

The repository still identifies AI models, their roles in the protocol, and the limits of synthetic inference. Editorial revisions to code and prose do not alter the provenance of the research.
