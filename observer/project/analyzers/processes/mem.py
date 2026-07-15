from __future__ import annotations
from project.analyzers.utils.process_coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessMemoryAnalysis,
    TotalMetrics,
    ObserverState as OB,
)


def analyze_memory(
    process: ProcessSnapshot,
    metrics: TotalMetrics,
) -> ProcessMemoryAnalysis:
    """
    Analyze process memory behaviour.
    """

    analysis = ProcessMemoryAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    LARGE_RSS = 1024 * 1024 * 1024       # 1GB
    LARGE_VMS = 10 * 1024 * 1024 * 1024 # 10GB
    LOW_RESIDENT_RATIO = 0.01


    # ---------------------------------------------------------
    # Copy metrics
    # ---------------------------------------------------------
    analysis.rss_bytes = process.rss_bytes
    analysis.vms_bytes = process.vms_bytes
    analysis.thread_count = process.thread_count
    analysis.resident_ratio = process.resident_ratio


    coverage.check(
        process.rss_bytes not in OB.values
    )

    coverage.check(
        process.vms_bytes not in OB.values
    )

    coverage.check(
        process.thread_count not in OB.values
    )

    coverage.check(
        process.resident_ratio not in OB.values
    )


    # ---------------------------------------------------------
    # Has memory
    # ---------------------------------------------------------

    if process.rss_bytes not in OB.values:

        allocated = (
            process.rss_bytes > 0
        )
        analysis.signals[
            "is_memory_allocated"
        ] = allocated


        if allocated:

            analysis.classifications.append(
                "resident_memory"
            )

    else:

        analysis.signals[
            "is_memory_allocated"
        ] = OB.NA



    # ---------------------------------------------------------
    # Large RSS
    # ---------------------------------------------------------
    if process.rss_bytes not in OB.values:

        large = (
            process.rss_bytes >= LARGE_RSS
        )

        analysis.signals[
            "is_memory_large"
        ] = large


        if large:

            analysis.classifications.append(
                "large_resident_memory"
            )

            analysis.recommendations.append(
                "Investigate memory growth if RSS continues increasing."
            )

    else:

        analysis.signals[
            "is_memory_large"
        ] = OB.NA



    # ---------------------------------------------------------
    # Large virtual memory
    # ---------------------------------------------------------
    if process.vms_bytes not in OB.values:

        large_vms = (
            process.vms_bytes >= LARGE_VMS
        )


        analysis.signals[
            "is_virtual_memory_large"
        ] = large_vms


        if large_vms:

            analysis.classifications.append(
                "large_virtual_memory"
            )


    else:

        analysis.signals[
            "is_virtual_memory_large"
        ] = OB.NA



    # ---------------------------------------------------------
    # Resident ratio
    # ---------------------------------------------------------

    if process.resident_ratio not in OB.values:

        fragmented = (
            process.resident_ratio
            <= LOW_RESIDENT_RATIO
        )


        analysis.signals[
            "is_memory_fragmented"
        ] = fragmented


        if fragmented:

            analysis.classifications.append(
                "low_resident_ratio"
            )


    else:

        analysis.signals[
            "is_memory_fragmented"
        ] = OB.NA



    # ---------------------------------------------------------
    # Thread count
    # ---------------------------------------------------------

    if process.thread_count not in OB.values:

        multi = (
            process.thread_count > 1
        )

        analysis.signals[
            "is_multithreaded"
        ] = multi


        analysis.signals[
            "is_single_threaded"
        ] = not multi


        if multi:

            analysis.classifications.append(
                "multithreaded"
            )

        else:

            analysis.classifications.append(
                "single_threaded"
            )


    else:

        analysis.signals[
            "is_multithreaded"
        ] = OB.NA

        analysis.signals[
            "is_single_threaded"
        ] = OB.NA



    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------

    if process.rss_bytes not in OB.values:

        analysis.facts.append(
            f"RSS: {process.rss_bytes:,} bytes"
        )


    if process.vms_bytes not in OB.values:

        analysis.facts.append(
            f"Virtual memory: {process.vms_bytes:,} bytes"
        )


    if process.thread_count not in OB.values:

        analysis.facts.append(
            f"Threads: {process.thread_count}"
        )


    if process.resident_ratio not in OB.values:

        analysis.facts.append(
            f"Resident ratio: {process.resident_ratio:.2f}"
        )


    coverage.apply(metrics)
    analysis.coverage = coverage.score(metrics)
    return analysis
