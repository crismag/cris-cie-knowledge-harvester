from __future__ import annotations

import argparse
from pathlib import Path

from cie_harvester.builders.capability_pack_builder import build_capability_pack
from cie_harvester.core.errors import ConfigError, HarvesterError, SourceError, ValidationError
from cie_harvester.core.logging import setup_logging
from cie_harvester.core.paths import (
    configs_dir,
    ensure_workspace_dirs,
    extracted_features_path,
    extracted_questions_path,
    is_safe_path_component,
    inventory_path_for_source,
    pack_path,
    project_root,
    repo_path_for_source,
    workspaces_dir,
)
from cie_harvester.core.yaml_io import ensure_yaml_file, load_yaml, write_yaml
from cie_harvester.extractors.hidden_requirement_extractor import extract_hidden_requirements
from cie_harvester.extractors.interview_question_extractor import extract_question_groups
from cie_harvester.extractors.module_extractor import extract_modules
from cie_harvester.extractors.role_permission_extractor import extract_role_permission_patterns
from cie_harvester.extractors.workflow_extractor import extract_workflow_patterns
from cie_harvester.exporters.cie_pack_exporter import export_pack as export_pack_to_target
from cie_harvester.scanners.structure_inventory import build_inventory
from cie_harvester.scoring.capability_scorer import score_capability
from cie_harvester.sources.github_source import clone_or_update_repo
from cie_harvester.sources.source_registry import add_source, find_source, list_sources, sources_for_domain
from cie_harvester.validators.pack_validator import validate_pack

DEFAULT_CONFIGS: dict[str, dict] = {
    "sources.yaml": {
        "sources": [
            {
                "name": "worklenz",
                "repo_url": "https://github.com/Worklenz/worklenz",
                "domain": "project_management",
                "license": "MIT",
                "enabled": True,
                "purpose": "Study project management, task lifecycle, teams, collaboration, and reporting patterns.",
                "allowed_usage": {
                    "study_patterns": True,
                    "reuse_code": False,
                    "generate_training_patterns": True,
                },
            }
        ]
    },
    "taxonomy.yaml": {
        "domains": {
            "project_management": {
                "triggers": [
                    "project management",
                    "task tracker",
                    "kanban",
                    "workflow management",
                    "team collaboration",
                ],
                "module_hints": [
                    "project",
                    "task",
                    "board",
                    "sprint",
                    "milestone",
                    "team",
                    "user",
                    "comment",
                    "attachment",
                    "notification",
                    "report",
                ],
            },
            "crm": {
                "triggers": ["crm", "customer management", "lead management", "sales pipeline"],
                "module_hints": ["customer", "lead", "contact", "deal", "quote", "invoice", "payment"],
            },
            "cms": {
                "triggers": ["cms", "content management", "blog", "publishing"],
                "module_hints": ["post", "page", "author", "category", "tag", "media", "comment"],
            },
        }
    },
    "scoring.yaml": {
        "scoring": {
            "feature_frequency": {"weight": 20},
            "interview_value": {"weight": 30},
            "domain_relevance": {"weight": 20},
            "generality": {"weight": 15},
            "implementation_bias_risk": {"weight": -15},
        },
        "promotion_rules": {
            "promote_if_score_above": 70,
            "reject_if": [
                "too_code_specific",
                "duplicate_pattern",
                "license_unclear",
                "not_relevant_to_interviewing",
                "framework_specific_without_domain_value",
            ],
        },
    },
    "export_targets.yaml": {
        "targets": {
            "local_cie": {
                "path": "../cris-cie/capability_packs",
                "description": "Local CRIS-CIE capability pack folder",
            }
        }
    },
}


def starter_schemas() -> dict[str, dict]:
    return {
        "source.schema.yaml": {
            "source": {
                "name": "string",
                "repo_url": "string",
                "domain": "string",
                "license": "string",
                "enabled": "boolean",
                "purpose": "string",
                "allowed_usage": {
                    "study_patterns": "boolean",
                    "reuse_code": "boolean",
                    "generate_training_patterns": "boolean",
                },
            }
        },
        "inventory.schema.yaml": {
            "inventory": {
                "source_name": "string",
                "repo_url": "string",
                "local_path": "string",
                "scanned_at": "string",
                "summary": {"total_files": "integer", "total_directories": "integer"},
                "detected": {
                    "languages": "list",
                    "frameworks": "list",
                    "package_files": "list",
                    "docs_files": "list",
                    "config_files": "list",
                    "test_files": "list",
                },
                "directories": {
                    "frontend": "list",
                    "backend": "list",
                    "api": "list",
                    "database": "list",
                    "docs": "list",
                    "tests": "list",
                    "deployment": "list",
                },
            }
        },
        "extracted_pattern.schema.yaml": {
            "extracted_pattern": {
                "modules": "list",
                "workflows": "list",
                "roles": "list",
                "hidden_requirements": "list",
            }
        },
        "interview_pattern.schema.yaml": {"interview_pattern": {"question_groups": "list"}},
        "capability_pack.schema.yaml": {
            "capability": {
                "id": "string",
                "name": "string",
                "version": "string",
                "domain": "string",
                "purpose": "list",
                "activation_triggers": "map",
                "modules": "list",
                "question_groups": "list",
                "hidden_requirement_checks": "list",
                "output_mapping": "map",
                "source_trace": "map",
            }
        },
    }


