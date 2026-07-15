from __future__ import annotations

from project.models.processes import RuntimeEvent


class EBPFReader:
    """
    Reads runtime events produced by the Observer
    eBPF program.

    The loader is responsible for loading the
    program into the kernel.

    This class is responsible only for receiving
    events and converting them into RuntimeEvent
    objects.
    """

    def __init__(self, loader):

        self.loader = loader

    def read(self) -> list[RuntimeEvent]:
        """
        Read available runtime events.

        Later this will consume events from the
        eBPF ring buffer.

        Returns
        -------
        list[RuntimeEvent]
        """

        #
        # TODO:
        #
        # while ring_buffer.poll():
        #     RuntimeEvent(...)
        #

        return []
