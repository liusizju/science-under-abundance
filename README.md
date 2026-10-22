# Science Under Abundance (SUA) Lab — Stage-1 Prototype

SUA Lab is a small, reusable multi-agent research sandbox for studying how AI-enabled research generation interacts with human verification, scientific priority, and scarce editorial/reviewer capacity.

This repository is a **proof of concept**, not a behavioral model of scientists. Its purpose is to make theoretical mechanisms inspectable and experimentally manipulable. The Stage-1 package includes a deterministic backend for reproducible smoke tests and adapters for locally accessible LLM infrastructure.

## What the prototype does

A run creates a synthetic scientific field with:

- **Researcher agents** that generate project ideas, choose a portfolio size, allocate verification effort, and decide when to submit.
- **Editor/reviewer capacity** that screens submissions and creates congestion when manuscript traffic grows.
- **Institutional reward regimes** that can emphasize quantity, best-K output, or scientific priority.
- **Metrics** for project volume, idea overlap, verification per project, desk rejection, external-review load, and resubmission traffic.

The current prototype is designed around three experiments:

1. **Generation and convergence** — does common AI assistance expand idea volume while increasing overlap?
2. **Quantity vs. best-K evaluation** — do broad output incentives amplify project proliferation and verification dilution?
3. **Publication bottleneck** — can stricter desk screening protect reviewers while shifting work into resubmission?

## Quick start (deterministic smoke test)

```bash
python scripts/run_demo.py
```

Outputs are written to `sample_results/`.

## Live LLM mode

### Ollama (recommended for reproducibility/accessibility)

```bash
python scripts/run_experiment.py --backend ollama --model llama3.1:8b --config configs/baseline.yaml
```

### OpenAI-compatible endpoint

```bash
export SUA_BASE_URL="http://localhost:8000/v1"
export SUA_API_KEY="optional"
python scripts/run_experiment.py --backend openai-compatible --model your-model --config configs/baseline.yaml
```

The project deliberately does not require one proprietary provider. All prompts, model identifiers, seeds, and raw responses are logged.

## Reproducibility

Each run records configuration and random seed, backend and model identifier, prompt text, raw model response, parsed agent decision, and derived metrics.

For nondeterministic LLM backends, cached traces can be shared so downstream analyses can be reproduced exactly.

## Important boundary

SUA Lab does **not** assume that LLM agents faithfully represent human researchers. The artifact is a theory-building and institutional-design laboratory. Human validation and cross-model robustness are part of the planned Stage-2 development.

## Associated proposal

Organization Science Special Issue: *AI-Enabled Frontiers in Organizational Science* (Stage-1 submission package, 2026).

## License

Code: MIT License. Synthetic seed corpus and documentation: CC BY 4.0.
