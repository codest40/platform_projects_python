"""
Memory Paging Analyzer.
Evaluates page fault activity using interval rates.
"""

from __future__ import annotations

from project.models.memory import MemoryData, HealthCheck
from project.analyzers.mem.data import build_result

def analyze_memory_paging(
    memory: MemoryData,
) -> build_result(name, state, list[HealthCheck]):

    checks: list[HealthCheck] = []
    total = memory.page_faults_per_sec
    major = memory.major_page_faults_per_sec
    minor = memory.minor_page_faults_per_sec
    count=0

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
        return build_result(name="paging", state="UNAVAILABLE", checks=checks)

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
        count+=1

    elif major >= 10:
        checks.append(
            HealthCheck(
                check="Major Page Faults",
                status="WARNING",
                reason=f"Elevated major page fault rate ({major:.2f}/s).",
            )
        )
        count+=1

    else:
        checks.append(
            HealthCheck(
                check="Major Page Faults",
                status="PASS",
                reason=f"Major page fault rate is normal ({major:.2f}/s).",
            )
        )
        count+=1

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
        count+=1

    else:
        checks.append(
            HealthCheck(
                check="Minor Page Faults",
                status="PASS",
                reason=f"Minor page fault rate normal ({minor:.0f}/s).",
            )
        )

    TOTAL=2
    if TOTAL==count:
      state="COMPLETE"
    else:
      state="PARTIAL"

    return build_result(name="paging", state=state, checks=checks)
