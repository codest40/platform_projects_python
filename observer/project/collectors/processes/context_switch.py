from project.models.processes import (
    ProcessSnapshot,
    ProcessCache,
    CollectorFailure,
)


def collect_context_switches(
    snapshot: ProcessSnapshot,
    cache: ProcessCache,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process context switch counters.

    Source:
        /proc/<pid>/status
    """

    try:

        if cache.status is None:
            raise RuntimeError("/proc/<pid>/status unavailable")

        for line in cache.status.splitlines():

            if line.startswith("voluntary_ctxt_switches:"):

                snapshot.voluntary_context_switches = int(
                    line.split()[1]
                )

            elif line.startswith("nonvoluntary_ctxt_switches:"):

                snapshot.involuntary_context_switches = int(
                    line.split()[1]
                )

            if (
                snapshot.voluntary_context_switches is not None
                and snapshot.involuntary_context_switches is not None
            ):
                break

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_context_switch: {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_context_switch",
                field="status",
                reason=str(e),
            )
        )

    return snapshot
