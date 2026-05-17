from __future__ import annotations

from pathlib import Path


def detect_license(repo_path: Path) -> str:
    """Return a common license filename if one exists in the repository root."""
    for candidate in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.md"):
        if (repo_path / candidate).exists():
            return candidate
    return "unknown"
