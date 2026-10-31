# Exploratory V2 reanalysis: candidate ideas versus selected ideas

**Not part of the original frozen Stage-1 pilot report.** This supplementary diagnostic was added after the Mei Yang V2 revision, which raised the possibility that narrower evaluation could concentrate researchers' selections on safer topics.

## Method

Using the exact raw trajectories from GitHub Actions run `39708296202`, calculate lexical token-set Jaccard overlap across all ideas **proposed** in a model × condition cell, then repeat using only ideas whose IDs were **selected** by agents. The original benchmark summaries and raw prompts/responses were not altered.

| Model | Evaluation | Candidate Jaccard | Selected Jaccard | Valid agents |
|---|---|---:|---:|---:|
| Qwen2.5-1.5B | Broad output | 0.1353 | 0.1701 | 6 |
| Qwen2.5-1.5B | Best-two | 0.1500 | 0.1579 | 6 |
| Qwen2.5-1.5B | High priority | 0.1295 | 0.1267 | 6 |
| SmolLM2-1.7B | Broad output | 0.1830 | 0.2237 | 5 |
| SmolLM2-1.7B | Best-two | 0.1858 | 0.2031 | 6 |
| SmolLM2-1.7B | High priority | 0.1316 | 0.1189 | 5 |

Interpretation: selected ideas are somewhat more lexically similar than all candidates under broad-output evaluation in both model families. Selected-idea overlap in the best-two regime is lower than broad-output overlap in this small pilot, but this is neither a validated novelty measure nor evidence of the causal effect of best-K rules.

**What it does not establish:** that an agent chose safer ideas, that substantive novelty changed, that a human researcher would behave the same way, or that these differences would survive alternative seeds or model sizes.

The point of recording this diagnostic is to distinguish the **generation margin** from the **selection margin**, which the original Stage-1 summary did not separate. Future work must use embeddings, clustering, and blinded ratings, and should specify the unit of comparison before interpreting similarity.

Re-run the calculation on the frozen raw JSONL files using the updated `scripts/analyze_stage1_benchmark.py` (the new `selected_idea_jaccard` field). The historical baseline `benchmark_summary.json` remains unchanged.
