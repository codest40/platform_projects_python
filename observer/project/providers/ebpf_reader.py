from __future__ import annotations
from project.models.processes import RuntimeEvent
from project.utils.helpers import start_count
import time
import select

class EBPFReader:
    """
    Read runtime events produced by the Observer
    eBPF runtime loader.
    """

    def __init__(self, loader) -> None:
        self.loader = loader
        self.did_read_succeed = None

    def start(self) -> None:
        self.loader.load()

    def stop(self) -> None:
        self.loader.unload()

    def read(self) -> list[RuntimeEvent]:
        """
        Read all currently available runtime events.
        """
        self.did_read_succeed = False
        self.start()
        stdout = self.loader.stdout

        if stdout is None:
            #print("[EBPF READER] stdout is Empty")
            return []

        events: list[RuntimeEvent] = []
        start_time = start_count()
        collection_window = 5
        while start_count() - start_time < collection_window:

            ready, _, _ = select.select([stdout], [], [], 0.1)
            if ready:
                line = stdout.readline()
            else:
                continue

            if not line:
                #time.sleep(0.1)
                continue

            line = line.strip()

            if not line.startswith("pid="):
                continue

            raw = {}

            for field in line.split():

                key, value = field.split("=", 1)

                raw[key] = int(value)

            print("EVENT:", line)
            print("Creating RuntimeEvent...")
            events.append(
                RuntimeEvent(
                    pid=raw["pid"],
                    tid=raw["tid"],
                    timestamp_ns=raw.get("time", 0),
                    category=raw["category"],
                    code=raw["code"],
                    value=raw["value"],
                )
            )

            if not stdout:
                break

        self.did_read_succeed = True
        return events
