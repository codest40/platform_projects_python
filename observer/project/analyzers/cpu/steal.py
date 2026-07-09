"""
CPU Steal & Throttling Analyzer.

Analyzes CPU time lost to virtualization or cgroup
throttling.

No severity aggregation.
No interpretation beyond individual checks.
"""

from __future__ import annotations

from project.models.cpu import CpuData
from project.models.events import HealthCheck
from project.analyzers.cpu.data import build_result


def analyze_steal(cpu: CpuData):

    checks: list[HealthCheck] = []

    count = 0
    TOTAL = 2

    # =====================================================
    # CPU Steal Time
    # =====================================================

    if cpu.steal_percent is not None:

        if cpu.steal_percent >= 10:
            status = "CRITICAL"

        elif cpu.steal_percent >= 3:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="CPU Steal Time",
                status=status,
                reason=f"CPU steal time: {cpu.steal_percent:.1f}%.",
            )
        )

        count += 1

    # =====================================================
    # CPU Throttling
    # =====================================================

    if cpu.cpu_throttle_ratio is not None:

        if cpu.cpu_throttle_ratio >= 0.10:
            status = "CRITICAL"

        elif cpu.cpu_throttle_ratio >= 0.02:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="CPU Throttling",
                status=status,
                reason=(
                    f"Throttle ratio: "
                    f"{cpu.cpu_throttle_ratio * 100:.2f}%."
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
                check="Throttled Periods",
                status=status,
                reason=(
                    f"CPU throttling events: "
                    f"{cpu.cpu_throttled_periods_per_sec:.1f} periods/sec."
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
                check="Throttled Time",
                status=status,
                reason=(
                    f"CPU throttled for "
                    f"{throttled_ms:.1f} ms/sec."
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
                check="CPU Steal",
                status="PASS",
                reason="CPU steal and throttling statistics are unavailable.",
            )
        )

        return build_result(
            name="steal",
            state="UNAVAILABLE",
            checks=checks,
        )

    # =====================================================
    # Result
    # =====================================================

    state = "COMPLETE" if count == TOTAL else "PARTIAL"

    return build_result(
        name="steal",
        state=state,
        checks=checks,
    )
