from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessIoAnalysis,
    ObserverState as OB,
)


def analyze_io(
    process: ProcessSnapshot,
) -> ProcessIoAnalysis:
    """
    Analyze process IO behaviour.
    """

    analysis = ProcessIoAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    HIGH_IO = 100 * 1024 * 1024
    HIGH_SYSCALL = 10000
    SMALL_IO = 4096
    LARGE_IO = 1024 * 1024


    # ---------------------------------------------------------
    # Copy metrics
    # ---------------------------------------------------------

    analysis.read_bytes_per_sec = (
        process.read_bytes_per_sec
    )

    analysis.write_bytes_per_sec = (
        process.write_bytes_per_sec
    )

    analysis.io_bytes_per_sec = (
        process.io_bytes_per_sec
    )

    analysis.read_write_ratio = (
        process.read_write_ratio
    )

    analysis.read_syscalls_per_sec = (
        process.read_syscalls_per_sec
    )

    analysis.write_syscalls_per_sec = (
        process.write_syscalls_per_sec
    )

    analysis.io_syscalls_per_sec = (
        process.io_syscalls_per_sec
    )

    analysis.cancelled_write_bytes = (
        process.cancelled_write_bytes
    )


    # ---------------------------------------------------------
    # Read activity
    # ---------------------------------------------------------

    coverage.check(
        process.read_bytes_per_sec not in OB.values
    )

    if process.read_bytes_per_sec not in OB.values:

        active = (
            process.read_bytes_per_sec > 0
        )

        analysis.signals[
            "is_read_active"
        ] = active


        if active:
            analysis.classifications.append(
                "read_active"
            )

    else:

        analysis.signals[
            "is_read_active"
        ] = OB.NA



    # ---------------------------------------------------------
    # Write activity
    # ---------------------------------------------------------

    coverage.check(
        process.write_bytes_per_sec not in OB.values
    )

    if process.write_bytes_per_sec not in OB.values:

        active = (
            process.write_bytes_per_sec > 0
        )

        analysis.signals[
            "is_write_active"
        ] = active


        if active:
            analysis.classifications.append(
                "write_active"
            )

    else:

        analysis.signals[
            "is_write_active"
        ] = OB.NA



    # ---------------------------------------------------------
    # Heavy IO
    # ---------------------------------------------------------

    coverage.check(
        process.io_bytes_per_sec not in OB.values
    )

    if process.io_bytes_per_sec not in OB.values:

        heavy = (
            process.io_bytes_per_sec >= HIGH_IO
        )

        analysis.signals[
            "is_io_heavy"
        ] = heavy


        if heavy:

            analysis.classifications.append(
                "heavy_io"
            )

            analysis.recommendations.append(
                "Investigate process IO if sustained."
            )

    else:

        analysis.signals[
            "is_io_heavy"
        ] = OB.NA



    # ---------------------------------------------------------
    # Read / Write pattern
    # ---------------------------------------------------------

    if process.read_write_ratio not in OB.values:

        ratio = process.read_write_ratio


        read_heavy = ratio > 2

        write_heavy = (
            ratio < 0.5
        )


        analysis.signals[
            "is_read_heavy"
        ] = read_heavy


        analysis.signals[
            "is_write_heavy"
        ] = write_heavy


        if read_heavy:

            analysis.classifications.append(
                "read_heavy"
            )


        elif write_heavy:

            analysis.classifications.append(
                "write_heavy"
            )


        else:

            analysis.classifications.append(
                "balanced_io"
            )

    else:

        analysis.signals[
            "is_read_heavy"
        ] = OB.NA

        analysis.signals[
            "is_write_heavy"
        ] = OB.NA



    # ---------------------------------------------------------
    # IO syscall pressure
    # ---------------------------------------------------------

    if process.io_syscalls_per_sec not in OB.values:

        syscall_heavy = (
            process.io_syscalls_per_sec
            >= HIGH_SYSCALL
        )


        analysis.signals[
            "is_io_syscall_heavy"
        ] = syscall_heavy


        if syscall_heavy:

            analysis.classifications.append(
                "high_io_syscall_rate"
            )


    else:

        analysis.signals[
            "is_io_syscall_heavy"
        ] = OB.NA



    # ---------------------------------------------------------
    # Cancelled writes
    # ---------------------------------------------------------

    if process.cancelled_write_bytes not in OB.values:

        cancelled = (
            process.cancelled_write_bytes > 0
        )


        analysis.signals[
            "has_cancelled_writes"
        ] = cancelled


        if cancelled:

            analysis.classifications.append(
                "cancelled_writes"
            )

            analysis.recommendations.append(
                "Investigate processes generating cancelled writes."
            )

    else:

        analysis.signals[
            "has_cancelled_writes"
        ] = OB.NA



    # ---------------------------------------------------------
    # IO size pattern
    # ---------------------------------------------------------

    if process.average_read_size not in OB.values:

        small = (
            process.average_read_size <= SMALL_IO
        )

        large = (
            process.average_read_size >= LARGE_IO
        )


        analysis.signals[
            "is_small_io_pattern"
        ] = small


        analysis.signals[
            "is_large_io_pattern"
        ] = large


    else:

        analysis.signals[
            "is_small_io_pattern"
        ] = OB.NA

        analysis.signals[
            "is_large_io_pattern"
        ] = OB.NA



    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------

    if process.read_bytes_per_sec not in OB.values:

        analysis.facts.append(
            f"Read rate: {process.read_bytes_per_sec:.2f} B/s"
        )


    if process.write_bytes_per_sec not in OB.values:

        analysis.facts.append(
            f"Write rate: {process.write_bytes_per_sec:.2f} B/s"
        )


    if process.io_bytes_per_sec not in OB.values:

        analysis.facts.append(
            f"Total IO: {process.io_bytes_per_sec:.2f} B/s"
        )


    if process.io_syscalls_per_sec not in OB.values:

        analysis.facts.append(
            f"IO syscalls: {process.io_syscalls_per_sec:.2f}/sec"
        )


    if process.average_read_size not in OB.values:

        analysis.facts.append(
            f"Average read size: {process.average_read_size:.0f} bytes"
        )


    if process.average_write_size not in OB.values:

        analysis.facts.append(
            f"Average write size: {process.average_write_size:.0f} bytes"
        )


    coverage.apply(process)
    return analysis
