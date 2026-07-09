"""
CPU collector using Linux cgroups.
Supports both cgroup v2 and cgroup v1.
Responsible ONLY for CPU cgroup metrics.
"""

from __future__ import annotations

from pathlib import Path

from project.models.cpu import CpuData


# ==========================================================
# Possible cgroup files
# ==========================================================

CGROUP_V2_CPU_STAT = Path("/sys/fs/cgroup/cpu.stat")

CGROUP_V1_CPU_STAT = Path("/sys/fs/cgroup/cpu/cpu.stat")


# ==========================================================
# Helpers
# ==========================================================

def _read_cpu_stat(path: Path) -> dict[str, int] | None:
    """
    Read cpu.stat into a dictionary.

    Example:
        usage_usec 12345
        nr_periods 100
        nr_throttled 5
        throttled_usec 1234
    """

    if not path.exists():
        return None

    values: dict[str, int] = {}

    try:

        with path.open() as f:

            for line in f:

                parts = line.split()

                if len(parts) != 2:
                    continue

                key, value = parts

                try:
                    values[key] = int(value)
                except ValueError:
                    continue

    except Exception:
        return None

    return values


# ==========================================================
# Collector
# ==========================================================

def collect_cgroup(cpu: CpuData) -> CpuData:
    """
    Populate CPU cgroup statistics.
    Supports both cgroup v2 and cgroup v1.
    """

    stat = None

    # ======================================================
    # cgroup v2
    # ======================================================

    if CGROUP_V2_CPU_STAT.exists():
        stat = _read_cpu_stat(CGROUP_V2_CPU_STAT)

    # ======================================================
    # cgroup v1
    # ======================================================

    elif CGROUP_V1_CPU_STAT.exists():
        stat = _read_cpu_stat(CGROUP_V1_CPU_STAT)

    if stat is None:
        return cpu

    # ======================================================
    # CPU Throttling
    # ======================================================
    cpu.cpu_throttle_periods = stat.get("nr_periods")
    cpu.cpu_throttled_periods = stat.get("nr_throttled")
    cpu.cpu_throttled_usec = stat.get("throttled_usec")

    return cpu
