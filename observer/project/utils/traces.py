"""
Platform Observer Tracing
Owns the runtime execution context.

Responsibilities
----------------
- Create traces
- Create spans
- Maintain parent/child relationships
- Attach trace information to events
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from uuid import uuid4
from project.utils.helpers import timestamp

# ==========================================================
# SPAN MODELS
# ==========================================================

@dataclass(slots=True)
class ActiveSpan:
    """
    Runtime span.
    Exists only while a function is executing.
    """

    span_id: str
    parent_span_id: str | None
    trace_id: str
    name: str

    started_at: str
    perf_start: float


@dataclass(slots=True)
class PlatformSpan:
    """
    Completed span.
    """

    span_id: str

    parent_span_id: str | None

    trace_id: str

    name: str

    started_at: str

    finished_at: str

    span_duration_ms: float


# ==========================================================
# TRACE CONTEXT
# ==========================================================

@dataclass(slots=True)
class TraceContext:

    trace_id: str | None = None

    span_stack: list[ActiveSpan] = field(default_factory=list)


trace_context = TraceContext()


# ==========================================================
# HELPERS
# ==========================================================

def new_id() -> str:
    return str(uuid4())


def now() -> str:
    return timestamp()


# ==========================================================
# TRACE
# ==========================================================

def start_trace() -> str:

    trace_context.trace_id = new_id()
    trace_context.span_stack.clear()

    return trace_context.trace_id


def ensure_trace() -> str:

    if trace_context.trace_id is None:
        start_trace()

    return trace_context.trace_id


def end_trace() -> None:

    trace_context.trace_id = None
    trace_context.span_stack.clear()


# ==========================================================
# SPANS
# ==========================================================

def current_span() -> ActiveSpan | None:

    if not trace_context.span_stack:
        return None

    return trace_context.span_stack[-1]


def push_span(name: str) -> ActiveSpan:

    ensure_trace()

    parent = current_span()

    span = ActiveSpan(
        span_id=new_id(),
        parent_span_id=parent.span_id if parent else None,
        trace_id=trace_context.trace_id,
        name=name,
        started_at=now(),
        perf_start=perf_counter(),
    )

    trace_context.span_stack.append(span)

    return span


def pop_span() -> PlatformSpan | None:

    if not trace_context.span_stack:
        return None

    active = trace_context.span_stack.pop()

    finished = now()

    duration = round(
        (perf_counter() - active.perf_start) * 1000,
        3,
    )

    return PlatformSpan(
        span_id=active.span_id,
        parent_span_id=active.parent_span_id,
        trace_id=active.trace_id,
        name=active.name,
        started_at=active.started_at,
        finished_at=finished,
        span_duration_ms=duration,
    )


# ==========================================================
# EVENT ATTACHMENT
# ==========================================================

def attach_tracing_data(event) -> None:
    """
    Attach tracing metadata to an event.
    """

    ensure_trace()

    span = current_span()

    event.event_id = new_id()
    event.trace_id = trace_context.trace_id

    if span:
        event.span_id = span.span_id
        event.parent_span_id = span.parent_span_id
