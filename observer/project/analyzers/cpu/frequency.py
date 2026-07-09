"""
CPU Frequency Analyzer.

Analyzes CPU operating frequency and scaling.

No severity aggregation.
No interpretation beyond individual checks.
"""

from __future__ import annotations

from project.models.cpu import CpuData
from project.models.events import HealthCheck
from project.analyzers.cpu.data import build_result


def analyze_frequency(cpu: CpuData):

    checks: list[HealthCheck] = []

    count = 0
    TOTAL = 4

    # =====================================================
    # Current Frequency
    # =====================================================

    if cpu.frequency_mhz is not None:

        checks.append(
            HealthCheck(
                check="Current Frequency",
                status="PASS",
                reason=f"Current CPU frequency: {cpu.frequency_mhz:.0f} MHz.",
            )
        )

        count += 1

    # =====================================================
    # Minimum Frequency
    # =====================================================

    if cpu.min_frequency_mhz is not None:

        checks.append(
            HealthCheck(
                check="Minimum Frequency",
                status="PASS",
                reason=f"Minimum CPU frequency: {cpu.min_frequency_mhz:.0f} MHz.",
            )
        )

        count += 1

    # =====================================================
    # Maximum Frequency
    # =====================================================

    if cpu.max_frequency_mhz is not None:

        checks.append(
            HealthCheck(
                check="Maximum Frequency",
                status="PASS",
                reason=f"Maximum CPU frequency: {cpu.max_frequency_mhz:.0f} MHz.",
            )
        )

        count += 1

    # =====================================================
    # Frequency Ratio
    # =====================================================

    if cpu.frequency_ratio is not None:

        if cpu.frequency_ratio <= 0.30:
            status = "CRITICAL"

        elif cpu.frequency_ratio <= 0.60:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="Frequency Scaling",
                status=status,
                reason=(
                    f"CPU is operating at "
                    f"{cpu.frequency_ratio * 100:.1f}% "
                    f"of its maximum frequency."
                ),
            )
        )

        count += 1

    # =====================================================
    # Missing Data
    # =====================================================

    if count == 0:

        checks.append(
            HealthCheck(
                check="CPU Frequency",
                status="PASS",
                reason="CPU frequency statistics are unavailable.",
            )
        )

        return build_result(
            name="frequency",
            state="UNAVAILABLE",
            checks=checks,
        )

    # =====================================================
    # Result
    # =====================================================

    state = "COMPLETE" if count == TOTAL else "PARTIAL"

    return build_result(
        name="frequency",
        state=state,
        checks=checks,
    )