def starter_skills() -> dict[str, str]:
    return {
        "common/repo_to_product_patterns.md": "# Repo to Product Patterns\n\nMap repository structure, package manifests, and docs into reusable product concepts.\n",
        "common/feature_to_question_transform.md": "# Feature to Question Transform\n\nConvert identified features into interview questions that reveal missing requirements.\n",
        "common/hidden_requirement_detection.md": "# Hidden Requirement Detection\n\nLook for audit trails, notifications, reporting, exports, permissions, recurring behavior, and settings.\n",
        "domains/project_management_skill.md": "# Project Management Skill\n\nFocus on project scope, task lifecycles, team collaboration, permissions, and reporting.\n",
        "domains/crm_skill.md": "# CRM Skill\n\nFocus on leads, contacts, pipelines, deals, and customer lifecycle patterns.\n",
        "domains/erp_skill.md": "# ERP Skill\n\nFocus on finance, inventory, procurement, and operational workflows.\n",
        "domains/cms_skill.md": "# CMS Skill\n\nFocus on pages, posts, publishing workflows, media, authors, and taxonomy.\n",
        "domains/ecommerce_skill.md": "# Ecommerce Skill\n\nFocus on catalog, cart, checkout, payments, fulfillment, and order management.\n",
    }


def ensure_starter_files() -> None:
    ensure_workspace_dirs()
    configs_dir().mkdir(parents=True, exist_ok=True)
    for filename, data in DEFAULT_CONFIGS.items():
        ensure_yaml_file(configs_dir() / filename, data)

    schema_dir = project_root() / "schemas"
    schema_dir.mkdir(parents=True, exist_ok=True)
    for filename, data in starter_schemas().items():
        ensure_yaml_file(schema_dir / filename, data)

    skills_root = project_root() / "skills"
    for relative_path, content in starter_skills().items():
        path = skills_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    for folder in [
        workspaces_dir(),
        workspaces_dir() / "repos",
        workspaces_dir() / "inventory",
        workspaces_dir() / "extracted",
        workspaces_dir() / "normalized",
        workspaces_dir() / "promoted",
        workspaces_dir() / "packs",
        workspaces_dir() / "exports",
    ]:
        folder.mkdir(parents=True, exist_ok=True)
        gitkeep = folder / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")


def _build_feature_entries(
    modules: list[dict],
    workflows: list[dict],
    roles: list[dict],
    hidden_requirements: list[str],
) -> list[dict]:
    features: list[dict] = []
    for module in modules:
        features.append({"name": module["name"], "type": "module", "confidence": module.get("confidence", 0.5)})
    for workflow in workflows:
        features.append(
            {
                "name": workflow["name"],
                "type": "workflow",
                "evidence": workflow.get("evidence"),
                "confidence": workflow.get("confidence", 0.5),
            }
        )
    for role in roles:
        features.append(
            {
                "name": role["name"],
                "type": "role_permission",
                "evidence": role.get("evidence"),
                "confidence": role.get("confidence", 0.5),
            }
        )
    for item in hidden_requirements:
        features.append({"name": item, "type": "hidden_requirement", "confidence": 0.4})
    return features


def cmd_init(_: argparse.Namespace) -> int:
    ensure_starter_files()
    return 0


def cmd_list_sources(_: argparse.Namespace) -> int:
    for source in list_sources():
        print(f"{source['name']}\t{source['domain']}\t{source['repo_url']}\t{'enabled' if source.get('enabled') else 'disabled'}")
    return 0


