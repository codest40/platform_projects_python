from __future__ import annotations
from project.models.disk import DiskData
from project.utils.runners import EventRunner
from project.utils.helpers import get_status

def filter_disk_state(result: EventRunner) -> dict:

    disk = result.data

    return {
        "collected_at": result.collected_at,

        "read_bytes": disk.read_bytes,
        "write_bytes": disk.write_bytes,

        "read_count": disk.read_count,
        "write_count": disk.write_count,

        "read_time_ms": disk.read_time_ms,
        "write_time_ms": disk.write_time_ms,

        "busy_time_ms": disk.busy_time_ms,
        "weighted_io_time_ms": disk.weighted_io_time_ms,

        "flush_count": disk.flush_count,
        "discard_bytes": disk.discard_bytes,

        "process_read_bytes": disk.process_read_bytes,
        "process_write_bytes": disk.process_write_bytes,

        "container_read_bytes": disk.container_read_bytes,
        "container_write_bytes": disk.container_write_bytes,
    }



#=======================================
MB = 1024 * 1024


def _delta(current: dict, previous: dict, key: str) -> float:
    return float(current.get(key, 0) or 0) - float(previous.get(key, 0) or 0)

def compute_disk_rates(
    disk: DiskData,
    previous: dict,
    current: dict,
) -> DiskData:

    elapsed = current["collected_at"] - previous["collected_at"]

    if elapsed <= 0:
        return disk

    # ==========================================================
    # Throughput
    # ==========================================================

    read_bytes = _delta(current, previous, "read_bytes")
    write_bytes = _delta(current, previous, "write_bytes")
    discard_bytes = _delta(current, previous, "discard_bytes")

    disk.read_mb_per_sec = (read_bytes / MB) / elapsed
    disk.write_mb_per_sec = (write_bytes / MB) / elapsed
    disk.total_mb_per_sec = (
        disk.read_mb_per_sec + disk.write_mb_per_sec
    )

    disk.discard_mb_per_sec = (discard_bytes / MB) / elapsed

    # ==========================================================
    # IOPS
    # ==========================================================

    read_ios = _delta(current, previous, "read_count")
    write_ios = _delta(current, previous, "write_count")

    disk.read_iops = read_ios / elapsed
    disk.write_iops = write_ios / elapsed
    disk.total_iops = (
        disk.read_iops + disk.write_iops
    )

    # ==========================================================
    # Average Latency
    # ==========================================================

    read_time = _delta(current, previous, "read_time_ms")
    write_time = _delta(current, previous, "write_time_ms")

    if read_ios > 0:
        disk.average_read_latency_ms = read_time / read_ios

    if write_ios > 0:
        disk.average_write_latency_ms = write_time / write_ios

    # ==========================================================
    # Device Utilization
    # ==========================================================

    busy = _delta(current, previous, "busy_time_ms")

    disk.device_utilization_percent = (
        busy / (elapsed * 1000)
    ) * 100

    # ==========================================================
    # Average Queue Depth
    # ==========================================================

    weighted = _delta(
        current,
        previous,
        "weighted_io_time_ms",
    )

    disk.average_queue_depth = (
        weighted / (elapsed * 1000)
    )

    # ==========================================================
    # Flush Rate
    # ==========================================================

    flushes = _delta(
        current,
        previous,
        "flush_count",
    )

    disk.flushes_per_sec = flushes / elapsed

    # ==========================================================
    # Process Throughput
    # ==========================================================

    proc_read = _delta(
        current,
        previous,
        "process_read_bytes",
    )

    proc_write = _delta(
        current,
        previous,
        "process_write_bytes",
    )

    disk.process_read_mb_per_sec = (
        proc_read / MB
    ) / elapsed

    disk.process_write_mb_per_sec = (
        proc_write / MB
    ) / elapsed

    # ==========================================================
    # Container Throughput
    # ==========================================================

    container_read = _delta(
        current,
        previous,
        "container_read_bytes",
    )

    container_write = _delta(
        current,
        previous,
        "container_write_bytes",
    )

    disk.container_read_mb_per_sec = (
        container_read / MB
    ) / elapsed

    disk.container_write_mb_per_sec = (
        container_write / MB
    ) / elapsed

    disk.status = get_status("SUCCESS")
    return disk
