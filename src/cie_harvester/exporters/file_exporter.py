from __future__ import annotations

import shutil
from pathlib import Path


def copy_tree(source: Path, destination: Path, overwrite: bool = True) -> Path:
    """Copy a directory tree to a destination path."""
    if destination.exists() and overwrite:
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    return destination
