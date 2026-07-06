"""
Process Memory Analyzer.
"""

from __future__ import annotations
from project.models.memory import MemoryData, HealthCheck

MB = 1024 * 1024


def analyze_process(memory: MemoryData) -> list[HealthCheck]:

    checks: list[HealthCheck] = []

    rss = memory.rss
    uss = memory.uss
    pss = memory.pss

    percent = memory.process_memory_percent
    growth = memory.process_memory_growth_mb_per_sec
    peak = memory.peak_memory

    # ==========================================================
    # Memory Utilization
    # ==========================================================

    if percent is None:
        checks.append(
            HealthCheck(
                check="Process Memory",
                status="PASS",
                reason="Process memory utilization unavailable.",
            )
        )
    elif percent >= 80:
        checks.append(
            HealthCheck(
                check="Process Memory",
                status="CRITICAL",
                reason=f"Process uses {percent:.1f}% of system memory.",
            )
        )
    elif percent >= 50:
        checks.append(
            HealthCheck(
                check="Process Memory",
                status="WARNING",
                reason=f"Process uses {percent:.1f}% of system memory.",
            )
        )
    else:
        checks.append(
            HealthCheck(
                check="Process Memory",
                status="PASS",
                reason=f"Process memory usage is healthy ({percent:.1f}%).",
            )
        )

    # ==========================================================
    # Memory Growth
    # ==========================================================

    if growth is None:
        checks.append(
            HealthCheck(
                check="Process Memory Growth",
                status="PASS",
                reason="Process memory growth unavailable.",
            )
        )
    elif growth > 100:
        checks.append(
            HealthCheck(
                check="Process Memory Growth",
                status="CRITICAL",
                reason=f"Rapid growth detected ({growth:.1f} MB/s).",
            )
        )
    elif growth > 20:
        checks.append(
            HealthCheck(
                check="Process Memory Growth",
                status="WARNING",
                reason=f"Elevated growth detected ({growth:.1f} MB/s).",
            )
        )
    else:
        checks.append(
            HealthCheck(
                check="Process Memory Growth",
                status="PASS",
                reason=f"Stable process memory growth ({growth:.1f} MB/s).",
            )
        )

    # ==========================================================
    # Peak Memory
    # ==========================================================

    if peak is not None:
        checks.append(
            HealthCheck(
                check="Peak Process Memory",
                status="PASS",
                reason=f"Peak usage: {peak / MB:.1f} MB.",
            )
        )

    # ==========================================================
    # Memory Layout
    # ==========================================================

    if rss is None or uss is None or pss is None:
        checks.append(
            HealthCheck(
                check="Process Memory Layout",
                status="PASS",
                reason="Detailed memory layout unavailable.",
            )
        )
    else:
        checks.append(
            HealthCheck(
                check="Process Memory Layout",
                status="PASS",
                reason=(
                    f"RSS={rss / MB:.1f} MB, "
                    f"USS={uss / MB:.1f} MB, "
                    f"PSS={pss / MB:.1f} MB."
                ),
            )
        )

    return checks
