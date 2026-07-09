"""
CPU Summary Engine.

Consumes:
- HealthCheck outputs from analyzers
- Signals from normalization layer

Produces:
- CpuAnalysis
"""

from __future__ import annotations

from project.models.cpu import CpuData, CpuAnalysis, Signal, HealthCheck
from project.utils.helpers import timestamp


# ==========================================================
# Severity Ranking
# ==========================================================

SEVERITY_RANK = {
    "PASS": 0,
    "WARNING": 1,
    "CRITICAL": 2,
}

ICON = {
    "INFO": "✅",
    "WARNING": "⚠️ ",
    "CRITICAL": "❌",
}

ANALYZER_STATE_SCORE = {
    "COMPLETE": 1.0,
    "PARTIAL": 0.8,
    "UNAVAILABLE": None,
}


# ==========================================================
# Helpers
# ==========================================================

def _resolve_severity(checks: list[HealthCheck]) -> str:

    worst = 0

    for check in checks:
        worst = max(
            worst,
            SEVERITY_RANK.get(check.status, 0),
        )

    if worst == 2:
        return "CRITICAL"

    if worst == 1:
        return "WARNING"

    return "INFO"


def _deduplicate(checks: list[HealthCheck]) -> list[HealthCheck]:

    seen = set()
    unique = []

    for check in checks:

        key = (check.check, check.status)

        if key in seen:
            continue

        seen.add(key)
        unique.append(check)

    return unique


# ==========================================================
# Summary
# ==========================================================

def summarize_cpu(
    cpu: CpuData,
    checks: list[HealthCheck],
    signals: list[Signal],
    metadata: dict,
) -> CpuAnalysis:

    checks = _deduplicate(checks)
    severity = _resolve_severity(checks)

    # ======================================================
    # Confidence
    # ======================================================

    analyzer_scores = []

    confidence_reasons = []

    for name, value in metadata.items():

        state = value["state"]

        score = ANALYZER_STATE_SCORE[state]

        if score is None:
            confidence_reasons.append(
                f"{name}: unavailable"
            )
            continue

        analyzer_scores.append(score)

        confidence_reasons.append(
            f"{name}: {state.lower()}"
        )

    coverage_score = (
        sum(analyzer_scores) / len(analyzer_scores)
        if analyzer_scores
        else 0
    )

    collector_score = (
        cpu.collected_successful /
        cpu.collected_total
        if cpu.collected_total
        else 0
    )

    signal_score = (
        cpu.signals_created /
        cpu.signals_expected
        if cpu.signals_expected
        else 0
    )

    score = (
          coverage_score * 0.52
        + signal_score   * 0.46
        + collector_score * 0.02
    )

    confidence_percent = round(score * 100)

    if score >= 0.75:
        level = "HIGH"
    elif score >= 0.50:
        level = "MEDIUM"
    else:
        level = "LOW"

    confidence = {
        "result": f"{level} {confidence_percent}%",
        "reasons": [
            f"analysis_score: {coverage_score:.2f}",
            f"signal_score: {signal_score:.2f}",
            f"collector_score: {collector_score:.2f}",
            *confidence_reasons,
        ],
    }

    # ======================================================
    # Recommendations
    # ======================================================

    recommendations = []

    for check in checks:

        if check.status == "CRITICAL":
            recommendations.append(
                f"Investigate: {check.check}"
            )

        elif check.status == "WARNING":
            recommendations.append(
                f"Monitor: {check.check}"
            )

    recommendations = list(dict.fromkeys(recommendations))

    if not recommendations:
        recommendations.append(
            "CPU is operating normally."
        )

    # ======================================================
    # Summary
    # ======================================================

    critical = sum(
        c.status == "CRITICAL"
        for c in checks
    )

    warning = sum(
        c.status == "WARNING"
        for c in checks
    )

    if severity == "CRITICAL":

        summary = (
            f"{ICON[severity]} CPU shows "
            f"{critical} critical issue(s) and "
            f"{warning} warning(s)."
        )

    elif severity == "WARNING":

        summary = (
            f"{ICON[severity]} CPU shows "
            f"{warning} warning(s) requiring attention."
        )

    else:

        summary = (
            f"{ICON['INFO']} CPU is operating within normal limits."
        )

    return CpuAnalysis(
        component="cpu",
        summary=summary,
        severity=severity,
        confidence=confidence,
        analyzed_at=str(timestamp() or "0.0"),
        recommendations=recommendations,
        health_checks=checks,
    )
