from __future__ import annotations
from project.models.processes import (
    ProcessSnapshot,
    ProcessCpuAnalysis,
    ObserverState as OB,
)
from project.analyzers.utils.coverage import Coverage

def analyze_cpu(
    process: ProcessSnapshot,
) -> ProcessCpuAnalysis:
    """
    Analyze CPU behaviour for a single process.
    """
    analysis = ProcessCpuAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()
    HIGH_CPU = 85.0
    IDLE_CPU = 5.0
    LONG_RUNNING = 3600.0

    coverage.check(process.cpu_percent not in OB.values)
    coverage.check(process.state not in OB.values)
    coverage.check(process.priority not in OB.values)
    coverage.check(process.nice not in OB.values)
    coverage.check(process.policy not in OB.values)
    coverage.check(process.runtime_seconds not in OB.values)
    coverage.check(process.max_cpu_time_soft not in OB.values)
    coverage.check(process.runtime_seconds not in OB.values)
    coverage.check(process.user_cpu_percent not in OB.values)
    coverage.check(process.system_cpu_percent not in OB.values)
    coverage.check(process.user_ticks_per_sec not in OB.values)
    coverage.check(process.system_ticks_per_sec not in OB.values)
    coverage.check(process.cpu_ticks_per_sec not in OB.values)
    coverage.check(process.processor not in OB.values)


    analysis.cpu_percent = process.cpu_percent
    analysis.user_cpu_percent = process.user_cpu_percent
    analysis.system_cpu_percent = process.system_cpu_percent
    analysis.user_ticks_per_sec = process.user_ticks_per_sec
    analysis.system_ticks_per_sec = process.system_ticks_per_sec
    analysis.cpu_ticks_per_sec = process.cpu_ticks_per_sec

    analysis.priority = process.priority
    analysis.nice = process.nice
    analysis.runtime_seconds = process.runtime_seconds


    if process.cpu_percent not in OB.values:
        high_cpu = process.cpu_percent >= HIGH_CPU
        analysis.signals["is_cpu_high"] = high_cpu
        if high_cpu:
            analysis.classifications.append("high_cpu_usage")
            analysis.recommendations.append(
              "Monitor or profile the process if high CPU usage is sustained."
            )
        else:
          analysis.classifications.append("normal_cpu_usage")
    else:
        analysis.signals["is_cpu_high"] = OB.NA
        analysis.classifications.append("cpu_usage_unknown")

    if process.cpu_percent not in OB.values:
        idle_cpu = process.cpu_percent <= IDLE_CPU
        analysis.signals["is_cpu_idle"] = idle_cpu
        if idle_cpu:
            analysis.classifications.append("cpu_idle")
        else:
            analysis.classifications.append("cpu_active")
    else:
        analysis.signals["is_cpu_idle"] = OB.NA

    if process.state not in OB.values:
        running = process.state == "R"
        analysis.signals["is_cpu_running"] = running
        if running:
            analysis.classifications.append("cpu_is_running")
        else:
            analysis.classifications.append("cpu_not_running")
    else:
        analysis.signals["is_cpu_running"] = OB.NA

    if (
        analysis.signals["is_cpu_high"] is not OB.NA
        and analysis.signals["is_cpu_running"] is not OB.NA
    ):
        cpu_bound = (
            analysis.signals["is_cpu_high"]
            and analysis.signals["is_cpu_running"]
        )
        analysis.signals["is_cpu_bound"] = cpu_bound
        if cpu_bound:
            analysis.classifications.append("cpu_bound")
            analysis.recommendations.append(
                "Profile the process if sustained."
            )
        else:
            analysis.classifications.append("not_cpu_bound")
    else:
        analysis.signals["is_cpu_bound"] = OB.NA

    if process.nice not in OB.values:
        high_priority = process.nice < 0
        analysis.signals["is_high_priority"] = high_priority
        if high_priority:
            analysis.classifications.append("high_priority")
    else:
        analysis.signals["is_high_priority"] = OB.NA

    if process.policy not in OB.values:
        realtime = process.policy in (1, 2, 6)
        analysis.signals["is_realtime_process"] = realtime
        if realtime:
            analysis.classifications.append("realtime_process")
            analysis.recommendations.append(
              "Verify that real-time scheduling is intentional."
            )
    else:
        analysis.signals["is_realtime_process"] = OB.NA

    if (
      process.runtime_seconds not in OB.values
      and isinstance(process.max_cpu_time_soft, (int, float))
    ):
        reached = (
            process.runtime_seconds >= process.max_cpu_time_soft
        )
        analysis.signals["is_cpu_time_limit_reached"] = reached
        if reached:
            analysis.classifications.append("cpu_time_limit_reached")
            analysis.recommendations.append(
                "Review the configured CPU time limit."
            )
    else:
        analysis.signals["is_cpu_time_limit_reached"] = OB.NA

    if process.runtime_seconds not in OB.values:
        analysis.runtime_seconds = process.runtime_seconds
        is_long_running = (
            process.runtime_seconds >= LONG_RUNNING
        )
        analysis.signals["is_long_running"] = is_long_running
        if is_long_running:
            analysis.classifications.append("long_running")
            analysis.recommendations.append(
                "Verify that prolonged execution is expected."
            )
        else:
            analysis.classifications.append("short_running")
    else:
        analysis.signals["is_long_running"] = OB.NA
        analysis.classifications.append("runtime_unknown")

    if (
      process.user_cpu_percent not in OB.values
      and process.system_cpu_percent not in OB.values
    ):
        analysis.user_cpu_percent = process.user_cpu_percent
        user_cpu_heavy = (
            process.user_cpu_percent > process.system_cpu_percent
        )
        analysis.signals["is_user_cpu_heavy"] = user_cpu_heavy
        if user_cpu_heavy:
            analysis.classifications.append("user_cpu_heavy")
    else:
        analysis.signals["is_user_cpu_heavy"] = OB.NA

    if (
        process.user_cpu_percent not in OB.values
        and process.system_cpu_percent not in OB.values
    ):
        analysis.system_cpu_percent = process.system_cpu_percent
        kernel_cpu_heavy = (
            process.system_cpu_percent > process.user_cpu_percent
        )
        analysis.signals["is_kernel_cpu_heavy"] = kernel_cpu_heavy
        if kernel_cpu_heavy:
            analysis.classifications.append("kernel_cpu_heavy")
            analysis.recommendations.append(
                "Investigate heavy kernel activity if unexpected."
            )
    else:
        analysis.signals["is_kernel_cpu_heavy"] = OB.NA

    if (
        process.user_ticks_per_sec not in OB.values
        and process.system_ticks_per_sec not in OB.values
    ):
        if process.user_ticks_per_sec > process.system_ticks_per_sec:
            analysis.cpu_type = "user_cpu"
        elif process.system_ticks_per_sec > process.user_ticks_per_sec:
            analysis.cpu_type = "kernel_cpu"
        else:
            analysis.cpu_type = "balanced"

    # Facts
    if process.cpu_percent not in OB.values:
        analysis.facts.append(
          f"CPU utilization is {process.cpu_percent:.1f}%."
        )
    if process.state not in OB.values:
        analysis.facts.append(
          f"Scheduler state is '{process.state}'."
        )
    if process.nice not in OB.values:
        analysis.facts.append(
          f"Nice value is {process.nice}."
        )
    if process.priority not in OB.values:
        analysis.facts.append(
          f"Scheduler priority is {process.priority}."
        )
    if process.policy not in OB.values:
        analysis.facts.append(
            f"Scheduling policy is {process.policy}."
        )
    if process.runtime_seconds not in OB.values:
        analysis.facts.append(
          f"Process runtime is {process.runtime_seconds:.1f} seconds."
        )
    if process.user_cpu_percent not in OB.values:
        analysis.facts.append(
          f"User CPU utilization is {process.user_cpu_percent:.1f}%."
        )

    if process.system_cpu_percent not in OB.values:
        analysis.facts.append(
          f"Kernel CPU utilization is {process.system_cpu_percent:.1f}%."
        )

    if process.system_ticks_per_sec not in OB.values:
        analysis.facts.append(
          f"Kernel CPU ticks/sec is {process.system_ticks_per_sec:.1f}%."
        )
    if process.user_ticks_per_sec not in OB.values:
        analysis.facts.append(
          f"User CPU ticks/sec is {process.user_ticks_per_sec:.1f}%."
        )
    if process.processor not in OB.values:
        analysis.last_processor = process.processor
        analysis.facts.append(
            f"Last executed on logical CPU {process.processor}."
        )

    coverage.apply(process)
    return analysis
