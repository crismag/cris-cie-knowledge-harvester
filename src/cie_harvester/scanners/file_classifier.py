from __future__ import annotations

from pathlib import Path

DOC_NAMES = {"readme", "changelog", "contributing", "docs", "license"}
CONFIG_FILES = {"pyproject.toml", "package.json", "requirements.txt", "setup.py", "setup.cfg", "go.mod", "cargo.toml", "pom.xml", "composer.json", "gemfile"}
PACKAGE_FILES = {"package.json", "pyproject.toml", "requirements.txt", "go.mod", "cargo.toml", "pom.xml", "composer.json", "gemfile"}
TEST_HINTS = ("test", "tests", "spec")
EXTENSION_LANGUAGES = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".php": "php",
    ".rb": "ruby",
    ".sh": "shell",
    ".md": "markdown",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".json": "json",
    ".toml": "toml",
    ".html": "html",
    ".css": "css",
}


def classify_file(path: str | Path) -> dict[str, object]:
    file_path = Path(path)
    name = file_path.name.lower()
    suffix = file_path.suffix.lower()
    language = EXTENSION_LANGUAGES.get(suffix, "unknown")
    is_doc = suffix == ".md" or any(token in name for token in DOC_NAMES)
    is_test = any(token in part.lower() for part in file_path.parts for token in TEST_HINTS) or any(token in name for token in TEST_HINTS)
    is_config = name in CONFIG_FILES or suffix in {".yml", ".yaml", ".json", ".toml", ".ini", ".cfg"}
    is_package = name in PACKAGE_FILES
    category = "source"
    if is_doc:
        category = "docs"
    elif is_test:
        category = "test"
    elif is_config:
        category = "config"
    elif is_package:
        category = "package"
    return {
        "path": str(file_path),
        "language": language,
        "category": category,
        "is_doc": is_doc,
        "is_test": is_test,
        "is_config": is_config,
        "is_package": is_package,
    }
