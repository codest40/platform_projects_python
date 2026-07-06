"""
Memory OOM / Allocation Failure Analyzer.
"""

from __future__ import annotations
from project.models.memory import MemoryData, HealthCheck
from project.analyzers.mem.data import build_result

def analyze_oom(memory: MemoryData) -> build_result(name, state, checks=list[HealthCheck]):
    """
    Analyze Out-Of-Memory activity.
    Focuses on actual memory exhaustion rather than
    memory pressure.
    """

    checks: list[HealthCheck] = []

    oom_rate = memory.oom_events_per_sec
    container_oom_rate = memory.container_oom_events_per_sec
    alloc_rate = memory.allocation_failures_per_sec

    total_oom = memory.oom_events
    container_oom = memory.container_oom_events
    alloc_total = memory.allocation_failures
    count=0

    # ==========================================================
    # Kernel OOM
    # ==========================================================

    if total_oom is None:
        checks.append(
            HealthCheck(
                check="Kernel OOM",
                status="PASS",
                reason="Kernel OOM statistics are unavailable.",
            )
        )

    elif oom_rate is not None and oom_rate > 0:
        checks.append(
            HealthCheck(
                check="Kernel OOM",
                status="CRITICAL",
                reason=(
                    f"Kernel OOM killer is active "
                    f"({oom_rate:.2f} events/sec). "
                    "Processes are being terminated due to memory exhaustion."
                ),
            )
        )
        count += 1

    elif total_oom > 0:
        checks.append(
            HealthCheck(
                check="Kernel OOM",
                status="WARNING",
                reason=(
                    f"{total_oom:,} kernel OOM event(s) have occurred since boot. "
                    "No new OOM events occurred during this interval."
                ),
            )
        )
        count += 1

    else:
        checks.append(
            HealthCheck(
                check="Kernel OOM",
                status="PASS",
                reason="No kernel OOM events detected.",
            )
        )
        count += 1

    # ==========================================================
    # Container OOM
    # ==========================================================

    if container_oom is None:
        checks.append(
            HealthCheck(
                check="Container OOM",
                status="PASS",
                reason="Container OOM statistics are unavailable.",
            )
        )

    elif container_oom_rate is not None and container_oom_rate > 0:
        checks.append(
            HealthCheck(
                check="Container OOM",
                status="CRITICAL",
                reason=(
                    f"Container OOM kills are occurring "
                    f"({container_oom_rate:.2f} events/sec)."
                ),
            )
        )
        count += 1

    elif container_oom > 0:
        checks.append(
            HealthCheck(
                check="Container OOM",
                status="WARNING",
                reason=(
                    f"{container_oom:,} container OOM kill(s) "
                    "have occurred since container startup."
                ),
            )
        )
        count += 1

    else:
        checks.append(
            HealthCheck(
                check="Container OOM",
                status="PASS",
                reason="No container OOM events detected.",
            )
        )
        count += 1

    # ==========================================================
    # Allocation Failures
    # ==========================================================

    if alloc_total is None:
        checks.append(
            HealthCheck(
                check="Allocation Failures",
                status="PASS",
                reason="Allocation failure statistics are unavailable.",
            )
        )

    elif alloc_rate is not None and alloc_rate > 0:
        checks.append(
            HealthCheck(
                check="Allocation Failures",
                status="CRITICAL",
                reason=(
                    f"Memory allocation failures are occurring "
                    f"({alloc_rate:.2f} failures/sec). "
                    "The kernel cannot satisfy allocation requests."
                ),
            )
        )
        count += 1

    elif alloc_total > 0:
        checks.append(
            HealthCheck(
                check="Allocation Failures",
                status="WARNING",
                reason=(
                    f"{alloc_total:,} allocation failure(s) "
                    "have occurred since boot."
                ),
            )
        )
        count += 1

    else:
        checks.append(
            HealthCheck(
                check="Allocation Failures",
                status="PASS",
                reason="No allocation failures detected.",
            )
        )
        count += 1

    TOTAL=3
    if TOTAL==count:
      state="COMPLETE"
    elif count == 0:
      state="UNAVAILABLE"
    else:
      state="PARTIAL"

    return build_result(name="oom", state=state, checks=checks)
