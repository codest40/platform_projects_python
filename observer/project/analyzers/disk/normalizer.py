"""
Disk Normalization Layer.

Converts DiskData → structured Signals.

This is the ONLY place where:
- unit normalization happens
- ratios are derived
- raw metrics are standardized
"""

from __future__ import annotations
from project.models.disk import DiskData, Signal

MB = 1024 * 1024


def normalize(disk: DiskData) -> list[Signal]:
    signals: list[Signal] = []

    # ==========================================================
    # Filesystem Capacity
    # ==========================================================

    disk.signals_expected += 1
    if disk.total is not None:
        signals.append(Signal(
            name="disk.total",
            value=disk.total / MB,
            domain="disk",
            type="total",
            unit="MB",
        ))
        disk.signals_created += 1

    disk.signals_expected += 1
    if disk.used is not None:
        signals.append(Signal(
            name="disk.used",
            value=disk.used / MB,
            domain="disk",
            type="total",
            unit="MB",
        ))
        disk.signals_created += 1

    disk.signals_expected += 1
    if disk.free is not None:
        signals.append(Signal(
            name="disk.free",
            value=disk.free / MB,
            domain="disk",
            type="total",
            unit="MB",
        ))
        disk.signals_created += 1

    disk.signals_expected += 1
    if disk.percent is not None:
        signals.append(Signal(
            name="disk.utilization_ratio",
            value=disk.percent / 100,
            domain="disk",
            type="ratio",
            unit="ratio",
        ))
        disk.signals_created += 1

    # ==========================================================
    # Pressure Stall Information
    # ==========================================================

    psi = [
        ("psi.some.10", disk.psi_some_avg10),
        ("psi.some.60", disk.psi_some_avg60),
        ("psi.some.300", disk.psi_some_avg300),
        ("psi.full.10", disk.psi_full_avg10),
        ("psi.full.60", disk.psi_full_avg60),
        ("psi.full.300", disk.psi_full_avg300),
    ]

    for name, value in psi:
        disk.signals_expected += 1

        if value is not None:
            signals.append(Signal(
                name=name,
                value=value,
                domain="kernel",
                type="ratio",
                unit="ratio",
            ))
            disk.signals_created += 1

    # ==========================================================
    # Device Utilization
    # ==========================================================

    disk.signals_expected += 1
    if disk.device_utilization_percent is not None:
        signals.append(Signal(
            name="disk.device_utilization",
            value=disk.device_utilization_percent / 100,
            domain="device",
            type="ratio",
            unit="ratio",
        ))
        disk.signals_created += 1

    # ==========================================================
    # Queue Depth
    # ==========================================================

    disk.signals_expected += 1
    if disk.average_queue_depth is not None:
        signals.append(Signal(
            name="disk.queue_depth",
            value=disk.average_queue_depth,
            domain="device",
            type="gauge",
            unit="requests",
        ))
        disk.signals_created += 1

    # ==========================================================
    # Latency
    # ==========================================================

    disk.signals_expected += 1
    if disk.average_read_latency_ms is not None:
        signals.append(Signal(
            name="disk.read_latency",
            value=disk.average_read_latency_ms,
            domain="device",
            type="latency",
            unit="ms",
        ))
        disk.signals_created += 1

    disk.signals_expected += 1
    if disk.average_write_latency_ms is not None:
        signals.append(Signal(
            name="disk.write_latency",
            value=disk.average_write_latency_ms,
            domain="device",
            type="latency",
            unit="ms",
        ))
        disk.signals_created += 1

    # ==========================================================
    # Disk Throughput (already computed)
    # ==========================================================

    disk.signals_expected += 1
    if disk.read_mb_per_sec is not None:
        signals.append(Signal(
            name="disk.read_rate",
            value=disk.read_mb_per_sec,
            domain="disk",
            type="rate",
            unit="MB/s",
        ))
        disk.signals_created += 1

    disk.signals_expected += 1
    if disk.write_mb_per_sec is not None:
        signals.append(Signal(
            name="disk.write_rate",
            value=disk.write_mb_per_sec,
            domain="disk",
            type="rate",
            unit="MB/s",
        ))
        disk.signals_created += 1

    # ==========================================================
    # IO Operations
    # ==========================================================

    disk.signals_expected += 1
    if disk.read_iops is not None:
        signals.append(Signal(
            name="disk.read_iops",
            value=disk.read_iops,
            domain="disk",
            type="rate",
            unit="ops/sec",
        ))
        disk.signals_created += 1

    disk.signals_expected += 1
    if disk.write_iops is not None:
        signals.append(Signal(
            name="disk.write_iops",
            value=disk.write_iops,
            domain="disk",
            type="rate",
            unit="ops/sec",
        ))
        disk.signals_created += 1

    # ==========================================================
    # Flush Activity
    # ==========================================================

    disk.signals_expected += 1
    if disk.flushes_per_sec is not None:
        signals.append(Signal(
            name="disk.flush_rate",
            value=disk.flushes_per_sec,
            domain="disk",
            type="rate",
            unit="flushes/sec",
        ))
        disk.signals_created += 1

    # ==========================================================
    # Process Disk IO
    # ==========================================================

    disk.signals_expected += 1
    if disk.process_read_mb_per_sec is not None:
        signals.append(Signal(
            name="process.read_rate",
            value=disk.process_read_mb_per_sec,
            domain="process",
            type="rate",
            unit="MB/s",
        ))
        disk.signals_created += 1

    disk.signals_expected += 1
    if disk.process_write_mb_per_sec is not None:
        signals.append(Signal(
            name="process.write_rate",
            value=disk.process_write_mb_per_sec,
            domain="process",
            type="rate",
            unit="MB/s",
        ))
        disk.signals_created += 1

    # ==========================================================
    # Container Disk IO
    # ==========================================================

    disk.signals_expected += 1
    if disk.container_read_mb_per_sec is not None:
        signals.append(Signal(
            name="container.read_rate",
            value=disk.container_read_mb_per_sec,
            domain="container",
            type="rate",
            unit="MB/s",
        ))
        disk.signals_created += 1

    disk.signals_expected += 1
    if disk.container_write_mb_per_sec is not None:
        signals.append(Signal(
            name="container.write_rate",
            value=disk.container_write_mb_per_sec,
            domain="container",
            type="rate",
            unit="MB/s",
        ))
        disk.signals_created += 1

    return signals
