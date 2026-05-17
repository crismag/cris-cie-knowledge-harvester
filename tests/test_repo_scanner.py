from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from cie_harvester.scanners.repo_scanner import scan_repository


class RepoScannerTests(unittest.TestCase):
    def test_scans_repository_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "src" / "app").mkdir(parents=True)
            (repo / "tests").mkdir()
            (repo / "docs").mkdir()
            (repo / "pyproject.toml").write_text("[tool.poetry]\nname = \"demo\"\n", encoding="utf-8")
            (repo / "README.md").write_text("# Demo", encoding="utf-8")
            (repo / "tests" / "test_app.py").write_text("def test_demo():\n    pass\n", encoding="utf-8")
            result = scan_repository(repo)
            self.assertGreaterEqual(result["summary"]["total_files"], 3)
            self.assertIn("python", result["detected"]["languages"])
            self.assertIn("pyproject.toml", result["detected"]["package_files"])
