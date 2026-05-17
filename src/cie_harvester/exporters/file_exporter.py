from __future__ import annotations

import shutil
from pathlib import Path


def copy_tree(source: Path, destination: Path, overwrite: bool = True) -> Path:
    if destination.exists() and overwrite:
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    return destination
