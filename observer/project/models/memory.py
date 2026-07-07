from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

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

@dataclass
class Signal:
    name: str
    value: float
    domain: str          # memory, container, process, kernel
    type: str            # rate | total | ratio
    unit: str | None = None

@dataclass(slots=True)
class HealthCheck:

    check: str
    reason: str
    status: Literal["PASS", "WARNING", "CRITICAL"] = "PASS"
    category: str | None=None


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
    # Paging (Raw Counters)
    # ==========================================================

    major_page_faults: int | None = None
    minor_page_faults: int | None = None
    total_page_faults: int | None = None

    pages_scanned: int | None = None
    pages_reclaimed: int | None = None

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
    # Interval Metrics
    # ==========================================================

    page_faults_per_sec: float | None = None
    major_page_faults_per_sec: float | None = None
    minor_page_faults_per_sec: float | None = None

    pages_scanned_per_sec: float | None = None
    pages_reclaimed_per_sec: float | None = None

    allocation_failures_per_sec: float | None = None
    swap_in_mb_per_sec: float | None=None
    swap_out_mb_per_sec: float | None = None
    pages_swapped_in_mb_per_sec: float | None = None
    pages_swapped_out_mb_per_sec: float | None = None

    available_memory_change_mb_per_sec: float | None = None
    used_memory_change_mb_per_sec: float | None = None

    dirty_growth_mb_per_sec: float | None = None
    writeback_growth_mb_per_sec: float | None = None

    cache_growth_mb_per_sec: float | None = None
    buffer_growth_mb_per_sec: float | None = None

    process_memory_growth_mb_per_sec: float | None = None
    container_memory_growth_mb_per_sec: float | None = None

    oom_events_per_sec: float | None = None
    container_oom_events_per_sec: float | None = None

    # ==========================================================
    # Metadata
    # ==========================================================

    comment: str | None = None
    collected_total: int | None=None
    collected_successful: int | None=None
    signals_expected: int = 0
    signals_created: int = 0
    seen: bool = False

# ==========================================================
# Memory Analysis
# ==========================================================
@dataclass(slots=True)
class AnalyzerResult:
    name: str
    state: Literal["COMPLETE", "PARTIAL", "UNAVAILABLE"]
    checks: list[HealthCheck] = field(default_factory=list)


@dataclass(slots=True)
class MemoryAnalysis:

    component: str

    summary: str

    analyzed_at: str

    severity: Literal["INFO", "WARNING", "CRITICAL"]

    pressure: str | None = None

    confidence: tuple | None = None

    duration_ms: float | None = None

    recommendations: list[str] = field(default_factory=list)

    health_checks: list[HealthCheck] = field(default_factory=list)

