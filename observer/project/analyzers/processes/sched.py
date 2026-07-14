from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessSchedulerAnalysis,
    ObserverState as OB,
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
    Analyze Linux scheduler behaviour.
    """
    analysis = ProcessSchedulerAnalysis(
        pid=process.pid,
        tid=process.tid,
    )


    coverage = Coverage()
    LONG_RUNNING = 3600

    # ---------------------------------------------------------
    # Copy values
    # ---------------------------------------------------------

    analysis.state = process.state
    analysis.priority = process.priority
    analysis.nice = process.nice
    analysis.rt_priority = process.rt_priority
    analysis.policy = process.policy
    analysis.processor = process.processor
    analysis.runtime_seconds = process.runtime_seconds
    analysis.start_time = process.start_time


    # ---------------------------------------------------------
    # Scheduler State
    # ---------------------------------------------------------

    coverage.check(
        process.state not in OB.values
    )
    if process.state not in OB.values:
        states = {

            "R": (
                "is_running",
                "running",
            ),

            "S": (
                "is_sleeping",
                "sleeping",
            ),

            "D": (
                "is_waiting_on_io",
                "uninterruptible_sleep",
            ),

            "T": (
                "is_stopped",
                "stopped",
            ),

            "Z": (
                "is_zombie",
                "zombie",
            ),

        }

        item = states.get(
            process.state
        )


        if item:
            signal, classification = item

            analysis.signals[signal] = True

            analysis.classifications.append(
                classification
            )
        else:
            analysis.classifications.append(
                "unknown_state"
            )


    else:
        for signal in [
            "is_running",
            "is_sleeping",
            "is_waiting_on_io",
            "is_stopped",
            "is_zombie",
        ]:

            analysis.signals[signal] = OB.NA



    # ---------------------------------------------------------
    # Priority
    # ---------------------------------------------------------

    coverage.check(
        process.priority not in OB.values
    )

    if process.priority not in OB.values:
        high = (
            process.priority < 100
        )


        analysis.signals[
            "has_high_priority"
        ] = high


        if high:

            analysis.classifications.append(
                "high_priority"
            )


    else:

        analysis.signals[
            "has_high_priority"
        ] = OB.NA



    # ---------------------------------------------------------
    # Nice
    # ---------------------------------------------------------

    coverage.check(
        process.nice not in OB.values
    )


    if process.nice not in OB.values:


        negative = (
            process.nice < 0
        )


        analysis.signals[
            "has_negative_nice"
        ] = negative


        if negative:

            analysis.classifications.append(
                "negative_nice"
            )


    else:

        analysis.signals[
            "has_negative_nice"
        ] = OB.NA



    # ---------------------------------------------------------
    # Real-time scheduling
    # ---------------------------------------------------------

    if process.rt_priority not in OB.values:


        realtime = (
            process.rt_priority > 0
        )


        analysis.signals[
            "is_realtime_process"
        ] = realtime


        if realtime:

            analysis.classifications.append(
                "realtime_process"
            )

            analysis.recommendations.append(
                "Verify that real-time scheduling is intentional."
            )


    else:

        analysis.signals[
            "is_realtime_process"
        ] = OB.NA



    # ---------------------------------------------------------
    # Scheduling Policy
    # ---------------------------------------------------------

    if process.policy not in OB.values:

        scheduler = SCHED_POLICY.get(
            process.policy,
            "unknown",
        )


        analysis.scheduler_class = scheduler


        policy_signal = {

            "fifo":
                "uses_fifo_scheduler",

            "rr":
                "uses_round_robin_scheduler",

            "deadline":
                "uses_deadline_scheduler",

        }.get(
            scheduler
        )


        if policy_signal:

            analysis.signals[
                policy_signal
            ] = True


            analysis.classifications.append(
                scheduler + "_scheduler"
            )


    # ---------------------------------------------------------
    # Long Running
    # ---------------------------------------------------------

    if process.runtime_seconds not in OB.values:


        long_running = (
            process.runtime_seconds >= LONG_RUNNING
        )


        analysis.signals[
            "is_long_running"
        ] = long_running


        if long_running:

            analysis.classifications.append(
                "long_running"
            )


    else:

        analysis.signals[
            "is_long_running"
        ] = OB.NA



    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------

    if process.state:

        analysis.facts.append(
            f"State: {process.state}"
        )


    if process.priority:

        analysis.facts.append(
            f"Priority: {process.priority}"
        )


    if process.nice is not None:

        analysis.facts.append(
            f"Nice: {process.nice}"
        )


    if process.rt_priority is not None:

        analysis.facts.append(
            f"RT priority: {process.rt_priority}"
        )


    if process.policy is not None:

        analysis.facts.append(
            f"Scheduling policy: {analysis.scheduler_class}"
        )


    if process.processor is not None:

        analysis.facts.append(
            f"Last CPU: {process.processor}"
        )


    if process.runtime_seconds is not None:

        analysis.facts.append(
            f"Runtime: {process.runtime_seconds:.1f}s"
        )

    coverage.apply(process)
    return analysis
