"""
Memory Commit Accounting Analyzer.

Pure detector for Linux commit accounting state.
No thresholds. No severity logic. No system interpretation.
"""

from __future__ import annotations
from project.models.memory import MemoryData, HealthCheck
from project.analyzers.mem.data import build_result

def analyze_commit(memory: MemoryData) -> build_result(name, state, checks=list[HealthCheck]):
    checks: list[HealthCheck] = []

    commit = memory.commit_percent
    committed = memory.committed_as
    limit = memory.commit_limit

    # ==========================================================
    # Availability
    # ==========================================================

    if commit is None or committed is None or limit is None:
        return build_result(name="commit", state="UNAVAILABLE", checks=[
            HealthCheck(
                check="Commit Accounting",
                status="PASS",
                reason="Commit accounting statistics are unavailable.",
            )
        ])

    # ==========================================================
    # Raw Commit Snapshot
    # ==========================================================

    checks.append(
        HealthCheck(
            check="Commit Accounting",
            status="PASS",
            reason=(
                f"Commit usage: {commit:.1f}% | "
                f"Committed: {committed:,} bytes | "
                f"Limit: {limit:,} bytes"
            ),
        )
    )

    # ==========================================================
    # Informational Context Only (NO DECISIONS)
    # ==========================================================

    checks.append(
        HealthCheck(
            check="Commit Context",
            status="PASS",
            reason=(
                "Commit accounting reflects virtual memory promises "
                "and may exceed physical memory depending on overcommit settings."
            ),
        )
    )

    return build_result(name="capacity", state="COMPLETE", checks=checks)
