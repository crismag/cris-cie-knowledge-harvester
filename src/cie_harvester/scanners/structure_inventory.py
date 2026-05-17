from __future__ import annotations

from pathlib import Path
from typing import Any

from cie_harvester.core.errors import ValidationError
from cie_harvester.scanners.repo_scanner import scan_repository


def build_inventory(source: dict[str, Any], repo_path: Path) -> dict[str, Any]:
    scan = scan_repository(repo_path)
    inventory = {
        "source_name": source["name"],
        "repo_url": source["repo_url"],
        "local_path": str(repo_path),
        "scanned_at": scan["scanned_at"],
        "summary": scan["summary"],
        "detected": scan["detected"],
        "directories": scan["directories"],
    }
    validate_inventory(inventory)
    return inventory


def validate_inventory(inventory: dict[str, Any]) -> None:
    required = ("source_name", "repo_url", "local_path", "scanned_at", "summary", "detected", "directories")
    missing = [field for field in required if field not in inventory]
    if missing:
        raise ValidationError(f"inventory missing required fields: {', '.join(missing)}")
    summary = inventory["summary"]
    for field in ("total_files", "total_directories"):
        if field not in summary:
            raise ValidationError(f"inventory.summary missing {field}")
