from __future__ import annotations
from pathlib import Path
from project.models.disk import DiskData


PRESSURE = Path("/proc/pressure/io")


def _read_pressure() -> dict[str, dict[str, float]]:
    """
    Example
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

            values = {}

            for item in parts[1:]:

                key, value = item.split("=")
                values[key] = float(value)

            data[level] = values

    return data


def collect_pressure(disk: DiskData) -> None:

    psi = _read_pressure()

    if not psi:
        return

    some = psi.get("some", {})
    full = psi.get("full", {})

    # ==========================================================
    # IO Pressure
    # ==========================================================

    disk.psi_some_avg10 = some.get("avg10")
    disk.psi_some_avg60 = some.get("avg60")
    disk.psi_some_avg300 = some.get("avg300")

    disk.psi_full_avg10 = full.get("avg10")
    disk.psi_full_avg60 = full.get("avg60")
    disk.psi_full_avg300 = full.get("avg300")
