from pathlib import Path
from project.models.processes import ProcessSnapshot, CollectorFailure, ProcessCache

KB = 1024

def collect_memory(
    snapshot: ProcessSnapshot,
    cache: ProcessCache,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect lightweight process memory information.
    Source:
        /proc/<pid>/status
    """

    try:
        if cache.status is None:
            raise RuntimeError("/proc/<pid>/status unavailable")
        status = cache.status.splitlines()
        for line in status:

                if line.startswith("VmRSS:"):

                    snapshot.rss_bytes = (
                        int(line.split()[1]) * KB
                    )

                elif line.startswith("VmSize:"):

                    snapshot.vms_bytes = (
                        int(line.split()[1]) * KB
                    )

                elif line.startswith("Threads:"):

                    snapshot.thread_count = int(
                        line.split()[1]
                    )

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_memory: {e}"
        )
        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_memory",
                field="status",
                reason=str(e),
            )
        )
    return snapshot
