from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from cie_harvester.builders.capability_pack_builder import build_capability_pack
from cie_harvester.core.yaml_io import load_yaml
from cie_harvester.validators.pack_validator import validate_pack


class CapabilityPackBuilderTests(unittest.TestCase):
    def test_build_and_validate_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "project_management_interviewer"
            taxonomy = {"triggers": ["project management"], "module_hints": ["project", "task"]}
            sources = [{"name": "worklenz", "repo_url": "https://github.com/Worklenz/worklenz", "domain": "project_management", "license": "MIT", "allowed_usage": {"study_patterns": True, "reuse_code": False, "generate_training_patterns": True}}]
            features = [{"name": "project", "type": "module"}, {"name": "workflow_management", "type": "workflow"}]
            questions = [{"id": "project_scope", "priority": "high", "questions": ["What types of projects will users manage?"]}]
            build_capability_pack(
                "project_management_interviewer",
                "project_management",
                taxonomy,
                sources,
                features,
                questions,
                [],
                {"promotion_rules": {"promote_if_score_above": 0, "reject_if": []}, "scoring": {}},
                output,
            )
            self.assertEqual(load_yaml(output / "CAPABILITY.yaml")["capability"]["id"], "project_management_interviewer")
            self.assertTrue(validate_pack(output)["valid"])
