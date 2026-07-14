from __future__ import annotations
from project.models.processes import (
    ProcessSnapshot,
    ProcessSummary,
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

    results = []

    for analyzer in analyses:
        analysis = analyzer(process)
        results.append(analysis)
        merge_analysis(summary, analysis)
    deduplicate_summary(summary)
    for field, rule in SUMMARY_RULES.items():
        setattr(
            summary,
            field,
            rule(results),
        )

    #summary.healthy = rules.is_process_healthy(summary)
    #summary.confidence = rules.calculate_confidence(results)
    #summary.severity = rules.calculate_severity(summary)

    return summary
