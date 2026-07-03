"""
Memory collector using Linux NUMA information.
"""

from __future__ import annotations
from pathlib import Path
from project.models.memory import MemoryData


NODES = Path("/sys/devices/system/node")
def collect_numa(memory: MemoryData) -> None:

    if not NODES.exists():
        return

    nodes = sorted(
        p for p in NODES.iterdir()
        if p.is_dir() and p.name.startswith("node")
    )

    memory.numa_nodes = len(nodes)

    local = 0
    remote = 0

    for node in nodes:

        stat = node / "numastat"

        if not stat.exists():
            continue

        with stat.open() as f:

            for line in f:

                parts = line.split()

                if len(parts) < 2:
                    continue

                name = parts[0]

                values = [int(v) for v in parts[1:]]

                total = sum(values)

                if name == "local_node":
                    local += total

                elif name == "other_node":
                    remote += total

    memory.numa_remote_accesses = remote

    if local + remote:
        memory.numa_imbalance = (
            remote / (local + remote)
        ) * 100
