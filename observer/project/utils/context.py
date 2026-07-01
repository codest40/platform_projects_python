"""
Platform Observer Logging Context
Provides runtime metadata, caller inspection, timestamps,
and PlatformEvent serialization used by the logging system.
"""

from __future__ import annotations

import inspect
import logging
import os
import socket
from pathlib import Path
from datetime import  datetime
from uuid import uuid4

from project.models.events import PlatformEvent
from project.utils.helpers import timestamp, context_helpers, log_levels

# =========================================================
# APPLICATION CONSTANTS
# =========================================================
helper = context_helpers()
log = log_levels()

SPAN_PREFIX = helper.span_prefix
PROJ_MODULE = helper.project_root
APP_NAME = helper.app_name
APP_VERSION = helper.app_version
SCHEMA_VERSION = helper.schema_version
LOG_LEVELS = log.log_levels

# =========================================================
# RUNTIME INFORMATION
# =========================================================

HOSTNAME = socket.gethostname()

PID = os.getpid()


# =========================================================
# LOGGEr RESOLUTION

def resolve_log_level(level: str | int) -> int:
    if isinstance(level, int):
        return level

    try:
        return LOG_LEVELS[level.upper()]
    except KeyError as exc:
        raise ValueError(
            f"Unknown severity '{level}'. "
            f"Expected one of: {', '.join(LOG_LEVELS)}"
        ) from exc


# =========================================================
# CALLER RESOLUTION
# =========================================================

def get_caller_context(func=None) -> dict[str, str | int]:
    """
    Determine who initiated call to emit()
    """
    if func is None:
        return {}

    try:
        filename = Path(func.__code__.co_filename)
        module = func.__module__

        if module == "__main__":
          try:
              proj_root = filename.parents[2]
              module = ".".join(filename.relative_to(proj_root).with_suffix("").parts)
          except ValueError:
              module = filename.stem

        return {
            "module": module,
            "function": func.__name__,
            "line": func.__code__.co_firstlineno,
            "file": func.__code__.co_filename,
        }

    except Exception as e:
        print("❌ ERROR Building Caller Context", e)


# FOR SPAN
def modify_module_path(module, filename):
    if module == "__main__":
        try:
            proj_root = filename.parents[2]
            module = ".".join(
                filename.relative_to(proj_root)
                        .with_suffix("")
                        .parts
            )
        except ValueError:
            module = filename.stem
    return module

def get_span_context() -> dict[str, str | int]:
    """
    Resolve the framework location responsible for emitting a span.

    Unlike event caller context, span context identifies the framework
    entry point that owns the span (for example run_collection()) while
    also recording the execution path that led to the emission.
    """

    frame = inspect.currentframe()

    if frame is None or frame.f_back is None:
        return {}

    frame = frame.f_back

    execution_path: list[str] = []
    caller: dict[str, str | int] | None = None

    try:
        while frame is not None:

            module = frame.f_globals.get("__name__", "")
            filename = Path(frame.f_code.co_filename)
            function = frame.f_code.co_name

            if (
              module.startswith(PROJ_MODULE)
              or module == "__main__"
            ):

                module = modify_module_path(module, filename)
                execution_path.append(
                  f"{module}.{function}() : line {frame.f_lineno}"
                )

            if (
                caller is None
                and module.startswith(SPAN_PREFIX)
            ):

                module = modify_module_path(module, filename)
                caller = {
                    "module": module,
                    "function": frame.f_code.co_name,
                    "line": frame.f_lineno,
                    "file": frame.f_code.co_filename,
                }

            frame = frame.f_back

        if caller is None:
            return {}

        caller["execution"] = execution_path

        return caller
    except Exeption as e:
      print("❌ Building Span Context Failed!", e)

    finally:
        del frame

# =========================================================
# SYSTEM METADATA
# =========================================================

def get_system_context() -> dict[str, str | int]:

    return {
        "hostname": HOSTNAME,
        "pid": PID,
        "application": APP_NAME,
        "version": APP_VERSION,
        "schema_version": SCHEMA_VERSION,
    }


# =========================================================
# EVENT SERIALIZATION
# =========================================================

def serialize_event(
    event: PlatformEvent,
    caller: dict[str, str | int],
) -> dict:
    """
    Convert a PlatformEvent into a structured dictionary.
    Runtime metadata + tracing ids is injected here before formatting.
    """

    return {
        "type": "event",

        "timestamp": timestamp(),

        "level": logging.getLevelName(event.severity),

        "event_name": event.event_name,

        "category": event.category,

        "collector": event.collector,

        "operation": event.operation,

        "summary": event.summary,

        "event_duration_ms": event.event_duration_ms,

        "cause": event.cause,

        "impact": event.impact,

        "recommendations": event.recommendations,

        "metadata": event.metadata,

        "tags": event.tags,

        "event_id": event.event_id,

        "trace_id": event.trace_id,

        "span_id": event.span_id,

        "parent_span_id": event.parent_span_id,

        "caller": caller,

        "system": get_system_context(),
    }



def serialize_span(span, caller):

    return {

        "type": "span",

        "trace_id": span.trace_id,

        "span_id": span.span_id,

        "parent_span_id": span.parent_span_id,

        "name": span.name,

        "started_at": span.started_at,

        "finished_at": span.finished_at,

        "span_duration_ms": span.span_duration_ms,

        "caller": caller,

        "system": get_system_context(),
    }
