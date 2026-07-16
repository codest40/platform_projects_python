from dataclasses import dataclass, field
from typing import Optional

class ObserverState:
    NIL = None
    NA = "N/A"        # Not applicable(General conclusin)
    NS = "N/S"        # Metric/source was confidently not observed/seen
    DF = "DEFAULT"    # Value does not matter here(No significanxce at this layer)
    values = frozenset({NIL, NA, NS, DF})

@dataclass
class ThreadSnapshot:

    tid: int
    name: str | None = None
    state: str | None = None
    processor: int | None = None
    priority: int | None = None
    nice: int | None = None
    rt_priority: int | None = None
    policy: int | None = None
    wchan: str | None = None
    uid: int | None = None
    user_ticks: int | None = None
    system_ticks: int | None = None
    voluntary_context_switches: int | None = None
    involuntary_context_switches: int | None = None
    start_time: float | None = None

@dataclass(slots=True)
class RuntimeEvent:
    pid: int
    timestamp: float
    category: str
    code: str
    value: int | None = None
    metadata: dict | None = None

@dataclass(slots=True)
class ProcessRuntimeEvents:
    is_event_available: bool | None=None
    did_loading_succeed: bool | None=None
    did_read_succeed: bool | None=None

    emfile: list[str] | None = None
    enfile: list[str] | None = None
    emfile_count: int | None = None
    enfile_count: int | None = None
    oom_kill_count: int | None = None
    oom_allocation_failures: int | None = None
    #fatal signals
    sigbus_count: int | None = None
    sigabrt_count: int | None = None
    sigill_count: int | None = None
    sigfpe_count: int | None = None
    sigpipe_count: int | None = None
    segfault_count: int | None = None
    # Filesystem / storage
    io_error_count: int | None = None
    filesystem_error_count: int | None = None
    nfs_error_count: int | None = None
    # Networking
    connect_failure_count: int | None = None
    accept_failure_count: int | None = None

    last_terminating_signal: int | None = None
    collection_errors: list[str] = field(default_factory=list)


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
    wchan: str | None = None

    # ==========================================================
    # Ownership
    # ==========================================================

    uid: Optional[int] = None
    gid: Optional[int] = None

    # ==========================================================
    # Memory
    # ==========================================================

    rss_bytes: Optional[int] = None
    vms_bytes: Optional[int] = None

    # ==========================================================
    # Threads
    # ==========================================================

    threads: list[ThreadSnapshot] | None=None
    thread_count: Optional[int] = None
    session: int | None = None
    process_group: int | None = None
    foreground_process_group: int | None = None
    tty_nr: int | None = None
    minor_page_faults: int | None = None
    major_page_faults: int | None = None
    rss_limit: int | None = None
    # ==========================================================
    # CPU Accounting
    # ==========================================================

    user_ticks: Optional[int] = None
    system_ticks: Optional[int] = None

    # ==========================================================
    # Lifetime
    # ==========================================================
    start_time_since_boot: Optional[int] = None
    start_time: Optional[float] = None
    runtime_seconds: Optional[float] = None
    runtime_collected_events: ProcessRuntimeEvents | None = None

    # ==========================================================
    # Container / Cgroups
    # ==========================================================

    cgroup: Optional[str] = None
    container_id: Optional[str] = None
    # ==========================================================
    # File Descriptors
    # ==========================================================

    open_fds: Optional[int] = None
    fd_utilization: Optional[float | str] = None

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
    cpu_ticks_per_sec: float | None = None

    # Mem
    resident_ratio: Optional[float] = None

    # ps
    read_bytes_per_sec: Optional[float] = None
    write_bytes_per_sec: Optional[float] = None

    read_syscalls_per_sec: Optional[float] = None
    write_syscalls_per_sec: Optional[float] = None

    voluntary_context_switches_per_sec: Optional[float] = None
    involuntary_context_switches_per_sec: Optional[float] = None
    total_context_switches_per_sec: Optional[float] = None
    voluntary_context_switch_ratio: Optional[float] = None
    involuntary_context_switch_ratio: Optional[float] = None

    # io
    io_bytes_per_sec: Optional[float] = None
    io_syscalls_per_sec: Optional[float] = None
    read_write_ratio: Optional[float] = None
    average_read_size: Optional[float] = None
    average_write_size: Optional[float] = None
    lifetime_average_read_size: Optional[float] = None
    lifetime_average_write_size: Optional[float] = None

    # ==========================================================
    # ID Metadata
    # ==========================================================
    username: str | None=None
    groupname: str | None=None
    user_shell: str | None=None
    user_home: str | None=None

    # ==========================================================
    # Resource Limits (/proc/<pid>/limits)
    # ==========================================================

    max_fds_soft: int | float | str | None = None
    max_fds_hard: int | float | str | None = None

    max_processes_soft: int | float | str | None = None
    max_processes_hard: int | float | str | None = None

    max_stack_size_soft: int | float | str | None = None
    max_stack_size_hard: int | float | str | None = None

    max_address_space_soft: int | float | str | None = None
    max_address_space_hard: int | float | str | None = None

    max_locked_memory_soft: int | float | str | None = None
    max_locked_memory_hard: int | float | str | None = None

    max_core_file_size_soft: int | float | str | None = None
    max_core_file_size_hard: int | float | str | None = None

    max_cpu_time_soft: int | float | str | None = None
    max_cpu_time_hard: int | float | str | None = None

    max_file_size_soft: int | float | str | None = None
    max_file_size_hard: int | float | str | None = None

    # ==========================================================
    # Threads Metadata
    # ==========================================================
    idle_threads: int | None = None
    running_threads: int | None = None
    sleeping_threads: int | None = None
    uninterruptible_threads: int | None = None
    zombie_threads: int | None = None

    # ==========================================================
    # Collection Metadata
    # ==========================================================
    collection_errors: list[str] = field(default_factory=list)
    processor: Optional[int] = None
    metrics_available: Optional[int] = None
    metrics_expected: Optional[int] = None

