from pathlib import Path
import re

from project.models.processes import ProcessSnapshot, CollectorFailure, ProcessCache

CONTAINER_ID = re.compile(r"[a-f0-9]{64}|[a-f0-9]{32}")

def collect_cgroup(
    snapshot: ProcessSnapshot,
    cache: ProcessCache,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process cgroup information.
    Source:
        /proc/<pid>/cgroup
    """

    try:

        if cache.cgroup is None:
            raise RuntimeError("/proc/<pid>/cgroup unavailable")

        content = cache.cgroup
        snapshot.cgroup = content.strip()
        match = CONTAINER_ID.search(content)

        if match:

            snapshot.container_id = match.group(0)

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_cgroup: {e}"
        )
        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_cgroup",
                field="cgroup",
                reason=str(e),
            )
        )

    return snapshot
