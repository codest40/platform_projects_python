"""
CPU Container Analyzer.

Detects CPU throttling experienced by container workloads.

Pure detector.
No summary logic.
"""

from __future__ import annotations

from project.models.cpu import CpuData
from project.models.events import HealthCheck
from project.analyzers.cpu.data import build_result


def analyze_container(cpu: CpuData):

    checks: list[HealthCheck] = []

    count = 0
    TOTAL = 3

    # =====================================================
    # Throttle Ratio
    # =====================================================

    if cpu.cpu_throttle_ratio is not None:

        if cpu.cpu_throttle_ratio >= 0.20:
            status = "CRITICAL"

        elif cpu.cpu_throttle_ratio >= 0.05:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="CPU Throttle Ratio",
                status=status,
                reason=(
                    f"CPU throttle ratio: "
                    f"{cpu.cpu_throttle_ratio:.3f}."
                ),
            )
        )

        count += 1

    # =====================================================
    # Throttled Periods
    # =====================================================

    if cpu.cpu_throttled_periods_per_sec is not None:

        if cpu.cpu_throttled_periods_per_sec >= 100:
            status = "CRITICAL"

        elif cpu.cpu_throttled_periods_per_sec >= 20:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="CPU Throttled Periods",
                status=status,
                reason=(
                    f"CPU throttled periods: "
                    f"{cpu.cpu_throttled_periods_per_sec:.2f} per second."
                ),
            )
        )

        count += 1

    # =====================================================
    # Throttled Time
    # =====================================================

    if cpu.cpu_throttled_usec_per_sec is not None:

        throttled_ms = cpu.cpu_throttled_usec_per_sec / 1000

        if throttled_ms >= 100:
            status = "CRITICAL"

        elif throttled_ms >= 20:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="CPU Throttled Time",
                status=status,
                reason=(
                    f"CPU throttled time: "
                    f"{throttled_ms:.2f} ms/sec."
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
                check="Container CPU",
                status="PASS",
                reason="Container CPU throttling statistics are unavailable.",
            )
        )

        return build_result(
            name="container",
            state="UNAVAILABLE",
            checks=checks,
        )

    # =====================================================
    # Result
    # =====================================================

    state = "COMPLETE" if count == TOTAL else "PARTIAL"

    return build_result(
        name="container",
        state=state,
        checks=checks,
    )
