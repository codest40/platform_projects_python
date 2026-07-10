from pathlib import Path

from project.models.processes import (
    ProcessSnapshot,
    ProcessCache,
    CollectorFailure,
)


def collect_fd(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
    cache: ProcessCache,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process file descriptor information.
    Sources:
        /proc/<pid>/fd
        /proc/<pid>/limits
    """

    #
    # ---------------------------------------------------------
    # Current open file descriptors
    # ---------------------------------------------------------
    #

    try:

        #snapshot.open_fds = len(list((proc_dir / "fd").iterdir()))
        snapshot.open_fds = sum(1 for _ in (proc_dir / "fd").iterdir())
    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_fd(open): {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_fd",
                field="open_fds",
                reason=str(e),
            )
        )

    #
    # ---------------------------------------------------------
    # Maximum file descriptors
    # ---------------------------------------------------------
    #

    try:

        if cache.limits is None:
            raise RuntimeError("/proc/<pid>/limits unavailable")

        for line in cache.limits.splitlines():

            if line.startswith("Max open files"):

                #
                # Format:
                # Max open files    1024    4096    files
                #

                parts = line.split()

                snapshot.max_fds = int(parts[-3])

                break

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_fd(limit): {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_fd",
                field="max_fds",
                reason=str(e),
            )
        )

    return snapshot
