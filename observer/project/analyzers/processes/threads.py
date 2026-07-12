from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessThreadAnalysis,
)


def analyze_threads(
    process: ProcessSnapshot,
) -> ProcessThreadAnalysis:
    """
    Analyze process thread topology and execution model.
    It simply describes how this process participates
    in Linux thread, session and process-group hierarchy.
    """

    analysis = ProcessThreadAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    #
    # ---------------------------------------------------------
    # Thread count
    # ---------------------------------------------------------
    #

    coverage.check(process.thread_count is not None)

    if process.thread_count is not None:

        analysis.thread_count = process.thread_count

        if process.thread_count > 1:
            analysis.classifications.append(
                "multi_threaded"
            )
        else:
            analysis.classifications.append(
                "single_threaded"
            )

        analysis.facts.append(
            f"Threads: {process.thread_count}"
        )

    #
    # ---------------------------------------------------------
    # Thread-group leader
    # ---------------------------------------------------------
    #

    coverage.check(process.tid is not None)

    if (
        process.pid is not None and
        process.tid is not None
    ):

        if process.pid == process.tid:

            analysis.classifications.append(
                "thread_group_leader"
            )
            analysis.facts.append(
                "Thread-group leader"
            )

        else:

            analysis.classifications.append(
                "worker_thread"
            )

            analysis.facts.append(
                "Worker Thread group"
            )
    # ---------------------------------------------------------
    # Session leader
    # ---------------------------------------------------------

    coverage.check(process.session is not None)

    if process.session is not None:

        analysis.session = process.session

        if process.pid == process.session:

            analysis.classifications.append(
                "session_leader"
            )

        analysis.facts.append(
            f"Session: {process.session}"
        )

    # ---------------------------------------------------------
    # Process group
    # ---------------------------------------------------------

    coverage.check(process.process_group is not None)
    if process.process_group is not None:

        analysis.process_group = (
            process.process_group
        )

        if process.pid == process.process_group:

            analysis.classifications.append(
                "process_group_leader"
            )

        analysis.facts.append(
            f"Process group: "
            f"{process.process_group}"
        )

    #
    # ---------------------------------------------------------
    # Foreground process group
    # ---------------------------------------------------------
    #

    coverage.check(
        process.foreground_process_group is not None
    )

    if process.foreground_process_group is not None:

        analysis.foreground_process_group = (
            process.foreground_process_group
        )

        if (
            process.process_group ==
            process.foreground_process_group
        ):

            analysis.classifications.append(
                "foreground_process_group"
            )

        else:

            analysis.classifications.append(
                "background_process_group"
            )

        analysis.facts.append(
            f"Foreground PG: "
            f"{process.foreground_process_group}"
        )

    #
    # ---------------------------------------------------------
    # Scheduler state
    # ---------------------------------------------------------
    #

    coverage.check(process.state is not None)

    if process.state is not None:

        analysis.state = process.state

        analysis.facts.append(
            f"State: {process.state}"
        )

    #
    # ---------------------------------------------------------
    # Priority
    # ---------------------------------------------------------
    #

    coverage.check(process.priority is not None)

    if process.priority is not None:

        analysis.priority = process.priority

    coverage.check(process.nice is not None)

    if process.nice is not None:

        analysis.nice = process.nice

    coverage.check(process.rt_priority is not None)

    if process.rt_priority is not None:

        analysis.rt_priority = (
            process.rt_priority
        )

    #
    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------
    #

    coverage.check(
        process.runtime_seconds is not None
    )

    if process.runtime_seconds is not None:

        analysis.runtime_seconds = (
            process.runtime_seconds
        )

    # ---------------------------------------------------------
    # CPU
    # ---------------------------------------------------------

    coverage.check(process.processor is not None)

    if process.processor is not None:

        analysis.processor = process.processor

    coverage.apply(process)
    return analysis
