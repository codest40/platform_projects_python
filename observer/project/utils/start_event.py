from dataclasses import dataclass, asdict, is_dataclass
from typing import Any
import inspect
from project.logging.logger import emit, emit_span, emit_exception, emit_analysis
from project.utils.runners import TraceObserver, EventRunner
from project.utils.adapters import adapt_event_model, adapt_analysis_model
from project.utils.context import get_caller_context
from project.utils.helpers import start_count
import traceback as tb
from threading import Lock
from collections import defaultdict
from pathlib import Path
import fcntl
import sys
import json

#================================================
# Compile and Run event
#==========================
# Process Lock
LOCK_DIR = Path("/tmp/observer-locks")
LOCK_DIR.mkdir(exist_ok=True)
this_script = sys.argv[0]

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
    "process": Lock(),
    "alert": Lock(),
}

def compiler(resource, func, args=(), kwargs=None,):
    kwargs = kwargs or {}
    lock = LOCKS.get(resource)
    process_lock = None

    if lock is None:
        raise ValueError(f"[COMPILER] Unknown resource: {resource} \n"
                     f"Reason: '{resource}' is NOT Found inside the Custom Resource Lock List defined in file \n"
                     f"File: {this_script} \n"
                     f"Suggsetion: Open the file and add '{resource}' to the dict or use a valid resource name already inside the dict.")
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
        print(f"❌ [COMPILER] [Errno 11 (LOCKED)]: Another {resource} process is already running")
        return None, None
    except Exception as e:
      print(f"❌ [COMPILER] ERROR: {e}")

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
        overrides=failure
    else:
        overrides=success

    payload = adapt_event_model(
          resource=resource,
          result=obj,
          overrides=overrides,
        )

    if obj.exception:
        emit_exception(
            caller=caller,
            exc_info=(
                obj.exc_type,
                obj.exception,
                obj.traceback_obj,
            ),
            **payload,
        )
    else:
        emit(
            caller=caller,
            **payload,
        )

    return obj



#=======================================================
# Run Analysis and log
#===================================================
def run_analysis(
    *,
    func,
    result,
    resource: str,
    success: dict | None = None,
    failure: dict | None = None,
    **kwargs,
):

    caller = get_caller_context(inspect.unwrap(func))
    start = start_count()

    try:
        analysis = func(result=result, **kwargs)
        duration_ms = start_count() - start

    except Exception:
        duration_ms = start_count() - start
        emit_exception(
            caller=caller,
            exc_info=sys.exc_info(),
            duration_ms = duration_ms
            **(failure or {}),
        )
        return None

    payload = adapt_analysis_model(
        resource=resource,
        analysis=analysis,
        overrides={
            **(success or {}),
            "duration_ms": duration_ms,
            },
    )

    emit_analysis(
        caller=caller,
        **payload,
    )

    return analysis


#==============================================================
# Save and Load Comparison data
#===========================================================
STATE_DIR = Path("project/state")

def save_state(resource: str, data: Any) -> None:

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    previous = STATE_DIR / f"{resource}_previous.json"
    current = STATE_DIR / f"{resource}_current.json"

    if is_dataclass(data):
      payload = asdict(data)
    elif isinstance(data, dict):
      payload = data
    else:
      raise TypeError("❌ save_state() expects a dataclass or dictionary.")


    if current.exists():
        previous.write_text(current.read_text())
    current.write_text(json.dumps(payload, indent=4))




#================================================
STATE_DIR = Path("project/state")

def load_states(resource: str) -> tuple[dict | None, dict | None]:
    """
    Load previous and current snapshots.
    Returns:
        (previous, current)
    """

    previous_file = STATE_DIR / f"{resource}_previous.json"
    current_file = STATE_DIR / f"{resource}_current.json"

    previous = None
    current = None

    if previous_file.exists():
        previous = json.loads(previous_file.read_text())

    if current_file.exists():
        current = json.loads(current_file.read_text())

    return previous, current


