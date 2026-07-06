from __future__ import annotations
from pathlib import Path
from project.models.memory import MemoryData


VMSTAT = Path("/proc/vmstat")
def _read_vmstat() -> dict[str, int]:
    """Read /proc/vmstat."""

    data: dict[str, int] = {}

    if not VMSTAT.exists():
        return data

    with VMSTAT.open() as f:
        for line in f:
            key, value = line.split()

            try:
                data[key] = int(value)
            except ValueError:
                continue

    return data


def collect_vmstat(memory: MemoryData) -> None:
    """Populate MemoryData using /proc/vmstat."""

    stats = _read_vmstat()

    # ==========================================================
    # Paging
    # ==========================================================
    memory.major_page_faults = stats.get("pgmajfault", 0)
    memory.minor_page_faults = stats.get("pgfault", 0) - memory.major_page_faults
    memory.total_page_faults = stats.get("pgfault", 0)

    # ==========================================================
    # Swap
    # ==========================================================
    memory.pages_swapped_in = stats.get("pswpin", 0)
    memory.pages_swapped_out = stats.get("pswpout", 0)

    # ==========================================================
    # Reclaim
    # ==========================================================
    pgscan = (
        stats.get("pgscan_kswapd", 0)
        + stats.get("pgscan_direct", 0)
        + stats.get("pgscan_khugepaged", 0)
    )

    pgsteal = (
        stats.get("pgsteal_kswapd", 0)
        + stats.get("pgsteal_direct", 0)
        + stats.get("pgsteal_khugepaged", 0)
    )

    memory.pages_scanned = pgscan
    memory.pages_reclaimed = pgsteal
    memory.reclaim_activity = pgscan

    # ==========================================================
    # Allocation / OOM
    # ==========================================================
    memory.allocation_failures = (
        stats.get("allocstall", 0)
        + stats.get("allocstall_dma", 0)
        + stats.get("allocstall_dma32", 0)
        + stats.get("allocstall_normal", 0)
        + stats.get("allocstall_movable", 0)
    )

    memory.oom_events = stats.get("oom_kill", 0)
