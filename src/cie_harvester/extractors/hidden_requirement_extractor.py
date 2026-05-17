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
    normalized_haystack = " ".join(haystack.split())
    normalized_hints = [" ".join(hint.lower().split()) for hint in HIDDEN_REQUIREMENT_HINTS]
    matches = [hint for hint, normalized_hint in zip(HIDDEN_REQUIREMENT_HINTS, normalized_hints) if normalized_hint in normalized_haystack]
    return dedupe_strings(matches)
