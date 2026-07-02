from dataclasses import dataclass
import inspect
from project.logging.logger import emit, emit_span, emit_exception, emit_analysis
from project.utils.runner import TraceObserver, EventRunner
from project.utils.context import get_caller_context
import traceback as tb
from threading import Lock
from collections import defaultdict
from pathlib import Path
import fcntl
import sys

#================================================
# Compile and Run event
#==========================
# Process Lock
LOCK_DIR = Path("/tmp/observer-locks")
LOCK_DIR.mkdir(exist_ok=True)

def acquire_process_lock(resource: str):
    file = open(LOCK_DIR / f"{resource}.lock", "w")
    fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return file

# Thread Lock
LOCKS = {
    "cpu": Lock(),
    "memory": Lock(),
    "disk": Lock(),
    "network": Lock(),
    "alert": Lock(),
}

def compiler(resource, func, args=(), kwargs=None,):
    kwargs = kwargs or {}
    lock = LOCKS.get(resource)
    process_lock = None

    if lock is None:
        raise ValueError(f"[COMPILER] Unknown resource: {resource}.")
    if not lock.acquire(blocking=False):
        raise RuntimeError(f"[COMPILER] Another {resource} event is already running in this thread.") from None
    try:
        process_lock = acquire_process_lock(resource)
        caller = get_caller_context(inspect.unwrap(func))
        with TraceObserver(resource=resource):
                with EventRunner(resource=resource) as obj:
                    obj.run(
                        func,
                        *args,
                        **kwargs,
                    )

        return obj, caller
    except BlockingIOError:
        print(f"[COMPILER] [Errno 11 (LOCKED)]: Another {resource} process is already running")
        return None, None
    except Exception as e:
      print(f"[COMPILER] ERROR: {e}")

    finally:
      if process_lock is not None:
            fcntl.flock(process_lock, fcntl.LOCK_UN)
            process_lock.close()

      lock.release()

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

    obj, caller = compiler(resource, func)
    if obj is None:
      return

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



def run_analysis(
    *,
    func,
    result,
    success: dict | None = None,
    failure: dict | None = None,
):

    caller = get_caller_context(inspect.unwrap(func))

    try:
        analysis = func(result)

    except Exception:
        emit_exception(
            caller=caller,
            exc_info=sys.exc_info(),
            **(failure or {}),
        )
        return None

    emit_analysis(
        caller=caller,
        event=analysis,
        **(success or {}),
    )

    return analysis
