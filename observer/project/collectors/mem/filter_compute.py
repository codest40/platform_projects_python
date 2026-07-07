from project.models.memory import MemoryData
from project.utils.runners import EventRunner


MB = 1024 * 1024


def filter_memory_state(result: EventRunner) -> dict:

    memory = result.data

    return {

        "collected_at": result.collected_at,

        # --------------------------------------------------
        # Swap Counters
        # --------------------------------------------------

        "swap_in": memory.swap_in,
        "swap_out": memory.swap_out,

        "pages_swapped_in": memory.pages_swapped_in,
        "pages_swapped_out": memory.pages_swapped_out,

        # --------------------------------------------------
        # Page Faults
        # --------------------------------------------------

        "major_page_faults": memory.major_page_faults,
        "minor_page_faults": memory.minor_page_faults,
        "total_page_faults": memory.total_page_faults,

        # --------------------------------------------------
        # VM Reclaim
        # --------------------------------------------------

        "pages_scanned": memory.pages_scanned,
        "pages_reclaimed": memory.pages_reclaimed,

        # --------------------------------------------------
        # Pressure
        # --------------------------------------------------

        "allocation_failures": memory.allocation_failures,
        "oom_events": memory.oom_events,
        "container_oom_events": memory.container_oom_events,

        # --------------------------------------------------
        # Memory Size
        # --------------------------------------------------

        "available": memory.available,
        "used": memory.used,
        "cached": memory.cached,
        "dirty_pages": memory.dirty_pages,
        "rss": memory.rss,
        "container_memory_usage": memory.container_memory_usage,
    }


def compute_memory_rates(
    memory: MemoryData,
    previous: dict,
    current: dict,
) -> MemoryData:
    """
    Compute interval metrics between two memory snapshots.
    """
    if previous["collected_at"] is None:
        return memory

    elapsed = current["collected_at"] - previous["collected_at"]

    if elapsed <= 0:
        return memory

    def rate(field: str) -> float:

        prev = previous.get(field)
        curr = current.get(field)

        if prev is None or curr is None:
            return 0.0

        delta = curr - prev

        if delta < 0:
            return 0.0

        return delta / elapsed

    def growth_mb(field: str) -> float:

        prev = previous.get(field)
        curr = current.get(field)

        if prev is None or curr is None:
            return 0.0

        return ((curr - prev) / MB) / elapsed

    # =====================================================
    # Swap Activity
    # =====================================================

    memory.swap_in_mb_per_sec = rate("swap_in") / MB
    memory.swap_out_mb_per_sec = rate("swap_out") / MB

    memory.pages_swapped_in_mb_per_sec = rate("pages_swapped_in")
    memory.pages_swapped_out_mb_per_sec = rate("pages_swapped_out")

    # =====================================================
    # Page Faults
    # =====================================================

    memory.major_page_faults_per_sec = rate(
        "major_page_faults"
    )

    memory.minor_page_faults_per_sec = rate(
        "minor_page_faults"
    )

    memory.page_faults_per_sec = rate(
        "total_page_faults"
    )

    # =====================================================
    # Memory Reclaim
    # =====================================================

    memory.pages_scanned_per_sec = rate(
        "pages_scanned"
    )

    memory.pages_reclaimed_per_sec = rate(
        "pages_reclaimed"
    )

    # =====================================================
    # Allocation / OOM
    # =====================================================

    memory.allocation_failures_per_sec = rate(
        "allocation_failures"
    )

    memory.oom_events_per_sec = rate(
        "oom_events"
    )

    memory.container_oom_events_per_sec = rate(
        "container_oom_events"
    )

    # =====================================================
    # Memory Growth (MB/sec)
    # =====================================================

    memory.available_memory_change_mb_per_sec = growth_mb(
        "available"
    )

    memory.used_memory_change_mb_per_sec = growth_mb(
        "used"
    )

    memory.cache_growth_mb_per_sec = growth_mb(
        "cached"
    )

    memory.dirty_growth_mb_per_sec = growth_mb(
        "dirty_pages"
    )

    memory.process_memory_growth_mb_per_sec = growth_mb(
        "rss"
    )

    memory.container_memory_growth_mb_per_sec = growth_mb(
        "container_memory_usage"
    )

    memory.seen = True

    return memory
