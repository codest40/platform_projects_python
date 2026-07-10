from pathlib import Path

from project.models.processes import ProcessSnapshot, CollectorFailure, ProcessCache


def collect_cpu(
    snapshot: ProcessSnapshot,
    cache: ProcessCache,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect lightweight CPU accounting information.
    Source:
        /proc/<pid>/stat
    """

    try:

        if cache.stat is None:
            raise RuntimeError("/proc/<pid>/stat unavailable")

        stat = cache.stat
        #
        # comm is enclosed in parentheses and may contain spaces.
        #
        _, remainder = stat.rsplit(")", 1)

        fields = remainder.strip().split()

        #
        # utime (field 14)
        #
        snapshot.user_ticks = int(fields[11])

        #
        # stime (field 15)
        #
        snapshot.system_ticks = int(fields[12])

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_cpu: {e}"
        )

        collector_failures.append(
          CollectorFailure(
            pid=snapshot.pid,
            collector="ps_cpu",
            field="stat",
            reason=str(e),
          )
        )

    return snapshot
