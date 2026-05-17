from __future__ import annotations

from pathlib import Path
from typing import Any

from cie_harvester.builders.markdown_builder import build_promotion_report, build_readme
from cie_harvester.builders.source_trace_builder import build_source_trace
from cie_harvester.core.errors import ValidationError
from cie_harvester.core.yaml_io import write_yaml
from cie_harvester.normalizers.duplicate_detector import dedupe_strings
from cie_harvester.scoring.capability_scorer import score_capability
from cie_harvester.scoring.promotion_rules import should_promote


def build_capability_pack(
    pack_id: str,
    domain: str,
    taxonomy_domain: dict[str, Any],
    sources: list[dict[str, Any]],
    extracted_features: list[dict[str, Any]],
    extracted_questions: list[dict[str, Any]],
    scoring_config: dict[str, Any],
    output_dir: Path,
) -> Path:
    modules = dedupe_strings([feature["name"] for feature in extracted_features] + list(taxonomy_domain.get("module_hints", [])))
    question_groups = extracted_questions or []
    hidden_requirements = dedupe_strings([item for feature in extracted_features for item in feature.get("hidden_requirements", [])])
    capability = {
        "capability": {
            "id": pack_id,
            "name": "Project Management Software Interviewer" if domain == "project_management" else f"{domain.replace('_', ' ').title()} Interviewer",
            "version": "0.1.0",
            "domain": domain,
            "purpose": [
                f"Guide CRIS-CIE interviews for {domain.replace('_', ' ')} systems.",
                "Detect missing domain requirements.",
                "Generate domain-specific question paths.",
            ],
            "activation_triggers": {"keywords": taxonomy_domain.get("triggers", [])},
            "modules": modules,
            "question_groups": [group.get("id") for group in question_groups],
            "hidden_requirement_checks": hidden_requirements,
            "output_mapping": {
                "features": "question_bank.yaml",
                "questions": "question_bank.yaml",
                "source_trace": "source_trace.yaml",
            },
            "source_trace": build_source_trace(sources),
        }
    }
    questions_payload = {"question_groups": question_groups}
    pack_data = {
        "CAPABILITY.yaml": capability,
        "triggers.yaml": capability["capability"]["activation_triggers"],
        "question_bank.yaml": questions_payload,
        "workflow_patterns.yaml": {"workflow_patterns": [feature for feature in extracted_features if feature.get("type") == "workflow"]},
        "role_permission_patterns.yaml": {"role_permission_patterns": [feature for feature in extracted_features if feature.get("type") == "role_permission"]},
        "hidden_requirements.yaml": {"hidden_requirement_checks": hidden_requirements},
        "output_mapping.yaml": capability["capability"]["output_mapping"],
        "source_trace.yaml": capability["capability"]["source_trace"],
    }
    score_report = score_capability(extracted_features, extracted_questions, hidden_requirements, taxonomy_domain, scoring_config)
    promoted, reasons = should_promote(score_report["score"], scoring_config, [])
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, payload in pack_data.items():
        write_yaml(output_dir / filename, payload)
    (output_dir / "README.md").write_text(build_readme(capability), encoding="utf-8")
    (output_dir / "promotion_report.md").write_text(build_promotion_report(pack_id, score_report, promoted, reasons), encoding="utf-8")
    return output_dir
