from __future__ import annotations

from typing import Any

from cie_harvester.normalizers.duplicate_detector import dedupe_strings


def extract_role_permission_patterns(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    haystack = " ".join(inventory.get("files", []) + inventory.get("directories", {}).get("backend", []) + inventory.get("directories", {}).get("api", [])).lower()
    roles = []
    for token in ("role", "permission", "auth", "acl", "admin", "owner", "member", "user"):
        if token in haystack:
            roles.append({"name": f"{token}_access", "evidence": token, "confidence": 0.7})
    names = dedupe_strings([role["name"] for role in roles])
    return [next(role for role in roles if role["name"] == name) for name in names]
