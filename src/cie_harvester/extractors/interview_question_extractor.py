from __future__ import annotations

from typing import Any

from cie_harvester.normalizers.duplicate_detector import dedupe_strings


def extract_question_groups(
    modules: list[dict[str, Any]],
    hidden_requirements: list[str],
    role_patterns: list[dict[str, Any]],
    domain: str,
) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    if domain == "project_management":
        if modules:
            groups.append(
                {
                    "id": "project_scope",
                    "priority": "high",
                    "questions": dedupe_strings(
                        [
                            "What types of projects will users manage?",
                            "Do projects have phases, milestones, or sprints?",
                            "Can projects be archived, cloned, or templated?",
                        ]
                    ),
                }
            )
            groups.append(
                {
                    "id": "task_workflow",
                    "priority": "high",
                    "questions": dedupe_strings(
                        [
                            "What statuses can a task have?",
                            "Who can create, assign, update, or close tasks?",
                            "Are subtasks required?",
                        ]
                    ),
                }
            )
    elif domain == "crm":
        groups.append(
            {
                "id": "customer_lifecycle",
                "priority": "high",
                "questions": dedupe_strings(
                    [
                        "What entities represent customers, leads, or contacts?",
                        "How do leads progress through the sales pipeline?",
                        "Which activities or follow-ups must be tracked?",
                    ]
                ),
            }
        )
    elif domain == "cms":
        groups.append(
            {
                "id": "content_workflow",
                "priority": "high",
                "questions": dedupe_strings(
                    [
                        "What content types will be managed?",
                        "How are drafts, reviews, and publishing handled?",
                        "What taxonomy or media management features are required?",
                    ]
                ),
            }
        )
    elif modules:
        groups.append(
            {
                "id": "domain_scope",
                "priority": "high",
                "questions": dedupe_strings(
                    [
                        "What core entities does the system manage?",
                        "What workflows are central to the product?",
                        "Which operational constraints matter most?",
                    ]
                ),
            }
        )
    if role_patterns:
        groups.append(
            {
                "id": "permissions",
                "priority": "high",
                "questions": dedupe_strings(
                    [
                        "What user roles are required?",
                        "Are permissions global, workspace-specific, project-specific, or task-specific?",
                        "Who can manage access and approvals?",
                    ]
                ),
            }
        )
    if hidden_requirements:
        groups.append(
            {
                "id": "hidden_requirements",
                "priority": "medium",
                "questions": [f"Should the system support {item}?" for item in hidden_requirements[:5]],
            }
        )
    return groups
