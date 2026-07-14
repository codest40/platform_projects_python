from project.models.processes import (
    ProcessSnapshot,
    CollectorFailure,
    ProcessRuntimeEvents,
    RuntimeEvent,
)
import signal
from project.providers.kernel_events import EBPFProvider
from project.providers.utils.helpers import ENABLE_RUNTIME_EVENTS as enable

enable = True

def collect_runtime_events(
    snapshot: ProcessSnapshot,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process runtime events.
    Events comes from: eBPF or tracefs
        - other kernel event providers
    """
    if not enable:
        return snapshot

    try:

        ebpf_provider = EBPFProvider()
        #if not ebpf_provider.available():
        #  return snapshot

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
