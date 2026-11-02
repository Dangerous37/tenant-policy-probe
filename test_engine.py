import json
import subprocess
import sys
import unittest
from pathlib import Path

from engine import evaluate


def example():
    return json.loads(Path(__file__).with_name("example.json").read_text(encoding="utf-8"))


class AcceptanceTests(unittest.TestCase):
    def test_example_cli(self):
        proc = subprocess.run([sys.executable, "cli.py", "example.json"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), evaluate(example()))

    def test_full_matrix(self):
        result = evaluate(example())
        self.assertTrue(result["passed"])
        self.assertEqual([r["observed"] for r in result["cases"]], [204,403,204,404,404,401])
        self.assertNotIn("demo-edit", str(result))

    def test_detects_policy_mismatch(self):
        data = example()
        data["cases"][1]["expected"] = 204
        self.assertFalse(evaluate(data)["passed"])
