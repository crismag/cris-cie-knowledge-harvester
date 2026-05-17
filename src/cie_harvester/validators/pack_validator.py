from __future__ import annotations

from pathlib import Path
from typing import Any

from cie_harvester.core.errors import ValidationError
from cie_harvester.core.yaml_io import load_yaml
from cie_harvester.validators.schema_validator import validate_capability_schema, validate_required_files


def validate_pack(pack_path: Path) -> dict[str, Any]:
    missing = validate_required_files(pack_path)
    if missing:
        raise ValidationError(f"pack missing required files: {', '.join(missing)}")
    capability = load_yaml(pack_path / "CAPABILITY.yaml")
    validate_capability_schema(capability)
    return {"valid": True, "missing": [], "files": sorted(path.name for path in pack_path.iterdir())}
