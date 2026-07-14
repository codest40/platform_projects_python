from __future__ import annotations
from project.models.processes import ProcessInventory
from project.utils.runners import EventRunner
#from project.logging.logger import emit
import os
import math

# ==========================================================
# Filter State
# ==========================================================

def filter_process_state(result: EventRunner) -> dict:
    """
    Snapshot only cumulative process counters needed for
    interval computation.
    """
    inventory: ProcessInventory = result.data
    return {
        "collected_at": result.collected_at,

        "processes": {
            process.pid: {
                # ------------------------------------------
                # CPU Accounting (/proc/<pid>/stat)
                # ------------------------------------------

                "user_ticks": process.user_ticks,
                "system_ticks": process.system_ticks,

                # ------------------------------------------
                # I/O Counters (/proc/<pid>/io)
                # ------------------------------------------

                "read_bytes": process.read_bytes,
                "write_bytes": process.write_bytes,
                "cancelled_write_bytes": process.cancelled_write_bytes,

                "read_syscalls": process.read_syscalls,
                "write_syscalls": process.write_syscalls,

                # ------------------------------------------
                # Context Switch Counters
                # ------------------------------------------

                "voluntary_context_switches": process.voluntary_context_switches,
                "involuntary_context_switches": process.involuntary_context_switches,
            }
            for process in inventory.processes
        },
    }


# ==========================================================
# Helpers
# ==========================================================
CLK_TCK = os.sysconf("SC_CLK_TCK")
UNLIMITED = float("inf")

def parse_limit(value):
    """
    Normalize a Linux resource limit.
    Returns:
        None          -> unavailable
        float("inf")  -> unlimited
        int           -> finite limit
    """
    UNLIMITED = float("inf")

    if value is None:
        return None
    if value == "unlimited":
        return UNLIMITED
    if isinstance(value, (int, float)):
        return value
    return int(value)

def _delta(current, previous):
    """
    Safe counter delta.
    """
    if current is None or previous is None:
        return None
    delta = current - previous
    if delta < 0:
        return None

    return delta


def _rate(current, previous, elapsed):
    """
    Convert cumulative counter into per-second rate.
    """
    delta = _delta(current, previous)
    if delta is None:
        return None
    if elapsed <= 0:
        return None
    return delta / elapsed


def _ratio(numerator, denominator):
    """
    Safe ratio helper.
    """
    if numerator is None:
        return None
    if denominator in (None, 0):
        return None
    if math.isinf(denominator) or math.isinf(numerator):
        return "N/A"
    return numerator / denominator

def _percent(rate, total):
    value = _ratio(rate, total)
    if value is None:
        return None
    return value * 100

# ==========================================================
# Compute Derived Metrics
# ==========================================================

def compute_process_rates(
    inventory: ProcessInventory,
    previous: dict | None,
    current: dict,
) -> ProcessInventory:
    """
    Compute all derived process metrics.
    """

    if previous is None:
        return inventory


    previous_time = previous.get("collected_at")
    if previous_time is None:
        return inventory

    elapsed = current["collected_at"] - previous_time

    if elapsed <= 0:
        return inventory

    previous_processes = { int(pid): data for pid, data in previous["processes"].items() }

    for process in inventory.processes:

        previous_process = previous_processes.get(process.pid)

        if previous_process is None:
            #emit(f"{process.pid}: no previous snapshot found")
            continue

        # ======================================================
        # CPU Accounting
        # ======================================================
        process.user_ticks_per_sec = _rate(
            process.user_ticks,
            previous_process["user_ticks"],
            elapsed,
        )

        process.system_ticks_per_sec = _rate(
            process.system_ticks,
            previous_process["system_ticks"],
            elapsed,
        )

        process.user_cpu_percent = _percent(
            process.user_ticks_per_sec,
            CLK_TCK,
        )

        process.system_cpu_percent = _percent(
            process.system_ticks_per_sec,
            CLK_TCK,
        )

        u = process.user_ticks_per_sec
        s = process.system_ticks_per_sec
        if u is not None and s is not None:
            process.cpu_ticks_per_sec = u + s

        u = process.user_cpu_percent
        s = process.system_cpu_percent
        if u is not None and s is not None:
            process.cpu_percent = u + s

        # ======================================================
        # Memory
        # ======================================================

        process.resident_ratio = _ratio(
            process.rss_bytes,
            process.vms_bytes,
        )

        # ======================================================
        # I/O
        # ======================================================

        process.read_bytes_per_sec = _rate(
            process.read_bytes,
            previous_process["read_bytes"],
            elapsed,
        )

        process.write_bytes_per_sec = _rate(
            process.write_bytes,
            previous_process["write_bytes"],
            elapsed,
        )

        process.read_syscalls_per_sec = _rate(
            process.read_syscalls,
            previous_process["read_syscalls"],
            elapsed,
        )

        process.write_syscalls_per_sec = _rate(
            process.write_syscalls,
            previous_process["write_syscalls"],
            elapsed,
        )

        r = process.read_bytes_per_sec
        w = process.write_bytes_per_sec

        if r is not None and w is not None:
            process.io_bytes_per_sec = r + w

        r = process.read_syscalls_per_sec
        w = process.write_syscalls_per_sec

        if r is not None and w is not None:
            process.io_syscalls_per_sec = r + w

        process.read_write_ratio = _ratio(
            process.read_bytes_per_sec,
            process.write_bytes_per_sec,
        )

        process.average_read_size = _ratio(
            process.read_bytes_per_sec,
            process.read_syscalls_per_sec,
        )

        process.average_write_size = _ratio(
            process.write_bytes_per_sec,
            process.write_syscalls_per_sec,
        )

        process.lifetime_average_read_size = _ratio(
            process.read_bytes,
            process.read_syscalls,
        )

        process.lifetime_average_write_size = _ratio(
            process.write_bytes,
            process.write_syscalls,
        )

        # ======================================================
        # Context Switching
        # ======================================================

        process.voluntary_context_switches_per_sec = _rate(
            process.voluntary_context_switches,
            previous_process["voluntary_context_switches"],
            elapsed,
        )

        process.involuntary_context_switches_per_sec = _rate(
            process.involuntary_context_switches,
            previous_process["involuntary_context_switches"],
            elapsed,
        )

        v = process.voluntary_context_switches_per_sec
        i = process.involuntary_context_switches_per_sec

        if v is not None and i is not None:
            process.total_context_switches_per_sec = v + i

        process.voluntary_context_switch_ratio = _ratio(
            process.voluntary_context_switches_per_sec,
            process.total_context_switches_per_sec,
        )

        process.involuntary_context_switch_ratio = _ratio(
            process.involuntary_context_switches_per_sec,
            process.total_context_switches_per_sec,
        )

        # ======================================================
        # File Descriptors
        # ======================================================

        process.fd_utilization = _ratio(
            process.open_fds,
            parse_limit(process.max_fds_soft),
        )

    #print(f"Current processes : {len(inventory.processes)}")
    #print(f"Previous processes: {len(previous_processes)}")
    #current_pids = {p.pid for p in inventory.processes}
    #previous_pids = set(previous_processes.keys())

    #print("Common:", len(current_pids & previous_pids))
    #print("New:", len(current_pids - previous_pids))
    #print("Gone:", len(previous_pids - current_pids))
    return inventory

