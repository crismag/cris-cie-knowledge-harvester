from __future__ import annotations

import unittest
from pathlib import Path
from cie_harvester.scanners.file_classifier import classify_file


class FileClassifierTests(unittest.TestCase):
    def test_classifies_test_docs_and_package_files(self) -> None:
        self.assertEqual(classify_file(Path("README.md"))["category"], "docs")
        self.assertTrue(classify_file(Path("tests/test_demo.py"))["is_test"])
        self.assertTrue(classify_file(Path("pyproject.toml"))["is_package"])
