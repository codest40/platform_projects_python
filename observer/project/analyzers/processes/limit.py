from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.analyzers.processes.data import LIMITS
from project.models.processes import (
    ProcessSnapshot,
    ProcessLimitsAnalysis,
)


def analyze_limits(
    process: ProcessSnapshot,
) -> ProcessLimitsAnalysis:
    """
    Analyze configured resource limits.
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
            soft,
        )

        setattr(
            analysis,
            hard_attr,
            hard,
        )

        #
        # Unlimited
        #

        if soft == "unlimited":
            analysis.classifications.append(
                f"{prefix}_soft_unlimited"
            )

        if hard == "unlimited":
            analysis.classifications.append(
                f"{prefix}_hard_unlimited"
            )

        #
        # Soft / Hard relationship
        #

        if (
            isinstance(soft, int)
            and isinstance(hard, int)
        ):

            if soft == hard:

                analysis.classifications.append(
                    f"{prefix}_fixed"
                )

            elif soft < hard:

                analysis.classifications.append(
                    f"{prefix}_soft_below_hard"
                )

        #
        # Facts
        #

        if soft is not None:

            analysis.facts.append(
                f"{label} soft limit: {soft}"
            )

        if hard is not None:

            analysis.facts.append(
                f"{label} hard limit: {hard}"
            )

    coverage.apply(process)
    return analysis
