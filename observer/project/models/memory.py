
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class MemoryData:

    # ==========================================================
    # Capacity
    # ==========================================================
    total: int = 0
    available: int = 0
    used: int = 0
    free: int = 0

    cached: int = 0
    buffers: int = 0
    shared: int = 0
    active: int = 0
    inactive: int = 0
    wired: int = 0
    slab: int = 0
    page_tables: int = 0
    kernel_stack: int = 0

    # ==========================================================
    # Utilization
    # ==========================================================
    percent: float = 0.0
    available_percent: float = 0.0
    used_percent: float = 0.0
    cache_percent: float = 0.0
    buffer_percent: float = 0.0

    # ==========================================================
    # Swap
    # ==========================================================
    swap_total: int = 0
    swap_used: int = 0
    swap_free: int = 0
    swap_percent: float = 0.0

    swap_in: int = 0
    swap_out: int = 0

    pages_swapped_in: int = 0
    pages_swapped_out: int = 0

    # ==========================================================
    # Virtual Memory
    # ==========================================================
    virtual_total: int = 0
    virtual_available: int = 0
    committed: int = 0
    commit_limit: int = 0
    commit_percent: float = 0.0

    # ==========================================================
    # Paging
    # ==========================================================
    major_page_faults: int = 0
    minor_page_faults: int = 0
    total_page_faults: int = 0

    page_fault_rate: float = 0.0
    page_scan_rate: float = 0.0
    page_reclaim_rate: float = 0.0

    # ==========================================================
    # Memory Pressure
    # ==========================================================
    pressure: str = ""
    low_memory_events: int = 0
    oom_events: int = 0
    allocation_failures: int = 0
    reclaim_activity: int = 0

    # ==========================================================
    # Huge Pages
    # ==========================================================
    huge_pages_total: int = 0
    huge_pages_free: int = 0
    huge_pages_reserved: int = 0
    huge_pages_used: int = 0
    huge_page_size: int = 0

    # ==========================================================
    # NUMA
    # ==========================================================
    numa_nodes: int = 0
    numa_remote_accesses: int = 0
    numa_imbalance: float = 0.0

    # ==========================================================
    # Process Memory
    # ==========================================================
    rss: int = 0
    vms: int = 0
    uss: int = 0
    pss: int = 0

    shared_memory: int = 0
    private_memory: int = 0

    process_memory_percent: float = 0.0
    peak_memory: int = 0

    anonymous_memory: int = 0
    file_backed_memory: int = 0

    # ==========================================================
    # Container Memory
    # ==========================================================
    container_memory_limit: int = 0
    container_memory_request: int = 0
    container_memory_usage: int = 0
    container_working_set: int = 0

    container_cache: int = 0
    container_rss: int = 0
    container_page_cache: int = 0

    container_oom_events: int = 0
    container_memory_throttling: int = 0
    cgroup_memory_usage: int = 0

    # ==========================================================
    # Kernel Memory
    # ==========================================================
    slab_reclaimable: int = 0
    slab_unreclaimable: int = 0
    vmalloc_used: int = 0

    dirty_pages: int = 0
    writeback_pages: int = 0

    # ==========================================================
    # Filesystem Cache
    # ==========================================================
    page_cache: int = 0
    dirty_cache: int = 0
    writeback_cache: int = 0

    dentry_cache: int = 0
    inode_cache: int = 0

    # ==========================================================
    # Performance
    # ==========================================================
    memory_growth_rate: float = 0.0
    memory_leak_detected: bool = False

    sustained_high_utilization: bool = False
    memory_spike_detected: bool = False

    cache_hit_ratio: float = 0.0
    cache_eviction_rate: float = 0.0

    # ==========================================================
    # Health
    # ==========================================================
    health: str = ""
