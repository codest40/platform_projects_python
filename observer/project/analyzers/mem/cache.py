"""
Filesystem Cache Analyzer.

Pure detector for filesystem cache state.
No severity decisions. No interpretation logic.
"""

from __future__ import annotations
from project.models.memory import MemoryData, HealthCheck, AnalyzerResult
from project.analyzers.mem.data import build_result

def analyze_cache(memory: MemoryData) -> build_result(name, state, checks=list[HealthCheck]):
    checks: list[HealthCheck] = []

    cache = memory.page_cache
    dirty = memory.dirty_pages
    writeback = memory.writeback_pages
    available = 0

    # ==========================================================
    # Cache Availability
    # ==========================================================

    if cache is None:
        return build_result(name="cache", state="UNAVAILABLE", checks = [
            HealthCheck(
                check="Filesystem Cache",
                status="PASS",
                reason="Filesystem cache statistics are unavailable.",
            )
        ])

    # ==========================================================
    # Writeback State (RAW SIGNAL ONLY)
    # ==========================================================

    if writeback is not None:
        checks.append(
            HealthCheck(
                check="Filesystem Cache - Writeback",
                status="PASS",
                reason=(
                    f"Writeback pages detected: {writeback} bytes. "
                    "Represents pages being flushed to storage."
                ),
            )
        )
        available += 1
    # ==========================================================
    # Dirty Page State (RAW SIGNAL ONLY)
    # ==========================================================

    if dirty is not None:
        checks.append(
            HealthCheck(
                check="Filesystem Cache - Dirty Pages",
                status="PASS",
                reason=(
                    f"Dirty pages detected: {dirty} bytes. "
                    "Represents modified pages pending flush."
                ),
            )
        )
        available += 1

    # ==========================================================
    # Cache Presence Signal
    # ==========================================================

    checks.append(
        HealthCheck(
            check="Filesystem Cache",
            status="PASS",
            reason="Filesystem cache snapshot collected successfully.",
        )
    )

    TOTAL=2
    if TOTAL == available:
      state="COMPLETE"
    else:
      state="PARTIAL"

    return build_result(name="cache", state=state, checks=checks)
