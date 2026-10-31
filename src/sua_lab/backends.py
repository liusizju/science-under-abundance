"""Model adapters for local and OpenAI-compatible inference servers."""

from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
from typing import Protocol
from urllib.request import Request, urlopen


class Backend(Protocol):
    name: str

    def generate(self, prompt: str, *, seed: int | None = None) -> str:
        ...


def _post_json(url: str, payload: dict, headers: dict | None = None) -> dict:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})},
    )
    with urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


@dataclass
class MockBackend:
    """Repeatable fixture for testing the pipeline, not researcher behavior."""

    name: str = "deterministic-mock-v2"

    def generate(self, prompt: str, *, seed: int | None = None) -> str:
        # Deliberately independent of prompt content and institutional treatment.
        rng = random.Random(seed if seed is not None else 0)
        concepts = [
            "relative performance",
            "verification scarcity",
            "priority racing",
            "attention allocation",
            "evaluation breadth",
            "review congestion",
            "professional judgment",
            "exploration",
            "algorithmic homogenization",
            "expert screening",
            "career incentives",
            "knowledge diversity",
        ]
        outcomes = [
            "workload",
            "verification effort",
            "idea diversity",
            "project selection",
            "review burden",
            "resubmission",
            "novelty",
            "quality",
            "abandonment",
        ]
        first, second = rng.sample(concepts, 2)
        outcome = rng.choice(outcomes)

        return json.dumps(
            {
                "question": (
                    f"When does {first} change how {second} shapes {outcome}?"
                ),
                "mechanism": (
                    f"The proposed mechanism links {first} to {second} through "
                    "a change in incentives or scarce attention."
                ),
                "keywords": [first, second, outcome],
                "verification_plan": (
                    "State a competing mechanism, identify one falsifying pattern, "
                    "and specify what evidence would discriminate between them."
                ),
            }
        )


@dataclass
class OllamaBackend:
    model: str
    base_url: str = "http://localhost:11434"
    name: str = "ollama"

    def generate(self, prompt: str, *, seed: int | None = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"seed": seed} if seed is not None else {},
        }
        response = _post_json(
            f"{self.base_url.rstrip('/')}/api/generate", payload
        )
        return response["response"]


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

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = _post_json(
            f"{self.base_url.rstrip('/')}/chat/completions",
            payload,
            headers=headers,
        )
        return response["choices"][0]["message"]["content"]


def make_backend(kind: str, model: str) -> Backend:
    normalized = kind.lower().replace("_", "-")
    if normalized == "mock":
        return MockBackend()
    if normalized == "ollama":
        return OllamaBackend(model=model)
    if normalized == "openai-compatible":
        return OpenAICompatibleBackend(
            model=model,
            base_url=os.environ.get("SUA_BASE_URL", "http://localhost:8000/v1"),
            api_key=os.environ.get("SUA_API_KEY", ""),
        )
    raise ValueError(f"Unsupported backend: {kind}")
