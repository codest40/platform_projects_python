from __future__ import annotations
from project.models.processes import (
    ProcessSnapshot,
    ProcessInventory,
    ProcessSummary,
    TotalMetrics,
    ObserverState as OB,
)
from project.analyzers.processes.all import analyses
from project.analyzers.processes import rules

SUMMARY_RULES = {
    "multithreaded": rules.is_multithreaded,
    "interactive": rules.is_interactive,
    "daemon": rules.is_daemon,
    "container": rules.is_container,
    "blocked": rules.is_blocked,
    "cpu_bound": rules.is_cpu_bound,
    "io_bound": rules.is_io_bound,
    "resource_constrained": rules.is_resource_constrained,
    "approaching_limits": rules.is_approaching_limits,
}

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

def deduplicate_summary(
    summary: ProcessSummary,
) -> None:
    """
    Remove duplicate entries while preserving order.
    """
    summary.facts = list(
        dict.fromkeys(summary.facts)
    )

    summary.classifications = list(
        dict.fromkeys(
            summary.classifications
        )
    )

    summary.recommendations = list(
        dict.fromkeys(
            summary.recommendations
        )
    )


def is_process_healthy(
    summary,
) -> bool | str | None:

    if (
        summary.blocked in OB.values and
        summary.resource_constrained in OB.values
    ):
        return OB.NA
    if summary.blocked is True:
        return False
    if summary.resource_constrained is True:
        return False
    return True

def calculate_severity(
    summary,
) -> str | None:
    """
    Determine the overall severity of the process.
    """
    if (
        summary.healthy in OB.values and
        summary.blocked in OB.values and
        summary.resource_constrained in OB.values and
        summary.approaching_limits in OB.values
    ):
        return OB.NA
    if summary.blocked is True:
        return "CRITICAL"
    if summary.resource_constrained is True:
        return "CRITICAL"
    if summary.approaching_limits is True:
        return "WARNING"
    if summary.healthy is True:
        return "PASS"
    return "WARNING"

def calculate_confidence(
    processes: TotalMetrics,
) -> str | None:
    """
    Estimate confidence in the overall process summary.
    """
    total = processes.total_available
    successful = processes.total_analyzed
    total_scores = processes.total_scores

    if (total in OB.values or successful in OB.values or total == 0):
        for x in (total, successful):
            if x is None or x == 0:
              return x

    score = successful / total
    if score >= 0.90:
        return "HIGH"
    if score >= 0.70:
        return "MEDIUM"
    return "LOW"


def calculate_coverage(results) -> str:
    coverages = [
        r.coverage
        for r in results
        if getattr(r, "coverage", None) is not None
    ]
    if not coverages:
        return "UNKNOWN"

    complete = coverages.count("COMPLETE")
    partial = coverages.count("PARTIAL")
    unavailable = coverages.count("UNAVAILABLE")
    total = len(coverages)
    score1 = complete + partial * 0.8
    score = score1/10

    if score > 0.7 or complete == total:
        return "COMPLETE"
    if score >= 0.4 or partial >= total / 2:
        return "PARTIAL"
    if unavailable > complete or score < 0.4:
       return "UNAVAILABLE"
    return OB.NA

def summarize_process(
    process: ProcessSnapshot,
) -> ProcessSummary:
    """
    Produce a high-level diagnosis for a process.
    """
    metrics = TotalMetrics()
    summary = ProcessSummary(
      pid=process.pid,
      tid=process.tid,
    )

    results = []
    for analyzer in analyses:
        analysis = analyzer(process, metrics)
        results.append(analysis)
        merge_analysis(summary, analysis)
    deduplicate_summary(summary)
    for field, rule in SUMMARY_RULES.items():
        setattr(
            summary,
            field,
            rule(results),
        )

    summary.healthy = is_process_healthy(summary)
    summary.severity = calculate_severity(summary)
    summary.confidence = calculate_confidence(metrics)
    summary.coverage = calculate_coverage(results)
    return summary
