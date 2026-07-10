from __future__ import annotations
from project.models.processes import ProcessInventory
from project.utils.runners import EventRunner


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

    return numerator / denominator


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

    previous_processes = previous["processes"]

    for process in inventory.processes:

        previous_process = previous_processes.get(process.pid)

        if previous_process is None:
            continue

        #
        # CPU Accounting
        #

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

        #
        # I/O
        #

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

        #
        # Context Switching
        #

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

        #
        # FD Utilization
        #

        process.fd_utilization = _ratio(
            process.open_fds,
            process.max_fds,
        )

    v = process.voluntary_context_switches_per_sec
    i = process.involuntary_context_switches_per_sec

    if v is not None and i is not None:
        process.total_context_switches_per_sec = v + i

    return inventory
