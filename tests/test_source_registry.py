from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from cie_harvester.sources.source_registry import add_source, find_source, list_sources


class SourceRegistryTests(unittest.TestCase):
    def test_add_and_find_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "sources.yaml"
            source = {
                "name": "demo",
                "repo_url": "https://example.com/demo.git",
                "domain": "project_management",
                "license": "MIT",
                "enabled": True,
                "purpose": "Demo",
                "allowed_usage": {"study_patterns": True, "reuse_code": False, "generate_training_patterns": True},
            }
            add_source(source, config)
            self.assertEqual(find_source("demo", config)["repo_url"], source["repo_url"])
            self.assertEqual(list_sources(config)[0]["name"], "demo")
