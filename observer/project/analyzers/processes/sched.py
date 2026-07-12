from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessSchedulerAnalysis,
)

SCHED_POLICY = {
    0: "other",
    1: "fifo",
    2: "rr",
    3: "batch",
    5: "idle",
    6: "deadline",
}


def analyze_scheduler(
    process: ProcessSnapshot,
) -> ProcessSchedulerAnalysis:
    """
    Analyze Linux scheduler behaviour for a process.
    """

    analysis = ProcessSchedulerAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    #
    # ---------------------------------------------------------
    # Scheduler State
    # ---------------------------------------------------------
    #

    coverage.check(process.state is not None)

    if process.state is not None:

        analysis.state = process.state

        STATE_CLASSIFICATIONS = {
            "R": "running",
            "S": "sleeping",
            "D": "uninterruptible_sleep",
            "T": "stopped",
            "t": "traced",
            "Z": "zombie",
            "X": "dead",
            "I": "idle",
        }

        classification = STATE_CLASSIFICATIONS.get(process.state)

        if classification:
            analysis.classifications.append(classification)

    #
    # ---------------------------------------------------------
    # Priority
    # ---------------------------------------------------------
    #

    coverage.check(process.priority is not None)

    if process.priority is not None:

        analysis.priority = process.priority

        if process.priority < 100:
            analysis.classifications.append("high_priority")
        else:
            analysis.classifications.append("normal_priority")

    #
    # ---------------------------------------------------------
    # Nice
    # ---------------------------------------------------------
    #

    coverage.check(process.nice is not None)

    if process.nice is not None:

        analysis.nice = process.nice

        if process.nice < 0:
            analysis.classifications.append("negative_nice")

    #
    # ---------------------------------------------------------
    # Real-time Priority
    # ---------------------------------------------------------
    #

    coverage.check(process.rt_priority is not None)

    if process.rt_priority is not None:

        analysis.rt_priority = process.rt_priority

        if process.rt_priority > 0:
            analysis.classifications.append("realtime")

    #
    # ---------------------------------------------------------
    # Scheduling Policy
    # ---------------------------------------------------------
    #

    coverage.check(process.policy is not None)

    if process.policy is not None:
        analysis.policy = process.policy
        scheduler_class = SCHED_POLICY.get(
            process.policy,
            "unknown",
        )
        analysis.scheduler_class = scheduler_class
        analysis.classifications.append(
            f"{scheduler_class}_scheduler"
        )

    #
    # ---------------------------------------------------------
    # Last CPU
    # ---------------------------------------------------------
    #

    coverage.check(process.processor is not None)

    if process.processor is not None:

        analysis.processor = process.processor

    #
    # ---------------------------------------------------------
    # Lifetime
    # ---------------------------------------------------------
    #

    coverage.check(process.runtime_seconds is not None)

    if process.runtime_seconds is not None:

        analysis.runtime_seconds = process.runtime_seconds

    coverage.check(process.start_time is not None)

    if process.start_time is not None:

        analysis.start_time = process.start_time

    #
    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------
    #
    if analysis.state is not None:
        analysis.facts.append(f"State: {analysis.state}")

    if analysis.priority is not None:
        analysis.facts.append(
            f"Priority: {analysis.priority}"
        )

    if analysis.nice is not None:
        analysis.facts.append(
            f"Nice: {analysis.nice}"
        )

    if analysis.rt_priority is not None:
        analysis.facts.append(
            f"RT priority: {analysis.rt_priority}"
        )

    if analysis.policy is not None:
      if analysis.policy:
        analysis.facts.append(
            f"Scheduling policy: {analysis.scheduler_class} {analysis.policy}"
        )

    if analysis.processor is not None:
        analysis.facts.append(
            f"Last CPU: {analysis.processor}"
        )

    if analysis.runtime_seconds is not None:
        analysis.facts.append(
            f"Runtime: {analysis.runtime_seconds:.1f}s"
        )
    if analysis.start_time is not None:
        analysis.facts.append(
            f"Started at: {analysis.start_time:.2f}s"
        )

    coverage.apply(process)
    return analysis
