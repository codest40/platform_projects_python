"""
CPU collector using /proc.
"""

from __future__ import annotations
from pathlib import Path
from project.models.cpu import CpuData


CPUINFO = Path("/proc/cpuinfo")


def _read_cpuinfo() -> list[str] | None:
    if not CPUINFO.exists():
        return None

    try:
        return CPUINFO.read_text().splitlines()

    except Exception:
        return None


def collect_proc(cpu: CpuData) -> CpuData:
    """
    Populate CPU information available from /proc.
    """

    lines = _read_cpuinfo()

    if lines is None:
        return cpu

    # ======================================================
    # CPU Model
    # ======================================================

    for line in lines:

        if line.startswith("model name"):

            cpu.cpu_model = line.split(":", 1)[1].strip()
        if line.startswith("cache size"):
            cpu.cache_size = line.split(":", 1)[1].strip()

            break

    return cpu