@dataclass(slots=True)
class TotalMetrics:
    total_analyzed: Optional[int] = None
    total_available: Optional[int] = None
    total_scores: list[float] = None

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
    tid: int | None = None
    name: str | None = None
    process_type: str | None = None
    command: Optional[str] = None
    executable_state: str | None = None
    cgroup: Optional[str] = None
    container_id: Optional[str] = None
    uid: Optional[int] = None
    gid: Optional[int] = None
    owner_type: str | None = None
    classifications: list[str] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)
    scheduler_class: str | None = None
    recommendations: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    coverage: str = "UNKNOWN"

@dataclass(slots=True)
class ProcessWaitChannelAnalysis:
    pid: int
    tid: int
    wait_channel: str | None = None
    wait_type: str | None = None
    facts: list[str] = field(default_factory=list)
    classifications: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    coverage: str = "UNKNOWN"

@dataclass(slots=True)
class ProcessSchedulerAnalysis:

    pid: int
    tid: int | None = None

    state: str | None = None
    priority: int | None = None
    nice: int | None = None
    rt_priority: int | None = None

    policy: int | None = None
    scheduler_class: str | None = None

    processor: int | None = None

    start_time: float | None = None
    runtime_seconds: float | None = None

    classifications: list[str] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    coverage: str = "UNKNOWN"

@dataclass(slots=True)
class ProcessContextSwitchAnalysis:

    pid: int
    tid: int | None = None

    voluntary_context_switches_per_sec: float | None = None
    involuntary_context_switches_per_sec: float | None = None
    total_context_switches_per_sec: float | None = None

    voluntary_ratio: float | None = None
    facts: list[str] = field(default_factory=list)
    classifications: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    coverage: str = "UNKNOWN"

@dataclass(slots=True)
class ProcessCpuAnalysis:

    pid: int
    tid: int | None = None

    cpu_percent: float | None = None
    user_cpu_percent: float | None = None
    system_cpu_percent: float | None = None
    cpu_ticks_per_sec: float | None = None
    user_ticks_per_sec: float | None = None
    system_ticks_per_sec: float | None = None

    cpu_type: str | None = None
    runtime_seconds: float | None = None
    last_processor: int | None = None

    priority: int | None = None
    nice: int | None = None

    classifications: list[str] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    coverage: str = "UNKNOWN"

