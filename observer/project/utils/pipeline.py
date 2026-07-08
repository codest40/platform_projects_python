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
def pipeline_runner(resource, collect_func, analyze_func, filter_func, compute_func, extra_metadata, alert_title=None, message=None, severity=None):
  result = run_collection(resource=resource, func=collect_func)
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
      #print(result)
      if not result.collected_at:
          print("❌ {resource} collected Result Does Not have collected_at filed")
          return

      payload = filter_func(result)
      save_state(resource, payload)
      previous, current = load_states(resource)
      if current is None:
          print("First sample.")
          time.sleep(5)
          result = run_collection()
          payload = filter_func(result)
          save_state(resource, payload)
          previous, current = load_states(resource)

      result = compute_func(
              result.data,
              previous,
              payload,
          )
      save_state(resource, payload)

      res = run_analysis(resource=resource, func=analyze_func, result=result)
      if not res:
          print(f"❌ {resource} Analysis Failed")
      print("✅ {resource} Metrics Analysis Passed")
  else:
    raise ObserverError(f"❌ [PIPELINE RUNNER] Unknown ERROR: Emit() response returned: {result.status}")
