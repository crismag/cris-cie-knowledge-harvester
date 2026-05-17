from __future__ import annotations

from typing import Any

from cie_harvester.normalizers.duplicate_detector import dedupe_strings

HIDDEN_REQUIREMENT_HINTS = [
    "audit trail",
    "notifications",
    "reporting",
    "imports and exports",
    "custom fields",
    "recurring tasks",
    "attachment limits",
    "activity history",
    "workspace settings",
]


def extract_hidden_requirements(inventory: dict[str, Any]) -> list[str]:
    haystack = " ".join(inventory.get("files", []) + [inventory.get("local_path", "")]).lower()
    matches = [hint for hint in HIDDEN_REQUIREMENT_HINTS if any(token in haystack for token in hint.split())]
    if not matches:
        matches = HIDDEN_REQUIREMENT_HINTS[:4]
    return dedupe_strings(matches)
