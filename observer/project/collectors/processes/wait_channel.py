from pathlib import Path

from project.models.processes import (
    ProcessSnapshot,
    CollectorFailure,
    ObserverState as OB,
)


def collect_wait_channel(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect kernel wait channel.

    Source:
        /proc/<pid>/wchan
    """

    try:

        wchan = (proc_dir / "wchan").read_text().strip()

        snapshot.wchan = (
            wchan if wchan != "-" else OB.NA
        )

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_wait_channel: {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_wait_channel",
                field="wchan",
                reason=str(e),
            )
        )

    return snapshot
