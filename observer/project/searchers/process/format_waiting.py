from __future__ import annotations

from .helpers import (
    format_duration,
)


def format_waiting(result) -> str:
    if not result.processes:
        return "No waiting processes found."

    lines = []

    lines.append("=" * 110)
    lines.append(f"WAITING PROCESSES ({len(result.processes)})")
    lines.append("=" * 110)

    lines.append(
        f"{'PID':>7}  "
        f"{'NAME':<24} "
        f"{'STATE':<5} "
        f"{'RUNTIME':>10}  "
        f"{'WAIT CHANNEL':>30}"
    )
    lines.append("-" * 110)

    for process in result.processes:
        runtime = format_duration(
            process.get("runtime_seconds")
        )

        lines.append(
            f"{process.get('pid', ''):>7}  "
            f"{(process.get('name') or '-'):<24} "
            f"{(process.get('state') or '-'):<5} "
            f"{runtime:>10}  "
            f"{(process.get('wait_channel') or 'N/A'):>15}"
        )

    if result.warnings:
        lines.append("")
        lines.append("Warnings")
        lines.append("--------")
        for warning in result.warnings:
            lines.append(f"• {warning}")

    return "\n".join(lines)
