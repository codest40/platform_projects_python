from __future__ import annotations
import psutil
from project.models.disk import DiskData
from project.collectors.disk.data import REAL_FS

def collect_usage(disk: DiskData) -> None:
    """
    Populate DiskData with filesystem usage information.
    """

    filesystems = []
    alltotal = 0

    for part in psutil.disk_partitions(all=False):

        try:
            usage = psutil.disk_usage(part.mountpoint)

        except (PermissionError, FileNotFoundError):
            continue

        alltotal += usage.total
        if (part.fstype == "squashfs" or part.fstype not in REAL_FS):
          continue

        filesystems.append(
            {
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            }
        )

        if part.mountpoint == "/":
          disk.primary_partition = part.device
          disk.mount_point = part.mountpoint
          disk.total = usage.total
          disk.used = usage.used
          disk.free = usage.free
          disk.percent = usage.percent

    disk.mounted_fs_total = alltotal
    disk.filesystems = filesystems
