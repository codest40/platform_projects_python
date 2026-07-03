"""
Memory collector using Linux PSI.

Reads:
/proc/pressure/memory
"""

from __future__ import annotations
from pathlib import Path
from project.models.memory import MemoryData


PRESSURE = Path("/proc/pressure/memory")


def _read_pressure() -> dict[str, dict[str, float]]:
    """
    Example:

    some avg10=0.00 avg60=0.12 avg300=0.25 total=12345
    full avg10=0.00 avg60=0.05 avg300=0.10 total=4567
    """

    data: dict[str, dict[str, float]] = {}

    if not PRESSURE.exists():
        return data

    with PRESSURE.open() as f:
        for line in f:
            parts = line.split()

            level = parts[0]

            values: dict[str, float] = {}

            for item in parts[1:]:
                key, value = item.split("=")
                values[key] = float(value)

            data[level] = values

    return data


def collect_pressure(memory: MemoryData) -> None:
    """
    Populate MemoryData using Linux PSI.
    """

    psi = _read_pressure()

    if not psi:
        return

    some = psi.get("some", {})
    full = psi.get("full", {})

    # ==========================================================
    # PSI (Some)
    # ==========================================================
    memory.psi_some_avg10 = some.get("avg10", 0.0)
    memory.psi_some_avg60 = some.get("avg60", 0.0)
    memory.psi_some_avg300 = some.get("avg300", 0.0)

    # ==========================================================
    # PSI (Full)
    # ==========================================================
    memory.psi_full_avg10 = full.get("avg10", 0.0)
    memory.psi_full_avg60 = full.get("avg60", 0.0)
    memory.psi_full_avg300 = full.get("avg300", 0.0)

    # ==========================================================
    # Optional Indicators
    # ==========================================================
    memory.low_memory_events = int(memory.psi_full_avg10 > 0)

