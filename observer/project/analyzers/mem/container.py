"""
Container Memory Analyzer.
"""

from __future__ import annotations
from project.models.memory import MemoryData, HealthCheck
from project.analyzers.mem.data import build_result

MB = 1024 * 1024


def analyze_container(memory: MemoryData) -> build_result(name, state, checks=list[HealthCheck]):
    """
    Analyze container memory utilization.
    This analyzer evaluates memory usage relative to the
    container's configured cgroup memory limit.
    """

    checks: list[HealthCheck] = []

    usage = memory.container_memory_usage
    limit = memory.container_memory_limit

    working_set = memory.container_working_set
    rss = memory.container_rss
    cache = memory.container_cache

    growth = memory.container_memory_growth_mb_per_sec
    oom_rate = memory.container_oom_events_per_sec

    count=0

    # ----------------------------------------------------------
    # Not running inside a memory-limited container
    # ----------------------------------------------------------

    if usage is None or limit is None:
        checks.append(
            HealthCheck(
                check="Container Memory",
                status="PASS",
                reason=(
                    "Container memory limits are unavailable "
                    "or this workload is not running inside a "
                    "memory-limited cgroup."
                ),
            )
        )
        return build_result(name="container", state="UNAVAILABLE", checks)

    utilization = usage / limit * 100

    # ----------------------------------------------------------
    # Utilization
    # ----------------------------------------------------------

    if utilization >= 95:
        checks.append(
            HealthCheck(
                check="Container Memory",
                status="CRITICAL",
                reason=(
                    f"Container memory utilization is "
                    f"{utilization:.1f}% of its configured limit."
                ),
            )
        )
        count += 1

    elif utilization >= 85:
        checks.append(
            HealthCheck(
                check="Container Memory",
                status="WARNING",
                reason=(
                    f"Container memory utilization is "
                    f"{utilization:.1f}% of its configured limit."
                ),
            )
        )
        count += 1

    else:
        checks.append(
            HealthCheck(
                check="Container Memory",
                status="PASS",
                reason=(
                    f"Container memory utilization is healthy "
                    f"({utilization:.1f}% of limit)."
                ),
            )
        )
        count += 1

    # ----------------------------------------------------------
    # Working Set
    # ----------------------------------------------------------

    if working_set is not None and utilization >= 90:
        checks.append(
            HealthCheck(
                check="Container Working Set",
                status="WARNING",
                reason=(
                    f"Working set is {working_set / MB:.1f} MB. "
                    "Most allocated memory appears actively used."
                ),
            )
        )
        count += 1

    # ----------------------------------------------------------
    # Memory Growth
    # ----------------------------------------------------------

    if growth is not None and growth > 50:
        checks.append(
            HealthCheck(
                check="Container Memory Growth",
                status="WARNING",
                reason=(
                    f"Container memory is increasing at "
                    f"{growth:.1f} MB/sec."
                ),
            )
        )
        count += 1

    # ----------------------------------------------------------
    # RSS
    # ----------------------------------------------------------

    if rss is not None:
        checks.append(
            HealthCheck(
                check="Container RSS",
                status="PASS",
                reason=f"Resident memory is {rss / MB:.1f} MB.",
            )
        )
        count += 1

    # ----------------------------------------------------------
    # Cache
    # ----------------------------------------------------------

    if cache is not None:
        checks.append(
            HealthCheck(
                check="Container Cache",
                status="PASS",
                reason=f"Filesystem cache is {cache / MB:.1f} MB.",
            )
        )
        count += 1

    # ----------------------------------------------------------
    # Container OOM
    # ----------------------------------------------------------

    if oom_rate is not None and oom_rate > 0:
        checks.append(
            HealthCheck(
                check="Container OOM",
                status="CRITICAL",
                reason=(
                    "Container OOM kills are occurring "
                    "during this collection interval."
                ),
            )
        )
        count += 1

    TOTAL=6
    if TOTAL == count:
      state="COMPLETED"
    else:
      state="PARTIAL"

    return build_result(name="container", state=state, checks=checks)

