from __future__ import annotations

import signal
from collections import defaultdict

from project.models.processes import (
    RuntimeEvent,
    ProcessRuntimeEvents,
)


class EBPFProvider:
    """
    Kernel runtime event provider.
    Currently returns mock events.
    Later this will read from an eBPF ring buffer.
    """

    def __init__(self) -> None:
        self.metadata: dict = {}

    def read_events(self) -> list[RuntimeEvent]:
        return [
            RuntimeEvent(
                pid=1234,
                timestamp=1720950000.55,
                category="fd",
                code="EMFILE",
            ),
            RuntimeEvent(
                pid=1234,
                timestamp=1720950001.10,
                category="fd",
                code="EMFILE",
            ),
            RuntimeEvent(
                pid=1234,
                timestamp=1720950010.20,
                category="signal",
                code="SIGSEGV",
            ),
            RuntimeEvent(
                pid=5678,
                timestamp=1720950020.10,
                category="memory",
                code="OOM_KILL",
            ),
        ]

    def read_process_events(
        self,
    ) -> dict[int, ProcessRuntimeEvents]:
        """
        Aggregate runtime events by PID.
        """
        processes: dict[int, ProcessRuntimeEvents] = defaultdict(
            ProcessRuntimeEvents
        )

        for event in self.read_events():

            events = processes[event.pid]
            if event.category == "fd":
              if event.code == "EMFILE":
                events.emfile_count = (
                    (events.emfile_count or 0) + 1
                )

              elif event.code == "ENFILE":
                events.enfile_count = (
                    (events.enfile_count or 0) + 1
                )

              elif event.code == "OOM_KILL":
                events.oom_kill_count = (
                    (events.oom_kill_count or 0) + 1
                )
            if event.category == "signal":
              if event.code == "SIGSEGV":
                events.segfault_count = (
                    (events.segfault_count or 0) + 1
                )
                events.last_terminating_signal = (
                    signal.SIGSEGV.value
                )

              elif event.code == "SIGBUS":
                events.sigbus_count = (
                    (events.sigbus_count or 0) + 1
                )
                events.last_terminating_signal = (
                    signal.SIGBUS.value
                )

              elif event.code == "SIGABRT":
                events.sigabrt_count = (
                    (events.sigabrt_count or 0) + 1
                )
                events.last_terminating_signal = (
                    signal.SIGABRT.value
                )

              elif event.code == "SIGILL":
                events.sigill_count = (
                    (events.sigill_count or 0) + 1
                )
                events.last_terminating_signal = (
                    signal.SIGILL.value
                )
            elif event.cateory == "others like mem, network, etc":
              pass
        return dict(processes)
