from __future__ import annotations

from cie_harvester.normalizers.duplicate_detector import dedupe_strings


def normalize_patterns(patterns: list[dict]) -> list[dict]:
    normalized = []
    seen = set()
    for pattern in patterns:
        name = pattern.get("name") or pattern.get("id") or pattern.get("title")
        key = str(name).lower().strip()
        if key not in seen:
            seen.add(key)
            normalized.append(pattern)
    return normalized
