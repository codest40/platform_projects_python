
# Observer Runner Context
from dataclasses import dataclass
import inspect
from project.logging.logger import emit, emit_span, emit_exception
from project.utils.helpers import line, timestamp, start_count
from project.utils.context import get_caller_context, get_span_context
from typing import Any, Callable
import traceback as tb
from project.utils.traces import (
    start_trace,
    end_trace,
    push_span,
    pop_span,
)

VALID_STATUS = frozenset({"PENDING", "RUNNING", "SUCCESS", "FAILED",})
def get_status(status: str) -> str:
    if status not in VALID_STATUS:
        raise ValueError(f"Invalid status: {status}")
    return status

#==================================================
# Context manager to Run an event
#==============================================
@dataclass(slots=True)
class EventObserver:

    resource: str
    start: float = 0.0
    duration_ms: float = 0.0
    data: Any = None

    exc_type: type | None = None
    exception: Exception | None = None
    traceback: Any | None = None
    traceback_obj: Any | None = None

    status: str = get_status("PENDING")

    def __enter__(self):

        if not isinstance(self.resource, str):
            raise TypeError(f"❌ {self.resource} resource must be supplied as a string")

        self.start = start_count()
        print(line())
        print(f"Starting {self.resource} Event Observer...")
        self.status = get_status("RUNNING")

        return self

    def run(self, func: Callable[..., Any], *args, **kwargs):

        self.data = func(*args, **kwargs)

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
              tb.format_exception(exc_type, exc_value, traceback)
            )
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



#=======================================================
# Run Collection + Span and report status to collector files
#===================================================

def run_collection(
    *,
    resource: str,
    func,
    success: dict | None = None,
    failure: dict | None = None,
  ):

  caller = get_caller_context(inspect.unwrap(func))

  with TraceObserver(resource=resource):

    with EventObserver(resource=resource) as obj:
        obj.run(func)

    if obj.exception:

        emit_exception(
            caller=caller,
            category=obj.exc_type.__name__,
            cause=str(obj.exception),
            impact=obj.status,
            exc_info=(
                obj.exc_type,
                obj.exception,
                obj.traceback_obj,
            ),
            **(failure or {}),
        )

    else:
        emit(
            caller=caller,
            metadata=obj.data,
            severity = obj.data.severity,
            summary = obj.data.summary,
            comment = obj.data.comment,
            duration_ms=obj.duration_ms,
            impact=obj.status,
            **(success or {}),
        )

    return obj
