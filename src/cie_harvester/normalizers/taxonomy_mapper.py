from __future__ import annotations


def map_domain_terms(items: list[str], taxonomy_domain: dict) -> list[str]:
    """Filter items to those matching taxonomy domain hints."""
    hints = [hint.lower() for hint in taxonomy_domain.get("module_hints", [])]
    result = []
    for item in items:
        lowered = item.lower()
        if any(hint in lowered for hint in hints):
            result.append(item)
    return result
