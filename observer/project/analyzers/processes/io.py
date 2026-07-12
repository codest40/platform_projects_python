from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessIoAnalysis,
)


def analyze_io(
    process: ProcessSnapshot,
) -> ProcessIoAnalysis:
    """
    Analyze process I/O behaviour.
    """

    analysis = ProcessIoAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    #
    # ---------------------------------------------------------
    # Read Throughput
    # ---------------------------------------------------------
    #

    coverage.check(process.read_bytes_per_sec is not None)

    if process.read_bytes_per_sec is not None:

        analysis.read_bytes_per_sec = (
            process.read_bytes_per_sec
        )

        if process.read_bytes_per_sec > 0:
            analysis.classifications.append(
                "read_active"
            )

    #
    # ---------------------------------------------------------
    # Write Throughput
    # ---------------------------------------------------------
    #

    coverage.check(process.write_bytes_per_sec is not None)

    if process.write_bytes_per_sec is not None:

        analysis.write_bytes_per_sec = (
            process.write_bytes_per_sec
        )

        if process.write_bytes_per_sec > 0:
            analysis.classifications.append(
                "write_active"
            )

    #
    # ---------------------------------------------------------
    # Total I/O Throughput
    # ---------------------------------------------------------
    #

    coverage.check(process.io_bytes_per_sec is not None)

    if process.io_bytes_per_sec is not None:

        analysis.io_bytes_per_sec = (
            process.io_bytes_per_sec
        )

    #
    # ---------------------------------------------------------
    # Read / Write Ratio
    # ---------------------------------------------------------
    #

    coverage.check(process.read_write_ratio is not None)

    if process.read_write_ratio is not None:

        analysis.read_write_ratio = (
            process.read_write_ratio
        )

        if process.read_write_ratio > 1:
            analysis.classifications.append(
                "read_heavy"
            )

        elif process.read_write_ratio < 1:
            analysis.classifications.append(
                "write_heavy"
            )

        else:
            analysis.classifications.append(
                "balanced_io"
            )

    #
    # ---------------------------------------------------------
    # Read Syscalls
    # ---------------------------------------------------------
    #

    coverage.check(
        process.read_syscalls_per_sec is not None
    )

    if process.read_syscalls_per_sec is not None:

        analysis.read_syscalls_per_sec = (
            process.read_syscalls_per_sec
        )

    #
    # ---------------------------------------------------------
    # Write Syscalls
    # ---------------------------------------------------------
    #

    coverage.check(
        process.write_syscalls_per_sec is not None
    )

    if process.write_syscalls_per_sec is not None:

        analysis.write_syscalls_per_sec = (
            process.write_syscalls_per_sec
        )

    #
    # ---------------------------------------------------------
    # Total Syscalls
    # ---------------------------------------------------------
    #

    coverage.check(
        process.io_syscalls_per_sec is not None
    )

    if process.io_syscalls_per_sec is not None:

        analysis.io_syscalls_per_sec = (
            process.io_syscalls_per_sec
        )

    #
    # ---------------------------------------------------------
    # Cancelled Writes
    # ---------------------------------------------------------
    #

    coverage.check(
        process.cancelled_write_bytes is not None
    )

    if process.cancelled_write_bytes is not None:

        analysis.cancelled_write_bytes = (
            process.cancelled_write_bytes
        )

        if process.cancelled_write_bytes > 0:

            analysis.classifications.append(
                "cancelled_writes"
            )

    coverage.check(process.average_read_size is not None)
    if process.average_read_size is not None:
        analysis.average_read_size = (
            process.average_read_size
        )

        analysis.facts.append(
                f"Average read size: {process.average_read_size:.0f} bytes/op"
            )

    coverage.check(process.average_write_size is not None)
    if process.average_write_size is not None:
        analysis.average_write_size = (
            process.average_write_size
        )

        analysis.facts.append(
                f"Average write size: {process.average_write_size:.0f} bytes/op"
            )

    coverage.check(process.lifetime_average_read_size is not None)
    if process.lifetime_average_read_size is not None:
        analysis.lifetime_average_read_size = (
            process.lifetime_average_read_size
        )
        analysis.facts.append(
               f"lifetime average read size: {process.lifetime_average_read_size:.0f} bytes/op"
            )

    coverage.check(process.lifetime_average_write_size is not None)
    if process.lifetime_average_write_size is not None:
        analysis.lifetime_average_write_size = (
            process.lifetime_average_write_size
        )
        analysis.facts.append(
               f"lifetime average write size: {process.lifetime_average_write_size:.0f} bytes/op"
            )

    #
    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------
    #

    if analysis.read_bytes_per_sec is not None:

        analysis.facts.append(
            f"Read: {analysis.read_bytes_per_sec:.2f} B/s"
        )

    if analysis.write_bytes_per_sec is not None:

        analysis.facts.append(
            f"Write: {analysis.write_bytes_per_sec:.2f} B/s"
        )

    if analysis.io_bytes_per_sec is not None:

        analysis.facts.append(
            f"Total I/O: {analysis.io_bytes_per_sec:.2f} B/s"
        )

    if analysis.io_syscalls_per_sec is not None:

        analysis.facts.append(
            f"I/O syscalls: "
            f"{analysis.io_syscalls_per_sec:.2f}/sec"
        )

    if analysis.cancelled_write_bytes is not None:

        analysis.facts.append(
            f"Cancelled writes: "
            f"{analysis.cancelled_write_bytes:,} bytes"
        )

    coverage.apply(process)
    return analysis
