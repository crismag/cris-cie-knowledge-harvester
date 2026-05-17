from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from cie_harvester.scanners.structure_inventory import build_inventory


class InventoryBuilderTests(unittest.TestCase):
    def test_build_inventory_contains_required_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "README.md").write_text("# Demo", encoding="utf-8")
            source = {
                "name": "demo",
                "repo_url": "https://example.com/demo.git",
                "domain": "project_management",
            }
            inventory = build_inventory(source, repo)
            self.assertEqual(inventory["source_name"], "demo")
            self.assertIn("summary", inventory)
            self.assertIn("detected", inventory)
