from pathlib import Path
import os

from project.models.processes import ProcessSnapshot, CollectorFailure, ProcessCache
CLK_TCK = os.sysconf(os.sysconf_names["SC_CLK_TCK"])


def collect_lifecycle(
    snapshot: ProcessSnapshot,
    cache: ProcessCache,
    uptime_seconds: float,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process lifetime information.
    Source:
        /proc/<pid>/stat

    """
    try:

        if cache.stat is None:
            raise RuntimeError("/proc/<pid>/stat unavailable")
        stat = cache.stat
        #
        # comm is enclosed in parentheses.
        #
        _, remainder = stat.rsplit(")", 1)

        fields = remainder.strip().split()

        #
        # Process start time since boot (clock ticks)
        #
        start_ticks = int(fields[19])

        #
        # Convert to seconds since boot.
        #
        snapshot.start_time = start_ticks / CLK_TCK

        #
        # Process runtime.
        #
        snapshot.runtime_seconds = max(
            0.0,
            uptime_seconds - snapshot.start_time,
        )

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_lifecycle: {e}"
        )
        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_lifecycle",
                field="stat",
                reason=str(e),
            )
        )

    return snapshot
