"""
Memory collector using Linux cgroups.
Supports both cgroup v2 and cgroup v1.
"""

from __future__ import annotations
from pathlib import Path
from project.models.memory import MemoryData


CGROUP_V2 = Path("/sys/fs/cgroup")
CGROUP_V1 = Path("/sys/fs/cgroup/memory")


def _read_int(path: Path) -> int:
    try:
        value = path.read_text().strip()

        if value == "max":
            return 0

        return int(value)

    except Exception:
        return 0


def _collect_v2(memory: MemoryData) -> bool:

    current = CGROUP_V2 / "memory.current"

    if not current.exists():
        return False

    memory.container_memory_usage = _read_int(current)
    memory.cgroup_memory_usage = memory.container_memory_usage

    memory.container_memory_limit = _read_int(
        CGROUP_V2 / "memory.max"
    )

    stat = CGROUP_V2 / "memory.stat"

    if stat.exists():

        with stat.open() as f:

            stats = {}

            for line in f:
                key, value = line.split()
                stats[key] = int(value)

        memory.container_rss = stats.get("anon", 0)
        memory.container_page_cache = stats.get("file", 0)
        memory.container_cache = stats.get("file", 0)

        memory.container_working_set = (
            memory.container_memory_usage
            - stats.get("inactive_file", 0)
        )

    events = CGROUP_V2 / "memory.events"

    if events.exists():

        with events.open() as f:

            stats = {}

            for line in f:
                key, value = line.split()
                stats[key] = int(value)

        memory.container_oom_events = stats.get("oom_kill", 0)

    return True


def _collect_v1(memory: MemoryData) -> bool:

    usage = CGROUP_V1 / "memory.usage_in_bytes"

    if not usage.exists():
        return False

    memory.container_memory_usage = _read_int(usage)
    memory.cgroup_memory_usage = memory.container_memory_usage

    memory.container_memory_limit = _read_int(
        CGROUP_V1 / "memory.limit_in_bytes"
    )

    stat = CGROUP_V1 / "memory.stat"

    if stat.exists():

        stats = {}

        with stat.open() as f:

            for line in f:
                key, value = line.split()
                stats[key] = int(value)

        memory.container_rss = stats.get("rss", 0)
        memory.container_cache = stats.get("cache", 0)
        memory.container_page_cache = stats.get("cache", 0)

        memory.container_working_set = (
            memory.container_memory_usage
            - stats.get("inactive_file", 0)
        )

    return True


def collect_cgroup(memory: MemoryData) -> None:

    if _collect_v2(memory):
        return

    _collect_v1(memory)
