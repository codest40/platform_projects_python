from pathlib import Path

from project.models.processes import ProcessSnapshot, CollectorFailure, ProcessCache


def collect_owner(
    snapshot: ProcessSnapshot,
    cache: ProcessCache,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process ownership information.

    Source:
        /proc/<pid>/status
    """

    try:
        if cache.status is None:
            raise RuntimeError("/proc/<pid>/stat unavailable")

        ff = cache.status.splitlines()
        for line in ff:

                if line.startswith("Uid:"):

                    snapshot.uid = int(line.split()[1])

                elif line.startswith("Gid:"):

                    snapshot.gid = int(line.split()[1])

                if (
                    snapshot.uid is not None
                    and snapshot.gid is not None
                ):
                    break

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_owner: {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_owner",
                field="status",
                reason=str(e),
            )
        )

    return snapshot
