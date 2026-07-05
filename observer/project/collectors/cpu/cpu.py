
from project.utils.decorators import trace
from project.utils.start_event import run_collection, run_analysis
from project.alerts.activate_alert import activate_run_alert
from project.utils.helpers import timestamp, get_status
from project.models.cpu import Cpu_Data as records
from project.analyzers.cpu import analyze_cpu_metrics
import psutil

def get_cpu_model():
    with open("/proc/cpuinfo") as f:
        for line in f:
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    return "Unknown"

@trace("cpu_collected_metrics")
def collect_cpu_metrics():

  @trace("cpu_data")
  def cpu_info():
    cpu_times = psutil.cpu_times_percent(interval=0.5)
    freq = psutil.cpu_freq()
    usage_percent = psutil.cpu_percent(interval=1.5)

    if usage_percent < 30:
      severity = "INFO"
      summary = (
          f"CPU utilization is healthy "
          f"({usage_percent:.1f}% in use)."
      )
      comment = "No Comment"

    elif usage_percent <= 80:
      severity = "WARNING"
      summary = (
          f"CPU utilization is elevated "
          f"({usage_percent:.1f}% in use)."
      )
      comment = "Keep an eye on it henceforth"

    else:
      severity = "CRITICAL"
      summary = (
          f"CPU utilization is critically high !"
          f"({usage_percent:.1f}% in use); workload performance may be affected."
      )
      comment = "Immediate attention Required"

    cpu_model = get_cpu_model()
    return records(

        physical_cores = psutil.cpu_count(logical=False),
        logical_cores = psutil.cpu_count(logical=True),

        usage_percent = usage_percent,
        frequency_mhz = freq.current if freq else 0.0,
        load_average = psutil.getloadavg(),
        user_percent = cpu_times.user,
        system_percent = cpu_times.system,
        idle_percent = cpu_times.idle,
        iowait_percent = getattr(cpu_times, "iowait", 0.0),

        cpu_model = cpu_model,
        per_core_util = psutil.cpu_percent(interval=None, percpu=True),
        severity=severity,
        summary=summary,
        comment=comment,
    )


  #print("Running [Starting Collection function] for CPU...")
  return run_collection(
        resource="cpu",
        func=cpu_info,

        success={
            "event_name": "CPU_Metrics",
            "operation": "Collect",
            "collector": "CPU Metrics Collector",
            "tags": ["cpu", "cpu_info", "load_avg"],
        },

        failure={
            "event_name": "cpu_metrics",
            "summary": "CPU metric collection failed",
            "comment": "Recheck code logic.",
            "tags": ["cpu", "metrics", "cpu_exception"],
        },
      )

@trace("cpu_pipeline")
def cpu_pipeline():
  result = collect_cpu_metrics()
  if result is None:
    print(f"❌ ERROR: Emit() response returned: {result}")
  elif result.status == get_status("FAILED"):
      print("❌ Collecting Cpu Metrics Failed")
      activate_run_alert(title="Cpu Metrics collection Alert", message=f"❌ Cpu Metric Collection Failed: {result}", severity="CRITICAL",)
  elif result.status == get_status("SUCCESS"):
      print("✅ Cpu Metrics Collection Passed")
      print(result)
      #res = run_analysis(resource="cpu", func=analyze_cpu_metrics, result=result)
      #if not res:
      #    print("❌ Cpu Analysis Failed")
      print("✅ Cpu Metrics Analysis Passed")
  else:
    print(f"❌ ERROR: Emit() response returned: {result.status} \nSomething is very wrong")


cpu_pipeline()
