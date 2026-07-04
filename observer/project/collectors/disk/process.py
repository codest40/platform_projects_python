"""Per-process disk IO collector."""

from __future__ import annotations
import psutil
from project.models.disk import DiskData


def collect_process_disk(disk: DiskData) -> None:

    try:
        process = psutil.Process()

        io = process.io_counters()

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        AttributeError,
    ):
        return

    # ==========================================================
    # Current Process IO
    # ==========================================================

    disk.read_count = io.read_count
    disk.write_count = io.write_count

    disk.read_bytes = io.read_bytes
    disk.write_bytes = io.write_bytes

    # Linux only
    disk.read_chars = getattr(io, "read_chars", None)
    disk.write_chars = getattr(io, "write_chars", None)

    disk.read_syscalls = getattr(io, "read_count", None)
    disk.write_syscalls = getattr(io, "write_count", None)
