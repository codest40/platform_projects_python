from project.models.processes import (
    ProcessSnapshot,
    CollectorFailure,
    ProcessRuntimeEvents,
)

def collect_runtime_events(
    snapshot: ProcessSnapshot,
    all_events: dict[int, ProcessRuntimeEvents],
    provider_state,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process runtime events for a process.
    """
    if all_events is None:
        snapshot.runtime_collected_events = ProcessRuntimeEvents()
        return snapshot

    try:
      events = all_events.get(snapshot.pid)
      #if events is not None:
      #    print(f"MATCHED: snapshot.pid={snapshot.pid}")
      #else:
      #    print(f"MISSEd : snapshot.pid={snapshot.pid}")

      if events is None:
          events = ProcessRuntimeEvents()

      events.is_event_available = provider_state["is_event_available"]
      events.did_loading_succeed = provider_state["did_loading_succeed"]
      events.did_read_succeed = provider_state["did_read_succeed"]
      snapshot.runtime_collected_events = events

    except Exception as e:
        print("[RUNTIME EVENTS COLLECTOR] Collector failed:", e)
        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="runtime_events",
                field="runtime_events",
                reason=str(e),
            )
        )
    return snapshot
