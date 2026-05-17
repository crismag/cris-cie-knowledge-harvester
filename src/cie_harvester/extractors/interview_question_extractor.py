from __future__ import annotations

from typing import Any

from cie_harvester.normalizers.duplicate_detector import dedupe_strings


def extract_question_groups(modules: list[dict[str, Any]], hidden_requirements: list[str], role_patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    module_names = [module["name"] for module in modules]
    groups = []
    if module_names:
        groups.append({
            "id": "project_scope",
            "priority": "high",
            "questions": dedupe_strings([
                "What types of projects will users manage?",
                "Do projects have phases, milestones, or sprints?",
                "Can projects be archived, cloned, or templated?",
            ]),
        })
        groups.append({
            "id": "task_workflow",
            "priority": "high",
            "questions": dedupe_strings([
                "What statuses can a task have?",
                "Who can create, assign, update, or close tasks?",
                "Are subtasks required?",
            ]),
        })
    if role_patterns:
        groups.append({
            "id": "permissions",
            "priority": "high",
            "questions": dedupe_strings([
                "What user roles are required?",
                "Are permissions global, workspace-specific, project-specific, or task-specific?",
                "Who can manage access and approvals?",
            ]),
        })
    if hidden_requirements:
        groups.append({
            "id": "hidden_requirements",
            "priority": "medium",
            "questions": [f"Should the system support {item}?" for item in hidden_requirements[:5]],
        })
    return groups
