from project.models.disk import DiskData, DiskAnalysis
from project.models.events import HealthCheck
from project.utils.helpers import timestamp, get_status


def analyze_disk_metrics(result: DiskData) -> DiskAnalysis:

    if result.status != get_status("SUCCESS"):
        raise RuntimeError(
            "❌ [DISK ANALYZER] Disk collection did not complete successfully."
        )

    disk: DiskData = result.data

    checks: list[HealthCheck] = []

    # ---------------------------------------------------
    # Filesystem Utilization
    # ---------------------------------------------------

    if disk.percent >= 90:
        checks.append(
            HealthCheck(
                check="Filesystem Utilization",
                status="🔴 CRITICAL",
                reason=f"Filesystem utilization is critically high ({disk.percent:.1f}%). Disk space exhaustion is imminent.",
            )
        )

    elif disk.percent >= 70:
        checks.append(
            HealthCheck(
                check="Filesystem Utilization",
                status="⚠️ WARNING",
                reason=f"Filesystem utilization is elevated ({disk.percent:.1f}%).",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Filesystem Utilization",
                status="✅ PASS",
                reason=f"Filesystem utilization is healthy ({disk.percent:.1f}%).",
            )
        )

    # ---------------------------------------------------
    # IO Pressure (PSI)
    # ---------------------------------------------------

    if (
        (disk.psi_full_avg10 or 0) > 0
        or (disk.psi_full_avg60 or 0) > 0
        or (disk.psi_full_avg300 or 0) > 0
    ):
        checks.append(
            HealthCheck(
                check="IO Pressure",
                status="🔴 CRITICAL",
                reason="Tasks are completely stalled waiting for storage resources.",
            )
        )

    elif (
        (disk.psi_some_avg10 or 0) >= 5
        or (disk.psi_some_avg60 or 0) >= 5
        or (disk.psi_some_avg300 or 0) >= 5
    ):
        checks.append(
            HealthCheck(
                check="IO Pressure",
                status="⚠️ WARNING",
                reason="Storage contention is beginning to delay task execution.",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="IO Pressure",
                status="✅ PASS",
                reason="No measurable storage pressure detected.",
            )
        )

    # ---------------------------------------------------
    # Outstanding IO
    # ---------------------------------------------------

    if disk.io_in_progress is not None:

        if disk.io_in_progress > 20:
            checks.append(
                HealthCheck(
                    check="Outstanding IO",
                    status="🔴 CRITICAL",
                    reason=f"{disk.io_in_progress} IO requests are currently outstanding.",
                )
            )

        elif disk.io_in_progress > 10:
            checks.append(
                HealthCheck(
                    check="Outstanding IO",
                    status="⚠️ WARNING",
                    reason=f"{disk.io_in_progress} IO requests are waiting for completion.",
                )
            )

        else:
            checks.append(
                HealthCheck(
                    check="Outstanding IO",
                    status="✅ PASS",
                    reason="No significant IO queue buildup detected.",
                )
            )

    # ---------------------------------------------------
    # IO Latency
    # ---------------------------------------------------

    if disk.average_wait_ms is not None:

        if disk.average_wait_ms >= 50:
            checks.append(
                HealthCheck(
                    check="IO Latency",
                    status="🔴 CRITICAL",
                    reason=f"Average IO wait time is {disk.average_wait_ms:.1f} ms.",
                )
            )

        elif disk.average_wait_ms >= 20:
            checks.append(
                HealthCheck(
                    check="IO Latency",
                    status="⚠️ WARNING",
                    reason=f"Average IO wait time is elevated ({disk.average_wait_ms:.1f} ms).",
                )
            )

        else:
            checks.append(
                HealthCheck(
                    check="IO Latency",
                    status="✅ PASS",
                    reason="Storage latency is within normal limits.",
                )
            )

    # ---------------------------------------------------
    # Dirty / Writeback Pages
    # ---------------------------------------------------

    dirty = disk.dirty_pages or 0
    writeback = disk.writeback_pages or 0

    if writeback > 1000:
        checks.append(
            HealthCheck(
                check="Writeback Activity",
                status="⚠️ WARNING",
                reason="Kernel writeback activity is elevated.",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Writeback Activity",
                status="✅ PASS",
                reason="Filesystem writeback activity is normal.",
            )
        )

    # ---------------------------------------------------
    # Process Disk IO
    # ---------------------------------------------------

    total_bytes = (
        (disk.process_read_bytes or 0)
        + (disk.process_write_bytes or 0)
    )

    if total_bytes > 1024 * 1024 * 1024:

        checks.append(
            HealthCheck(
                check="Process Disk IO",
                status="⚠️ WARNING",
                reason="Current process is generating heavy disk IO.",
            )
        )

    else:

        checks.append(
            HealthCheck(
                check="Process Disk IO",
                status="✅ PASS",
                reason="Current process disk activity is within expected limits.",
            )
        )

    # ---------------------------------------------------
    # Flush Activity
    # ---------------------------------------------------

    if (
        disk.flush_time_ms is not None
        and disk.flush_time_ms > 0
    ):
        checks.append(
            HealthCheck(
                check="Flush Activity",
                status="✅ PASS",
                reason="Flush operations are being recorded normally.",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Flush Activity",
                status="✅ PASS",
                reason="No abnormal flush activity detected.",
            )
        )

    # ---------------------------------------------------
    # Overall Verdict
    # ---------------------------------------------------

    statuses = {c.status for c in checks}

    confidence = "High"

    if any("CRITICAL" in s for s in statuses):

        severity = "CRITICAL"

        summary = "Storage remains a primary suspect."

        recommendations = [
            "Identify processes generating heavy disk IO.",
            "Review filesystem capacity.",
            "Inspect IO pressure and outstanding IO requests.",
            "Investigate writeback activity.",
            "Verify storage device performance.",
        ]

    elif any("WARNING" in s for s in statuses):

        severity = "WARNING"

        summary = "Storage shows warning signs but cannot yet be blamed."

        recommendations = [
            "Monitor storage utilization and IO pressure.",
            "Watch for increasing writeback or queue buildup.",
            "Continue observing storage latency.",
        ]

    else:

        severity = "INFO"

        summary = "Storage can reasonably be ruled out."

        recommendations = [
            "Storage does not appear to be the limiting resource.",
            "Continue investigating CPU, memory, or network.",
        ]

    return DiskAnalysis(
        component="Disk",
        summary=summary,
        confidence=confidence,
        severity=severity,
        health_checks=checks,
        analyzed_at=timestamp(),
        recommendations=recommendations,
    )
