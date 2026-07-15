from __future__ import annotations

from project.analyzers.utils.process_coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessFdAnalysis,
    TotalMetrics,
    ObserverState as OB,
)
import signal

def analyze_fd(
    process: ProcessSnapshot,
    metrics: TotalMetrics,
) -> ProcessFdAnalysis:
    """
    Analyze process file descriptor usage.
    """

    analysis = ProcessFdAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    HIGH_FD_USAGE = 0.80
    NEAR_FD_LIMIT = 0.90
    LOW_FD_REMAINING = 32
    sig = 11

    # ---------------------------------------------------------
    # Coverage
    # ---------------------------------------------------------

    coverage.check(process.open_fds not in OB.values)
    coverage.check(process.max_fds_soft not in OB.values)
    coverage.check(process.max_fds_hard not in OB.values)
    coverage.check(process.fd_utilization not in OB.values)
    coverage.check(process.runtime_collected_events not in OB.values)

    # ---------------------------------------------------------
    # Copy Metrics
    # ---------------------------------------------------------

    analysis.open_fds = process.open_fds
    analysis.max_fds_soft = process.max_fds_soft
    analysis.max_fds_hard = process.max_fds_hard
    analysis.fd_utilization = process.fd_utilization

    # ---------------------------------------------------------
    # Has Open FDs
    # ---------------------------------------------------------

    if process.open_fds not in OB.values:
        has_open = process.open_fds > 0
        analysis.signals["has_open_fds"] = has_open
        if not has_open:
            analysis.classifications.append("no_open_fds")
    else:
        analysis.signals["has_open_fds"] = OB.NA

    # ---------------------------------------------------------
    # High FD Usage
    # ---------------------------------------------------------

    if process.fd_utilization not in OB.values:
        high_usage = (
            process.fd_utilization >= HIGH_FD_USAGE
        )
        analysis.signals["is_high_fd_usage"] = high_usage

        if high_usage:
            analysis.classifications.append("high_fd_usage")
            analysis.recommendations.append(
                "Monitor file descriptor usage if it remains high."
            )
    else:
        analysis.signals["is_high_fd_usage"] = OB.NA

    # ---------------------------------------------------------
    # Near FD Limit
    # ---------------------------------------------------------

    if process.fd_utilization not in OB.values:
        near_limit = (
            process.fd_utilization >= NEAR_FD_LIMIT
        )
        analysis.signals["is_near_fd_limit"] = near_limit
        if near_limit:
            analysis.classifications.append("near_fd_limit")
            analysis.recommendations.append(
                "Increase the file descriptor limit or reduce descriptor usage."
            )
        else:
            analysis.classifications.append("fd_limit_not_near")
    else:
        analysis.signals["is_near_fd_limit"] = OB.NA

    # ---------------------------------------------------------
    # FD Limit Reached
    # ---------------------------------------------------------

    if (
        process.open_fds not in OB.values
        and isinstance(process.max_fds_soft, int)
    ):
        reached = (
            process.open_fds >= process.max_fds_soft
        )
        analysis.signals["is_fd_limit_reached"] = reached
        if reached:
            analysis.classifications.append("fd_limit_reached")
            analysis.recommendations.append(
                "The process has reached its file descriptor limit."
            )
        else:
            analysis.classifications.append("fd_limit_not_reached")
    else:
        analysis.signals["is_fd_limit_reached"] = OB.NA

    # ---------------------------------------------------------
    # Unlimited FD Limit
    # ---------------------------------------------------------

    if process.max_fds_soft not in OB.values:

        unlimited = (
            process.max_fds_soft == "unlimited"
            or process.max_fds_soft == float("inf")
        )
        analysis.signals["is_fd_limit_unlimited"] = unlimited
        if unlimited:
            analysis.classifications.append(
                "fd_limit_unlimited"
            )
    else:
        analysis.signals["is_fd_limit_unlimited"] = OB.NA

    # ---------------------------------------------------------
    # Low FD Availability
    # ---------------------------------------------------------

    if (
        process.open_fds not in OB.values
        and isinstance(process.max_fds_soft, int)
    ):
        remaining = (
            process.max_fds_soft - process.open_fds
        )
        low_remaining = (
            remaining <= LOW_FD_REMAINING
        )
        analysis.signals["is_low_fd_availability"] = (
            low_remaining
        )
        if low_remaining:
            analysis.classifications.append(
                "low_fd_availability"
            )
            analysis.recommendations.append(
                "Very few file descriptors remain available."
            )
    else:
        analysis.signals["is_low_fd_availability"] = OB.NA

    # ---------------------------------------------------------
    # FD Exhausted
    # ---------------------------------------------------------
    events = process.runtime_collected_events
    if events is not None:
      if events.emfile_count is not None:
            exhausted = (
              events.emfile_count > 0
            )
            analysis.signals[
              "is_fd_exhausted"
            ] = exhausted
            if exhausted:
                analysis.classifications.append(
                  "fd_exhausted"
                )
                analysis.recommendations.append(
                  "The process experienced file descriptor allocation failures."
                )
      else:
          analysis.classifications.append(
              f"fd_exhausted_{OB.NS}"
            )
    else:
            analysis.signals[
              "is_fd_exhausted"
            ] = OB.NA

    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------

    if process.open_fds not in OB.values:
        analysis.facts.append(
            f"Open file descriptors: {process.open_fds}."
        )
    if process.max_fds_soft not in OB.values:
        analysis.facts.append(
            f"Soft FD limit: {process.max_fds_soft}."
        )
    if process.max_fds_hard not in OB.values:
        analysis.facts.append(
            f"Hard FD limit: {process.max_fds_hard}."
        )
    if process.fd_utilization not in OB.values:
        analysis.facts.append(
            f"FD utilization: {process.fd_utilization:.1%}."
        )
    if (
        process.open_fds not in OB.values
        and isinstance(process.max_fds_soft, int)
    ):
        remaining = (
            process.max_fds_soft - process.open_fds
        )
        analysis.facts.append(
            f"{remaining} file descriptors remain before the soft limit."
        )
    if events not in OB.values:
      if (events.last_terminating_signal not in OB.values
        and last_terminating_signal == sig):
        analysis.facts.append(
          f"Process was terminated by {signal.Signals(sig).name} (sig)."
        )

    coverage.apply(metrics)
    analysis.coverage = coverage.score(metrics)
    return analysis
