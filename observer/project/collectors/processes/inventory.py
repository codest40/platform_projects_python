from pathlib import Path

from project.models.processes import (
    ProcessInventory,
    ProcessSnapshot,
    InaccessibleProcess,
    CollectorFailure,
    ProcessCache,
)

from project.collectors.processes.identity import collect_identity
from project.collectors.processes.scheduler import collect_scheduler
from project.collectors.processes.owner import collect_owner
from project.collectors.processes.memory import collect_memory
from project.collectors.processes.cpu import collect_cpu
from project.collectors.processes.lifecycle import collect_lifecycle
from project.collectors.processes.cgroup import collect_cgroup

PROC = Path("/proc")

def build_cache(proc_dir: Path) -> ProcessCache:

    cache = ProcessCache()

    try:
        cache.stat = (proc_dir / "stat").read_text()
    except Exception:
        pass

    try:
      cache.status = (proc_dir / "status").read_text()
    except Exception:
        pass

    try:
        cache.cmdline = (proc_dir / "cmdline").read_bytes()
    except Exception:
      pass

    try:
        cache.cgroup = (proc_dir / "cgroup").read_text()
    except Exception:
        pass

    return cache

def collect_process_inventory() -> ProcessInventory:
    """
    Build a lightweight inventory of all running processes.

    This is the only module responsible for walking /proc.
    All snapshot collectors populate a shared ProcessSnapshot.
    """

    inventory = ProcessInventory()

    # Read system uptime once.
    with open("/proc/uptime") as f:
        uptime_seconds = float(f.readline().split()[0])

    for entry in PROC.iterdir():

        if not entry.name.isdigit():
            continue
        inventory.total_processes += 1
        inventory.collected_total += 1

        pid = int(entry.name)
        proc_dir = entry
        cache = build_cache(proc_dir)

        snapshot = ProcessSnapshot(pid=pid)

        try:

            snapshot = collect_identity(snapshot, proc_dir, cache, inventory.collector_failures,)
            snapshot = collect_scheduler(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_owner(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_memory(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_cpu(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_lifecycle(
                snapshot,
                cache,
                uptime_seconds,
                inventory.collector_failures,
            )
            snapshot = collect_cgroup(snapshot, cache, inventory.collector_failures,)

            inventory.accessible_processes += 1
            inventory.collected_successful += 1
            inventory.processes.append(snapshot)
        except (ProcessLookupError, FileNotFoundError) as both:
            #
            # Process exited while collecting.
            if isinstance(both, ProcessLookupError):
                  reason="process exited during collection",
            else:
                  reason="process File Not Found"

            inventory.inaccessible_processes.append(
                    InaccessibleProcess(
                      pid=pid,
                      reason=reason,
                    )
            )

            continue

        except Exception as e:

            snapshot.collection_errors.append(
                f"inventory: {e}"
            )

            inventory.inaccessible_processes.append(
                InaccessibleProcess(
                    pid=pid,
                    reason=str(e),
                )
            )

    return inventory

if __name__ == "__main__":
    inventory = collect_process_inventory()

    print(f"Collected {inventory.collected_successful}/{inventory.collected_total}")
    print(
        f"Visible: {inventory.total_processes} | "
        f"Accessible: {inventory.accessible_processes} | "
        f"Inaccessible: {inventory.inaccessible_processes} | "
        #f"Failures: {inventory.collector_failures} "
    )
    for process in inventory.processes[:10]:
        print(process)
