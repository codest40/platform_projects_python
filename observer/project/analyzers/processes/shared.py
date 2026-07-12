from __future__ import annotations

from collections.abc import Callable
from typing import Any


def build_fact(
    analysis,
    label: str,
    value: Any,
    formatter: Callable[[Any], str] | None = None,
) -> None:
    """
    Append a formatted fact if the value exists.

    Examples
    --------
    build_fact(analysis, "Priority", process.priority)

    build_fact(
        analysis,
        "RSS",
        process.rss_bytes,
        formatter=format_bytes,
    )

    build_fact(
        analysis,
        "CPU",
        process.cpu_percent,
        formatter=format_percent,
    )
    """

    if value is None:
        return

    if formatter is not None:
        value = formatter(value)

    analysis.facts.append(
        f"{label}: {value}"
    )


def format_bytes(value: int | float) -> str:
    """
    Human-readable byte formatter.
    """

    units = (
        "B",
        "KiB",
        "MiB",
        "GiB",
        "TiB",
    )

    value = float(value)

    for unit in units:

        if abs(value) < 1024:
            return f"{value:.1f} {unit}"

        value /= 1024

    return f"{value:.1f} PiB"


def format_rate(
    value: int | float,
    unit: str = "",
) -> str:
    """
    Format a per-second rate.
    """

    if unit:
        return f"{value:.2f} {unit}/sec"

    return f"{value:.2f}/sec"


def format_percent(
    value: int | float,
) -> str:
    """
    Format percentage.
    Accepts values already expressed as percent.
    """

    return f"{value:.1f}%"

def format_duration(
    seconds: float,
) -> str:
    """
    Human-readable duration.
    """

    seconds = int(seconds)

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days:
        return (
            f"{days}d "
            f"{hours}h "
            f"{minutes}m"
        )

    if hours:
        return (
            f"{hours}h "
            f"{minutes}m "
            f"{seconds}s"
        )

    if minutes:
        return (
            f"{minutes}m "
            f"{seconds}s"
        )

    return f"{seconds}s"


def coverage_percent(
    available: int,
    expected: int,
) -> float:

    if not instance(available, int):
        raise
    if not instance(expected, int):
        raise
    if expected == 0:
        return 0.0

    return (available / expected) * 100


