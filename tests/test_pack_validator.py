from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cie_harvester.builders.capability_pack_builder import build_capability_pack
from cie_harvester.validators.pack_validator import validate_pack


class PackValidatorTests(unittest.TestCase):
    def test_validate_pack_reports_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "pack"
            taxonomy = {"triggers": ["cms"], "module_hints": ["post"]}
            sources = [{"name": "demo", "repo_url": "https://example.com/demo.git", "domain": "cms", "license": "MIT", "allowed_usage": {"study_patterns": True, "reuse_code": False, "generate_training_patterns": True}}]
            build_capability_pack("cms_interviewer", "cms", taxonomy, sources, [], [], {"promotion_rules": {"promote_if_score_above": 0, "reject_if": []}, "scoring": {}}, output)
            self.assertTrue(validate_pack(output)["valid"])
