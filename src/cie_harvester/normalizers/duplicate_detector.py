from __future__ import annotations


def normalize_string(value: str) -> str:
    return " ".join(value.lower().strip().split())


def dedupe_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = normalize_string(value)
        if key and key not in seen:
            seen.add(key)
            result.append(value)
    return result
