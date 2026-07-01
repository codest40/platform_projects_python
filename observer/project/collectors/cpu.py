
from project.utils.decorators import trace
from project.utils.start_event import run_collection
from project.utils.helpers import (
    timestamp, start_count
    )
from project.models.cpu import Cpu_Data as records
import psutil
import platform

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

        cpu_model = platform.processor(),
        per_core_util = psutil.cpu_percent(interval=None, percpu=True),
        severity=severity,
        summary=summary,
        comment=comment,
    )


  print("Running [Starting Collection function] for CPU...")
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

