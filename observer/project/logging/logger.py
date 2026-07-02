"""
Platform Observer Logger
"""

from __future__ import annotations
from project.models.events import PlatformEvent
from project.models.events import AnalysisEvent

from project.logging.logging_core import logger
from project.utils.context import get_caller_context, get_span_context, resolve_log_level
from project.utils.modify import safe_event
from project.utils.traces import attach_tracing_data as attach

# ==========================================================
# EVENT EMISSION
# ==========================================================
def emit(*args, caller=None, **kwargs) -> None:

    event = safe_event(*args, **kwargs)
    attach(event)

    if caller is None:
      caller = get_caller_context()

    logger.log(
        level=resolve_log_level(event.severity),
        msg=event.summary,
        extra={
            "platform_event": event,
            "caller": caller,
        },
    )

def emit_all(event: PlatformEvent, caller=None) -> None:
    if caller is None:
        caller = get_caller_context()
    attach(event)
    logger.log(
        level=resolve_log_level(event.severity),
        msg=event.summary,
        extra={
            "platform_event": event,
            "caller": caller,
        },
    )


def emit_span(span: PlatformSpan, caller) -> None:
    if caller is None:
        caller = get_span_context()

    logger.log(
        level=resolve_log_level("INFO"),
        msg=span.name,
        extra={
            "platform_span": span,
            "caller": caller,
        },
    )
def emit_analysis(event: AnalysisEvent, caller=None) -> None:
    if caller is None:
        caller = get_caller_context()

    attach(event)
    logger.log(
        level=resolve_log_level(event.severity),
        msg=event.summary,
        extra={
            "analysis_event": event,
            "caller": caller,
        },
    )

# EXCEPTION EMISSION
def emit_exception(*args, caller=None, **kwargs) -> None:
    event = safe_event(*args, **kwargs)
    attach(event)
    if caller is None:
        caller = get_caller_context()

    logger.log(
        level=resolve_log_level(event.severity),
        msg=event.summary,
        exc_info=event.exc_info,
        extra={
            "platform_event": event,
            "caller": caller,
        },
    )
