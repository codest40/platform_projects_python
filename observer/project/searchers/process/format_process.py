from __future__ import annotations
from project.searchers.process.helpers import (
    format_section,
    format_field,
    format_bullet_list,
    format_bytes,
    format_percent,
    format_ratio,
    format_duration,
    format_number,
)


def format_process(result) -> str:
    if not result.processes:
        return "\n".join(result.warnings)

    p = result.processes[0]

    lines = []
    lines.append("=" * 70)
    lines.append(f"PROCESS {p.get('pid')}")
    lines.append("=" * 70)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    format_section(lines, "Summary")
    format_field(lines, "Healthy", p.get("healthy"))
    format_field(lines, "Severity", p.get("severity"))
    format_field(lines, "Confidence", p.get("confidence"))
    format_field(lines, "Coverage", p.get("coverage"))

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    format_section(lines, "Identity")
    format_field(lines, "Name", p.get("name"))
    format_field(lines, "PID", format_number(p.get("pid")))
    format_field(lines, "Parent PID", format_number(p.get("ppid")))
    format_field(lines, "Command", p.get("command"))
    format_field(lines, "Executable", p.get("executable"))
    format_field(lines, "Owner", p.get("owner_type"))
    format_field(lines, "UID", format_number(p.get("uid")))
    format_field(lines, "GID", format_number(p.get("gid")))
    format_field(lines, "Container", p.get("container_id"))

    # ------------------------------------------------------------------
    # Scheduler
    # ------------------------------------------------------------------

    format_section(lines, "Scheduler")
    format_field(lines, "State", p.get("state"))
    format_field(lines, "Priority", format_number(p.get("priority")))
    format_field(lines, "Nice", format_number(p.get("nice")))
    format_field(lines, "RT Priority", format_number(p.get("rt_priority")))
    format_field(lines, "Policy", p.get("scheduler_class"))
    format_field(lines, "CPU", format_number(p.get("processor")))
    format_field(lines, "Runtime", format_duration(p.get("runtime_seconds")))

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------

    format_section(lines, "Memory")
    format_field(lines, "RSS", format_bytes(p.get("rss_bytes")))
    format_field(lines, "Virtual", format_bytes(p.get("vms_bytes")))
    format_field(lines, "Resident Ratio", format_ratio(p.get("resident_ratio")))
    format_field(lines, "Threads", format_number(p.get("thread_count")))

    # ------------------------------------------------------------------
    # CPU
    # ------------------------------------------------------------------

    format_section(lines, "CPU")
    format_field(lines, "CPU %", format_percent(p.get("cpu_percent")))
    format_field(lines, "User CPU %", format_percent(p.get("user_cpu_percent")))
    format_field(lines, "System CPU %", format_percent(p.get("system_cpu_percent")))

    # ------------------------------------------------------------------
    # I/O
    # ------------------------------------------------------------------

    format_section(lines, "I/O")
    format_field(lines, "Read B/s", format_bytes(p.get("read_bytes_per_sec")))
    format_field(lines, "Write B/s", format_bytes(p.get("write_bytes_per_sec")))
    format_field(lines, "Total B/s", format_bytes(p.get("io_bytes_per_sec")))

    # ------------------------------------------------------------------
    # File Descriptors
    # ------------------------------------------------------------------

    format_section(lines, "File Descriptors")
    format_field(lines, "Open", format_number(p.get("open_fds")))
    format_field(lines, "Soft Limit", format_number(p.get("max_fds_soft")))
    format_field(lines, "Hard Limit", format_number(p.get("max_fds_hard")))
    format_field(lines, "Utilization", format_ratio(p.get("fd_utilization")))

    # ------------------------------------------------------------------
    # Runtime Events
    # ------------------------------------------------------------------

    format_section(lines, "Runtime Events")

    runtime = p.get("runtime_collected_events")

    if runtime:
        for key, value in runtime.items():
            format_field(lines, key, value)
    else:
        lines.append("None")

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    format_section(lines, "Signals")

    signals = p.get("signals", {})

    if signals:
        for key in sorted(signals):
            format_field(lines, key, signals[key])
    else:
        lines.append("None")

    # ------------------------------------------------------------------
    # Facts
    # ------------------------------------------------------------------

    format_section(lines, "Facts")
    format_bullet_list(lines, p.get("facts"))

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------

    format_section(lines, "Recommendations")
    format_bullet_list(lines, p.get("recommendations"))

    # ------------------------------------------------------------------
    # Classifications
    # ------------------------------------------------------------------

    format_section(lines, "Classifications")
    format_bullet_list(lines, p.get("classifications"))
    return "\n".join(lines)
