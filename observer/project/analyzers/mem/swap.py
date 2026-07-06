"""
Swap Analyzer.

Evaluates swap configuration, utilization,
and swap activity over time.
"""

from __future__ import annotations

from project.models.memory import MemoryData, HealthCheck

def analyze_swap(
    memory: MemoryData,
) -> list[HealthCheck]:

    # ==========================================================
    # Swap Configuration
    # ==========================================================
    checks: list[HealthCheck] = []
    if memory.swap_total is None or memory.swap_total == 0:

        checks.append(
            HealthCheck(
                check="Swap",
                status="PASS",
                reason="No swap space is configured on this system.",
            )
        )

        return checks

    # ==========================================================
    # Swap Utilization
    # ==========================================================

    swap_percent = memory.swap_percent

    if swap_percent is None:
        checks.append(
            HealthCheck(
                check="Swap Utilization",
                status="PASS",
                reason="Swap utilization data unavailable.",
            )
        )
    elif swap_percent >= 80:
        checks.append(
            HealthCheck(
                check="Swap Utilization",
                status="CRITICAL",
                reason=f"Swap utilization very high ({swap_percent:.1f}%).",
            )
        )
    elif swap_percent >= 30:
        checks.append(
            HealthCheck(
                check="Swap Utilization",
                status="WARNING",
                reason=f"Swap utilization elevated ({swap_percent:.1f}%).",
            )
        )
    else:
        checks.append(
            HealthCheck(
                check="Swap Utilization",
                status="PASS",
                reason=f"Swap utilization healthy ({swap_percent:.1f}%).",
            )
        )

    # ==========================================================
    # Swap IO Activity (MB/s level signal)
    # ==========================================================

    swap_in = memory.swap_in_mb_per_sec
    swap_out = memory.swap_out_mb_per_sec

    if swap_in is None or swap_out is None:
        checks.append(
            HealthCheck(
                check="Swap Activity",
                status="PASS",
                reason="Swap IO activity data unavailable.",
            )
        )
    elif swap_in >= 10 or swap_out >= 10:
        checks.append(
            HealthCheck(
                check="Swap Activity",
                status="CRITICAL",
                reason=f"High swap IO activity (in={swap_in:.2f}, out={swap_out:.2f} MB/s).",
            )
        )
    elif swap_in > 0 or swap_out > 0:
        checks.append(
            HealthCheck(
                check="Swap Activity",
                status="WARNING",
                reason=f"Swap IO activity detected (in={swap_in:.2f}, out={swap_out:.2f} MB/s).",
            )
        )
    else:
        checks.append(
            HealthCheck(
                check="Swap Activity",
                status="PASS",
                reason="No swap IO activity detected.",
            )
        )

    # ==========================================================
    # Swap Paging Activity (separate domain)
    # ==========================================================

    pages_in = memory.pages_swapped_in
    pages_out = memory.pages_swapped_out

    if pages_in is None or pages_out is None:
        checks.append(
            HealthCheck(
                check="Swap Paging",
                status="PASS",
                reason="Swap paging statistics unavailable.",
            )
        )
    elif pages_in >= 1000 or pages_out >= 1000:
        checks.append(
            HealthCheck(
                check="Swap Paging",
                status="CRITICAL",
                reason=f"Heavy swap paging (in={pages_in}, out={pages_out}).",
            )
        )
    elif pages_in > 0 or pages_out > 0:
        checks.append(
            HealthCheck(
                check="Swap Paging",
                status="WARNING",
                reason=f"Swap paging activity detected (in={pages_in}, out={pages_out}).",
            )
        )
    else:
        checks.append(
            HealthCheck(
                check="Swap Paging",
                status="PASS",
                reason="No swap paging activity detected.",
            )
        )

    return checks
