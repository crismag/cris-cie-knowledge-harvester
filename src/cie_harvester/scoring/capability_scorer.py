from __future__ import annotations


FEATURE_FREQUENCY_MULTIPLIER = 20
FEATURE_FREQUENCY_CAP = 40
INTERVIEW_VALUE_MULTIPLIER = 2
INTERVIEW_VALUE_CAP = 30
DOMAIN_RELEVANCE_MULTIPLIER = 4
DOMAIN_RELEVANCE_CAP = 20
GENERALITY_MULTIPLIER = 3
GENERALITY_CAP = 15


def score_capability(
    modules: list[dict],
    questions: list[dict],
    hidden_requirements: list[str],
    taxonomy_domain: dict,
    scoring_config: dict,
) -> dict:
    """Score extracted capability data using configurable weights."""
    weights = scoring_config.get("scoring", scoring_config)
    base = 0
    base += min(
        len(modules) * weights.get("feature_frequency", {}).get("weight", FEATURE_FREQUENCY_MULTIPLIER),
        FEATURE_FREQUENCY_CAP,
    )
    base += min(
        sum(len(group.get("questions", [])) for group in questions)
        * weights.get("interview_value", {}).get("weight", INTERVIEW_VALUE_MULTIPLIER),
        INTERVIEW_VALUE_CAP,
    )
    base += min(
        len(set(taxonomy_domain.get("module_hints", [])) & {module["name"] for module in modules})
        * weights.get("domain_relevance", {}).get("weight", DOMAIN_RELEVANCE_MULTIPLIER),
        DOMAIN_RELEVANCE_CAP,
    )
    base += min(
        len(set(hidden_requirements)) * weights.get("generality", {}).get("weight", GENERALITY_MULTIPLIER),
        GENERALITY_CAP,
    )
    base += weights.get("implementation_bias_risk", {}).get("weight", -15)
    return {"score": max(0, min(100, base)), "breakdown": {"modules": len(modules), "questions": len(questions), "hidden_requirements": len(hidden_requirements)}}
