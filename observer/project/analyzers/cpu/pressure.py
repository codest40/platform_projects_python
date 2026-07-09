"""
CPU Pressure Analyzer.

Analyzes Linux PSI (Pressure Stall Information)
for CPU scheduling pressure.

No severity aggregation.
No interpretation beyond individual checks.
"""

from __future__ import annotations

from project.models.cpu import CpuData, HealthCheck
from project.analyzers.cpu.data import build_result


def analyze_pressure(cpu: CpuData):

    checks: list[HealthCheck] = []

    count = 0
    TOTAL = 6

    metrics = [
        ("CPU PSI Some (10s)", cpu.psi_some_avg10),
        ("CPU PSI Some (60s)", cpu.psi_some_avg60),
        ("CPU PSI Some (300s)", cpu.psi_some_avg300),
        ("CPU PSI Full (10s)", cpu.psi_full_avg10),
        ("CPU PSI Full (60s)", cpu.psi_full_avg60),
        ("CPU PSI Full (300s)", cpu.psi_full_avg300),
    ]

    for check_name, value in metrics:

        if value is None:
            continue

        # =====================================================
        # Full Stall PSI
        # =====================================================

        if "Full" in check_name:

            if value >= 5:
                status = "CRITICAL"

            elif value >= 1:
                status = "WARNING"

            else:
                status = "PASS"

        # =====================================================
        # Some Stall PSI
        # =====================================================

        else:

            if value >= 20:
                status = "CRITICAL"

            elif value >= 5:
                status = "WARNING"

            else:
                status = "PASS"

        checks.append(
            HealthCheck(
                check=check_name,
                status=status,
                reason=f"{check_name}: {value:.2f}%.",
            )
        )

        count += 1

    # =====================================================
    # Missing Data
    # =====================================================

    if count == 0:

        checks.append(
            HealthCheck(
                check="CPU Pressure",
                status="PASS",
                reason="CPU PSI statistics are unavailable.",
            )
        )

        return build_result(
            name="pressure",
            state="UNAVAILABLE",
            checks=checks,
        )

    # =====================================================
    # Result
    # =====================================================

    state = "COMPLETE" if count == TOTAL else "PARTIAL"

    return build_result(
        name="pressure",
        state=state,
        checks=checks,
    )
