
# Observer Runner Context
from __future__ import annotations
from dataclasses import dataclass
import inspect
from project.logging.logger import emit, emit_span, emit_exception
from project.utils.helpers import line, timestamp, start_count, get_status
from project.utils.context import get_caller_context, get_span_context
from typing import Any, Callable
import traceback as tb
import time
from project.utils.traces import (
    start_trace,
    end_trace,
    push_span,
    pop_span,
)

#==================================================
# Context manager to Run an event
#==============================================

@dataclass(slots=True)
class EventRunner:

    resource: str
    start: float = 0.0
    duration_ms: float = 0.0
    data: Any = None

    exc_type: type | None = None
    exception: Exception | None = None
    traceback: str | None = None
    traceback_obj: Any | None = None

    attempts: int = 0

    status: str = get_status("PENDING")
    comment: str | None = None

    def __enter__(self):

        if not isinstance(self.resource, str):
            raise TypeError(
                f"❌ {self.resource} resource must be supplied as a string"
            )

        self.start = start_count()

        print(line())
        print(f"Starting {self.resource} Event Observer...")

        self.status = get_status("RUNNING")

        return self

    def run(
        self,
        func: Callable[..., Any],
        *args,
        retries: int = 0,
        retry_delay: float = 0.0,
        retry_exceptions: tuple[type[Exception], ...] = (Exception,),
        **kwargs,
    ):

        last_exception = None

        for attempt in range(retries + 1):

            self.attempts = attempt + 1

            try:

                self.data = func(*args, **kwargs)
                return self

            except retry_exceptions as exc:

                last_exception = exc

                if attempt == retries:
                    break

                if retry_delay > 0:
                    time.sleep(retry_delay)

        self.exception = last_exception
        self.exc_type = type(last_exception)
        self.traceback_obj = last_exception.__traceback__
        self.traceback = "".join(
            tb.format_exception(
                type(last_exception),
                last_exception,
                last_exception.__traceback__,
            )
        )

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.duration_ms = (
            start_count() - self.start
        ) * 1000

        if exc_value is not None:

            self.exception = exc_value
            self.exc_type = exc_type
            self.traceback_obj = traceback
            self.traceback = "".join(
                tb.format_exception(
                    exc_type,
                    exc_value,
                    traceback,
                )
            )

            self.status = get_status("FAILED")

            return True

        if self.exception is not None:

            self.status = get_status("FAILED")

            return True

        self.status = get_status("SUCCESS")

        print(f"✅ {self.resource} Event Observer complete.")

        return False

#================================================
# Orchestrator for Span
#===============================================

@dataclass(slots=True)
class TraceObserver:

    resource: str

    def __enter__(self):

        start_trace()

        push_span(self.resource)

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        span = pop_span()
        caller = get_span_context()

        if span is not None:
            emit_span(span, caller)

        end_trace()

        return False



# ==========================================================
# EVENT RUNNER COMPONENTS
# ==========================================================

def event_validate(
    *,
    retries: int,
    retry_delay: float,
    retry_exceptions: tuple[type[Exception], ...],
) -> None:
    """
    Validate EventRunner execution options.
    """

    if retries < 0:
        raise ValueError(
            f"❌ retries must be >= 0, got {retries}"
        )

    if retry_delay < 0:
        raise ValueError(
            f"❌ retry_delay must be >= 0, got {retry_delay}"
        )

    if not isinstance(retry_exceptions, tuple):
        raise TypeError(
            "❌ retry_exceptions must be a tuple of Exception types."
        )

    if not retry_exceptions:
        raise ValueError(
            "❌ retry_exceptions cannot be empty."
        )

    for exc in retry_exceptions:

        if not inspect.isclass(exc):
            raise TypeError(
                f"❌ {exc!r} is not a class."
            )

        if not issubclass(exc, Exception):
            raise TypeError(
                f"❌ {exc.__name__} must inherit from Exception."
            )


# ==========================================================
# EVENT RUNNER COMPONENTS
# ==========================================================

def event_record_exception(
    runner: EventRunner,
    exc: Exception,
) -> None:
    """
    Record an exception on the EventRunner.
    """

    runner.exception = exc
    runner.exc_type = type(exc)
    runner.traceback_obj = exc.__traceback__

    runner.traceback = "".join(
        tb.format_exception(
            type(exc),
            exc,
            exc.__traceback__,
        )
    )



# ==========================================================
# EVENT RUNNER COMPONENTS
# ==========================================================

def event_sleep(delay: float) -> None:
    """
    Pause execution before the next retry.
    """

    if delay <= 0:
        return

    time.sleep(delay)

# ==========================================================
# EVENT RUNNER COMPONENTS
# ==========================================================

def event_execute(
    runner: EventRunner,
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> None:
    """
    Execute a callable and store its result.
    """

    runner.attempts += 1

    runner.data = func(*args, **kwargs)


# ==========================================================
# EVENT RUNNER COMPONENTS
# ==========================================================

def event_retry(
    runner: EventRunner,
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    retries: int,
    retry_delay: float,
    retry_exceptions: tuple[type[Exception], ...],
) -> None:
    """
    Execute a callable with retry support.
    """

    for attempt in range(retries + 1):

        try:

            event_execute(
                runner,
                func,
                args,
                kwargs,
            )

            return

        except retry_exceptions as exc:

            event_record_exception(
                runner,
                exc,
            )

            if attempt == retries:
                return

            event_sleep(retry_delay)



"""
event_validate()
event_execute()
event_retry()
event_record_exception()
event_sleep()
event_finish()
"""
