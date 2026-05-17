from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    current = Path(__file__).resolve()
    required_dirs = ("configs", "schemas", "skills")

    for parent in current.parents:
        if all((parent / directory).is_dir() for directory in required_dirs):
            return parent

    return current.parents[1]


def configs_dir(root: Path | None = None) -> Path:
    return (root or project_root()) / "configs"


def schemas_dir(root: Path | None = None) -> Path:
    return (root or project_root()) / "schemas"


def skills_dir(root: Path | None = None) -> Path:
    return (root or project_root()) / "skills"


def workspaces_dir(root: Path | None = None) -> Path:
    return (root or project_root()) / "workspaces"


def repos_dir(root: Path | None = None) -> Path:
    return workspaces_dir(root) / "repos"


def inventory_dir(root: Path | None = None) -> Path:
    return workspaces_dir(root) / "inventory"


def extracted_dir(root: Path | None = None) -> Path:
    return workspaces_dir(root) / "extracted"


def normalized_dir(root: Path | None = None) -> Path:
    return workspaces_dir(root) / "normalized"


def promoted_dir(root: Path | None = None) -> Path:
    return workspaces_dir(root) / "promoted"


def packs_dir(root: Path | None = None) -> Path:
    return workspaces_dir(root) / "packs"


def exports_dir(root: Path | None = None) -> Path:
    return workspaces_dir(root) / "exports"


def config_file(name: str, root: Path | None = None) -> Path:
    return configs_dir(root) / name


def schema_file(name: str, root: Path | None = None) -> Path:
    return schemas_dir(root) / name


def repo_path_for_source(source_name: str, root: Path | None = None) -> Path:
    return repos_dir(root) / source_name


def inventory_path_for_source(source_name: str, root: Path | None = None) -> Path:
    return inventory_dir(root) / f"{source_name}.inventory.yaml"


def extracted_features_path(source_name: str, root: Path | None = None) -> Path:
    return extracted_dir(root) / f"{source_name}.features.yaml"


def extracted_questions_path(source_name: str, root: Path | None = None) -> Path:
    return extracted_dir(root) / f"{source_name}.questions.yaml"


def pack_path(pack_id: str, root: Path | None = None) -> Path:
    return packs_dir(root) / pack_id


def ensure_workspace_dirs(root: Path | None = None) -> None:
    for path in [repos_dir(root), inventory_dir(root), extracted_dir(root), normalized_dir(root), promoted_dir(root), packs_dir(root), exports_dir(root)]:
        path.mkdir(parents=True, exist_ok=True)
