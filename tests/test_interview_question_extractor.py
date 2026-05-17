from __future__ import annotations

import unittest

from cie_harvester.extractors.interview_question_extractor import extract_question_groups


class InterviewQuestionExtractorTests(unittest.TestCase):
    def test_uses_domain_specific_question_groups(self) -> None:
        groups = extract_question_groups(
            modules=[{"name": "customer"}],
            hidden_requirements=[],
            role_patterns=[],
            domain="crm",
        )
        self.assertEqual(groups[0]["id"], "customer_lifecycle")
        self.assertNotIn("project_scope", {group["id"] for group in groups})
