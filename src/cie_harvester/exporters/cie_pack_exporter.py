from __future__ import annotations

from pathlib import Path

from cie_harvester.exporters.file_exporter import copy_tree


def export_pack(pack_path: Path, target_root: Path, pack_id: str | None = None) -> Path:
    destination = target_root / (pack_id or pack_path.name)
    return copy_tree(pack_path, destination, overwrite=True)
