from __future__ import annotations
from dataclasses import fields
from statistics import mean
from project.models.cpu import CpuData
from project.utils.runners import EventRunner


# ==========================================================
# Filter State
# ==========================================================

def filter_cpu_state(result: EventRunner) -> dict:
    """
    Snapshot only cumulative counters needed for interval computation.
    """

    cpu = result.data

    return {
        "collected_at": result.collected_at,

        # --------------------------------------------------
        # Scheduler Counters
        # --------------------------------------------------

        "context_switches": cpu.context_switches,
        "interrupts": cpu.interrupts,
        "soft_interrupts": cpu.soft_interrupts,
        "syscalls": cpu.syscalls,

        # --------------------------------------------------
        # CPU Throttling Counters
        # --------------------------------------------------

        "cpu_throttled_periods": cpu.cpu_throttled_periods,
        "cpu_throttled_usec": cpu.cpu_throttled_usec,
    }


# ==========================================================
# Helpers
# ==========================================================

def _delta(current: dict, previous: dict, key: str) -> float:
    """
    Counter delta between two snapshots.
    """

    return (
        float(current.get(key, 0) or 0)
        - float(previous.get(key, 0) or 0)
    )


def _rate(
    current: dict,
    previous: dict,
    key: str,
    elapsed: float,
) -> float | None:
    """
    Convert cumulative counter into per-second rate.
    """

    delta = _delta(current, previous, key)

    if delta < 0:
        return None

    return delta / elapsed


def _ratio(
    numerator: float | int | None,
    denominator: float | int | None,
) -> float | None:
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

def compute_cpu_rates(
    cpu: CpuData,
    previous: dict | None,
    current: dict,
) -> CpuData:
    """
    Compute derived CPU metrics.
    Pure computation only.
    No thresholds.
    No health decisions.
    """

    if previous is None:
        return cpu

    previous_time = previous.get("collected_at", None)
    if previous_time is None:
        return cpu

    elapsed = current["collected_at"] - previous_time

    if elapsed <= 0:
        return cpu

    # =====================================================
    # Scheduler Rates
    # =====================================================

    cpu.context_switches_per_sec = _rate(
        current,
        previous,
        "context_switches",
        elapsed,
    )

    cpu.interrupts_per_sec = _rate(
        current,
        previous,
        "interrupts",
        elapsed,
    )

    cpu.soft_interrupts_per_sec = _rate(
        current,
        previous,
        "soft_interrupts",
        elapsed,
    )

    cpu.syscalls_per_sec = _rate(
        current,
        previous,
        "syscalls",
        elapsed,
    )

    # =====================================================
    # CPU Throttling Rates
    # =====================================================

    cpu.cpu_throttled_periods_per_sec = _rate(
        current,
        previous,
        "cpu_throttled_periods",
        elapsed,
    )

    cpu.cpu_throttled_usec_per_sec = _rate(
        current,
        previous,
        "cpu_throttled_usec",
        elapsed,
    )

    # =====================================================
    # Load Normalization
    # =====================================================

    if cpu.logical_cores > 0:

        cpu.load_per_core_1 = (
            cpu.load_average[0] / cpu.logical_cores
        )

        cpu.load_per_core_5 = (
            cpu.load_average[1] / cpu.logical_cores
        )

        cpu.load_per_core_15 = (
            cpu.load_average[2] / cpu.logical_cores
        )

    # =====================================================
    # Core Balance
    # =====================================================

    if cpu.per_core_util:

        cpu.highest_core_percent = max(cpu.per_core_util)
        cpu.lowest_core_percent = min(cpu.per_core_util)
        cpu.average_core_percent = mean(cpu.per_core_util)

        cpu.core_spread_percent = (
            cpu.highest_core_percent
            - cpu.lowest_core_percent
        )

        cpu.core_imbalance_percent = (
            cpu.highest_core_percent
            - cpu.average_core_percent
        )

    # =====================================================
    # Frequency
    # =====================================================

    cpu.frequency_ratio = _ratio(
        cpu.frequency_mhz,
        cpu.max_frequency_mhz,
    )

    # =====================================================
    # Kernel Activity
    # =====================================================

    cpu.kernel_ratio = _ratio(
        cpu.system_percent,
        cpu.user_percent + cpu.system_percent,
    )

    # =====================================================
    # Optional Derived Throttle Metric
    # This is NOT Linux's cgroup throttle_ratio.
    # It simply indicates how often throttling occurs
    # relative to scheduler context switching.
    # =====================================================

    cpu.cpu_throttle_ratio = _ratio(
        cpu.cpu_throttled_periods,
        cpu.cpu_throttle_periods,
    )

    cpu.cpu_throttle_event_ratio = _ratio(
        cpu.cpu_throttled_periods_per_sec,
        cpu.context_switches_per_sec,
    )

    cpu.collected_total = len(fields(CpuData))
    cpu.collected_successful = cpu.collected_total
    cpu.seen = True

    return cpu
