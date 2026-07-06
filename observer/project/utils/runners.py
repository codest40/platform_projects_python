
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
    collected_at: float = 0.0
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
                self.collected_at = timestamp(unix=True)
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



