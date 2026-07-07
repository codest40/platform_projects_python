"""
Process Memory Analyzer.
"""

from __future__ import annotations
from project.models.memory import MemoryData, HealthCheck
from project.analyzers.mem.data import build_result

MB = 1024 * 1024


def analyze_process(memory: MemoryData) -> build_result(name, state, checks=list[HealthCheck]):

    checks: list[HealthCheck] = []

    rss = memory.rss
    uss = memory.uss
    pss = memory.pss

    percent = memory.process_memory_percent
    growth = memory.process_memory_growth_mb_per_sec
    peak = memory.peak_memory

    count = 0
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
        count+=1

    elif percent >= 50:
        checks.append(
            HealthCheck(
                check="Process Memory",
                status="WARNING",
                reason=f"Process uses {percent:.1f}% of system memory.",
            )
        )
        count+=1
    else:
        checks.append(
            HealthCheck(
                check="Process Memory",
                status="PASS",
                reason=f"Process memory usage is healthy ({percent:.1f}%).",
            )
        )
        count+=1

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
        count+=1

    elif growth > 20:
        checks.append(
            HealthCheck(
                check="Process Memory Growth",
                status="WARNING",
                reason=f"Elevated growth detected ({growth:.1f} MB/s).",
            )
        )
        count+=1
    else:
        checks.append(
            HealthCheck(
                check="Process Memory Growth",
                status="PASS",
                reason=f"Stable process memory growth ({growth:.1f} MB/s).",
            )
        )
        count+=1

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
        count+=1

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
        count+=1

    TOTAL=4
    if TOTAL==count:
      state="COMPLETE"
    else:
      state="PARTIAL"

    return build_result(name="process", state=state, checks=checks)
