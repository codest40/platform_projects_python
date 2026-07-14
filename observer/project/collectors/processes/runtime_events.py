from project.models.processes import (
    ProcessSnapshot,
    CollectorFailure,
    ProcessRuntimeEvents,
    RuntimeEvent,
)
import signal
from project.providers.kernel_events import EBPF_EVENTS


def collect_runtime_events(
    snapshot: ProcessSnapshot,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process runtime events.
    Events comes from: eBPF or tracefs
        - other kernel event providers
    """

    try:

        events = snapshot.runtime_events
        if events is None:
            events = ProcessRuntimeEvents()

        runtime_events = EBPF_EVENTS
        for event in runtime_events:
            if event.pid != snapshot.pid:
                continue


            if event.code == "EMFILE":
                if events.emfile_count is None:
                    events.emfile_count = 0
                events.emfile_count += 1

            elif event.code == "ENFILE":
                if events.enfile_count is None:
                    events.enfile_count = 0

                events.enfile_count += 1


            elif event.code == "SIGSEGV":

                if events.segfault_count is None:
                    events.segfault_count = 0
                events.segfault_count += 1
                events.last_terminating_signal = signal.SIGSEGV.value


            elif event.code == "SIGBUS":
                if events.sigbus_count is None:
                    events.sigbus_count = 0
                events.sigbus_count += 1
                events.last_terminating_signal = signal.SIGBUS.value


            elif event.code == "SIGABRT":
                if events.sigabrt_count is None:
                    events.sigabrt_count = 0
                events.sigabrt_count += 1
                events.last_terminating_signal = signal.SIGABRT.value


            elif event.code == "SIGILL":
                if events.sigill_count is None:
                    events.sigill_count = 0
                events.sigill_count += 1
                events.last_terminating_signal = signal.SIGILL.value

            elif event.code == "OOM_KILL":
                if events.oom_kill_count is None:
                    events.oom_kill_count = 0
                events.oom_kill_count += 1

        snapshot.runtime_events = events
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
