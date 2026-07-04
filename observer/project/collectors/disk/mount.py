from __future__ import annotations
import psutil
from project.models.disk import DiskData
from project.collectors.disk.data import REAL_FS


def collect_mounts(disk: DiskData) -> None:

    partitions = psutil.disk_partitions(all=False)
    disk.mounts = [
            {
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "options": part.opts,
            }
            for part in partitions
            if part.fstype in REAL_FS
    ]
    disk.mount_count = len(disk.mounts)
