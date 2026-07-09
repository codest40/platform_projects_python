"""
CPU scheduler collector.
Collects scheduler-related metrics from Linux procfs.
These metrics are optional and Linux-version dependent.
"""

from __future__ import annotations
from pathlib import Path
from project.models.cpu import CpuData
import psutil
import time


PROC_STAT = Path("/proc/stat")

def collect_sched(cpu: CpuData) -> CpuData:
    """
    Populate scheduler metrics from /proc/stat.
    Missing metrics are left unchanged.
    """

    if not PROC_STAT.exists():
        return cpu

    try:
        with PROC_STAT.open() as f:

            for line in f:

                parts = line.split()

                if not parts:
                    continue

                key = parts[0]

                # ------------------------------------------
                # Context Switches
                # ------------------------------------------

                if key == "ctxt" and len(parts) >= 2:
                    if cpu.context_switches is None:
                      cpu.context_switches = int(parts[1])

                # ------------------------------------------
                # Interrupts
                # ------------------------------------------

                elif key == "intr" and len(parts) >= 2:
                    if cpu.interrupts is None:
                        cpu.interrupts = int(parts[1])

                # ------------------------------------------
                # Soft IRQ
                # ------------------------------------------

                elif key == "softirq" and len(parts) >= 2:
                    if cpu.soft_interrupts is None:
                        cpu.soft_interrupts = int(parts[1])

    except (OSError, ValueError):
        pass


    top = None

    for p in psutil.process_iter(["pid", "name"]):
        try:
            usage = p.cpu_percent(None)

            if top is None or usage > top[0]:
                top = (
                    usage,
                    p.info["pid"],
                    p.info["name"],
                )

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if top is not None:
        cpu.top_process_cpu_percent = top[0]
        cpu.top_process_pid = top[1]
        cpu.top_process_name = top[2]


    return cpu
