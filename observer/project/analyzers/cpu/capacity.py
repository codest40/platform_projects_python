"""
CPU Capacity Analyzer.
Detects whether CPU compute capacity is becoming exhausted.
"""

from __future__ import annotations
from project.models.cpu import Cpu_Data, HealthCheck
from project.analyzers.cpu.data import build_result


def analyze_capacity(cpu: Cpu_Data):

    checks: list[HealthCheck] = []
    count = 0
    TOTAL = 4

    # =====================================================
    # CPU Utilization
    # =====================================================

    if cpu.usage_percent is not None:

        if cpu.usage_percent >= 90:
            status = "CRITICAL"
        elif cpu.usage_percent >= 70:
            status = "WARNING"
        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="CPU Utilization",
                status=status,
                reason=f"CPU utilization: {cpu.usage_percent:.1f}%.",
            )
        )
        count += 1

    # =====================================================
    # Idle CPU
    # =====================================================

    if cpu.idle_percent is not None:

        if cpu.idle_percent <= 10:
            status = "CRITICAL"
        elif cpu.idle_percent <= 30:
            status = "WARNING"
        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="Idle CPU",
                status=status,
                reason=f"Idle CPU time: {cpu.idle_percent:.1f}%.",
            )
        )
        count += 1

    # =====================================================
    # Operating Frequency
    # =====================================================

    if cpu.frequency_ratio is not None:

        if cpu.frequency_ratio < 0.50:
            status = "WARNING"
        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="Operating Frequency",
                status=status,
                reason=f"CPU frequency ratio: {cpu.frequency_ratio:.2f}.",
            )
        )
        count += 1

    # =====================================================
    # CPU Throttling
    # =====================================================

    if cpu.throttle_ratio is not None:

        if cpu.throttle_ratio >= 0.10:
            status = "CRITICAL"
        elif cpu.throttle_ratio > 0:
            status = "WARNING"
        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="CPU Throttling",
                status=status,
                reason=f"Throttle ratio: {cpu.throttle_ratio:.3f}.",
            )
        )
        count += 1

    # =====================================================
    # Missing Data
    # =====================================================

    if count == 0:
        checks.append(
            HealthCheck(
                check="CPU Capacity",
                status="PASS",
                reason="CPU capacity statistics are unavailable.",
            )
        )

        return build_result(
            name="capacity",
            state="UNAVAILABLE",
            checks=checks,
        )

    state = "COMPLETE" if count == TOTAL else "PARTIAL"

    return build_result(
        name="capacity",
        state=state,
        checks=checks,
    )
