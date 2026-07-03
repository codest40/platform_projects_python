"""
Logging Formatters
Provides JSON and human-readable formatters for
Platform Observer log records.
"""

from __future__ import annotations

import json
import logging
from dataclasses import fields, is_dataclass

from project.models.events import PlatformEvent, AnalysisEvent
from project.utils.context import (
    serialize_event,
    serialize_span,
    serialize_analysis,
)


# =========================================================
# JSON FORMATTER
# =========================================================

class JsonFormatter(logging.Formatter):
    """
    Writes one JSON object per line.
    """

    def format(self, record: logging.LogRecord) -> str:

        payload = None

        if hasattr(record, "platform_event"):
            payload = serialize_event(
                record.platform_event,
                record.caller,
            )

        elif hasattr(record, "analysis_event"):
            payload = serialize_analysis(
                record.analysis_event,
                record.caller,
            )

        elif hasattr(record, "platform_span"):
            payload = serialize_span(
                record.platform_span,
                record.caller,
            )

        else:
            return super().format(record)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(
            payload,
            default=str,
            ensure_ascii=False,
        )


# =========================================================
# PRETTY PRINT HELPERS
# =========================================================

def print_object(
    obj,
    *,
    lines: list[str],
    indent: int = 0,
    skip: set[str] | None = None,
):
    """
    Recursively pretty-print any object.
    """

    skip = skip or set()
    prefix = " " * indent

    if obj is None:
        lines.append(f"{prefix}None")
        return

    if isinstance(obj, (str, int, float, bool)):
        lines.append(f"{prefix}{obj}")
        return

    if is_dataclass(obj):
        obj = {
            f.name: getattr(obj, f.name)
            for f in fields(obj)
        }

    elif hasattr(obj, "__dict__"):
        obj = vars(obj)

    if isinstance(obj, dict):

        for key, value in obj.items():

            if key in skip:
                continue

            if value is None:
                continue

            if isinstance(value, (dict, list, tuple, set)) or is_dataclass(value):

                lines.append(f"{prefix}{key}:")

                print_object(
                    value,
                    lines=lines,
                    indent=indent + 4,
                    skip=skip,
                )

            else:

                lines.append(
                    f"{prefix}{key:<22} {value}"
                )

        return

    if isinstance(obj, (list, tuple, set)):

        for item in obj:

            if isinstance(item, (dict, list, tuple, set)) or is_dataclass(item):

                lines.append(f"{prefix}-")

                print_object(
                    item,
                    lines=lines,
                    indent=indent + 4,
                    skip=skip,
                )

            else:

                lines.append(
                    f"{prefix}- {item}"
                )

        return

    lines.append(f"{prefix}{repr(obj)}")


# =========================================================
# PRETTY FORMATTER
# =========================================================

class PrettyFormatter(logging.Formatter):

    separator = "-" * 80

    def format(self, record):

        if hasattr(record, "platform_event"):

            event = record.platform_event

            return self._format_object(
                title=f"[{event.severity}] {event.event_name}",
                obj=event,
                caller=record.caller,
                exc_info=record.exc_info,
            )

        if hasattr(record, "analysis_event"):

            return self._format_object(
                title="[ANALYSIS]",
                obj=record.analysis_event,
                caller=record.caller,
                exc_info=record.exc_info,
            )

        if hasattr(record, "platform_span"):

            return self._format_span(record)

        return super().format(record)

    def _format_object(
        self,
        *,
        title,
        obj,
        caller,
        exc_info=None,
    ):

        lines = [
            self.separator,
            title,
            "",
        ]

        print_object(
            obj,
            lines=lines,
        )

        if caller:

            lines.extend([
                "",
                "Caller",
            ])

            print_object(
                caller,
                lines=lines,
                indent=2,
            )

        if exc_info:

            lines.extend([
                "",
                "Exception",
                self.formatException(exc_info),
            ])

        lines.append(self.separator)

        return "\n".join(lines)

    def _format_span(self, record):

        span = record.platform_span

        lines = [
            self.separator,
            "[SPAN]",
            "",
        ]

        print_object(
            span,
            lines=lines,
        )

        lines.extend([
            "",
            "Caller",
        ])

        print_object(
            record.caller,
            lines=lines,
            indent=2,
            skip={"execution"},
        )

        if record.caller.get("execution"):

            lines.extend([
                "",
                "Execution Path",
            ])

            for i, step in enumerate(record.caller["execution"], start=1):
                lines.append(f"  {i}. {step}")

        lines.append(self.separator)

        return "\n".join(lines)
