from __future__ import annotations

from pathlib import Path
from typing import Any

from cie_harvester.core.errors import ValidationError


def validate_capability_schema(data: dict[str, Any]) -> None:
    capability = data.get("capability")
    if not isinstance(capability, dict):
        raise ValidationError("CAPABILITY.yaml must contain a capability map")
    required = ("id", "name", "version", "domain", "purpose", "activation_triggers", "modules", "question_groups", "hidden_requirement_checks", "output_mapping", "source_trace")
    missing = [field for field in required if field not in capability]
    if missing:
        raise ValidationError(f"capability missing required fields: {', '.join(missing)}")


def validate_required_files(pack_path: Path) -> list[str]:
    required = ["CAPABILITY.yaml", "README.md", "triggers.yaml", "question_bank.yaml", "workflow_patterns.yaml", "role_permission_patterns.yaml", "hidden_requirements.yaml", "output_mapping.yaml", "source_trace.yaml", "promotion_report.md"]
    return [name for name in required if not (pack_path / name).exists()]
