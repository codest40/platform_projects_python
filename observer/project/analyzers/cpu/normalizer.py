"""
CPU Normalization Layer.
Converts Cpu_Data → structured Signals.

This is the place where:
- unit normalization happens
- ratios are derived
- raw metrics are standardized
"""

from __future__ import annotations
from project.models.cpu import Cpu_Data, Signal


def normalize(cpu: Cpu_Data) -> list[Signal]:

    signals: list[Signal] = []

    # ==========================================================
    # CPU Capacity
    # ==========================================================

    cpu.signals_expected += 1
    if cpu.physical_cores is not None:
        signals.append(Signal(
            name="cpu.physical_cores",
            value=cpu.physical_cores,
            domain="cpu",
            type="capacity",
            unit="cores",
        ))
        cpu.signals_created += 1

    cpu.signals_expected += 1
    if cpu.logical_cores is not None:
        signals.append(Signal(
            name="cpu.logical_cores",
            value=cpu.logical_cores,
            domain="cpu",
            type="capacity",
            unit="cores",
        ))
        cpu.signals_created += 1

    # ==========================================================
    # Utilization
    # ==========================================================

    cpu.signals_expected += 1
    if cpu.usage_percent is not None:
        signals.append(Signal(
            name="cpu.utilization_ratio",
            value=cpu.usage_percent / 100,
            domain="cpu",
            type="ratio",
            unit="ratio",
        ))
        cpu.signals_created += 1

    cpu.signals_expected += 1
    if cpu.idle_percent is not None:
        signals.append(Signal(
            name="cpu.idle_ratio",
            value=cpu.idle_percent / 100,
            domain="cpu",
            type="ratio",
            unit="ratio",
        ))
        cpu.signals_created += 1

    # ==========================================================
    # CPU Time Breakdown
    # ==========================================================

    breakdown = [
        ("cpu.user_ratio", cpu.user_percent),
        ("cpu.system_ratio", cpu.system_percent),
        ("cpu.iowait_ratio", cpu.iowait_percent),
        ("cpu.steal_ratio", cpu.steal_percent),
        ("cpu.irq_ratio", cpu.irq_percent),
        ("cpu.softirq_ratio", cpu.softirq_percent),
        ("cpu.nice_ratio", cpu.nice_percent),
    ]

    for name, value in breakdown:

        cpu.signals_expected += 1

        if value is not None:
            signals.append(Signal(
                name=name,
                value=value / 100,
                domain="cpu",
                type="ratio",
                unit="ratio",
            ))
            cpu.signals_created += 1

    # ==========================================================
    # Scheduler Activity
    # ==========================================================

    scheduler = [
        ("scheduler.context_switches", cpu.context_switches_per_sec),
        ("scheduler.interrupts", cpu.interrupts_per_sec),
        ("scheduler.soft_interrupts", cpu.soft_interrupts_per_sec),
        ("scheduler.syscalls", cpu.syscalls_per_sec),
    ]

    for name, value in scheduler:

        cpu.signals_expected += 1

        if value is not None:
            signals.append(Signal(
                name=name,
                value=value,
                domain="kernel",
                type="rate",
                unit="events/sec",
            ))
            cpu.signals_created += 1

    # ==========================================================
    # Frequency
    # ==========================================================

    cpu.signals_expected += 1
    if cpu.frequency_mhz is not None:
        signals.append(Signal(
            name="cpu.frequency",
            value=cpu.frequency_mhz,
            domain="cpu",
            type="gauge",
            unit="MHz",
        ))
        cpu.signals_created += 1

    cpu.signals_expected += 1
    if cpu.frequency_ratio is not None:
        signals.append(Signal(
            name="cpu.frequency_ratio",
            value=cpu.frequency_ratio,
            domain="cpu",
            type="ratio",
            unit="ratio",
        ))
        cpu.signals_created += 1

    # ==========================================================
    # Load
    # ==========================================================

    load = [
        ("cpu.load.1", cpu.load_per_core_1),
        ("cpu.load.5", cpu.load_per_core_5),
        ("cpu.load.15", cpu.load_per_core_15),
    ]

    for name, value in load:

        cpu.signals_expected += 1

        if value is not None:
            signals.append(Signal(
                name=name,
                value=value,
                domain="cpu",
                type="ratio",
                unit="load/core",
            ))
            cpu.signals_created += 1

    # ==========================================================
    # Core Balance
    # ==========================================================

    balance = [
        ("cpu.highest_core", cpu.highest_core_percent),
        ("cpu.average_core", cpu.average_core_percent),
        ("cpu.core_imbalance", cpu.core_imbalance_percent),
    ]

    for name, value in balance:

        cpu.signals_expected += 1

        if value is not None:
            signals.append(Signal(
                name=name,
                value=value,
                domain="cpu",
                type="gauge",
                unit="percent",
            ))
            cpu.signals_created += 1

    # ==========================================================
    # Kernel Ratio
    # ==========================================================

    cpu.signals_expected += 1
    if cpu.kernel_ratio is not None:
        signals.append(Signal(
            name="cpu.kernel_ratio",
            value=cpu.kernel_ratio,
            domain="kernel",
            type="ratio",
            unit="ratio",
        ))
        cpu.signals_created += 1

    # ==========================================================
    # Pressure Stall Information
    # ==========================================================

    psi = [
        ("psi.some.10", cpu.psi_some_avg10),
        ("psi.some.60", cpu.psi_some_avg60),
        ("psi.some.300", cpu.psi_some_avg300),
        ("psi.full.10", cpu.psi_full_avg10),
        ("psi.full.60", cpu.psi_full_avg60),
        ("psi.full.300", cpu.psi_full_avg300),
    ]

    for name, value in psi:

        cpu.signals_expected += 1

        if value is not None:
            signals.append(Signal(
                name=name,
                value=value,
                domain="kernel",
                type="ratio",
                unit="ratio",
            ))
            cpu.signals_created += 1

    # ==========================================================
    # CPU Throttling
    # ==========================================================

    cpu.signals_expected += 1
    if cpu.throttled_periods_per_sec is not None:
        signals.append(Signal(
            name="cpu.throttled_periods",
            value=cpu.throttled_periods_per_sec,
            domain="container",
            type="rate",
            unit="events/sec",
        ))
        cpu.signals_created += 1

    cpu.signals_expected += 1
    if cpu.throttled_usec_per_sec is not None:
        signals.append(Signal(
            name="cpu.throttled_time",
            value=cpu.throttled_usec_per_sec,
            domain="container",
            type="rate",
            unit="usec/sec",
        ))
        cpu.signals_created += 1

    cpu.signals_expected += 1
    if cpu.throttle_ratio is not None:
        signals.append(Signal(
            name="cpu.throttle_ratio",
            value=cpu.throttle_ratio,
            domain="container",
            type="ratio",
            unit="ratio",
        ))
        cpu.signals_created += 1

    # ==========================================================
    # Top CPU Process
    # ==========================================================

    cpu.signals_expected += 1
    if cpu.top_process_cpu_percent is not None:
        signals.append(Signal(
            name="process.cpu_utilization",
            value=cpu.top_process_cpu_percent / 100,
            domain="process",
            type="ratio",
            unit="ratio",
        ))
        cpu.signals_created += 1

    return signals
