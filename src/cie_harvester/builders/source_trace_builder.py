from __future__ import annotations

from typing import Any


def build_source_trace(sources: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "studied_projects": [
            {
                "name": source["name"],
                "repo_url": source["repo_url"],
                "license": source.get("license", "unknown"),
                "domain": source["domain"],
                "usage": source.get("allowed_usage", {}),
            }
            for source in sources
        ]
    }
