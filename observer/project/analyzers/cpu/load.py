"""
CPU Load Analyzer.
Detects CPU load relative to available logical cores.
"""

from __future__ import annotations
from project.models.cpu import CpuData, HealthCheck
from project.analyzers.cpu.data import build_result


def analyze_load(cpu: CpuData):
    """
    Analyze normalized CPU load.
    """

    checks: list[HealthCheck] = []

    count = 0
    TOTAL = 3

    loads = [
        ("1 min", cpu.load_per_core_1),
        ("5 min", cpu.load_per_core_5),
        ("15 min", cpu.load_per_core_15),
    ]

    for label, value in loads:

        if value is None:
            continue

        if value >= 1.0:
            status = "CRITICAL"

        elif value >= 0.7:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check=f"Load Average ({label})",
                status=status,
                reason=f"{label} load per logical core: {value:.2f}.",
            )
        )

        count += 1

    # =====================================================
    # Missing Data
    # =====================================================

    if count == 0:
        checks.append(
            HealthCheck(
                check="CPU Load",
                status="PASS",
                reason="CPU load statistics are unavailable.",
            )
        )

        return build_result(
            name="load",
            state="UNAVAILABLE",
            checks=checks,
        )

    # =====================================================
    # Result
    # =====================================================

    state = "COMPLETE" if count == TOTAL else "PARTIAL"

    return build_result(
        name="load",
        state=state,
        checks=checks,
    )
