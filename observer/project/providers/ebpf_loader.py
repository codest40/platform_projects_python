from __future__ import annotations

from pathlib import Path
import shutil


class EBPFLoader:
    """
    Loads and manages Observer eBPF programs.

    Responsibilities
    ----------------
    - Detect whether eBPF is available.
    - Locate the compiled Observer eBPF program.
    - Load it into the kernel.
    - Unload it when requested.

    This class intentionally knows nothing about
    RuntimeEvent or analyzers.
    """

    # Compiled eBPF object shipped with Observer.
    PROGRAM = (
        Path(__file__).parent
        / "process_events.bpf.o"
    )

    def __init__(self) -> None:
        self.loaded = False
        self.handle = None

    @classmethod
    def available(cls) -> bool:
        """
        Return True if this machine appears capable of
        loading Observer's eBPF program.
        """

        return (
            cls.PROGRAM.exists()
            and Path("/sys/fs/bpf").exists()
        )

    def load(self):
        """
        Load the eBPF program.

        Later this will use libbpf (or another loader)
        to load PROGRAM into the kernel.
        """

        if self.loaded:
            return self.handle

        if not self.available():
            raise RuntimeError(
                "eBPF is unavailable on this system."
            )

        #
        # TODO
        #
        # handle = libbpf.load(PROGRAM)
        #
        # self.handle = handle
        #

        self.loaded = True

        return self.handle

    def unload(self):
        """
        Unload the eBPF program.
        """

        if not self.loaded:
            return

        # destroy links
        # close ring buffer
        # detach programs
        self.loaded = False
        self.handle = None
