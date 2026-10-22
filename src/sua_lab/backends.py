from __future__ import annotations
import json, os, random, urllib.request
from dataclasses import dataclass
from typing import Protocol

class Backend(Protocol):
    name: str
    def generate(self, prompt: str, *, seed: int | None = None) -> str: ...

@dataclass
class MockBackend:
    """Deterministic backend used for unit tests and plumbing demonstrations."""
    name: str = "deterministic-mock-v1"

    def generate(self, prompt: str, *, seed: int | None = None) -> str:
        rng = random.Random(seed or 0)
        high_ai = any(tag in prompt for tag in ["0.80", "0.81", "0.82", "0.83", "0.84", "0.85", "0.86", "0.87", "0.88", "0.89", "0.90", "0.91", "0.92", "0.93", "0.94", "0.95", "0.96", "0.97", "0.98", "0.99", "1.00"])
        mechanisms = (["verification scarcity", "priority racing", "evaluation breadth"] if high_ai else [
            "relative performance", "verification scarcity", "priority racing",
            "attention allocation", "evaluation breadth", "review congestion"
        ])
        outcomes = (["verification effort", "idea overlap", "workload"] if high_ai else [
            "workload", "idea overlap", "verification effort", "desk screening",
            "resubmission", "knowledge diversity"
        ])
        m1, m2 = rng.sample(mechanisms, 2)
        out = rng.choice(outcomes)
        return json.dumps({
            "question": f"How does {m1} interact with {m2} to shape {out}?",
            "mechanism": f"{m1} changes incentives while {m2} constrains adjustment.",
            "keywords": [m1, m2, out],
            "verification_plan": "Check assumptions, competing mechanisms, and one falsifying case."
        })

@dataclass
class OllamaBackend:
    model: str
    base_url: str = "http://localhost:11434"
    name: str = "ollama"

    def generate(self, prompt: str, *, seed: int | None = None) -> str:
        body = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"seed": seed} if seed is not None else {}
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))["response"]

@dataclass
class OpenAICompatibleBackend:
    model: str
    base_url: str
    api_key: str = ""
    name: str = "openai-compatible"

    def generate(self, prompt: str, *, seed: int | None = None) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
        }
        if seed is not None:
            payload["seed"] = seed
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"), headers=headers,
        )
        with urllib.request.urlopen(req, timeout=180) as resp:
            obj = json.loads(resp.read().decode("utf-8"))
            return obj["choices"][0]["message"]["content"]

def make_backend(kind: str, model: str):
    kind = kind.lower()
    if kind == "mock":
        return MockBackend()
    if kind == "ollama":
        return OllamaBackend(model=model)
    if kind in {"openai-compatible", "openai_compatible"}:
        return OpenAICompatibleBackend(
            model=model,
            base_url=os.environ.get("SUA_BASE_URL", "http://localhost:8000/v1"),
            api_key=os.environ.get("SUA_API_KEY", ""),
        )
    raise ValueError(f"Unknown backend: {kind}")
