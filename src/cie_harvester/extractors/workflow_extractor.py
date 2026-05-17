from __future__ import annotations

from typing import Any

from cie_harvester.normalizers.duplicate_detector import dedupe_strings

WORKFLOW_HINTS = {
    "workflow": "workflow_management",
    "approval": "approval_flow",
    "pipeline": "pipeline_flow",
    "status": "status_flow",
    "notification": "notification_flow",
    "sprint": "sprint_workflow",
    "milestone": "milestone_workflow",
}


def extract_workflow_patterns(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    haystack = " ".join(inventory.get("files", []) + inventory.get("directories", {}).get("backend", []) + inventory.get("directories", {}).get("api", [])).lower()
    patterns = []
    for token, label in WORKFLOW_HINTS.items():
        if token in haystack:
            patterns.append({"name": label, "evidence": token, "confidence": 0.7})
    if not patterns and inventory.get("detected", {}).get("frameworks"):
        patterns.append({"name": "basic_request_flow", "evidence": "framework_presence", "confidence": 0.4})
    names = dedupe_strings([pattern["name"] for pattern in patterns])
    pattern_map = {}
    for pattern in patterns:
        pattern_map.setdefault(pattern["name"], pattern)
    return [pattern_map[name] for name in names]
