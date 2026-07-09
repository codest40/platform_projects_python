from __future__ import annotations
from project.utils.decorators import trace
from project.models.cpu import CpuData
from project.analyzers.cpu.cpu import analyze_cpu_metrics
from project.collectors.cpu.psutil import collect_psutil
from project.collectors.cpu.proc import collect_proc
from project.collectors.cpu.pressure import collect_pressure
from project.collectors.cpu.cgroup import collect_cgroup
from project.collectors.cpu.sched import collect_sched
from project.collectors.cpu.filter_compute import (
    filter_cpu_state,
    compute_cpu_rates,
)
from project.utils.pipeline import pipeline_runner
from project.utils.helpers import timestamp

@trace("collect_cpu_metrics")
def collect_cpu_metrics() -> CpuData:

    @trace("cpu_data")
    def cpu_info(cpu_model) -> CpuData:

        cpu = cpu_model()

        collect_psutil(cpu)
        collect_proc(cpu)
        collect_pressure(cpu)
        collect_cgroup(cpu)
        collect_sched(cpu)
        cpu.collected_at = timestamp()

        if cpu.usage_percent is None:
            severity = "INFO"
            summary = "CPU utilization unavailable."
            comment = "Collector could not determine CPU usage."

        elif cpu.usage_percent < 40:
            severity = "INFO"
            summary = (
                f"CPU utilization is healthy "
                f"({cpu.usage_percent:.1f}% in use)."
            )
            comment = "No further Comment"

        elif cpu.usage_percent <= 75:
            severity = "WARNING"
            summary = (
                f"CPU utilization is elevated "
                f"({cpu.usage_percent:.1f}% in use)."
            )
            comment = "Keep an eye on it henceforth"

        else:
            severity = "CRITICAL"
            summary = (
                f"CPU utilization is critically high "
                f"({cpu.usage_percent:.1f}% in use); workload performance may be affected."
            )
            comment = "Immediate attention Required"

        cpu.severity=severity
        cpu.summary=summary
        cpu.comment=comment
        return cpu

    return cpu_info(CpuData)



success={
            "event_name": "CPU_Metrics",
            "operation": "Collect",
            "collector": "CPU Metrics Collector",
            "tags": ["cpu", "cpu_info", "load_avg"],
}

failure={
            "event_name": "cpu_metrics",
            "summary": "CPU metric collection failed",
            "comment": "Recheck code logic.",
            "tags": ["cpu", "metrics", "cpu_exception"],
}


@trace("start_cpu_run")
def start_cpu_collection():
  result = pipeline_runner(
      resource="cpu",
      collect_func=collect_cpu_metrics,
      analyze_func=analyze_cpu_metrics,
      filter_func=filter_cpu_state,
      compute_func=compute_cpu_rates,
      extra_metadata={"collect_success": success, "collect_failure": failure},
  )

  return result

@trace("cpu_pipeline")
def cpu_pipeline():
    start_cpu_collection()

cpu_pipeline()
