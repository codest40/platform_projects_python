from __future__ import annotations

from .helpers import (
    format_bytes,
    format_number,
    format_ratio,
)


def format_high_memory(result) -> str:
    if not result.processes:
        return "No processes found."

    lines = []

    lines.append("=" * 90)
    lines.append(f"HIGHEST MEMORY PROCESSES: {len(result.processes)}")
    lines.append("=" * 90)

    lines.append(
        f"{'PID':>8}  "
        f"{'NAME':<24} "
        f"{'RSS (Raw+Byte)':>10}  "
        f"{'VMS (Raw+Byte)':>25}  "
        f"{'THR':>16}  "
        f"{'RESIDENT (%+Raw)':>15}"
    )

    lines.append("-" * 90)

    for process in result.processes:
        lines.append(
            f"{process.get('pid', ''):>8}  "
            f"{(process.get('name') or '-'):<24} "
            f"{format_bytes(process.get('rss_bytes')):>12}  "
            f"{format_bytes(process.get('vms_bytes')):>12}  "
            f"{process.get('thread_count', '-'):>5}  "
            f"{format_ratio(process.get('resident_ratio')):>10}"
        )

    lines.append("")
    #lines.append("Raw Values")
    #lines.append("----------")

    """
    for process in result.processes:
        lines.append(f"PID {process.get('pid')} ({process.get('name')})")
        lines.append(
            f"  RSS : {format_number(process.get('rss_bytes'))} bytes"
        )
        lines.append(
            f"  VMS : {format_number(process.get('vms_bytes'))} bytes"
        )
        lines.append("")
    """

    if result.warnings:
        lines.append("Warnings")
        lines.append("--------")
        for warning in result.warnings:
            lines.append(f"• {warning}")

    return "\n".join(lines)
