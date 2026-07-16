from __future__ import annotations

from project.providers.ebpf_loader import EBPFLoader
from project.providers.ebpf_reader import EBPFReader
from project.providers.runtime import RuntimeAggregator


class EBPFProvider:
    """
    Process runtime event provider backed by the
    Observer eBPF runtime collector.

    If eBPF is unavailable, this provider behaves
    as a no-op and simply returns no events.
    """
    def __init__(self) -> None:

        self.loader = EBPFLoader()
        self.reader = EBPFReader(self.loader)
        self.runtime = RuntimeAggregator(
            self.reader
        )

    @property
    def is_event_available(self):
        """
        Return whether the runtime eBPF collector
        is available on this system.
        """
        return self.loader.available()

    @property
    def did_loading_succeed(self):
        return self.loader.did_loading_succeed

    @property
    def did_read_succeed(self):
        return self.reader.did_read_succeed

    def read_process_events(self) -> dict:
        """
        Return runtime events grouped by PID.
        If eBPF is unavailable, an empty result
        is returned so the rest of the Observer
        pipeline continues normally.
        """
        if not self.is_event_available:
            return {}

        #print("Calling RuntimeAggregator.read()")
        return self.runtime.read()
