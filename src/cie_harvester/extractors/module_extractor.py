from __future__ import annotations

from typing import Any

from cie_harvester.normalizers.duplicate_detector import dedupe_strings


def extract_modules(inventory: dict[str, Any], taxonomy: dict[str, Any]) -> list[dict[str, Any]]:
    hints = taxonomy.get("module_hints", [])
    haystack = " ".join([
        inventory.get("local_path", ""),
        *inventory.get("detected", {}).get("languages", []),
        *inventory.get("detected", {}).get("frameworks", []),
        *inventory.get("directories", {}).get("frontend", []),
        *inventory.get("directories", {}).get("backend", []),
        *inventory.get("directories", {}).get("api", []),
        *inventory.get("directories", {}).get("database", []),
        *inventory.get("directories", {}).get("docs", []),
        *inventory.get("directories", {}).get("tests", []),
        *inventory.get("directories", {}).get("deployment", []),
        *inventory.get("detected", {}).get("package_files", []),
    ]).lower()
    modules = []
    for hint in hints:
        if hint.lower() in haystack:
            modules.append({"name": hint, "source": "taxonomy", "confidence": 0.8})
    for directory in inventory.get("directories", {}).get("frontend", []) + inventory.get("directories", {}).get("backend", []):
        name = directory.split("/")[-1]
        modules.append({"name": name, "source": "directory", "confidence": 0.6})
    normalized = dedupe_strings([module["name"] for module in modules])
    result = []
    for name in normalized:
        source = next((module["source"] for module in modules if module["name"] == name), "taxonomy")
        confidence = next((module["confidence"] for module in modules if module["name"] == name), 0.5)
        result.append({"name": name, "source": source, "confidence": confidence})
    return result
