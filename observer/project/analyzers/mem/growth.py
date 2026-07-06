"""
Memory Growth Analyzer.

Pure detector for interval-based memory change signals.
"""

from __future__ import annotations

from project.models.memory import MemoryData, HealthCheck

def analyze_memory_growth(
    memory: MemoryData,
) -> list[HealthCheck]:

    # ==========================================================
    # Used Memory Growth
    # ==========================================================
    checks: list[HealthCheck] = []

    if memory.used_memory_change_mb_per_sec is not None:
        checks.append(
            HealthCheck(
                check="Used Memory Growth",
                status="PASS",
                reason=(
                    f"Used memory change: "
                    f"{memory.used_memory_change_mb_per_sec:.2f} MB/s"
                ),
            )
        )

    # ==========================================================
    # Available Memory Change
    # ==========================================================

    if memory.available_memory_change_mb_per_sec is not None:
        checks.append(
            HealthCheck(
                check="Available Memory Change",
                status="PASS",
                reason=(
                    f"Available memory change: "
                    f"{memory.available_memory_change_mb_per_sec:.2f} MB/s"
                ),
            )
        )

    # ==========================================================
    # Cache Growth
    # ==========================================================

    if memory.cache_growth_mb_per_sec is not None:
        checks.append(
            HealthCheck(
                check="Cache Growth",
                status="PASS",
                reason=(
                    f"Cache growth: "
                    f"{memory.cache_growth_mb_per_sec:.2f} MB/s"
                ),
            )
        )

    # ==========================================================
    # Dirty Page Growth
    # ==========================================================

    if memory.dirty_growth_mb_per_sec is not None:
        checks.append(
            HealthCheck(
                check="Dirty Page Growth",
                status="PASS",
                reason=(
                    f"Dirty page growth: "
                    f"{memory.dirty_growth_mb_per_sec:.2f} MB/s"
                ),
            )
        )

    # ==========================================================
    # Process Memory Growth
    # ==========================================================

    if memory.process_memory_growth_mb_per_sec is not None:
        checks.append(
            HealthCheck(
                check="Process Memory Growth",
                status="PASS",
                reason=(
                    f"Process memory growth: "
                    f"{memory.process_memory_growth_mb_per_sec:.2f} MB/s"
                ),
            )
        )

    # ==========================================================
    # Container Memory Growth
    # ==========================================================

    if memory.container_memory_growth_mb_per_sec is not None:
        checks.append(
            HealthCheck(
                check="Container Memory Growth",
                status="PASS",
                reason=(
                    f"Container memory growth: "
                    f"{memory.container_memory_growth_mb_per_sec:.2f} MB/s"
                ),
            )
        )

    return checks
