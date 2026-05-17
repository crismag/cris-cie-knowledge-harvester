from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from cie_harvester.core.errors import SourceError
from cie_harvester.core.paths import repo_path_for_source, repos_dir


def _run_git(args: list[str], cwd: Path | None = None) -> None:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise SourceError(message)


def clone_or_update_repo(source: dict[str, Any], root: Path | None = None) -> Path:
    repo_url = source["repo_url"]
    local_path = repo_path_for_source(source["name"], root)
    local_path.parent.mkdir(parents=True, exist_ok=True)
    repos_dir(root).mkdir(parents=True, exist_ok=True)
    if local_path.exists():
        if not (local_path / ".git").exists():
            raise SourceError(f"existing path is not a git repository: {local_path}")
        _run_git(["-C", str(local_path), "pull", "--ff-only"])
    else:
        _run_git(["clone", repo_url, str(local_path)], cwd=repos_dir(root))
    return local_path
