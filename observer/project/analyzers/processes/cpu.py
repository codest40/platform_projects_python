from __future__ import annotations

from project.models.processes import (
    ProcessSnapshot,
    ProcessCpuAnalysis,
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
    #
    # ---------------------------------------------------------
    # CPU Activity
    # ---------------------------------------------------------
    #

    total_rate = 0.0

    coverage.check(process.user_ticks_per_sec is not None)
    if process.user_ticks_per_sec is not None:
        total_rate += process.user_ticks_per_sec

    coverage.check(process.system_ticks_per_sec is not None)
    if process.system_ticks_per_sec is not None:
        total_rate += process.system_ticks_per_sec

    analysis.cpu_ticks_per_sec = total_rate

    if total_rate > 0:
        analysis.classifications.append("cpu_active")
    else:
        analysis.classifications.append("cpu_idle")

    #
    # ---------------------------------------------------------
    # User vs Kernel CPU
    # ---------------------------------------------------------
    #
    if (
        process.user_ticks_per_sec is not None
        and process.system_ticks_per_sec is not None
    ):
      user = process.user_ticks_per_sec or 0
      system = process.system_ticks_per_sec or 0

      if user > system:
        analysis.cpu_type = "user_cpu"

      elif system > user:
        analysis.cpu_type = "kernel_cpu"

      else:
        analysis.cpu_type = "balanced"

    #
    # ---------------------------------------------------------
    # Scheduler State
    # ---------------------------------------------------------
    #
    coverage.check(process.state is not None)
    if process.state == "R":
        analysis.classifications.append("running")

    elif process.state == "S":
        analysis.classifications.append("sleeping")

    elif process.state == "D":
        analysis.classifications.append("uninterruptible_sleep")

    elif process.state == "T":
        analysis.classifications.append("stopped")

    elif process.state == "Z":
        analysis.classifications.append("zombie")

    #
    # ---------------------------------------------------------
    # CPU Affinity Observation
    # ---------------------------------------------------------
    #

    coverage.check(process.processor is not None)
    if process.processor is not None:

        analysis.last_processor = process.processor

        analysis.facts.append(
            f"Last executed on CPU {process.processor}"
        )

    #
    # ---------------------------------------------------------
    # Priority
    # ---------------------------------------------------------
    #
    coverage.check(process.priority is not None)
    if process.priority is not None:

        analysis.priority = process.priority

        if process.priority < 100:
            analysis.classifications.append(
                "high_priority"
            )

    coverage.check(process.nice is not None)
    if process.nice is not None:

        analysis.nice = process.nice

        if process.nice < 0:
            analysis.classifications.append(
                "negative_nice"
            )

    #
    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------
    #
    coverage.check(process.runtime_seconds is not None)
    if process.runtime_seconds is not None:

        analysis.runtime_seconds = process.runtime_seconds

    #
    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------
    #

    if process.user_ticks_per_sec is not None:

        analysis.facts.append(
            f"User CPU: {process.user_ticks_per_sec:.2f} ticks/sec"
        )

    if process.system_ticks_per_sec is not None:

        analysis.facts.append(
            f"Kernel CPU: {process.system_ticks_per_sec:.2f} ticks/sec"
        )

    if process.state:

        analysis.facts.append(
            f"Scheduler state: {process.state}"
        )

    coverage.apply(process)

    return analysis
