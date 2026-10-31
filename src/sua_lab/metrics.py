"""Lightweight lexical diagnostics used by the prototype.

These measures are not substitutes for assessing conceptual novelty.
"""

from __future__ import annotations

import re
from itertools import combinations
from typing import Sequence

_WORD_PATTERN = re.compile(r"[a-zA-Z]{3,}")


def tokens(text: str) -> list[str]:
    return _WORD_PATTERN.findall(text.lower())


def jaccard(first: str, second: str) -> float:
    left, right = set(tokens(first)), set(tokens(second))
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def pairwise_overlap(texts: Sequence[str]) -> float:
    if len(texts) < 2:
        return 0.0
    return mean([jaccard(first, second) for first, second in combinations(texts, 2)])
