from __future__ import annotations

from project.analyzers.utils.process_coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessContextSwitchAnalysis,
    ObserverState as OB,
)


def analyze_context_switch(
    process: ProcessSnapshot,
    metrics: TotalMetrics,
) -> ProcessContextSwitchAnalysis:
    """
    Analyze scheduler context-switch behaviour for a single process.
    """

    analysis = ProcessContextSwitchAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()
    HIGH_CONTEXT_SWITCH_RATE = 1000.0
    HIGH_VOLUNTARY_SWITCH_RATE = 700.0
    HIGH_INVOLUNTARY_SWITCH_RATE = 300.0
    CONTEXT_SWITCH_STORM = 5000.0
    VOLUNTARY_DOMINANT = 0.70
    INVOLUNTARY_DOMINANT = 0.30

    # ---------------------------------------------------------
    # Coverage
    # ---------------------------------------------------------

    coverage.check(
        process.voluntary_context_switches_per_sec not in OB.values
    )
    coverage.check(
        process.involuntary_context_switches_per_sec not in OB.values
    )
    coverage.check(
        process.total_context_switches_per_sec not in OB.values
    )
    coverage.check(
        process.voluntary_context_switch_ratio not in OB.values
    )


    analysis.voluntary_context_switches_per_sec = (
        process.voluntary_context_switches_per_sec
    )
    analysis.involuntary_context_switches_per_sec = (
        process.involuntary_context_switches_per_sec
    )
    analysis.total_context_switches_per_sec = (
        process.total_context_switches_per_sec
    )
    analysis.voluntary_ratio = (
        process.voluntary_context_switch_ratio
    )

    # ---------------------------------------------------------
    # High Total Context Switch Rate
    # ---------------------------------------------------------
    if process.total_context_switches_per_sec not in OB.values:
        high_total = (
            process.total_context_switches_per_sec
            >= HIGH_CONTEXT_SWITCH_RATE
        )
        analysis.signals["is_high_context_switch_rate"] = high_total
        if high_total:
            analysis.classifications.append(
                "high_context_switch_rate"
            )
            analysis.recommendations.append(
                "Monitor sustained context-switch activity to determine whether it is expected."
            )

    else:
        analysis.signals["is_high_context_switch_rate"] = OB.NA

    # ---------------------------------------------------------
    # High Voluntary Context Switch Rate
    # ---------------------------------------------------------
    if process.voluntary_context_switches_per_sec not in OB.values:
        high_voluntary = (
            process.voluntary_context_switches_per_sec
            >= HIGH_VOLUNTARY_SWITCH_RATE
        )

        analysis.signals[
            "is_high_voluntary_context_switch_rate"
        ] = high_voluntary

        if high_voluntary:
            analysis.classifications.append(
                "high_voluntary_switching"
            )
    else:
        analysis.signals[
            "is_high_voluntary_context_switch_rate"
        ] = OB.NA

    # ---------------------------------------------------------
    # High Involuntary Context Switch Rate
    # ---------------------------------------------------------

    if process.involuntary_context_switches_per_sec not in OB.values:
        high_involuntary = (
            process.involuntary_context_switches_per_sec
            >= HIGH_INVOLUNTARY_SWITCH_RATE
        )
        analysis.signals[
            "is_high_involuntary_context_switch_rate"
        ] = high_involuntary

        if high_involuntary:

            analysis.classifications.append(
                "high_involuntary_switching"
            )

            analysis.recommendations.append(
                "Investigate scheduler pressure or CPU contention."
            )
    else:
        analysis.signals[
            "is_high_involuntary_context_switch_rate"
        ] = OB.NA

    # ---------------------------------------------------------
    # Dominant Switch Type
    # ---------------------------------------------------------

    if process.voluntary_context_switch_ratio not in OB.values:

        voluntary_dominant = (
            process.voluntary_context_switch_ratio
            >= VOLUNTARY_DOMINANT
        )

        involuntary_dominant = (
            process.voluntary_context_switch_ratio
            <= INVOLUNTARY_DOMINANT
        )
        analysis.signals[
            "is_voluntary_context_switch_dominant"
        ] = voluntary_dominant

        analysis.signals[
            "is_involuntary_context_switch_dominant"
        ] = involuntary_dominant

        if voluntary_dominant:
            analysis.classifications.append(
                "voluntary_switch_dominant"
            )
            analysis.classifications.append(
                "frequently_gives_up_cpu"
            )
        elif involuntary_dominant:
            analysis.classifications.append(
                "involuntary_switch_dominant"
            )
            analysis.classifications.append(
                "rarely_gives_up_cpu"
            )
    else:
        analysis.signals[
            "is_voluntary_context_switch_dominant"
        ] = OB.NA

        analysis.signals[
            "is_involuntary_context_switch_dominant"
        ] = OB.NA

    # ---------------------------------------------------------
    # Context Switch Storm
    # ---------------------------------------------------------
    if process.total_context_switches_per_sec not in OB.values:
        storm = (
            process.total_context_switches_per_sec
            >= CONTEXT_SWITCH_STORM
        )
        analysis.signals[
            "is_context_switch_storm"
        ] = storm

        if storm:
            analysis.classifications.append(
                "context_switch_storm"
            )
            analysis.recommendations.append(
                "Investigate excessive scheduling activity, lock contention, or synchronization overhead."
            )
    else:
        analysis.signals[
            "is_context_switch_storm"
        ] = OB.NA

    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------
    if process.voluntary_context_switches_per_sec not in OB.values:
        analysis.facts.append(
            f"Voluntary context switches: "
            f"{process.voluntary_context_switches_per_sec:.2f}/sec."
        )
    if process.involuntary_context_switches_per_sec not in OB.values:
        analysis.facts.append(
            f"Involuntary context switches: "
            f"{process.involuntary_context_switches_per_sec:.2f}/sec."
        )

    if process.total_context_switches_per_sec not in OB.values:
        analysis.facts.append(
            f"Total context switches: "
            f"{process.total_context_switches_per_sec:.2f}/sec."
        )

    if process.voluntary_context_switch_ratio not in OB.values:
        analysis.facts.append(
            f"Voluntary switches account for "
            f"{process.voluntary_context_switch_ratio:.1%} "
            "of all context switches."
        )
        analysis.facts.append(
            f"Involuntary switches account for "
            f"{1 - process.voluntary_context_switch_ratio:.1%} "
            "of all context switches."
        )

    coverage.apply(metrics)
    analysis.coverage = coverage.score(metrics)

    return analysis
