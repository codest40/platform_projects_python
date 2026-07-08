from project.utils.decorators import trace
from project.utils.helpers import timestamp
from project.models.cpu import Cpu_Data as records
from project.analyzers.cpu.cpu import analyze_cpu_metrics
from project.utils.pipeline import pipeline_runner
from project.collectors.cpu.filter_compute import filter_cpu_state, compute_cpu_rates
import psutil

def get_cpu_model():
    with open("/proc/cpuinfo") as f:
        for line in f:
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    return "Unknown"


@trace("collect_cpu_metrics")
def collect_cpu_metrics():

    @trace("cpu_data")
    def cpu_info():

        cpu_times = psutil.cpu_times_percent(interval=0.5)
        cpu_stats = psutil.cpu_stats()
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
                f"CPU utilization is critically high "
                f"({usage_percent:.1f}% in use); workload performance may be affected."
            )
            comment = "Immediate attention Required"

        cpu_model = get_cpu_model()

        return records(

            # ==================================================
            # CPU Information
            # ==================================================

            cpu_model=cpu_model,
            physical_cores=psutil.cpu_count(logical=False),
            logical_cores=psutil.cpu_count(logical=True),

            # ==================================================
            # Utilization
            # ==================================================

            usage_percent=usage_percent,
            per_core_util=psutil.cpu_percent(interval=None, percpu=True),

            # ==================================================
            # CPU Time Breakdown
            # ==================================================

            user_percent=cpu_times.user,
            system_percent=cpu_times.system,
            idle_percent=cpu_times.idle,
            iowait_percent=getattr(cpu_times, "iowait", 0.0),

            steal_percent=getattr(cpu_times, "steal", 0.0),
            irq_percent=getattr(cpu_times, "irq", 0.0),
            softirq_percent=getattr(cpu_times, "softirq", 0.0),
            nice_percent=getattr(cpu_times, "nice", 0.0),

            # ==================================================
            # Scheduler
            # ==================================================

            context_switches=cpu_stats.ctx_switches,
            interrupts=cpu_stats.interrupts,
            soft_interrupts=cpu_stats.soft_interrupts,
            syscalls=getattr(cpu_stats, "syscalls", 0),

            # ==================================================
            # Frequency / Load
            # ==================================================

            frequency_mhz=freq.current if freq else 0.0,
            max_frequency_mhz=freq.max if freq else 0.0,
            min_frequency_mhz=freq.min if freq else 0.0,

            load_average=psutil.getloadavg(),

            # ==================================================
            # Summary
            # ==================================================

            severity=severity,
            summary=summary,
            comment=comment,
        )


    return cpu_info()



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
