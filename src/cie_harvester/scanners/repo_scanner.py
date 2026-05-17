from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from cie_harvester.scanners.docs_scanner import docs_files
from cie_harvester.scanners.file_classifier import classify_file
from cie_harvester.scanners.package_scanner import detect_frameworks, package_files

DEFAULT_IGNORED_DIRS = {".git", "node_modules", ".venv", "dist", "build", "target", "coverage", "__pycache__", ".idea", ".vscode"}


def scan_repository(repo_path: Path, ignored_dirs: set[str] | None = None) -> dict:
    ignored = set(ignored_dirs or DEFAULT_IGNORED_DIRS)
    files: list[Path] = []
    directories: set[Path] = set()
    for current_root, dirnames, filenames in os.walk(repo_path):
        dirnames[:] = [name for name in dirnames if name not in ignored]
        current = Path(current_root)
        directories.add(current)
        for filename in filenames:
            path = current / filename
            files.append(path)
    relative_files = [path.relative_to(repo_path) for path in files]
    package_paths = package_files(relative_files)
    doc_paths = docs_files(relative_files)

    # Classify each file once to avoid repeated scanning
    classifications = {path: classify_file(path) for path in relative_files}

    config_paths = [str(path) for path, info in classifications.items() if info["is_config"]]
    test_paths = [str(path) for path, info in classifications.items() if info["is_test"]]
    languages = sorted(
        {
            str(info["language"])
            for info in classifications.values()
            if info["language"] != "unknown"
        }
    )

    frameworks = detect_frameworks(repo_path, [repo_path / path for path in relative_files])
    categorized_dirs = _categorize_directories(repo_path, directories)
    return {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_files": len(relative_files),
            "total_directories": len(directories),
        },
        "detected": {
            "languages": languages,
            "frameworks": frameworks,
            "package_files": package_paths,
            "docs_files": doc_paths,
            "config_files": config_paths,
            "test_files": test_paths,
        },
        "directories": categorized_dirs,
        "files": [str(path) for path in relative_files],
    }


def _categorize_directories(repo_path: Path, directories: set[Path]) -> dict[str, list[str]]:
    buckets = {"frontend": [], "backend": [], "api": [], "database": [], "docs": [], "tests": [], "deployment": []}
    hints = {
        "frontend": {"frontend", "client", "web", "ui"},
        "backend": {"backend", "server", "service", "app"},
        "api": {"api", "rest", "graphql"},
        "database": {"db", "database", "migrations", "schema"},
        "docs": {"docs", "documentation"},
        "tests": {"test", "tests", "spec"},
        "deployment": {"deploy", "deployment", "infra", "docker", "k8s", "kubernetes", "terraform", "helm", "ci", "cd", "github"},
    }
    for directory in directories:
        try:
            relative = directory.relative_to(repo_path)
        except ValueError:
            continue
        parts = {part.lower() for part in relative.parts}
        for bucket, tokens in hints.items():
            if parts & tokens:
                buckets[bucket].append(str(relative))
    return {key: sorted(set(values)) for key, values in buckets.items()}
