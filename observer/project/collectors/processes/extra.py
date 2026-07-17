from pathlib import Path
from project.models.processes import ProcessCache

def build_cache(proc_dir: Path) -> ProcessCache:
    cache = ProcessCache()
    try:
        cache.stat = (proc_dir / "stat").read_text()
    except Exception:
        pass

    try:
      cache.status = (proc_dir / "status").read_text()
    except Exception:
        pass

    try:
        cache.cmdline = (proc_dir / "cmdline").read_bytes()
    except Exception:
      pass

    try:
        cache.cgroup = (proc_dir / "cgroup").read_text()
    except Exception:
        pass

    try:
        cache.io = (proc_dir / "io").read_text()
    except Exception:
        pass

    return cache


def separate_runtime_events(all_events, live_event_pids, provider_state):
    matched_events = {}
    ended_events = {}

    for pid, events in all_events.items():
        if pid in live_event_pids:
            matched_events[pid] = events
        else:
            ended_events[pid] = events

    for event in ended_events.values():
        event.is_event_available = provider_state["is_event_available"]
        event.did_loading_succeed = provider_state["did_loading_succeed"]
        event.did_read_succeed = provider_state["did_read_succeed"]


    return matched_events, ended_events
