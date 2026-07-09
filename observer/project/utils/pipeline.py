from project.utils.helpers import get_status
from project.alerts.activate_alert import activate_run_alert
from project.utils.start_event import run_collection, run_analysis, save_state, load_states

#============================================
# Observer ID Error
#=============================
class ObserverError(Exception):
    """Raised when an unknown error occurs."""
    pass

#===========================================
# Pipeline runner
#=============================================
def pipeline_runner(resource, collect_func, analyze_func, filter_func, compute_func, extra_metadata=None, alert_title=None, message=None, severity=None):
    extra_metadata = extra_metadata or {}
    collect_success = extra_metadata.get("collect_success")
    collect_failure = extra_metadata.get("collect_failure")
    alert_title = extra_metadata.get("alert_title", alert_title)
    message = extra_metadata.get("alert_message", message)
    severity = extra_metadata.get("severity", severity)

    result = run_collection(resource=resource, func=collect_func,
      success=collect_success, failure=collect_failure,
    )

    if result is None:
        raise ValueError(f"❌ [PIPELINE RUNNER] {resource} ERROR: Emit() response returned: {result}")
    elif result.status == get_status("FAILED"):
        if alert_title is None:
          title=f"{resource} Metrics collection Alert"
        if message is None:
          message=f"❌ {resource} Metric Collection failed {result}"
        if severity is None:
          severity = "CRITICAL"
        print(f"❌ Collecting {resource} Metrics Failed")
        activate_run_alert(title=title, message=message, severity=severity,)
    elif result.status == get_status("SUCCESS"):
        print(f"✅ {resource} Metrics Collection Passed")
        if not result.collected_at:
            print(f"❌ {resource} collected Result Does Not have collected_at filed")
            return

        payload = filter_func(result)
        save_state(resource, payload)
        previous, current = load_states(resource)

        def create_sample():
            print("First sample Run.")
            time.sleep(5)
            result = run_collection()
            payload = filter_func(result)
            save_state(resource, payload)
            previous, current = load_states(resource)

        if current is None:
            create_sample()
        if previous is None:
            create_sample()

        result = compute_func(
                result.data,
                previous,
                payload,
                )
        save_state(resource, payload)

        res = run_analysis(resource=resource, func=analyze_func, result=result)
        if not res:
            print(f"❌ {resource} Analysis Failed")
        print(f"✅ {resource} Metrics Analysis Passed")
    else:
      raise ObserverError(f"❌ [PIPELINE RUNNER] Unknown ERROR: Emit() response returned: {result.status}")
