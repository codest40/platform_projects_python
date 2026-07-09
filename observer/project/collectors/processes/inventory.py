from pathlib import Path

from project.models.processes import (
    ProcessInventory,
    ProcessSnapshot,
)

from project.collectors.processes.identity import collect_identity
from project.collectors.processes.scheduler import collect_scheduler
from project.collectors.processes.owner import collect_owner
from project.collectors.processes.memory import collect_memory
from project.collectors.processes.cpu import collect_cpu
from project.collectors.processes.lifecycle import collect_lifecycle
from project.collectors.processes.cgroup import collect_cgroup


PROC = Path("/proc")


def collect_process_inventory() -> ProcessInventory:
    """
    Build a lightweight inventory of all running processes.

    This is the only module responsible for walking /proc.
    All snapshot collectors populate a shared ProcessSnapshot.
    """

    inventory = ProcessInventory()

    #
    # Read system uptime once.
    #
    with open("/proc/uptime") as f:
        uptime_seconds = float(f.readline().split()[0])

    for entry in PROC.iterdir():

        if not entry.name.isdigit():
            continue

        inventory.collected_total += 1

        pid = int(entry.name)
        proc_dir = entry

        snapshot = ProcessSnapshot(pid=pid)

        try:

            snapshot = collect_identity(snapshot, proc_dir)
            snapshot = collect_scheduler(snapshot, proc_dir)
            snapshot = collect_owner(snapshot, proc_dir)
            snapshot = collect_memory(snapshot, proc_dir)
            snapshot = collect_cpu(snapshot, proc_dir)
            snapshot = collect_lifecycle(
                snapshot,
                proc_dir,
                uptime_seconds,
            )
            snapshot = collect_cgroup(snapshot, proc_dir)

            inventory.collected_successful += 1

        except ProcessLookupError:
            #
            # Process exited while collecting.
            #
            continue

        except FileNotFoundError:
            #
            # Process exited while collecting.
            #
            continue

        except Exception as e:

            snapshot.collection_errors.append(
                f"inventory: {e}"
            )

        inventory.processes.append(snapshot)

    return inventory

if __name__ == "__main__":
    inventory = collect_process_inventory()

    print(f"Collected {inventory.collected_successful}/{inventory.collected_total}")

    for process in inventory.processes[:10]:
        print(process)
