from dataclasses import dataclass, field
from typing import Optional


@dataclass(slots=True)
class ProcessSnapshot:

    pid: int
    ppid: Optional[int] = None
    tid: int | None = None

    name: Optional[str] = None
    command: Optional[str] = None
    executable: Optional[str] = None

    # ==========================================================
    # Scheduler
    # ==========================================================

    state: Optional[str] = None

    priority: Optional[int] = None
    nice: Optional[int] = None
    rt_priority: Optional[int] = None
    policy: Optional[int] = None

    # ==========================================================
    # Ownership
    # ==========================================================

    uid: Optional[int] = None
    gid: Optional[int] = None

    # ==========================================================
    # Memory (cheap)
    # ==========================================================

    rss_bytes: Optional[int] = None
    vms_bytes: Optional[int] = None

    # ==========================================================
    # Threads
    # ==========================================================

    thread_count: Optional[int] = None

    # ==========================================================
    # CPU Accounting
    # ==========================================================

    user_ticks: Optional[int] = None
    system_ticks: Optional[int] = None

    # ==========================================================
    # Lifetime
    # ==========================================================

    start_time: Optional[float] = None
    runtime_seconds: Optional[float] = None

    # ==========================================================
    # Container / Cgroups
    # ==========================================================

    cgroup: Optional[str] = None
    container_id: Optional[str] = None

    # ==========================================================
    # File Descriptors
    # ==========================================================

    open_fds: Optional[int] = None
    max_fds: Optional[int] = None
    fd_utilization: Optional[float] = None

    # ==========================================================
    # Process I/O
    # ==========================================================

    read_syscalls: Optional[int] = None
    write_syscalls: Optional[int] = None

    read_chars: Optional[int] = None
    write_chars: Optional[int] = None

    read_bytes: Optional[int] = None
    write_bytes: Optional[int] = None
    cancelled_write_bytes: Optional[int] = None

    # ==========================================================
    # Context Switching
    # ==========================================================

    voluntary_context_switches: Optional[int] = None
    involuntary_context_switches: Optional[int] = None

    # ==========================================================
    # Derived
    # ==========================================================

    user_cpu_percent: Optional[float] = None
    system_cpu_percent: Optional[float] = None
    cpu_percent: Optional[float] = None
    user_ticks_per_sec: Optional[float] = None
    system_ticks_per_sec: Optional[float] = None

    read_bytes_per_sec: Optional[float] = None
    write_bytes_per_sec: Optional[float] = None

    read_syscalls_per_sec: Optional[float] = None
    write_syscalls_per_sec: Optional[float] = None

    voluntary_context_switches_per_sec: Optional[float] = None
    involuntary_context_switches_per_sec: Optional[float] = None
    total_context_switches_per_sec: Optional[float] = None
    # ==========================================================
    # ID Metadata
    # ==========================================================
    username: str | None
    groupname: str | None
    user_shell: str | None
    user_home: str | None
    # ==========================================================
    # Collection Metadata
    # ==========================================================

    collection_errors: list[str] = field(default_factory=list)
    processor: Optional[int] = None
    metrics_available: Optional[int] = None
    metrics_expected: Optional[int] = None

@dataclass(slots=True)
class InaccessibleProcess:

    pid: int
    reason: str

@dataclass(slots=True)
class CollectorFailure:
    pid: int
    collector: str
    field: str
    reason: str

@dataclass(slots=True)
class ProcessInventory:
    processes: list[ProcessSnapshot] = field(default_factory=list)

    total_processes: int = 0
    accessible_processes: int = 0
    inaccessible_processes: list[InaccessibleProcess] = field(
        default_factory=list
    )
    collector_failures: list[CollectorFailure] = field(default_factory=list)
    collected_total: int = 0
    collected_successful: int = 0


@dataclass(slots=True)
class ProcessCache:

    stat: Optional[str] = None
    status: Optional[str] = None
    cmdline: Optional[bytes] = None
    cgroup: Optional[str] = None
    limits: str | None = None
    io: str | None = None

@dataclass(slots=True)
class ProcessIdentityAnalysis:

    pid: int
    process_type: str | None = None
    executable_state: str | None = None
    owner_type: str | None = None
    classifications: list[str] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)
    scheduler_class: str | None = None
