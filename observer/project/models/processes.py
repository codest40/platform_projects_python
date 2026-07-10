from dataclasses import dataclass, field
from typing import Optional


@dataclass(slots=True)
class ProcessSnapshot:

    pid: int
    ppid: Optional[int] = None

    name: Optional[str] = None
    command: Optional[str] = None
    executable: Optional[str] = None

    # ==========================================================
    # Scheduler
    # ==========================================================

    state: Optional[str] = None

    priority: Optional[int] = None
    nice: Optional[int] = None

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
    # Collection Metadata
    # ==========================================================

    collection_errors: list[str] = field(default_factory=list)
    processor: Optional[int] = None

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
