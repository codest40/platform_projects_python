from __future__ import annotations

import signal
from collections import defaultdict

from project.models.processes import (
    ProcessRuntimeEvents,
    RuntimeEvent,
)


#
# Runtime event categories
#

EVENT_FD = 1
EVENT_MEMORY = 2
EVENT_SIGNAL = 3


#
# Runtime event codes
#

CODE_EMFILE = 1
CODE_ENFILE = 2

CODE_OOM_KILL = 100

CODE_SIGSEGV = 200
CODE_SIGBUS = 201
CODE_SIGABRT = 202
CODE_SIGILL = 203
CODE_SIGFPE = 204
CODE_SIGPIPE = 205


class RuntimeAggregator:
    """
    Aggregate RuntimeEvent objects into
    ProcessRuntimeEvents grouped by PID.
    """

    def __init__(self, reader) -> None:
        self.reader = reader

    def read(
        self,
    ) -> dict[int, ProcessRuntimeEvents]:
        #print("Inside RuntimeAggregator.read()")
        processes: dict[
            int,
            ProcessRuntimeEvents,
        ] = defaultdict(ProcessRuntimeEvents)

        runtime_events: list[
            RuntimeEvent
        ] = self.reader.read()

        for event in runtime_events:

            events = processes[event.pid]

            # File descriptor events
            if event.category == EVENT_FD:
                if event.code == CODE_EMFILE:
                    events.emfile_count = (
                        (events.emfile_count or 0) + 1
                    )

                elif event.code == CODE_ENFILE:

                    events.enfile_count = (
                        (events.enfile_count or 0) + 1
                    )

            # Memory events
            elif event.category == EVENT_MEMORY:

                if event.code == CODE_OOM_KILL:

                    events.oom_kill_count = (
                        (events.oom_kill_count or 0) + 1
                    )

            # Fatal signals
            elif event.category == EVENT_SIGNAL:

                if event.code == CODE_SIGSEGV:

                    events.segfault_count = (
                        (events.segfault_count or 0) + 1
                    )

                    events.last_terminating_signal = (
                        signal.SIGSEGV.value
                    )

                elif event.code == CODE_SIGBUS:

                    events.sigbus_count = (
                        (events.sigbus_count or 0) + 1
                    )

                    events.last_terminating_signal = (
                        signal.SIGBUS.value
                    )

                elif event.code == CODE_SIGABRT:

                    events.sigabrt_count = (
                        (events.sigabrt_count or 0) + 1
                    )

                    events.last_terminating_signal = (
                        signal.SIGABRT.value
                    )

                elif event.code == CODE_SIGILL:

                    events.sigill_count = (
                        (events.sigill_count or 0) + 1
                    )

                    events.last_terminating_signal = (
                        signal.SIGILL.value
                    )

                elif event.code == CODE_SIGFPE:

                    events.sigfpe_count = (
                        (events.sigfpe_count or 0) + 1
                    )

                    events.last_terminating_signal = (
                        signal.SIGFPE.value
                    )

                elif event.code == CODE_SIGPIPE:

                    events.sigpipe_count = (
                        (events.sigpipe_count or 0) + 1
                    )

                    events.last_terminating_signal = (
                        signal.SIGPIPE.value
                    )

        return dict(processes)
