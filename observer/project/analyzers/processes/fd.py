from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessFdAnalysis,
)


def analyze_fd(
    process: ProcessSnapshot,
) -> ProcessFdAnalysis:
    """
    Analyze file descriptor usage.
    """

    analysis = ProcessFdAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    #
    # ---------------------------------------------------------
    # Open File Descriptors
    # ---------------------------------------------------------
    #

    coverage.check(process.open_fds is not None)

    if process.open_fds is not None:

        analysis.open_fds = process.open_fds

    #
    # ---------------------------------------------------------
    # FD Limit
    # ---------------------------------------------------------
    #

    coverage.check(process.max_fds is not None)

    if process.max_fds is not None:

        analysis.max_fds = process.max_fds

    #
    # ---------------------------------------------------------
    # FD Utilization
    # ---------------------------------------------------------
    #

    coverage.check(process.fd_utilization is not None)

    if process.fd_utilization is not None:

        analysis.fd_utilization = (
            process.fd_utilization
        )

    #
    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------
    #

    if analysis.open_fds is not None:

        analysis.facts.append(
            f"Open FDs: {analysis.open_fds}"
        )

    if analysis.max_fds is not None:

        analysis.facts.append(
            f"FD limit: {analysis.max_fds}"
        )

    if analysis.fd_utilization is not None:

        analysis.facts.append(
            f"FD utilization: "
            f"{analysis.fd_utilization:.2%}"
        )

    analysis.metrics_available = coverage.available
    analysis.metrics_expected = coverage.expected

    return analysis
