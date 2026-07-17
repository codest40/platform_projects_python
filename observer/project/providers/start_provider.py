from project.models.processes import (ProcessRuntimeEvents)
import signal
from project.providers.kernel_events import EBPFProvider


def get_provider_runtime_events():
    """
    Collect process runtime events.
    Events comes from: eBPF or tracefs
    """
    runtime_events = ProcessRuntimeEvents()
    provider_state = {
          "is_event_available": False,
          "did_loading_succeed": None,
          "did_read_succeed": None,
    }

    try:
        ebpf_provider = EBPFProvider()
        #print("Provider created")
        #print("Available:", ebpf_provider.is_event_available)
        if not ebpf_provider.is_event_available:
            return runtime_events, provider_state

    except Exception as e:
        #print("EBPFProvider creation failed:", e)
        return runtime_events, provider_state

    process_events = {}
    try:
        #print("Calling read_process_events()")

        process_events = ebpf_provider.read_process_events()
        provider_state = {
          "is_event_available": ebpf_provider.is_event_available,
          "did_loading_succeed": ebpf_provider.did_loading_succeed,
          "did_read_succeed": ebpf_provider.did_read_succeed,
        }

        events = process_events
        #print("========== START_PROVIDER ==========")
        #print("Provider state:", provider_state)
        #print("Event PIDs:", list(process_events.keys()))
        #for pid, event in process_events.items():
        #    print(pid, event)
        #print("====================================")
    except Exception as e:
        print("Collector failed:", e)

    return events, provider_state
