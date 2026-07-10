from pathlib import Path
from project.models.processes import ProcessSnapshot, CollectorFailure, ProcessCache


def collect_scheduler(
    snapshot: ProcessSnapshot,
    cache: ProcessCache,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect scheduler-related process attributes.
    Source:
        /proc/<pid>/stat
    """

    try:
        if cache.stat is None:
            raise RuntimeError("/proc/<pid>/stat unavailable")
        stat = cache.stat

        # comm is enclosed in parentheses and may contain spaces.
        # Split after the closing parenthesis.
        _, remainder = stat.rsplit(")", 1)

        fields = remainder.strip().split()

        snapshot.state = fields[0]
        snapshot.ppid = int(fields[1])

        #
        # priority (field 18)
        #
        snapshot.priority = int(fields[15])

        # nice (field 19)
        snapshot.nice = int(fields[16])

        # last CPU the process executed on
        # processor (field 39)
        snapshot.processor = int(fields[36])
        # real-time priority (field 40)

        snapshot.rt_priority = int(fields[37])
        # scheduling policy (field 41)
        snapshot.policy = int(fields[38])

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_scheduler: {e}"
        )

        collector_failures.append(
            CollectorFailure(
              pid=snapshot.pid,
              collector="ps_scheduler",
              field="stat",
              reason=str(e),
          )
      )
    return snapshot