def cmd_add_source(args: argparse.Namespace) -> int:
    source = {
        "name": args.name,
        "repo_url": args.repo,
        "domain": args.domain,
        "license": args.license,
        "enabled": True,
        "purpose": args.purpose or "Harvest reusable patterns.",
        "allowed_usage": {"study_patterns": True, "reuse_code": False, "generate_training_patterns": True},
    }
    add_source(source)
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    source = find_source(args.source)
    if not source:
        raise ConfigError(f"unknown source: {args.source}")
    ensure_workspace_dirs()
    clone_or_update_repo(source)
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    source = find_source(args.source)
    if not source:
        raise ConfigError(f"unknown source: {args.source}")
    repo_path = repo_path_for_source(source["name"])
    if not repo_path.exists():
        raise SourceError(f"repo not fetched: {repo_path}")
    inventory = build_inventory(source, repo_path)
    write_yaml(inventory_path_for_source(source["name"]), inventory)
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    source = find_source(args.source)
    if not source:
        raise ConfigError(f"unknown source: {args.source}")
    inventory_path = inventory_path_for_source(source["name"])
    if not inventory_path.exists():
        raise SourceError(f"inventory not found: {inventory_path}")
    inventory = load_yaml(inventory_path)
    taxonomy = load_yaml(configs_dir() / "taxonomy.yaml").get("domains", {}).get(source["domain"], {})
    modules = extract_modules(inventory, taxonomy)
    workflows = extract_workflow_patterns(inventory)
    roles = extract_role_permission_patterns(inventory)
    hidden = extract_hidden_requirements(inventory)
    features = _build_feature_entries(modules, workflows, roles, hidden)
    questions = {"question_groups": extract_question_groups(modules, hidden, roles, source["domain"])}
    write_yaml(extracted_features_path(source["name"]), {"features": features, "modules": modules, "workflows": workflows, "roles": roles, "hidden_requirements": hidden})
    write_yaml(extracted_questions_path(source["name"]), questions)
    return 0


def cmd_build_pack(args: argparse.Namespace) -> int:
    if not is_safe_path_component(args.pack_id):
        raise ConfigError("pack id must be a safe path component")
    sources = sources_for_domain(args.domain)
    if not sources:
        raise ConfigError(f"no enabled sources for domain: {args.domain}")
    taxonomy = load_yaml(configs_dir() / "taxonomy.yaml").get("domains", {}).get(args.domain, {})
    scoring = load_yaml(configs_dir() / "scoring.yaml")
    extracted_features: list[dict] = []
    extracted_questions: list[dict] = []
    hidden_requirements: list[str] = []
    for source in sources:
        features_path = extracted_features_path(source["name"])
        questions_path = extracted_questions_path(source["name"])
        if features_path.exists():
            feature_payload = load_yaml(features_path)
            extracted_features.extend(feature_payload.get("features", []))
            hidden_requirements.extend(feature_payload.get("hidden_requirements", []))
        if questions_path.exists():
            extracted_questions.extend(load_yaml(questions_path).get("question_groups", []))
    if not extracted_questions:
        extracted_questions = extract_question_groups([], [], [], args.domain)
    output_dir = pack_path(args.pack_id)
    build_capability_pack(
        args.pack_id,
        args.domain,
        taxonomy,
        sources,
        extracted_features,
        extracted_questions,
        hidden_requirements,
        scoring,
        output_dir,
    )
    return 0


def cmd_validate_pack(args: argparse.Namespace) -> int:
    if not is_safe_path_component(args.pack):
        raise ConfigError("pack id must be a safe path component")
    result = validate_pack(pack_path(args.pack))
    print(result)
    return 0


def cmd_export_pack(args: argparse.Namespace) -> int:
    if not is_safe_path_component(args.pack):
        raise ConfigError("pack id must be a safe path component")
    validate_pack(pack_path(args.pack))
    target = Path(args.target).expanduser()
    export_pack_to_target(pack_path(args.pack), target, args.pack)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cie-harvest")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init").set_defaults(func=cmd_init)
    subparsers.add_parser("list-sources").set_defaults(func=cmd_list_sources)

    add_parser = subparsers.add_parser("add-source")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--repo", required=True)
    add_parser.add_argument("--domain", required=True)
    add_parser.add_argument("--license", required=True)
    add_parser.add_argument("--purpose")
    add_parser.set_defaults(func=cmd_add_source)

    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("--source", required=True)
    fetch_parser.set_defaults(func=cmd_fetch)

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("--source", required=True)
    scan_parser.set_defaults(func=cmd_scan)

    extract_parser = subparsers.add_parser("extract")
    extract_parser.add_argument("--source", required=True)
    extract_parser.set_defaults(func=cmd_extract)

    build_pack_parser = subparsers.add_parser("build-pack")
    build_pack_parser.add_argument("--domain", required=True)
    build_pack_parser.add_argument("--pack-id", required=True)
    build_pack_parser.set_defaults(func=cmd_build_pack)

    validate_parser = subparsers.add_parser("validate-pack")
    validate_parser.add_argument("--pack", required=True)
    validate_parser.set_defaults(func=cmd_validate_pack)

    export_parser = subparsers.add_parser("export-pack")
    export_parser.add_argument("--pack", required=True)
    export_parser.add_argument("--target", required=True)
    export_parser.set_defaults(func=cmd_export_pack)

    return parser


def main() -> int:
    setup_logging()
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (ConfigError, SourceError, ValidationError, HarvesterError) as exc:
        parser.error(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
