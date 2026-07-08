"""
CPU IO Wait Analyzer.

Detects CPU time spent waiting for storage IO.
"""

from __future__ import annotations

from project.models.cpu import Cpu_Data
from project.models.events import HealthCheck
from project.analyzers.cpu.data import build_result


def analyze_iowait(cpu: Cpu_Data):
    checks: list[HealthCheck] = []
    count = 0

    if cpu.iowait_percent is not None:

        if cpu.iowait_percent >= 20:
            status = "CRITICAL"

        elif cpu.iowait_percent >= 5:
            status = "WARNING"

        else:
            status = "PASS"

        checks.append(
            HealthCheck(
                check="IO Wait",
                status=status,
                reason=f"CPU time waiting for IO: {cpu.iowait_percent:.1f}%.",
            )
        )
        count += 1

    if count == 0:
        checks.append(
            HealthCheck(
                check="IO Wait",
                status="PASS",
                reason="IO wait statistics are unavailable.",
            )
        )
        return build_result(
            name="iowait",
            state="UNAVAILABLE",
            checks=checks,
        )

    return build_result(
        name="iowait",
        state="COMPLETE",
        checks=checks,
    )
