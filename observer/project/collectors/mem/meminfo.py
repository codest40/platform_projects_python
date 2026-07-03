from __future__ import annotations
from pathlib import Path
from project.models.memory import MemoryData


MEMINFO = Path("/proc/meminfo")


def _read_meminfo() -> dict[str, int]:
    """
    Read /proc/meminfo. Returns values in bytes.
    """

    data: dict[str, int] = {}

    if not MEMINFO.exists():
        return data

    with MEMINFO.open() as f:
        for line in f:
            key, value = line.split(":", 1)

            value = value.strip().split()[0]

            data[key] = int(value) * 1024

    return data


def collect_meminfo(memory: MemoryData) -> None:
    """Populate MemoryData from /proc/meminfo."""

    info = _read_meminfo()

    # ==========================================================
    # Kernel Memory
    # ==========================================================
    memory.page_tables = info.get("PageTables", 0)
    memory.kernel_stack = info.get("KernelStack", 0)

    memory.slab = info.get("Slab", memory.slab)
    memory.slab_reclaimable = info.get("SReclaimable", 0)
    memory.slab_unreclaimable = info.get("SUnreclaim", 0)

    memory.vmalloc_used = info.get("VmallocUsed", 0)

    # ==========================================================
    # Virtual Memory
    # ==========================================================
    memory.committed_as = info.get("Committed_AS", 0)
    memory.commit_limit = info.get("CommitLimit", 0)

    if memory.commit_limit:
        memory.commit_percent = (
            memory.committed_as / memory.commit_limit * 100
        )

    # ==========================================================
    # Huge Pages
    # ==========================================================
    memory.huge_pages_total = info.get("HugePages_Total", 0)
    memory.huge_pages_free = info.get("HugePages_Free", 0)
    memory.huge_pages_reserved = info.get("HugePages_Rsvd", 0)

    memory.huge_pages_used = (
        memory.huge_pages_total - memory.huge_pages_free
    )

    memory.huge_page_size = info.get("Hugepagesize", 0)

    # ==========================================================
    # Filesystem Cache
    # ==========================================================
    memory.page_cache = info.get("Cached", memory.cached)
    memory.dirty_pages = info.get("Dirty", 0)
    memory.writeback_pages = info.get("Writeback", 0)

    memory.dirty_cache = memory.dirty_pages
    memory.writeback_cache = memory.writeback_pages

    memory.inode_cache = info.get("InodeCache", 0)
    memory.dentry_cache = info.get("DentryCache", 0)
