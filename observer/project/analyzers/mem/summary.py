"""
Memory Summary Engine.

This is the final decision layer.

It consumes:
- HealthCheck outputs from analyzers
- Signals from normalization layer

It produces:
- MemoryAnalysis (final system state)
"""

from __future__ import annotations

from project.models.memory import MemoryData, HealthCheck, MemoryAnalysis, Signal
from project.utils.helpers import timestamp

# ==========================================================
# Severity ranking (global resolution system)
# ==========================================================

SEVERITY_RANK = {
    "INFO": 0,
    "WARNING": 1,
    "CRITICAL": 2,
}

icon = {
    "INFO": "✅",
    "WARNING": "⚠️ ",
    "CRITICAL": "❌",
}


def _resolve_severity(checks: list[HealthCheck]) -> str:
    """
    Pick the highest severity across all checks.
    """
    worst = 0

    for c in checks:
        worst = max(worst, SEVERITY_RANK.get(c.status, 0))

    for k, v in SEVERITY_RANK.items():
        if v == worst:
            return k

    return "INFO"


def _deduplicate_checks(checks: list[HealthCheck]) -> list[HealthCheck]:
    """
    Remove duplicate checks based on (check name + status).
    Keeps first occurrence (important for stability).
    """
    seen = set()
    unique = []

    for c in checks:
        key = (c.check, c.status)

        if key in seen:
            continue

        seen.add(key)
        unique.append(c)

    return unique


def _resolve_pressure(checks: list[HealthCheck]) -> str | None:
    """
    Extract memory pressure state from Pressure analyzer.
    """
    for c in checks:
        if c.check == "Memory Pressure":
            if "CRITICAL" in c.status:
                return "Severe"
            if "WARNING" in c.status:
                return "Moderate"
            return "Low"
    return None


def summarize_memory(
    memory: MemoryData,
    checks: list[HealthCheck],
    signals: list[Signal],
) -> MemoryAnalysis:

    # ==========================================================
    # Clean inputs
    # ==========================================================

    checks = _deduplicate_checks(checks)

    severity = _resolve_severity(checks)
    pressure = _resolve_pressure(checks)

    # ==========================================================
    # Confidence (simple heuristic for now)
    # ==========================================================

    signal_count = len(signals)

    if signal_count > 40:
        confidence = "HIGH"
    elif signal_count > 20:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    # ==========================================================
    # Build recommendations (rule-based, NOT ML)
    # ==========================================================

    recommendations: list[str] = []

    for c in checks:
        if c.status == "CRITICAL":
            recommendations.append(f"Investigate: {c.check}")
        elif c.status == "WARNING":
            recommendations.append(f"Monitor: {c.check}")

    # remove duplicates
    recommendations = list(dict.fromkeys(recommendations))

    # ==========================================================
    # Summary text generation (deterministic)
    # ==========================================================

    critical_count = sum(1 for c in checks if c.status == "CRITICAL")
    warning_count = sum(1 for c in checks if c.status == "WARNING")

    if severity == "CRITICAL":
        summary = (
            f"{icon[severity]} System is under severe memory stress with "
            f"{critical_count} critical issue(s) and "
            f"{warning_count} warning(s)."
        )

    elif severity == "WARNING":
        summary = (
            f"{icon[severity]} Memory system shows elevated risk with "
            f"{warning_count} warning(s) detected."
        )

    else:
        severity = "INFO"
        summary = (
            f"{icon[severity]} Memory system is operating within normal parameters."
        )

    # ==========================================================
    # Final analysis object
    # ==========================================================

    return MemoryAnalysis(
        component="memory",
        summary=summary,
        severity=severity,
        analyzed_at=str(timestamp() or "0.0"),
        pressure=pressure,
        confidence=confidence,
        recommendations=recommendations,
        health_checks=checks,
    )
