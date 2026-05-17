from __future__ import annotations

from pathlib import Path

__version__ = "0.1.0"

_package_dir = Path(__file__).resolve().parent
_src_package_dir = _package_dir.parent / "src" / "cie_harvester"
if _src_package_dir.exists():
    __path__.append(str(_src_package_dir))  # type: ignore[name-defined]
