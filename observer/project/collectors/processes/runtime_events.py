from project.models.processes import (
    ProcessSnapshot,
    CollectorFailure,
    ProcessRuntimeEvents,
)
import signal
from project.providers.kernel_events import EBPFProvider

def collect_runtime_events(
    snapshot: ProcessSnapshot,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process runtime events.
    Events comes from: eBPF or tracefs
    """
    try:
        ebpf_provider = EBPFProvider()
        if not ebpf_provider.available():
          return snapshot
    except Exception as e:
        return snapshot

    try:
        process_events = ebpf_provider.read_process_events()
        snapshot.runtime_collected_events = (
            process_events.get(snapshot.pid)
            or ProcessRuntimeEvents()
        )

    except Exception as e:
        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="runtime_events",
                field="runtime_events",
                reason=str(e),
            )
        )

    return snapshot
