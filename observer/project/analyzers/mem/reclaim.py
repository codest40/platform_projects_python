"""
Memory Reclaim Analyzer.

Evaluates kernel page scanning and page reclaim activity.
"""

from __future__ import annotations

from project.models.memory import MemoryData, HealthCheck
from project.analyzers.mem.data import build_result

def analyze_memory_reclaim(
    memory: MemoryData,
) -> build_result(name, state, checks=list[HealthCheck]):

    checks: list[HealthCheck] = []
    scanned = memory.pages_scanned_per_sec
    reclaimed = memory.pages_reclaimed_per_sec

    # ==========================================================
    # Missing Data
    # ==========================================================

    if scanned is None or reclaimed is None:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="PASS",
                reason="Memory reclaim statistics are unavailable.",
            )
        )
        return build_result(name="reclaim", state="UNAVAILABLE", checks=checks)

    # ==========================================================
    # Idle State
    # ==========================================================

    if scanned == 0 and reclaimed == 0:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="PASS",
                reason="No memory reclaim activity detected.",
            )
        )
        return build_result(name="reclaim", state="COMPLETE", checks=checks)

    # ==========================================================
    # Efficiency (derived locally, but NOT normalized yet)
    # ==========================================================

    efficiency = (
        (reclaimed / scanned * 100) if scanned else 100
    )

    # ==========================================================
    # Severe imbalance
    # ==========================================================

    if scanned >= 1000 and efficiency < 10:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="CRITICAL",
                reason=(
                    f"High scanning ({scanned:.0f} pages/s) with poor reclaim "
                    f"efficiency ({efficiency:.1f}%)."
                ),
            )
        )

    # ==========================================================
    # Heavy reclaim pressure
    # ==========================================================

    elif scanned >= 1000:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="WARNING",
                reason=(
                    f"Heavy memory reclaim activity "
                    f"({scanned:.0f} scanned, "
                    f"{reclaimed:.0f} reclaimed, "
                    f"{efficiency:.1f}% efficiency)."
                ),
            )
        )

    # ==========================================================
    # Moderate activity
    # ==========================================================

    elif scanned >= 100:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="WARNING",
                reason=(
                    f"Moderate reclaim activity "
                    f"({scanned:.0f} scanned, "
                    f"{reclaimed:.0f} reclaimed, "
                    f"{efficiency:.1f}% efficiency)."
                ),
            )
        )

    # ==========================================================
    # Healthy
    # ==========================================================

    else:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="PASS",
                reason=(
                    f"Light reclaim activity "
                    f"({scanned:.0f} scanned, "
                    f"{reclaimed:.0f} reclaimed, "
                    f"{efficiency:.1f}% efficiency)."
                ),
            )
        )

    return build_result(name="reclaim", state="COMPLETE", checks=checks)
