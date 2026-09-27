from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = (
    ROOT
    / "plugins"
    / "act4k1007-reclaimer"
    / "skills"
    / "act4k1007-reclaimer"
    / "scripts"
)
FIXTURES = ROOT / "tests" / "fixtures"


class ScriptTests(unittest.TestCase):
    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_DIR / name), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_exact_profile_matches(self) -> None:
        result = self.run_script(
            "verify_device.py", "--fixture", str(FIXTURES / "exact-match.json")
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout.split("\nExact profile match", 1)[0])["compatible"])

    def test_unknown_fingerprint_stops(self) -> None:
        result = self.run_script(
            "verify_device.py",
            "--fixture",
            str(FIXTURES / "wrong-fingerprint.json"),
        )
        self.assertEqual(result.returncode, 3)
        self.assertIn("STOP", result.stderr)

    def test_support_report_omits_transport_identifiers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            result = self.run_script(
                "support_report.py",
                "--fixture",
                str(FIXTURES / "exact-match.json"),
                "--output",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            serialized = json.dumps(report).lower()
            self.assertNotIn("serial", serialized)
            self.assertNotIn("mac_address", serialized)
            self.assertNotIn("android_id", serialized)


if __name__ == "__main__":
    unittest.main()
