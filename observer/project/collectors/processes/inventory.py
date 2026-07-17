from pathlib import Path
from project.models.processes import (
    ProcessInventory,
    ProcessSnapshot,
    InaccessibleProcess,
    CollectorFailure,
    ProcessCache,
)
from project.providers.start_provider import get_provider_runtime_events
from project.collectors.processes.extra import build_cache, separate_runtime_events
from project.collectors.processes.identity import collect_identity
from project.collectors.processes.scheduler import collect_scheduler
from project.collectors.processes.owner import collect_owner
from project.collectors.processes.memory import collect_memory
from project.collectors.processes.cpu import collect_cpu
from project.collectors.processes.lifecycle import collect_lifecycle
from project.collectors.processes.cgroup import collect_cgroup
from project.collectors.processes.context_switch import collect_context_switches
from project.collectors.processes.io import collect_io
from project.collectors.processes.fd import collect_fd
from project.collectors.processes.limit import collect_limits
from project.collectors.processes.wait_channel import collect_wait_channel
from project.collectors.processes.threads import collect_threads
from project.collectors.processes.runtime_events import collect_runtime_events
from project.collectors.processes.filter_compute import (
    filter_process_state, compute_process_rates,
  )
from project.analyzers.processes.ps import analyze_process_metrics
from project.utils.pipeline import pipeline_runner
from project.utils.helpers import timestamp
from project.utils.decorators import trace



PROC = Path("/proc")

@trace("process_inventory")
def collect_process_inventory() -> ProcessInventory:
    """
    Build a lightweight inventory of all running processes.
    This is the only module responsible for walking /proc.
    All snapshot collectors populate a shared ProcessSnapshot.
    """

    inventory = ProcessInventory()
    proc_entries = [
        entry for entry in PROC.iterdir() if entry.name.isdigit()
    ]

    runtime_events, provider_state = get_provider_runtime_events()

    live_pids = set()
    live_pids = { int(entry.name) for entry in proc_entries}
    matched_events, ended_events = separate_runtime_events(
       runtime_events, live_pids, provider_state
    )
    runtime_events = matched_events
    inventory.ended_process_events = ended_events
    inventory.live_process_events = runtime_events

    with open("/proc/uptime") as f:
        uptime_seconds = float(f.readline().split()[0])

    for entry in proc_entries:

        if not entry.name.isdigit():
            continue
        inventory.total_processes += 1
        inventory.collected_total += 1

        pid = int(entry.name)
        proc_dir = entry
        cache = build_cache(proc_dir)

        snapshot = ProcessSnapshot(pid=pid, tid=pid,)

        try:

            snapshot = collect_identity(snapshot, proc_dir, cache, inventory.collector_failures,)
            snapshot = collect_scheduler(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_owner(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_memory(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_cpu(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_lifecycle(
                snapshot,
                cache,
                uptime_seconds,
                inventory.collector_failures,
            )
            snapshot = collect_cgroup(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_fd(
                snapshot,
                proc_dir,
                inventory.collector_failures,
            )
            snapshot = collect_io(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_context_switches(snapshot, cache, inventory.collector_failures,)
            snapshot = collect_limits(snapshot, proc_dir, inventory.collector_failures,)
            snapshot = collect_wait_channel(snapshot, proc_dir, inventory.collector_failures,)
            snapshot = collect_threads(snapshot, proc_dir, inventory.collector_failures,)
            snapshot = collect_runtime_events(snapshot, runtime_events, provider_state, inventory.collector_failures,)

            inventory.accessible_processes += 1
            inventory.collected_successful += 1
            inventory.processes.append(snapshot)
        except (ProcessLookupError, FileNotFoundError) as both:

            # Process exited while collecting.
            if isinstance(both, ProcessLookupError):
                  reason="process exited during collection",
            else:
                  reason="process File Not Found"

            inventory.inaccessible_processes.append(
                    InaccessibleProcess(
                      pid=pid,
                      reason=reason,
                    )
            )

            continue

        except Exception as e:

            snapshot.collection_errors.append(
                f"[PS inventory]: {e}"
            )

            inventory.inaccessible_processes.append(
                InaccessibleProcess(
                    pid=pid,
                    reason=str(e),
                )
            )
    return inventory

@trace("start_process_run")
def start_process_collection():
  result = pipeline_runner(
      resource="process",
      collect_func=collect_process_inventory,
      analyze_func=analyze_process_metrics,
      filter_func=filter_process_state,
      compute_func=compute_process_rates,
  )

  if result.resource.lower() == "process":
    print("FROM INVENTORY: Returned Result ID is correct")
    inventory = result.data
    print(f"Missed events: {inventory.runtime_orphaned_events}")
  else:
    print("Wrong Id for Process Event")
  return result

@trace("process_pipeline")
def process_pipeline():
    return start_process_collection()


process_pipeline()

