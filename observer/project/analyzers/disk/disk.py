from project.models.disk import DiskData, DiskAnalysis
from project.models.events import HealthCheck
from project.utils.helpers import timestamp, get_status


def analyze_disk_metrics(result) -> DiskAnalysis:

    if not result.seen:
        raise RuntimeError(
            "❌ [DISK ANALYZER] Disk Pipeline did NOT reach Computation Stage."
        )

    disk: DiskData = result

    checks: list[HealthCheck] = []

    # ==========================================================
    # Filesystem Capacity
    # ==========================================================

    if disk.percent >= 90:
        checks.append(
            HealthCheck(
                check="Filesystem Capacity",
                status="🔴 CRITICAL",
                reason=f"Filesystem utilization is critically high ({disk.percent:.1f}%).",
            )
        )

    elif disk.percent >= 70:
        checks.append(
            HealthCheck(
                check="Filesystem Capacity",
                status="⚠️ WARNING",
                reason=f"Filesystem utilization is elevated ({disk.percent:.1f}%).",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Filesystem Capacity",
                status="✅ PASS",
                reason=f"Filesystem utilization is healthy ({disk.percent:.1f}%).",
            )
        )

    # ==========================================================
    # IO Pressure (PSI)
    # ==========================================================

    if (
        (disk.psi_full_avg10 or 0) > 0
        or (disk.psi_full_avg60 or 0) > 0
        or (disk.psi_full_avg300 or 0) > 0
    ):

        checks.append(
            HealthCheck(
                check="IO Pressure",
                status="🔴 CRITICAL",
                reason="Tasks are completely stalled waiting for storage.",
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
                reason="Storage pressure is delaying task execution.",
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

    # ==========================================================
    # Device Utilization
    # ==========================================================

    util = disk.device_utilization_percent

    if util is not None:

        if util >= 95:

            status = "🔴 CRITICAL"
            reason = f"Storage device is busy {util:.1f}% of the time."

        elif util >= 80:

            status = "⚠️ WARNING"
            reason = f"Storage device utilization is elevated ({util:.1f}%)."

        else:

            status = "✅ PASS"
            reason = "Device utilization is within normal limits."

        checks.append(
            HealthCheck(
                check="Device Utilization",
                status=status,
                reason=reason,
            )
        )

    # ==========================================================
    # Queue Depth
    # ==========================================================

    queue = disk.average_queue_depth

    if queue is not None:

        if queue >= 5:

            status = "🔴 CRITICAL"
            reason = f"Average queue depth is {queue:.2f}."

        elif queue >= 2:

            status = "⚠️ WARNING"
            reason = f"Average queue depth is increasing ({queue:.2f})."

        else:

            status = "✅ PASS"
            reason = "No significant queue buildup detected."

        checks.append(
            HealthCheck(
                check="Queue Depth",
                status=status,
                reason=reason,
            )
        )

    # ==========================================================
    # IO Latency
    # ==========================================================

    latency = max(
        disk.average_read_latency_ms or 0,
        disk.average_write_latency_ms or 0,
    )

    if latency > 0:

        if latency >= 50:

            status = "🔴 CRITICAL"
            reason = f"Average device latency is {latency:.1f} ms."

        elif latency >= 20:

            status = "⚠️ WARNING"
            reason = f"Average device latency is elevated ({latency:.1f} ms)."

        else:

            status = "✅ PASS"
            reason = "Storage latency is healthy."

        checks.append(
            HealthCheck(
                check="IO Latency",
                status=status,
                reason=reason,
            )
        )

    # ==========================================================
    # Writeback Activity
    # ==========================================================

    if disk.flushes_per_sec is not None:

        if disk.flushes_per_sec >= 500:

            status = "⚠️ WARNING"
            reason = "Flush activity is elevated."

        else:

            status = "✅ PASS"
            reason = "Flush activity is normal."

        checks.append(
            HealthCheck(
                check="Writeback Activity",
                status=status,
                reason=reason,
            )
        )

    # ==========================================================
    # Process Disk IO
    # ==========================================================

    proc_io = (
        (disk.process_read_mb_per_sec or 0)
        + (disk.process_write_mb_per_sec or 0)
    )

    if proc_io >= 100:

        status = "⚠️ WARNING"
        reason = "Current process is generating heavy disk throughput."

    else:

        status = "✅ PASS"
        reason = "Current process disk activity is within expected limits."

    checks.append(
        HealthCheck(
            check="Process Disk IO",
            status=status,
            reason=reason,
        )
    )

    # ==========================================================
    # Container Disk IO
    # ==========================================================

    container_io = (
        (disk.container_read_mb_per_sec or 0)
        + (disk.container_write_mb_per_sec or 0)
    )

    if container_io >= 100:

        status = "⚠️ WARNING"
        reason = "Container workloads are generating heavy storage throughput."

    else:

        status = "✅ PASS"
        reason = "Container storage activity is within expected limits."

    checks.append(
        HealthCheck(
            check="Container Disk IO",
            status=status,
            reason=reason,
        )
    )

    # ==========================================================
    # Correlate Evidence
    # ==========================================================

    evidence = []

    if (disk.psi_full_avg10 or 0) > 0:
        evidence.append("psi")

    if (disk.device_utilization_percent or 0) >= 95:
        evidence.append("utilization")

    if latency >= 50:
        evidence.append("latency")

    if (disk.average_queue_depth or 0) >= 5:
        evidence.append("queue")

    if disk.percent >= 90:
        evidence.append("capacity")

    if (disk.flushes_per_sec or 0) >= 500:
        evidence.append("flush")

    if proc_io >= 100:
        evidence.append("process")

    if container_io >= 100:
        evidence.append("container")

    performance = {
        "psi",
        "utilization",
        "latency",
        "queue",
    }

    performance_hits = len(performance & set(evidence))
    capacity_issue = "capacity" in evidence

    recommendations: list[str] = []

    if capacity_issue:
        recommendations.append(
            "Review filesystem capacity and reclaim disk space."
        )

    if "psi" in evidence:
        recommendations.append(
            "Investigate tasks stalled waiting for storage resources."
        )

    if "latency" in evidence:
        recommendations.append(
            "Investigate elevated storage latency."
        )

    if "queue" in evidence:
        recommendations.append(
            "Identify processes contributing to IO queue buildup."
        )

    if "utilization" in evidence:
        recommendations.append(
            "Review sustained device utilization."
        )

    if "process" in evidence:
        recommendations.append(
            "Inspect processes generating heavy disk activity."
        )

    if "container" in evidence:
        recommendations.append(
            "Inspect container workloads producing heavy storage traffic."
        )

    if performance_hits >= 3:

        severity = "CRITICAL"
        confidence = "High"

        summary = (
            "Multiple independent indicators point to storage as the primary "
            "performance bottleneck."
        )

    elif performance_hits >= 2 or (
        performance_hits >= 1 and capacity_issue
    ):

        severity = "WARNING"
        confidence = "Medium"

        summary = (
            "Storage shows several warning indicators and should be investigated."
        )

    elif capacity_issue:

        severity = "WARNING"
        confidence = "Medium"

        summary = (
            "Filesystem capacity is becoming constrained, although broader storage "
            "performance remains stable."
        )

    else:

        severity = "INFO"
        confidence = "High"
        recommendations.append(
            "Nothing to reccomend. Disk is healthy"
        )
        summary = (
            "Storage appears healthy and is unlikely to be responsible for the "
            "observed system behaviour."
        )

    return DiskAnalysis(
        component="Disk",
        summary=summary,
        confidence=confidence,
        severity=severity,
        health_checks=checks,
        analyzed_at=timestamp(),
        recommendations=recommendations,
    )
