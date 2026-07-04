from __future__ import annotations
from pathlib import Path
from project.models.disk import DiskData


DISKSTATS = Path("/proc/diskstats")


def collect_diskstats(disk: DiskData) -> None:
    if not DISKSTATS.exists():
        return

    with DISKSTATS.open() as f:

        for line in f:

            fields = line.split()

            if len(fields) < 14:
                continue

            major, minor, device, \
            reads, reads_merged, sectors_read, read_ms, \
            writes, writes_merged, sectors_written, write_ms, \
            in_flight, io_ticks, queue_ms, *extra = fields

            if (
                device.startswith(("loop", "ram", "dm-", "zram"))
                or device[-1].isdigit()
            ):
                continue

            disk.device = device

            # Device IO
            disk.read_count = int(reads)
            disk.write_count = int(writes)
            disk.read_bytes = int(sectors_read) * 512
            disk.write_bytes = int(sectors_written) * 512

            disk.read_time_ms = int(read_ms)
            disk.write_time_ms = int(write_ms)

            # Device State
            disk.io_in_progress = int(in_flight)
            disk.busy_time_ms = int(io_ticks)
            disk.weighted_io_time_ms = int(queue_ms)

            # Discard statistics (kernel dependent)
            if len(extra) >= 4:
                disk.discard_count = int(extra[0])
                discard_sectors = int(extra[2])
                disk.discard_bytes = discard_sectors * 512
                disk.discard_time_ms = int(extra[3])

            # Flush statistics (kernel dependent)
            if len(extra) >= 6:
                disk.flush_count = int(extra[4])
                disk.flush_time_ms = int(extra[5])

            break
