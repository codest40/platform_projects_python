"""
Memory Normalization Layer.

Converts MemoryData → structured Signals ie add more meaning to each metrics
This is the ONLY place where:
- unit normalization happens
- ratios are derived
- raw metrics are standardized
"""

from __future__ import annotations
from dataclasses import dataclass
from project.models.memory import MemoryData, Signal


MB = 1024 * 1024

def normalize(memory: MemoryData) -> list[Signal]:
    signals: list[Signal] = []

    # ==========================================================
    # Host Memory (core snapshot signals)
    # ==========================================================
    memory.signals_expected +=1
    if memory.total is not None:
        signals.append(Signal(
            name="memory.total",
            value=memory.total / MB,
            domain="memory",
            type="total",
            unit="MB"
        ))
        memory.signals_created +=1

    memory.signals_expected +=1
    if memory.used is not None:
        signals.append(Signal(
            name="memory.used",
            value=memory.used / MB,
            domain="memory",
            type="total",
            unit="MB"
        ))
        memory.signals_created +=1

    memory.signals_expected +=1
    if memory.available is not None:
        signals.append(Signal(
            name="memory.available",
            value=memory.available / MB,
            domain="memory",
            type="total",
            unit="MB"
        ))
        memory.signals_created +=1


    # ==========================================================
    # Utilization ratios (normalized, not raw)
    # ==========================================================
    memory.signals_expected +=1
    if memory.used is not None and memory.total is not None:
        signals.append(Signal(
            name="memory.utilization_ratio",
            value=memory.used / memory.total,
            domain="memory",
            type="ratio",
            unit="ratio"
        ))
        memory.signals_created +=1

    memory.signals_expected +=1
    if memory.available is not None and memory.total is not None:
        signals.append(Signal(
            name="memory.available_ratio",
            value=memory.available / memory.total,
            domain="memory",
            type="ratio",
            unit="ratio"
        ))
        memory.signals_created +=1

    # ==========================================================
    # Swap normalization
    # ==========================================================
    memory.signals_expected +=1
    if memory.swap_total is not None:
        signals.append(Signal(
            name="swap.total",
            value=memory.swap_total / MB,
            domain="memory",
            type="total",
            unit="MB"
        ))
        memory.signals_created +=1

    memory.signals_expected +=1
    if memory.swap_used is not None:
        signals.append(Signal(
            name="swap.used",
            value=memory.swap_used / MB,
            domain="memory",
            type="total",
            unit="MB"
        ))
        memory.signals_created +=1

    memory.signals_expected +=1
    if memory.swap_percent is not None:
        signals.append(Signal(
            name="swap.utilization_ratio",
            value=memory.swap_percent / 100,
            domain="memory",
            type="ratio",
            unit="ratio"
        ))
        memory.signals_created +=1

    # ==========================================================
    # Commit normalization
    # ==========================================================

    memory.signals_expected +=1
    if memory.commit_percent is not None:
        signals.append(Signal(
            name="commit.utilization_ratio",
            value=memory.commit_percent / 100,
            domain="memory",
            type="ratio",
            unit="ratio"
        ))
        memory.signals_created +=1

    # ==========================================================
    # PSI (RAW ONLY — NO INTERPRETATION)
    # ==========================================================
    psi_fields = [
        ("psi.some.10", memory.psi_some_avg10),
        ("psi.some.60", memory.psi_some_avg60),
        ("psi.some.300", memory.psi_some_avg300),
        ("psi.full.10", memory.psi_full_avg10),
        ("psi.full.60", memory.psi_full_avg60),
        ("psi.full.300", memory.psi_full_avg300),
    ]

    for name, value in psi_fields:
        memory.signals_expected +=1
        if value is not None:
            signals.append(Signal(
                name=name,
                value=value,
                domain="kernel",
                type="ratio",
                unit="ratio"
            ))
            memory.signals_created +=1

    # ==========================================================
    # Paging signals
    # ==========================================================
    memory.signals_expected +=1
    if memory.page_faults_per_sec is not None:
        signals.append(Signal(
            name="paging.page_faults",
            value=memory.page_faults_per_sec,
            domain="kernel",
            type="rate",
            unit="events/sec"
        ))
        memory.signals_created +=1


    memory.signals_expected +=1
    if memory.major_page_faults_per_sec is not None:
        signals.append(Signal(
            name="paging.major_faults",
            value=memory.major_page_faults_per_sec,
            domain="kernel",
            type="rate",
            unit="events/sec"
        ))
        memory.signals_created +=1

    memory.signals_expected +=1
    if memory.minor_page_faults_per_sec is not None:
        signals.append(Signal(
            name="paging.minor_faults",
            value=memory.minor_page_faults_per_sec,
            domain="kernel",
            type="rate",
            unit="events/sec"
        ))
        memory.signals_created +=1

    # ==========================================================
    # Swap activity (already rates)
    # ==========================================================

    memory.signals_expected +=1
    if memory.swap_in_mb_per_sec is not None:
        signals.append(Signal(
            name="swap.in_rate",
            value=memory.swap_in_mb_per_sec,
            domain="memory",
            type="rate",
            unit="MB/s"
        ))
        memory.signals_created +=1

    memory.signals_expected +=1
    if memory.swap_out_mb_per_sec is not None:
        signals.append(Signal(
            name="swap.out_rate",
            value=memory.swap_out_mb_per_sec,
            domain="memory",
            type="rate",
            unit="MB/s"
        ))
        memory.signals_created +=1

    # ==========================================================
    # Process memory growth (already rate)
    # ==========================================================
    memory.signals_expected +=1
    if memory.process_memory_growth_mb_per_sec is not None:
        signals.append(Signal(
            name="process.memory_growth",
            value=memory.process_memory_growth_mb_per_sec,
            domain="process",
            type="rate",
            unit="MB/s"
        ))
        memory.signals_created +=1

    memory.signals_expected +=1
    if memory.container_memory_growth_mb_per_sec is not None:
        signals.append(Signal(
            name="container.memory_growth",
            value=memory.container_memory_growth_mb_per_sec,
            domain="container",
            type="rate",
            unit="MB/s"
        ))
        memory.signals_created +=1

    # ==========================================================
    # OOM signals
    # ==========================================================
    memory.signals_expected +=1
    if memory.oom_events_per_sec is not None:
        signals.append(Signal(
            name="oom.kernel_rate",
            value=memory.oom_events_per_sec,
            domain="kernel",
            type="rate",
            unit="events/sec"
        ))
        memory.signals_created +=1

    memory.signals_expected +=1
    if memory.container_oom_events_per_sec is not None:
        signals.append(Signal(
            name="oom.container_rate",
            value=memory.container_oom_events_per_sec,
            domain="container",
            type="rate",
            unit="events/sec"
        ))
        memory.signals_created +=1

    return signals
