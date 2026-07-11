from __future__ import annotations
from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessMemoryAnalysis,
)


def analyze_memory(
    process: ProcessSnapshot,
) -> ProcessMemoryAnalysis:
    """
    Analyze process memory characteristics.
    Uses normalized values only.
    """

    analysis = ProcessMemoryAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    #
    # ---------------------------------------------------------
    # Resident Memory
    # ---------------------------------------------------------
    #

    coverage.check(process.rss_bytes is not None)

    if process.rss_bytes is not None:

        analysis.rss_bytes = process.rss_bytes

        if process.rss_bytes > 0:
            analysis.classifications.append(
                "resident_memory"
            )

    #
    # ---------------------------------------------------------
    # Virtual Memory
    # ---------------------------------------------------------
    #

    coverage.check(process.vms_bytes is not None)

    if process.vms_bytes is not None:

        analysis.vms_bytes = process.vms_bytes

        if process.vms_bytes > 0:
            analysis.classifications.append(
                "virtual_memory"
            )

    #
    # ---------------------------------------------------------
    # Thread Count
    # ---------------------------------------------------------
    #

    coverage.check(process.thread_count is not None)

    if process.thread_count is not None:

        analysis.thread_count = process.thread_count

        if process.thread_count > 1:
            analysis.classifications.append(
                "multithreaded"
            )
        else:
            analysis.classifications.append(
                "single_threaded"
            )

    #
    # ---------------------------------------------------------
    # RSS / VMS Ratio
    # ---------------------------------------------------------
    #

    coverage.check(process.resident_ratio is not None)
    if process.resident_ratio is not None:
        analysis.resident_ratio = process.resident_ratio

        if analysis.resident_ratio > 0.90:
            analysis.classifications.append(
              "memory_resident"
            )

        elif analysis.resident_ratio < 0.20:
            analysis.classifications.append(
              "mostly_virtual"
            )

    #
    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------
    #

    if analysis.rss_bytes is not None:

        analysis.facts.append(
            f"RSS: {analysis.rss_bytes:,} bytes"
        )

    if analysis.vms_bytes is not None:

        analysis.facts.append(
            f"Virtual memory: {analysis.vms_bytes:,} bytes"
        )

    if analysis.thread_count is not None:

        analysis.facts.append(
            f"Threads: {analysis.thread_count}"
        )

    if analysis.resident_ratio is not None:

        analysis.facts.append(
            f"Resident ratio: {analysis.resident_ratio:.2f}"
        )

    analysis.metrics_available = coverage.available
    analysis.metrics_expected = coverage.expected

    return analysis
