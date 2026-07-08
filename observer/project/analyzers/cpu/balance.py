"""
CPU Core Balance Analyzer.
Detects uneven workload distribution across CPU cores.
"""

from __future__ import annotations
from project.models.cpu import Cpu_Data, HealthCheck
from project.analyzers.cpu.data import build_result


def analyze_balance(cpu: Cpu_Data):

    checks: list[HealthCheck] = []

    count = 0
    TOTAL = 5

    # =====================================================
    # Hottest Core
    # =====================================================

    if cpu.highest_core_percent is not None:

        if cpu.highest_core_percent >= 95:
            status = "CRITICAL"
        elif cpu.highest_core_percent >= 85:
            status = "WARNING"
        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="Highest Core Utilization",
                status=status,
                reason=f"Hottest CPU core utilization: {cpu.highest_core_percent:.1f}%.",
            )
        )

        count += 1
    # =====================================================
    # Lowest Core Utilization
    # =====================================================

    if cpu.lowest_core_percent is not None:

        if cpu.lowest_core_percent <= 5:
          status = "WARNING"
        else:
          status = "PASS"

        checks.append(
            HealthCheck(
              check="Lowest Core Utilization",
              status=status,
              reason=f"Least utilized CPU core: {cpu.lowest_core_percent:.1f}%.",
            )
        )

        count += 1

    # =====================================================
    # Average Core Utilization
    # =====================================================

    if cpu.average_core_percent is not None:

        if cpu.average_core_percent >= 90:
            status = "CRITICAL"
        elif cpu.average_core_percent >= 65:
            status = "WARNING"
        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="Average Core Utilization",
                status=status,
                reason=f"Average core utilization: {cpu.average_core_percent:.1f}%.",
            )
        )

        count += 1

    # =====================================================
    # Core Imbalance
    # =====================================================

    if cpu.core_imbalance_percent is not None:

        if cpu.core_imbalance_percent >= 50:
            status = "CRITICAL"

        elif cpu.core_imbalance_percent >= 25:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="Core Balance",
                status=status,
                reason=f"Difference between busiest core and average utilization: "
                       f"{cpu.core_imbalance_percent:.1f}%.",
            )
        )

        count += 1
    # =====================================================
    # Core Spread
    # =====================================================

    if cpu.core_spread_percent is not None:

        if cpu.core_spread_percent >= 80:
          status = "CRITICAL"

        elif cpu.core_spread_percent >= 50:
          status = "WARNING"

        else:
          status = "PASS"

        checks.append(
            HealthCheck(
                check="Core Spread",
                status=status,
                reason=f"Difference between busiest and least busy core: "
                       f"{cpu.core_spread_percent:.1f}%.",
            )
        )
        count += 1

    # =====================================================
    # Missing Data
    # =====================================================

    if count == 0:

        checks.append(
            HealthCheck(
                check="Core Balance",
                status="PASS",
                reason="Per-core utilization statistics are unavailable.",
            )
        )

        return build_result(
            name="balance",
            state="UNAVAILABLE",
            checks=checks,
        )

    # =====================================================
    # Result
    # =====================================================

    state = "COMPLETE" if count == TOTAL else "PARTIAL"

    return build_result(
        name="balance",
        state=state,
        checks=checks,
    )
