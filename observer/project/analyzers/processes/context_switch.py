from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessContextSwitchAnalysis,
)


def analyze_context_switch(
    process: ProcessSnapshot,
) -> ProcessContextSwitchAnalysis:
    """
    Analyze scheduler context-switch behaviour.
    """

    analysis = ProcessContextSwitchAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    # ---------------------------------------------------------
    # Voluntary Context Switches
    # ---------------------------------------------------------

    coverage.check(
        process.voluntary_context_switches_per_sec is not None
    )

    if process.voluntary_context_switches_per_sec is not None:

        analysis.voluntary_context_switches_per_sec = (
            process.voluntary_context_switches_per_sec
        )

    # ---------------------------------------------------------
    # Involuntary Context Switches
    # ---------------------------------------------------------

    coverage.check(
        process.involuntary_context_switches_per_sec is not None
    )

    if process.involuntary_context_switches_per_sec is not None:

        analysis.involuntary_context_switches_per_sec = (
            process.involuntary_context_switches_per_sec
        )

    # ---------------------------------------------------------
    # Total Context Switch Rate
    # ---------------------------------------------------------

    coverage.check(
        process.total_context_switches_per_sec is not None
    )

    if process.total_context_switches_per_sec is not None:

        analysis.total_context_switches_per_sec = (
            process.total_context_switches_per_sec
        )

    # ---------------------------------------------------------
    # Voluntary Ratio
    # ---------------------------------------------------------

    coverage.check(
        process.voluntary_ratio is not None
    )

    if process.voluntary_ratio is not None:

        analysis.voluntary_ratio = (
            process.voluntary_ratio
        )

    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------

    if analysis.voluntary_context_switches_per_sec is not None:

        analysis.facts.append(
            "Voluntary switches: "
            f"{analysis.voluntary_context_switches_per_sec:.2f}/sec"
        )

    if analysis.involuntary_context_switches_per_sec is not None:

        analysis.facts.append(
            "Involuntary switches: "
            f"{analysis.involuntary_context_switches_per_sec:.2f}/sec"
        )

    if analysis.total_context_switches_per_sec is not None:

        analysis.facts.append(
            "Total switches: "
            f"{analysis.context_switches_per_sec:.2f}/sec"
        )

    if analysis.voluntary_ratio is not None:

        analysis.facts.append(
            f"Voluntary ratio: {analysis.voluntary_ratio:.2%}"
        )

    coverage.apply(process)
    return analysis
