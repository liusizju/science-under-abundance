"""Regression checks for parsing, accounting, and simulation assumptions."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sua_lab.backends import MockBackend
from sua_lab.metrics import jaccard
from sua_lab.simulation import Config, Simulation


def benchmark_module():
    script = ROOT / "scripts" / "run_stage1_benchmark.py"
    spec = importlib.util.spec_from_file_location("benchmark_runner", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SimulationTests(unittest.TestCase):
    def test_new_idea_overlap_only_uses_its_own_comparisons(self):
        prior = ["alpha gamma", "delta epsilon"]
        actual = Simulation._overlap_with_prior("alpha beta", prior)
        expected = (jaccard("alpha beta", prior[0]) + 0.0) / 2
        self.assertAlmostEqual(actual, expected)

    def test_invalid_configurations_are_rejected(self):
        with self.assertRaises(ValueError):
            Config(n_researchers=0)
        with self.assertRaises(ValueError):
            Config(review_capacity=0)
        with self.assertRaises(ValueError):
            Config(best_k=0)
        with self.assertRaises(ValueError):
            Config(max_resubmissions=-1)

    def test_mock_responses_do_not_follow_institutional_prompts(self):
        backend = MockBackend()
        result_a = backend.generate("Output count is rewarded.", seed=24)
        result_b = backend.generate("Only the best two count.", seed=24)
        self.assertEqual(result_a, result_b)


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = benchmark_module()

    def test_noncompliant_allocations_are_flagged(self):
        record = {
            "ideas": [
                {"id": i, "question": f"Research question {i}"}
                for i in range(1, 5)
            ],
            "selected_ids": [1, 2],
            "verification": {"1": 25, "2": 35},
            "priority_response": {
                "action": "verify_more",
                "reason": "Check assumptions",
                "revised_verification": 50,
            },
        }
        decision = self.runner.normalize(record)
        self.assertIsNotNone(decision)
        self.assertAlmostEqual(decision["reported_verification_total"], 60)
        self.assertIn("allocation_sum_not_100", decision["protocol_warnings"])
        self.assertAlmostEqual(sum(decision["allocations"].values()), 100)

    def test_malformed_records_are_not_counted_as_valid(self):
        self.assertIsNone(self.runner.normalize(None))
        self.assertIsNone(self.runner.normalize({"ideas": [], "selected_ids": []}))
        self.assertIsNone(
            self.runner.normalize(
                {"ideas": [{"question": "A"}], "selected_ids": [42]}
            )
        )

    def test_grid_excludes_institutional_prompt_configurations(self):
        with tempfile.TemporaryDirectory() as temporary:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "run_grid.py"),
                    "--backend",
                    "mock",
                    "--out",
                    temporary,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            rows = json.loads(
                (Path(temporary) / "grid_summary.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                {row["condition"] for row in rows},
                {"baseline", "high_ai_bestk", "high_ai_quantity"},
            )


if __name__ == "__main__":
    unittest.main()
