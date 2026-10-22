from __future__ import annotations
import json, os, random, urllib.request
from dataclasses import dataclass
from typing import Protocol

class Backend(Protocol):
    name: str
    def generate(self, prompt: str, *, seed: int | None = None) -> str: ...

@dataclass
class MockBackend:
    """Deterministic backend for plumbing tests only.

    The mock deliberately does not condition its semantic output on the treatment
    parameters. It is used to verify logging, parsing, and simulation mechanics;
    it is not evidence for idea convergence or any behavioral prediction.
    """
    name: str = "deterministic-mock-v2"

    def generate(self, prompt: str, *, seed: int | None = None) -> str:
        rng = random.Random(seed or 0)
        concepts = [
            "relative performance", "verification scarcity", "priority racing",
            "attention allocation", "evaluation breadth", "review congestion",
            "professional judgment", "exploration", "algorithmic homogenization",
            "expert screening", "career incentives", "knowledge diversity"
        ]
        outcomes = [
            "workload", "verification effort", "idea diversity", "project selection",
            "review burden", "resubmission", "novelty", "quality", "abandonment"
        ]
        m1, m2 = rng.sample(concepts, 2)
        out = rng.choice(outcomes)
        return json.dumps({
            "question": f"When does {m1} change how {m2} shapes {out}?",
            "mechanism": f"The proposed mechanism links {m1} to {m2} through a change in incentives or scarce attention.",
            "keywords": [m1, m2, out],
            "verification_plan": "State a competing mechanism, identify one falsifying pattern, and specify what evidence would discriminate between them."
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
