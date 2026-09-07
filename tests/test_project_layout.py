"""Tests for the T009.03 continuous-integration contract."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.check_sensitive_paths import find_sensitive_paths  # noqa: E402


class ContinuousIntegrationContractTests(unittest.TestCase):
    def test_workflow_runs_root_tests_on_python_312(self) -> None:
        workflow = (PROJECT_ROOT / ".github/workflows/tests.yml").read_text(encoding="utf-8")

        self.assertIn('python-version: "3.12"', workflow)
        self.assertIn("python scripts/check_sensitive_paths.py --tracked", workflow)
        self.assertIn('python -m unittest discover -s tests -p "test*.py" -v', workflow)
        self.assertIn("contents: read", workflow)
        self.assertNotIn("continue-on-error", workflow)
        self.assertNotIn("|| true", workflow)

    def test_sensitive_path_policy_rejects_common_secret_files(self) -> None:
        candidates = [
            "src/qimen_core/__init__.py",
            ".env",
            "deploy/.env.production",
            "keys/service.pem",
            ".ssh/id_rsa",
            "ops/.aws/credentials",
            "config/credentials.json",
        ]

        self.assertEqual(
            find_sensitive_paths(candidates),
            [
                ".env",
                ".ssh/id_rsa",
                "config/credentials.json",
                "deploy/.env.production",
                "keys/service.pem",
                "ops/.aws/credentials",
            ],
        )

    def test_sensitive_path_policy_allows_normal_project_files(self) -> None:
        self.assertEqual(
            find_sensitive_paths(
                [
                    "pyproject.toml",
                    "src/qimen_core/__init__.py",
                    "tests/test_project_layout.py",
                    "docs/engineering/environment.md",
                ]
            ),
            [],
        )

    def test_failing_unittest_process_returns_nonzero(self) -> None:
        program = (
            "import unittest\n"
            "class IntentionalFailure(unittest.TestCase):\n"
            "    def test_failure(self): self.fail('intentional CI probe')\n"
            "unittest.main()\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", program],
            cwd=PROJECT_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAILED (failures=1)", result.stderr)
        self.assertIn("Ran 1 test", result.stderr)


if __name__ == "__main__":
    unittest.main()
