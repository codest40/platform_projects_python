from __future__ import annotations

from project.models.processes import ObserverState as OB


def format_na(value):
    if value is OB.NS:
        return OB.NS
    if value in OB.values:
        return OB.NA
    return value


def format_number(value):
    value = format_na(value)

    if value == OB.NA:
        return value

    if isinstance(value, int):
        return f"{value:,}"

    if isinstance(value, float):
        return f"{value:,.2f}"

    return str(value)


def format_bytes(value):
    value = format_na(value)

    if value == OB.NA:
        return value

    raw = int(value)

    units = (
        "B",
        "KiB",
        "MiB",
        "GiB",
        "TiB",
    )

    size = float(raw)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{raw:,} B ({size:.1f} {unit})"
        size /= 1024


def format_percent(value):
    value = format_na(value)

    if value == OB.NA:
        return value

    return f"{float(value):.2f}% ({value})"


def format_ratio(value):
    value = format_na(value)

    if value == OB.NA:
        return value

    return f"{float(value) * 100:.2f}% ({value})"


def format_duration(seconds):
    seconds = format_na(seconds)

    if seconds == OB.NA:
        return seconds

    total = float(seconds)

    h, rem = divmod(int(total), 3600)
    m, s = divmod(rem, 60)

    return f"{h:02}:{m:02}:{s:02} ({total:.1f} sec)"


def format_field(lines, label, value):
    lines.append(f"{label:<20}: {format_na(value)}")


def format_section(lines, title):
    lines.append("")
    lines.append(title)
    lines.append("-" * len(title))


def format_bullet_list(lines, values):
    if not values:
        lines.append("  None")
        return

    for value in values:
        lines.append(f"  • {value}")
