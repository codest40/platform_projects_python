from __future__ import annotations
from dataclasses import dataclass, field
from project.models.events import HealthCheck


# ==========================================================
# Collector Selection
# ==========================================================

@dataclass(slots=True)
class GetDiskType:
    psutil: bool = False
    diskstats: bool = False
    pressure: bool = False
    mounts: bool = False
    filesystems: bool = False
    process: bool = False
    cgroup: bool = False

@dataclass
class Signal:
    name: str
    value: float
    domain: str
    type: str            # rate | total | ratio
    unit: str | None = None

# ==========================================================
# Disk Data
# ==========================================================

@dataclass(slots=True)
class DiskData:

    # ======================================================
    # Primary Filesystem
    # ======================================================

    device: str | None = None
    primary_partition: str | None = None
    mount_point: str | None = None

    total: int = 0
    used: int = 0
    free: int = 0

    percent: float | None = None
    read_only: bool | None = None
    mounted_fs_total: int | None = None

    # ======================================================
    # Mounted Filesystems
    # ======================================================

    mount_count: int | None = None
    mounts: list[dict] | None = None
    filesystems: list[dict] | None = None

    # ======================================================
    # Device IO Statistics (Raw Counters)
    # ======================================================

    read_count: int | None = None
    write_count: int | None = None

    read_bytes: int | None = None
    write_bytes: int | None = None

    read_time_ms: int | None = None
    write_time_ms: int | None = None

    io_in_progress: int | None = None
    busy_time_ms: int | None = None
    weighted_io_time_ms: int | None = None

    discard_count: int | None = None
    discard_bytes: int | None = None
    discard_time_ms: int | None = None

    flush_count: int | None = None
    flush_time_ms: int | None = None

    # ======================================================
    # Queue / Latency
    # ======================================================

    queue_depth: float | None = None

    average_wait_ms: float | None = None
    average_service_time_ms: float | None = None
    utilization_percent: float | None = None

    # ======================================================
    # Filesystem Cache / Writeback
    # ======================================================

    dirty_pages: int | None = None
    writeback_pages: int | None = None

    # ======================================================
    # Linux PSI (Pressure Stall Information)
    # ======================================================

    psi_some_avg10: float | None = None
    psi_some_avg60: float | None = None
    psi_some_avg300: float | None = None

    psi_full_avg10: float | None = None
    psi_full_avg60: float | None = None
    psi_full_avg300: float | None = None

    # ======================================================
    # Process Disk IO
    # ======================================================

    process_read_count: int | None = None
    process_write_count: int | None = None

    process_read_bytes: int | None = None
    process_write_bytes: int | None = None

    read_chars: int | None = None
    write_chars: int | None = None

    read_syscalls: int | None = None
    write_syscalls: int | None = None

    # ======================================================
    # Container / cgroup IO
    # ======================================================

    container_read_bytes: int | None = None
    container_write_bytes: int |None = None

    container_read_ios: int | None = None
    container_write_ios: int | None = None

    container_io_pressure: float | None = None

    # ======================================================
    # Interval Metrics (/proc/diskstats)
    # ======================================================

    read_mb_per_sec: float | None = None
    write_mb_per_sec: float | None = None
    total_mb_per_sec: float | None = None

    read_iops: float | None = None
    write_iops: float | None = None
    total_iops: float | None = None

    average_read_latency_ms: float | None = None
    average_write_latency_ms: float | None = None

    device_utilization_percent: float | None = None
    average_queue_depth: float | None = None

    flushes_per_sec: float | None = None
    discard_mb_per_sec: float | None = None

    process_read_mb_per_sec: float | None = None
    process_write_mb_per_sec: float | None = None

    container_read_mb_per_sec: float | None = None
    container_write_mb_per_sec: float | None = None

    collected_at: float | None = None
    collected_total: int = 0
    collected_successful: int = 0
    signals_expected: int = 0
    signals_created: int = 0
    seen: bool = False

# ==========================================================
# Analysis
# ==========================================================

@dataclass(slots=True)
class DiskAnalysis:

    component: str

    summary: str

    severity: str

    analyzed_at: str

    confidence: tuple | None = None

    signals: list | None=None

    duration_ms: float | None = None

    recommendations: list[str] = field(default_factory=list)

    health_checks: list[HealthCheck] = field(default_factory=list)
