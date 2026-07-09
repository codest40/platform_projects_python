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
class ProcessInventory:
    processes: list[ProcessSnapshot] = field(default_factory=list)

    total_processes: int = 0
    accessible_processes: int = 0
    inaccessible_processes: int = 0

    collected_total: int = 0
    collected_successful: int = 0

