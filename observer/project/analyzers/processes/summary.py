from __future__ import annotations

from project.models.processes import (
    ProcessSnapshot,
    ProcessSummary,
)

from project.analyzers.processes.all import analyses
from project.analyzers.processes import rules


def merge_analysis(
    summary: ProcessSummary,
    analysis,
) -> None:
    """
    Merge analyzer output into the process summary.
    """

    summary.facts.extend(
        analysis.facts
    )

    summary.recommendations.extend(
        analysis.recommendations
    )

    summary.classifications.extend(
        analysis.classifications
    )


def summarize_process(
    process: ProcessSnapshot,
) -> ProcessSummary:
    """
    Produce a high-level diagnosis for a process.
    """

    summary = ProcessSummary(
        pid=process.pid,
        tid=process.tid,
    )

    #
    # ---------------------------------------------------------
    # Run analyzers
    # ---------------------------------------------------------
    #

    results = []

    for analyzer in analyses:

        analysis = analyzer(process)

        results.append(
            analysis
        )

        merge_analysis(
            summary,
            analysis,
        )

    # ---------------------------------------------------------
    # High-level process behavior
    # ---------------------------------------------------------

    summary.multithreaded = (
        rules.is_multithreaded(results)
    )

    summary.interactive = (
        rules.is_interactive(results)
    )

    summary.daemon = (
        rules.is_daemon(results)
    )

    summary.container = (
        rules.is_container(results)
    )

    summary.blocked = (
        rules.is_blocked(results)
    )

    summary.cpu_bound = (
        rules.is_cpu_bound(results)
    )

    summary.io_bound = (
        rules.is_io_bound(results)
    )

    summary.resource_constrained = (
        rules.is_resource_constrained(results)
    )

    summary.approaching_limits = (
        rules.is_approaching_limits(results)
    )

    # ---------------------------------------------------------
    # Overall diagnosis
    # ---------------------------------------------------------
    summary.healthy = (
        rules.is_process_healthy(summary)
    )

    summary.confidence = (
        rules.calculate_confidence(results)
    )

    summary.severity = (
        rules.calculate_severity(summary)
    )

    return summary
