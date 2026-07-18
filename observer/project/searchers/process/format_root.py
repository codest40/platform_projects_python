from __future__ import annotations

from .helpers import format_number


def format_root(result) -> str:
    if not result.processes:
        return "No root-owned processes found."

    lines = []

    lines.append("=" * 125)
    lines.append(f"ROOT-OWNED PROCESSES: {len(result.processes)}")
    lines.append("=" * 125)

    lines.append(
        f"{'PID':>8}  "
        f"{'NAME':<24} "
        f"{'STATE':<6} "
        f"{'CPU':>8}  "
        f"{'THR':>5}  "
        f"{'FDS':>6}  "
        f"{'UID':>5}  "
        f"{'GID':>5}  "
        f"{'COMMAND'}"
    )

    lines.append("-" * 125)

    for process in result.processes:

        cpu = process.get("cpu_percent")
        cpu = "-" if cpu is None else f"{cpu:.1f}%"

        lines.append(
            f"{process.get('pid', ''):>8}  "
            f"{(process.get('name') or 'N/A'):<24} "
            f"{(process.get('state') or 'N/A'):<6} "
            f"{cpu:>8}  "
            f"{format_number(process.get('thread_count')):>5}  "
            f"{format_number(process.get('open_fds')):>6}  "
            f"{format_number(process.get('uid')):>5}  "
            f"{format_number(process.get('gid')):>5}  "
            f"{process.get('command') or 'N/A'}"
        )

    if result.warnings:
        lines.append("")
        lines.append("Warnings")
        lines.append("--------")
        for warning in result.warnings:
            lines.append(f"• {warning}")

    return "\n".join(lines)
