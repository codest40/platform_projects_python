"""
Filesystem Cache Analyzer.

Pure detector for filesystem cache state.
No severity decisions. No interpretation logic.
"""

from __future__ import annotations
from project.models.memory import MemoryData, HealthCheck, AnalyzerResult

get_metadata(x, y, z):
    return AnalyzerResult(name=x, state=y, checks=z,)
# AnalyzerResult(name="Paging", state="UNAVAILABLE",checks=checks,)

def analyze_cache(memory: MemoryData) -> list[HealthCheck]:
    checks: list[HealthCheck] = []

    cache = memory.page_cache
    dirty = memory.dirty_pages
    writeback = memory.writeback_pages

    # ==========================================================
    # Cache Availability
    # ==========================================================

    if cache is None:
        return get_metadata("cache", "UNAVAILABLE", checks = [
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

    return get_metadata("cache", "COMPLETE", checks)
