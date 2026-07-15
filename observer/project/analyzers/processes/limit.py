from __future__ import annotations
from project.analyzers.utils.process_coverage import Coverage
from project.analyzers.processes.data import LIMITS
from project.models.processes import (
    ProcessSnapshot,
    TotalMetrics,
    ProcessLimitsAnalysis,
)


def analyze_limits(
    process: ProcessSnapshot,
    metrics: TotalMetrics,
) -> ProcessLimitsAnalysis:
    """
    Analyze process resource limits.
    """

    analysis = ProcessLimitsAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    for prefix, label, soft_attr, hard_attr in LIMITS:
        soft = getattr(process, soft_attr)
        hard = getattr(process, hard_attr)

        coverage.check(
            soft is not None or hard is not None
        )


        setattr(
            analysis,
            soft_attr,
            soft
        )

        setattr(
            analysis,
            hard_attr,
            hard
        )


        # Unlimited
        unlimited_soft = (
            soft == "unlimited"
        )

        unlimited_hard = (
            hard == "unlimited"
        )


        analysis.signals[
            f"is_{prefix}_soft_unlimited"
        ] = unlimited_soft


        analysis.signals[
            f"is_{prefix}_hard_unlimited"
        ] = unlimited_hard


        if unlimited_soft:

            analysis.classifications.append(
                f"{prefix}_soft_unlimited"
            )


        if unlimited_hard:

            analysis.classifications.append(
                f"{prefix}_hard_unlimited"
            )


        # Soft / hard relationship
        if (
            isinstance(soft, int)
            and isinstance(hard, int)
        ):

            fixed = (
                soft == hard
            )

            below = (
                soft < hard
            )


            analysis.signals[
                f"is_{prefix}_locked"
            ] = fixed


            analysis.signals[
                f"is_{prefix}_adjustable"
            ] = below


            if fixed:

                analysis.classifications.append(
                    f"{prefix}_fixed"
                )

                analysis.recommendations.append(
                    f"{label} soft limit equals hard limit."
                )


            elif below:

                analysis.classifications.append(
                    f"{prefix}_soft_below_hard"
                )


        # Facts
        if soft is not None:

            analysis.facts.append(
                f"{label} soft limit: {soft}"
            )


        if hard is not None:

            analysis.facts.append(
                f"{label} hard limit: {hard}"
            )

    coverage.apply(metrics)
    analysis.coverage = coverage.score(metrics)
    return analysis
