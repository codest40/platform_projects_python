"""
CPU collector using psutil.

No Linux file parsing.
No cgroup parsing.
No PSI parsing.
"""

from __future__ import annotations
import psutil
from project.models.cpu import CpuData


def collect_psutil(cpu: CpuData) -> CpuData:
    """
    Populate CPU metrics available from psutil.
    """
    # ======================================================
    # CPU Utilization
    # ======================================================
    for p in psutil.process_iter():
        try:
            p.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    cpu.usage_percent = psutil.cpu_percent(interval=1.5)
    cpu.per_core_util = psutil.cpu_percent(
        interval=None,
        percpu=True,
    )

    # ======================================================
    # CPU Time Breakdown
    # ======================================================

    cpu_times = psutil.cpu_times_percent(interval=0.5)

    cpu.user_percent = cpu_times.user
    cpu.system_percent = cpu_times.system
    cpu.idle_percent = cpu_times.idle

    cpu.iowait_percent = getattr(
        cpu_times,
        "iowait",
        None,
    )

    cpu.steal_percent = getattr(
        cpu_times,
        "steal",
        None,
    )

    cpu.irq_percent = getattr(
        cpu_times,
        "irq",
        None,
    )

    cpu.softirq_percent = getattr(
        cpu_times,
        "softirq",
        None,
    )

    cpu.nice_percent = getattr(
        cpu_times,
        "nice",
        None,
    )

    # ======================================================
    # Scheduler Statistics
    # ======================================================

    stats = psutil.cpu_stats()

    cpu.context_switches = stats.ctx_switches
    cpu.interrupts = stats.interrupts
    cpu.soft_interrupts = stats.soft_interrupts
    cpu.syscalls = getattr(
        stats,
        "syscalls",
        None,
    )

    # ======================================================
    # Frequency
    # ======================================================

    freq = psutil.cpu_freq()

    if freq is not None:
        cpu.frequency_mhz = freq.current if freq else None
        cpu.min_frequency_mhz = freq.min if freq else None
        cpu.max_frequency_mhz = freq.max if freq else None

    # ======================================================
    # CPU Capacity
    # ======================================================

    cpu.physical_cores = psutil.cpu_count(
        logical=False,
    )

    cpu.logical_cores = psutil.cpu_count(
        logical=True,
    )

    # ======================================================
    # Load Average
    # ======================================================

    try:
        cpu.load_average = psutil.getloadavg()
    except (AttributeError, OSError):
        cpu.load_average = None

    return cpu
