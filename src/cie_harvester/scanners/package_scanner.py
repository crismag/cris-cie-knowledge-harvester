from __future__ import annotations

import json
from pathlib import Path

from cie_harvester.scanners.file_classifier import classify_file


def package_files(files: list[Path]) -> list[str]:
    return [str(path) for path in files if classify_file(path)["is_package"]]


def detect_frameworks(repo_path: Path, files: list[Path]) -> list[str]:
    frameworks: set[str] = set()
    for path in files:
        name = path.name.lower()
        text = ""
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if name == "package.json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                data = {}
            deps = " ".join(
                [
                    *data.get("dependencies", {}).keys(),
                    *data.get("devDependencies", {}).keys(),
                ]
            ).lower()
            for token, framework in {"react": "react", "next": "nextjs", "vue": "vue", "angular": "angular", "express": "express", "nestjs": "nestjs"}.items():
                if token in deps:
                    frameworks.add(framework)
        elif name in {"requirements.txt", "pyproject.toml", "setup.py", "setup.cfg"}:
            lowered = text.lower()
            for token, framework in {"django": "django", "flask": "flask", "fastapi": "fastapi"}.items():
                if token in lowered:
                    frameworks.add(framework)
        elif name == "go.mod":
            lowered = text.lower()
            for token, framework in {"gin": "gin", "echo": "echo", "fiber": "fiber"}.items():
                if token in lowered:
                    frameworks.add(framework)
        elif name == "cargo.toml":
            lowered = text.lower()
            for token, framework in {"actix": "actix", "rocket": "rocket", "axum": "axum"}.items():
                if token in lowered:
                    frameworks.add(framework)
        elif name == "pom.xml":
            if "spring" in text.lower():
                frameworks.add("spring")
        elif name == "composer.json":
            lowered = text.lower()
            for token, framework in {"laravel": "laravel", "symfony": "symfony"}.items():
                if token in lowered:
                    frameworks.add(framework)
        elif name == "gemfile":
            lowered = text.lower()
            for token, framework in {"rails": "rails", "sinatra": "sinatra"}.items():
                if token in lowered:
                    frameworks.add(framework)
    return sorted(frameworks)
