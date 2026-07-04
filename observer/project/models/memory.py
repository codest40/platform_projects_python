from __future__ import annotations
from dataclasses import dataclass, field


# ==========================================================
# Collector Selection
# ==========================================================

@dataclass(slots=True)
class GetMemType:
    psutil: bool = False
    pressure: bool = False
    meminfo: bool = False
    vmstat: bool = False
    cgroup: bool = False
    numa: bool = False
    process: bool = False


# ==========================================================
# Memory Snapshot
# ==========================================================

@dataclass(slots=True)
class MemoryData:

    # ==========================================================
    # Host Memory
    # ==========================================================
    total: int = 0
    available: int = 0
    used: int = 0
    free: int = 0

    cached: int | None = None
    buffers: int | None = None
    shared: int | None = None

    active: int | None = None
    inactive: int | None = None

    slab: int | None = None
    slab_reclaimable: int | None = None
    slab_unreclaimable: int | None = None

    page_tables: int | None = None
    kernel_stack: int | None = None

    wired: int | None = None          # BSD/macOS
    vmalloc_used: int | None = None

    # ==========================================================
    # Utilization
    # ==========================================================
    percent: float | None = None

    available_percent: float | None = None
    used_percent: float | None = None

    cache_percent: float | None = None
    buffer_percent: float | None = None

    # ==========================================================
    # Swap
    # ==========================================================
    swap_total: int | None = None
    swap_used: int | None = None
    swap_free: int | None = None
    swap_percent: float | None = None

    swap_in: int | None = None
    swap_out: int | None = None

    pages_swapped_in: int | None = None
    pages_swapped_out: int | None = None

    # ==========================================================
    # Commit Accounting
    # ==========================================================
    committed_as: int | None = None
    commit_limit: int | None = None
    commit_percent: float | None = None

    # ==========================================================
    # Paging
    # ==========================================================
    major_page_faults: int | None = None
    major_page_fault_rate: int | None = None
    minor_page_faults: int | None = None
    total_page_faults: int | None = None

    page_scan_rate: float | None = None
    page_reclaim_rate: float | None = None

    reclaim_activity: int | None = None
    allocation_failures: int | None = None

    # ==========================================================
    # Memory Pressure (Linux PSI)
    # ==========================================================
    psi_some_avg10: float | None = None
    psi_some_avg60: float | None = None
    psi_some_avg300: float | None = None

    psi_full_avg10: float | None = None
    psi_full_avg60: float | None = None
    psi_full_avg300: float | None = None

    low_memory_events: int | None = None
    oom_events: int | None = None

    # ==========================================================
    # Huge Pages
    # ==========================================================
    huge_pages_total: int | None = None
    huge_pages_free: int | None = None
    huge_pages_reserved: int | None = None
    huge_pages_used: int | None = None
    huge_page_size: int | None = None

    # ==========================================================
    # NUMA
    # ==========================================================
    numa_nodes: int | None = None
    numa_remote_accesses: int | None = None
    numa_imbalance: float | None = None

    # ==========================================================
    # Process Memory
    # ==========================================================
    rss: int | None = None
    vms: int | None = None
    uss: int | None = None
    pss: int | None = None

    shared_memory: int | None = None
    private_memory: int | None = None

    anonymous_memory: int | None = None
    file_backed_memory: int | None = None

    process_memory_percent: float | None = None
    peak_memory: int | None = None

    # ==========================================================
    # Container / cgroup
    # ==========================================================
    cgroup_memory_usage: int | None = None

    container_memory_usage: int | None = None
    container_memory_limit: int | None = None
    container_working_set: int | None = None

    container_cache: int | None = None
    container_page_cache: int | None = None
    container_rss: int | None = None

    container_oom_events: int | None = None

    # ==========================================================
    # Filesystem Cache
    # ==========================================================
    page_cache: int | None = None

    dirty_pages: int | None = None
    writeback_pages: int | None = None

    dirty_cache: int | None = None
    writeback_cache: int | None = None

    dentry_cache: int | None = None
    inode_cache: int | None = None

    # ==========================================================
    # Derived Metrics for Analyzer to use
    # ==========================================================
    page_fault_rate: float | None = None

    memory_growth_rate: float | None = None

    cache_hit_ratio: float | None = None
    cache_eviction_rate: float | None = None

    memory_spike_detected: bool | None = None
    memory_leak_detected: bool | None = None

    sustained_high_utilization: bool | None = None

    # ==========================================================
    # Analyzer Summary
    # ==========================================================
    pressure: str | None = None
    health: str | None = None
    comment: str | None = None


@dataclass(slots=True)
class MemoryAnalysis:
    health_checks: list[HealthCheck]
    recommendations: list[str] = field(default_factory=list)
    component: str | None=None
    analyzed_at: str | None=None
    summary: str | None=None
    severity: str | None=None
    pressure: str | None = None
    confidence: str | None=None
