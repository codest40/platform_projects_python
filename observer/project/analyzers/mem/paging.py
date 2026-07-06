"""
Memory Paging Analyzer.
Evaluates page fault activity using interval rates.
"""

from __future__ import annotations

from project.models.memory import MemoryData, HealthCheck

def analyze_memory_paging(
    memory: MemoryData,
) -> list[HealthCheck]:

    checks: list[HealthCheck] = []
    total = memory.page_faults_per_sec
    major = memory.major_page_faults_per_sec
    minor = memory.minor_page_faults_per_sec

    # ==========================================================
    # Missing Data Guard
    # ==========================================================

    if total is None or major is None or minor is None:
        checks.append(
            HealthCheck(
                check="Memory Paging",
                status="PASS",
                reason="Page fault statistics are unavailable.",
            )
        )
        return checks

    # ==========================================================
    # Major Page Faults
    # ==========================================================

    if major >= 100:
        checks.append(
            HealthCheck(
                check="Major Page Faults",
                status="CRITICAL",
                reason=(
                    f"Major page faults at {major:.2f}/s. "
                    "Frequent disk-backed page fetches."
                ),
            )
        )

    elif major >= 10:
        checks.append(
            HealthCheck(
                check="Major Page Faults",
                status="WARNING",
                reason=f"Elevated major page fault rate ({major:.2f}/s).",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Major Page Faults",
                status="PASS",
                reason=f"Major page fault rate is normal ({major:.2f}/s).",
            )
        )

    # ==========================================================
    # Minor Page Faults
    # ==========================================================

    if minor >= 50000:
        checks.append(
            HealthCheck(
                check="Minor Page Faults",
                status="WARNING",
                reason=f"High minor page fault rate ({minor:.0f}/s).",
            )
        )
    else:
        checks.append(
            HealthCheck(
                check="Minor Page Faults",
                status="PASS",
                reason=f"Minor page fault rate normal ({minor:.0f}/s).",
            )
        )

    return checks
