from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path


class EBPFLoader:
    """
    Manage the Observer eBPF runtime process.
    """
    DIRECTORY = Path(__file__).parent / "ebpf"
    LOADER = DIRECTORY / "runtime_loader"
    OBJECT = DIRECTORY / "runtime.bpf.o"

    def __init__(self) -> None:
        self.process: subprocess.Popen | None = None
        self.did_loading_succeed = False

    @classmethod
    def available(cls) -> bool:
        """
        Return True if the eBPF runtime can be started.
        """
        return (
            cls.LOADER.exists()
            and os.access(cls.LOADER, os.X_OK)
            and cls.OBJECT.exists()
            and Path("/sys/fs/bpf").exists()
        )

    @property
    def running(self) -> bool:

        return (
            self.process is not None
            and self.process.poll() is None
        )

    def load(self) -> None:
        """
        Start the runtime loader.
        """
        if self.running:
            return

        if not self.available():
            raise RuntimeError(
                "Observer eBPF runtime is unavailable."
            )

        self.process = subprocess.Popen(
            ["stdbuf", "-o0", str(self.LOADER)],
            #[str(self.LOADER)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        self.did_loading_succeed = (
            self.process is not None
            and self.process.poll() is None
        )
        #print("PID:", self.process.pid)
        #print("Running:", self.process.poll() is None)
        #import time
        #time.sleep(2)
        #print("Reading one line...")
        #print(repr(self.process.stdout.readline()))

    def unload(self) -> None:
        """
        Stop the runtime loader.
        """

        if not self.running:
            return

        self.process.send_signal(signal.SIGINT)

        try:
            self.process.wait(timeout=5)

        except subprocess.TimeoutExpired:

            self.process.kill()
            self.process.wait()

        self.process = None

    @property
    def stdout(self):

        if not self.running:
            return None

        return self.process.stdout

    @property
    def stderr(self):

        if not self.running:
            return None

        return self.process.stderr
