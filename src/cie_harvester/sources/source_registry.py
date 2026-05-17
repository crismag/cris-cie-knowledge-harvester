from __future__ import annotations

from pathlib import Path
from typing import Any

from cie_harvester.core.errors import ConfigError
from cie_harvester.core.paths import config_file, is_safe_path_component
from cie_harvester.core.yaml_io import load_yaml, write_yaml

REQUIRED_FIELDS = ("name", "repo_url", "domain", "license", "enabled", "purpose", "allowed_usage")
REQUIRED_USAGE_FIELDS = ("study_patterns", "reuse_code", "generate_training_patterns")


def registry_path(path: Path | None = None) -> Path:
    return path or config_file("sources.yaml")


def load_sources(config_path: Path | None = None) -> dict[str, Any]:
    return load_yaml(registry_path(config_path))


def list_sources(config_path: Path | None = None) -> list[dict[str, Any]]:
    return list(load_sources(config_path).get("sources", []))


def find_source(name: str, config_path: Path | None = None) -> dict[str, Any] | None:
    return next((source for source in list_sources(config_path) if source.get("name") == name), None)


def sources_for_domain(domain: str, config_path: Path | None = None) -> list[dict[str, Any]]:
    return [source for source in list_sources(config_path) if source.get("domain") == domain and source.get("enabled", False)]


def validate_source_entry(source: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in source]
    if missing:
        raise ConfigError(f"source entry missing required fields: {', '.join(missing)}")
    if not is_safe_path_component(str(source["name"])):
        raise ConfigError("source name must be a safe path component")
    usage = source.get("allowed_usage", {})
    missing_usage = [field for field in REQUIRED_USAGE_FIELDS if field not in usage]
    if missing_usage:
        raise ConfigError(f"allowed_usage missing required fields: {', '.join(missing_usage)}")


def add_source(source: dict[str, Any], config_path: Path | None = None) -> dict[str, Any]:
    validate_source_entry(source)
    path = registry_path(config_path)
    data = load_yaml(path)
    sources = list(data.get("sources", []))
    if any(existing.get("name") == source["name"] for existing in sources):
        raise ConfigError(f"source '{source['name']}' already exists")
    sources.append(source)
    data["sources"] = sources
    write_yaml(path, data)
    return source
