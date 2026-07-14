from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessThreadAnalysis,
    ObserverState as OB,
)


def analyze_threads(
    process: ProcessSnapshot,
) -> ProcessThreadAnalysis:
    """
    Analyze process thread topology.
    Describes how a process participates in Linux thread,
    session and process-group hierarchy.
    """

    analysis = ProcessThreadAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    # ---------------------------------------------------------
    # Copy metrics
    # ---------------------------------------------------------

    analysis.thread_count = process.thread_count
    analysis.session = process.session
    analysis.process_group = process.process_group
    analysis.foreground_process_group = (
        process.foreground_process_group
    )

    analysis.state = process.state
    analysis.priority = process.priority
    analysis.nice = process.nice
    analysis.rt_priority = process.rt_priority
    analysis.runtime_seconds = process.runtime_seconds
    analysis.processor = process.processor

    analysis.running_threads = process.running_threads
    analysis.sleeping_threads = process.sleeping_threads
    analysis.blocked_threads = process.uninterruptible_threads
    analysis.zombie_threads = process.zombie_threads
    analysis.idle_threads = process.idle_threads

    # ---------------------------------------------------------
    # Thread count
    # ---------------------------------------------------------

    coverage.check(process.thread_count not in OB.values)

    if process.thread_count not in OB.values:

        multi = process.thread_count > 1

        analysis.signals["is_multithreaded"] = multi
        analysis.signals["is_single_threaded"] = not multi

        if multi:
            analysis.classifications.append(
                "multithreaded"
            )
        else:
            analysis.classifications.append(
                "single_threaded"
            )

        if process.thread_count > 500:
            analysis.recommendations.append(
                "Verify that the high thread count is expected."
            )

    else:
        analysis.signals["is_multithreaded"] = OB.NA
        analysis.signals["is_single_threaded"] = OB.NA

    # ---------------------------------------------------------
    # Thread group leader
    # ---------------------------------------------------------

    coverage.check(process.tid not in OB.values)

    if (
        process.pid not in OB.values
        and process.tid not in OB.values
    ):

        leader = process.pid == process.tid

        analysis.signals["is_thread_group_leader"] = leader
        analysis.signals["is_worker_thread"] = not leader

        if leader:
            analysis.classifications.append(
                "thread_group_leader"
            )
        else:
            analysis.classifications.append(
                "worker_thread"
            )

    else:
        analysis.signals["is_thread_group_leader"] = OB.NA
        analysis.signals["is_worker_thread"] = OB.NA

    # ---------------------------------------------------------
    # Session leader
    # ---------------------------------------------------------

    coverage.check(process.session not in OB.values)

    if process.session not in OB.values:

        leader = process.pid == process.session

        analysis.signals["is_session_leader"] = leader

        if leader:
            analysis.classifications.append(
                "session_leader"
            )

    else:
        analysis.signals["is_session_leader"] = OB.NA

    # ---------------------------------------------------------
    # Process group leader
    # ---------------------------------------------------------

    coverage.check(process.process_group not in OB.values)

    if process.process_group not in OB.values:

        leader = (
            process.pid == process.process_group
        )

        analysis.signals[
            "is_process_group_leader"
        ] = leader

        if leader:
            analysis.classifications.append(
                "process_group_leader"
            )

    else:
        analysis.signals[
            "is_process_group_leader"
        ] = OB.NA

    # ---------------------------------------------------------
    # Foreground / Background
    # ---------------------------------------------------------

    coverage.check(
        process.foreground_process_group
        not in OB.values
    )

    if (
        process.process_group not in OB.values
        and process.foreground_process_group
        not in OB.values
    ):

        foreground = (
            process.process_group
            == process.foreground_process_group
        )

        analysis.signals[
            "is_foreground_process_group"
        ] = foreground

        analysis.signals[
            "is_background_process_group"
        ] = not foreground

        if foreground:
            analysis.classifications.append(
                "foreground_process_group"
            )
        else:
            analysis.classifications.append(
                "background_process_group"
            )

    else:
        analysis.signals[
            "is_foreground_process_group"
        ] = OB.NA

        analysis.signals[
            "is_background_process_group"
        ] = OB.NA

    # ---------------------------------------------------------
    # Thread states
    # ---------------------------------------------------------

    thread_states = [
        (
            "running_threads",
            "has_running_threads",
            "running_threads",
        ),
        (
            "sleeping_threads",
            "has_sleeping_threads",
            "sleeping_threads",
        ),
        (
            "uninterruptible_threads",
            "has_blocked_threads",
            "blocked_threads",
        ),
        (
            "zombie_threads",
            "has_zombie_threads",
            "zombie_threads",
        ),
        (
            "idle_threads",
            "has_idle_threads",
            "idle_threads",
        ),
    ]

    for attr, signal, classification in thread_states:

        value = getattr(process, attr)

        coverage.check(value not in OB.values)

        if value not in OB.values:

            analysis.signals[signal] = value > 0

            if value > 0:
                analysis.classifications.append(
                    classification
                )

                if signal == "has_blocked_threads":
                    analysis.recommendations.append(
                        "Investigate blocked threads if they persist."
                    )

                if signal == "has_zombie_threads":
                    analysis.recommendations.append(
                        "Verify that terminated threads are being cleaned up."
                    )

        else:
            analysis.signals[signal] = OB.NA

    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------

    if process.thread_count not in OB.values:
        analysis.facts.append(
            f"Threads: {process.thread_count}"
        )

    if process.running_threads not in OB.values:
        analysis.facts.append(
            f"Running threads: {process.running_threads}"
        )

    if process.sleeping_threads not in OB.values:
        analysis.facts.append(
            f"Sleeping threads: {process.sleeping_threads}"
        )

    if process.uninterruptible_threads not in OB.values:
        analysis.facts.append(
            f"Blocked threads: {process.uninterruptible_threads}"
        )

    if process.idle_threads not in OB.values:
        analysis.facts.append(
            f"Idle threads: {process.idle_threads}"
        )

    if process.zombie_threads not in OB.values:
        analysis.facts.append(
            f"Zombie threads: {process.zombie_threads}"
        )

    if process.session not in OB.values:
        analysis.facts.append(
            f"Session: {process.session}"
        )

    if process.process_group not in OB.values:
        analysis.facts.append(
            f"Process group: {process.process_group}"
        )

    if process.foreground_process_group not in OB.values:
        analysis.facts.append(
            f"Foreground PG: {process.foreground_process_group}"
        )

    if process.processor not in OB.values:
        analysis.facts.append(
            f"Last CPU: {process.processor}"
        )

    if process.runtime_seconds not in OB.values:
        analysis.facts.append(
            f"Runtime: {process.runtime_seconds:.1f}s"
        )
    coverage.apply(process)
    return analysis
