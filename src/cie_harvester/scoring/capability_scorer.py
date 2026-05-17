from __future__ import annotations


def score_capability(modules: list[dict], questions: list[dict], hidden_requirements: list[str], taxonomy_domain: dict, scoring: dict) -> dict:
    weights = scoring.get("scoring", scoring)
    base = 0
    base += min(len(modules) * weights.get("feature_frequency", {}).get("weight", 20), 40)
    base += min(sum(len(group.get("questions", [])) for group in questions) * 2, weights.get("interview_value", {}).get("weight", 30))
    base += min(len(set(taxonomy_domain.get("module_hints", [])) & {module["name"] for module in modules}) * 4, weights.get("domain_relevance", {}).get("weight", 20))
    base += min(len(set(hidden_requirements)) * 3, weights.get("generality", {}).get("weight", 15))
    base += weights.get("implementation_bias_risk", {}).get("weight", -15)
    return {"score": max(0, min(100, base)), "breakdown": {"modules": len(modules), "questions": len(questions), "hidden_requirements": len(hidden_requirements)}}
