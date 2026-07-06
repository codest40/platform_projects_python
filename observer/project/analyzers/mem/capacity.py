"""
Memory Capacity Analyzer.

Pure detector for host memory capacity state.
No severity logic. No thresholds. No interpretation.
"""

from __future__ import annotations
from project.models.memory import MemoryData, HealthCheck

def analyze_capacity(
    memory: MemoryData,
) -> list[HealthCheck]:
    """
    Analyze host memory capacity snapshot.
    """

    checks: list[HealthCheck] = []
    available = memory.available_percent
    used = memory.used_percent

    # =====================================================
    # Availability Signal
    # =====================================================

    if available is not None:
        checks.append(
            HealthCheck(
                check="Memory Capacity - Available",
                status="PASS",
                reason=f"Available memory snapshot: {available:.1f}%",
            )
        )

    # =====================================================
    # Usage Signal
    # =====================================================

    if used is not None:
        checks.append(
            HealthCheck(
                check="Memory Capacity - Used",
                status="PASS",
                reason=f"Used memory snapshot: {used:.1f}%",
            )
        )

    # =====================================================
    # Missing Data Case
    # =====================================================

    if available is None and used is None:
        checks.append(
            HealthCheck(
                check="Memory Capacity",
                status="PASS",
                reason="Memory capacity statistics are unavailable.",
            )
        )

    return checks
