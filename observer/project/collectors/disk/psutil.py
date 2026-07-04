from __future__ import annotations
import psutil
from project.models.disk import DiskData


def collect_psutil_disk(disk: DiskData) -> None:

    usage = psutil.disk_usage("/")
    io = psutil.disk_io_counters()

    # ==========================================================
    # Filesystem Capacity
    # ==========================================================

    disk.total = usage.total
    disk.used = usage.used
    disk.free = usage.free

    disk.percent = usage.percent

    # ==========================================================
    # Disk IO
    # ==========================================================

    if io is None:
        return

    disk.read_count = io.read_count
    disk.write_count = io.write_count

    disk.read_bytes = io.read_bytes
    disk.write_bytes = io.write_bytes

    disk.read_time_ms = getattr(io, "read_time", None)
    disk.write_time_ms = getattr(io, "write_time", None)

    disk.busy_time_ms = getattr(io, "busy_time", None)
