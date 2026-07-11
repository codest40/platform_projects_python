from pathlib import Path

from project.models.processes import (
    ProcessSnapshot,
    CollectorFailure,
)


def collect_fd(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process file descriptor information.
    Sources:
        /proc/<pid>/fd
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


    return snapshot
