from __future__ import annotations
from pathlib import Path
from project.models.disk import DiskData


CGROUP_IO = Path("/sys/fs/cgroup/io.stat")


def _parse_value(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def collect_cgroup(disk: DiskData) -> None:

    if not CGROUP_IO.exists():
        return

    read_bytes = 0
    write_bytes = 0

    read_ios = 0
    write_ios = 0

    with CGROUP_IO.open() as f:

        for line in f:

            for item in line.split()[1:]:

                key, value = item.split("=")

                if key == "rbytes":
                    read_bytes += _parse_value(value)

                elif key == "wbytes":
                    write_bytes += _parse_value(value)

                elif key == "rios":
                    read_ios += _parse_value(value)

                elif key == "wios":
                    write_ios += _parse_value(value)

    # ==========================================================
    # Container IO
    # ==========================================================

    disk.container_read_bytes = read_bytes
    disk.container_write_bytes = write_bytes

    disk.container_read_ios = read_ios
    disk.container_write_ios = write_ios
