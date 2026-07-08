"""
CPU Kernel Activity Analyzer.
Analyzes how CPU time is divided between user-space
and kernel-space execution.
"""

from __future__ import annotations

from project.models.cpu import Cpu_Data, HealthCheck
from project.analyzers.cpu.data import build_result


def analyze_kernel(cpu: Cpu_Data):

    checks: list[HealthCheck] = []

    count = 0
    TOTAL = 3

    # =====================================================
    # Kernel CPU Time
    # =====================================================

    if cpu.system_percent is not None:

        if cpu.system_percent > 50:
            status = "CRITICAL"

        elif cpu.system_percent >= 20:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="Kernel CPU Time",
                status=status,
                reason=f"Kernel CPU utilization: {cpu.system_percent:.1f}%.",
            )
        )

        count += 1

    # =====================================================
    # User CPU Time
    # =====================================================

    if cpu.user_percent is not None:

        checks.append(
            HealthCheck(
                check="User CPU Time",
                status="PASS",
                reason=f"User CPU utilization: {cpu.user_percent:.1f}%.",
            )
        )

        count += 1

    # =====================================================
    # Kernel Ratio
    # =====================================================

    if cpu.kernel_ratio is not None:

        if cpu.kernel_ratio >= 0.60:
            status = "CRITICAL"

        elif cpu.kernel_ratio >= 0.40:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="Kernel Ratio",
                status=status,
                reason=(
                    f"Kernel accounts for "
                    f"{cpu.kernel_ratio * 100:.1f}% "
                    f"of active CPU time."
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
                check="Kernel Activity",
                status="PASS",
                reason="Kernel CPU statistics are unavailable.",
            )
        )

        return build_result(
            name="kernel",
            state="UNAVAILABLE",
            checks=checks,
        )

    # =====================================================
    # Result
    # =====================================================

    state = "COMPLETE" if count == TOTAL else "PARTIAL"

    return build_result(
        name="kernel",
        state=state,
        checks=checks,
    )
