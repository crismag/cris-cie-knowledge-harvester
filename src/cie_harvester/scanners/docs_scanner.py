from __future__ import annotations

from pathlib import Path

from cie_harvester.scanners.file_classifier import classify_file


def docs_files(files: list[Path]) -> list[str]:
    return [str(path) for path in files if classify_file(path)["is_doc"]]
