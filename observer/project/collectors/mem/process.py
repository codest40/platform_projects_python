"""
Process memory collector.
Collects memory statistics for the current process.
"""

from __future__ import annotations
import psutil
from project.models.memory import MemoryData


def collect_process_memory(
    memory: MemoryData,
    pid: int | None = None,
) -> None:
    """
    Populate MemoryData with process memory statistics.
    If pid is None, collect statistics for the current process.
    """

    try:
        process = psutil.Process(pid)
    except Exception:
        return

    # ==========================================================
    # Basic Memory
    # ==========================================================
    info = process.memory_info()

    memory.rss = info.rss
    memory.vms = info.vms

    memory.shared_memory = getattr(info, "shared", 0)

    # ==========================================================
    # Extended Memory
    # ==========================================================
    try:
        full = process.memory_full_info()

        memory.uss = getattr(full, "uss", 0)
        memory.pss = getattr(full, "pss", 0)

    except Exception:
        pass

    # ==========================================================
    # Process Utilization
    # ==========================================================
    try:
        memory.process_memory_percent = process.memory_percent()
    except Exception:
        pass
