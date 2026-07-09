"""
CPU Pressure (PSI) collector.
Collects Linux Pressure Stall Information (PSI).

Source:
    /proc/pressure/cpu
    or
    /sys/fs/cgroup/cpu.pressure
"""

from __future__ import annotations

from pathlib import Path

from project.models.cpu import CpuData as Cpu_Data


CPU_PRESSURE_PATHS = (
    Path("/proc/pressure/cpu"),
    Path("/sys/fs/cgroup/cpu.pressure"),
)


def _parse_pressure(text: str) -> dict[str, float]:
    """
    Parse Linux PSI file.

    Example:
    some avg10=0.00 avg60=0.01 avg300=0.02 total=12345
    full avg10=0.00 avg60=0.00 avg300=0.00 total=0
    """

    values: dict[str, float] = {}

    for line in text.splitlines():

        parts = line.split()

        if len(parts) < 2:
            continue

        prefix = parts[0]

        for item in parts[1:]:

            if "=" not in item:
                continue

            key, value = item.split("=", 1)

            if key.startswith("avg"):

                try:
                    values[f"{prefix}_{key}"] = float(value)
                except ValueError:
                    pass

    return values


def collect_pressure(cpu: Cpu_Data) -> Cpu_Data:
    """
    Collect CPU PSI metrics.
    Missing files are ignored.
    """

    pressure_file = None

    for path in CPU_PRESSURE_PATHS:
        if path.exists():
            pressure_file = path
            break

    if pressure_file is None:
        return cpu

    try:

        values = _parse_pressure(
            pressure_file.read_text()
        )

        cpu.psi_some_avg10 = values.get("some_avg10")
        cpu.psi_some_avg60 = values.get("some_avg60")
        cpu.psi_some_avg300 = values.get("some_avg300")

        cpu.psi_full_avg10 = values.get("full_avg10")
        cpu.psi_full_avg60 = values.get("full_avg60")
        cpu.psi_full_avg300 = values.get("full_avg300")

    except Exception:
        pass

    return cpu
