from __future__ import annotations

from typing import Any


def build_readme(pack: dict[str, Any]) -> str:
    capability = pack["capability"]
    lines = [
        f"# {capability['name']}",
        "",
        capability.get("purpose", [""])[0] if capability.get("purpose") else "",
        "",
        f"Domain: {capability['domain']}",
        f"Version: {capability['version']}",
    ]
    return "\n".join(lines) + "\n"


def build_promotion_report(pack_id: str, score_report: dict[str, Any], promoted: bool, reasons: list[str]) -> str:
    lines = [
        f"# Promotion report: {pack_id}",
        "",
        f"Score: {score_report.get('score', 0)}",
        f"Promoted: {str(promoted).lower()}",
    ]
    if reasons:
        lines.append(f"Reasons: {', '.join(reasons)}")
    return "\n".join(lines) + "\n"