@dataclass(slots=True)
class ProcessThreadAnalysis:

    pid: int
    tid: int | None = None
    thread_count: int | None = None
    session: int | None = None
    process_group: int | None = None
    foreground_process_group: int | None = None
    state: str | None = None
    priority: int | None = None
    nice: int | None = None
    rt_priority: int | None = None
    runtime_seconds: float | None = None
    processor: int | None = None

    running_threads: int | None = None
    sleeping_threads: int | None = None
    blocked_threads: int | None = None
    zombie_threads: int | None = None
    idle_threads: int | None = None
    classifications: list[str] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    coverage: str = "UNKNOWN"

@dataclass(slots=True)
class ProcessFdAnalysis:

    pid: int
    tid: int | None = None

    open_fds: int | None = None
    max_fds_soft: int | float | str | None = None
    max_fds_hard: int | float | str | None = None
    fd_utilization: float | None = None

    facts: list[str] = field(default_factory=list)
    classifications: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    coverage: str = "UNKNOWN"


@dataclass(slots=True)
class ProcessLimitsAnalysis:

    pid: int
    tid: int | None = None

    max_cpu_time_soft: int | str | None = None
    max_cpu_time_hard: int | str | None = None

    max_file_size_soft: int | str | None = None
    max_file_size_hard: int | str | None = None

    max_stack_size_soft: int | str | None = None
    max_stack_size_hard: int | str | None = None

    max_core_file_size_soft: int | str | None = None
    max_core_file_size_hard: int | str | None = None

    max_locked_memory_soft: int | str | None = None
    max_locked_memory_hard: int | str | None = None

    max_processes_soft: int | str | None = None
    max_processes_hard: int | str | None = None

    max_fds_soft: int | str | None = None
    max_fds_hard: int | str | None = None

    max_address_space_soft: int | str | None = None
    max_address_space_hard: int | str | None = None

    classifications: list[str] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    coverage: str = "UNKNOWN"

@dataclass(slots=True)
class ProcessIoAnalysis:

    pid: int
    tid: int | None = None

    read_bytes_per_sec: float | None = None
    write_bytes_per_sec: float | None = None
    io_bytes_per_sec: float | None = None
    read_write_ratio: float | None = None
    read_syscalls_per_sec: float | None = None
    write_syscalls_per_sec: float | None = None
    io_syscalls_per_sec: float | None = None
    cancelled_write_bytes: int | None = None
    average_read_size: float | None = None
    average_write_size: float | None = None
    lifetime_average_read_size: float | None = None
    lifetime_average_write_size: float | None = None
    classifications: list[str] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    coverage: str = "UNKNOWN"

@dataclass(slots=True)
class ProcessMemoryAnalysis:

    pid: int
    tid: int | None = None

    rss_bytes: int | None = None
    vms_bytes: int | None = None

    thread_count: int | None = None

    resident_ratio: float | None = None

    classifications: list[str] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)
    signals: dict[str, bool] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    coverage: str = "UNKNOWN"

@dataclass(slots=True)
class ProcessSummary:

    pid: int
    tid: int | None = None

    healthy: bool | None = None
    cpu_bound: bool | None = None
    io_bound: bool | None = None
    blocked: bool | None = None
    multithreaded: bool | None = None
    interactive: bool | None = None
    daemon: bool | None = None
    container: bool | None = None
    resource_constrained: bool | None = None
    approaching_limits: bool | None = None

    severity: str | None = None
    confidence: str | None = None

    facts: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    classifications: list[str] = field(default_factory=list)
    coverage: str = "UNKNOWN"
    analyses: list = field(default_factory=list)


@dataclass(slots=True)
class ProcessSummaryInventory:

    processes: list[ProcessSummary] = field(
        default_factory=list
    )
    analyzed_total: int = 0
    analyzed_successful: int = 0
    analyzed_failed: int = 0
    analysis_errors: list[str] = field(
        default_factory=list
    )
    analyzed_at: str | None=None
    confidence: str | None=None
