from __future__ import annotations


def should_promote(score: int, rules: dict, flags: list[str] | None = None) -> tuple[bool, list[str]]:
    rejected = set(rules.get("promotion_rules", rules).get("reject_if", []))
    flags = flags or []
    reasons = [flag for flag in flags if flag in rejected]
    threshold = rules.get("promotion_rules", rules).get("promote_if_score_above", 70)
    if reasons:
        return False, reasons
    if score < threshold:
        return False, [f"score_below_threshold:{threshold}"]
    return True, []
