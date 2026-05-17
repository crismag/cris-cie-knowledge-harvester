from __future__ import annotations


def should_promote(score: int, promotion_config: dict, flags: list[str] | None = None) -> tuple[bool, list[str]]:
    rejected = set(promotion_config.get("promotion_rules", promotion_config).get("reject_if", []))
    flags = flags or []
    reasons = [flag for flag in flags if flag in rejected]
    threshold = promotion_config.get("promotion_rules", promotion_config).get("promote_if_score_above", 70)
    if reasons:
        return False, reasons
    if score < threshold:
        return False, [f"score_below_threshold:{threshold}"]
    return True, []
