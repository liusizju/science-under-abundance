from __future__ import annotations
import re

def tokens(text: str):
    return re.findall(r"[a-zA-Z]{3,}", text.lower())

def jaccard(a: str, b: str) -> float:
    A, B = set(tokens(a)), set(tokens(b))
    if not A and not B: return 1.0
    if not A or not B: return 0.0
    return len(A & B) / len(A | B)

def pairwise_overlap(texts: list[str]) -> float:
    if len(texts) < 2: return 0.0
    vals = []
    for i in range(len(texts)):
        for j in range(i+1, len(texts)):
            vals.append(jaccard(texts[i], texts[j]))
    return sum(vals)/len(vals)

def mean(xs):
    return sum(xs)/len(xs) if xs else 0.0
