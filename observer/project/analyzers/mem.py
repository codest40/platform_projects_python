from project.models.memory import MemoryData, MemoryAnalysis
from project.models.events import HealthCheck
from project.utils.helpers import timestamp, get_status


def analyze_memory_metrics(result) -> MemoryAnalysis:

    if result.status != get_status("SUCCESS"):
        raise RuntimeError(
            "❌ [MEMORY ANALYZER] Memory collection did not complete successfully."
        )

    memory: MemoryData = result.data
    checks: list[HealthCheck] = []

# ---------------------------------------------------
# Available Memory
# ---------------------------------------------------

    available = memory.available_percent or 0.0

    if available < 10:
        checks.append(
            HealthCheck(
                check="Available Memory",
                status="🔴 CRITICAL",
                reason=(
                    f"Only {available:.1f}% memory remains available. "
                    "The system is at risk of memory pressure."
                ),
            )
        )

    elif available < 20:
        checks.append(
            HealthCheck(
                check="Available Memory",
                status="⚠️ WARNING",
                reason=(
                    f"Available memory is becoming limited "
                    f"({available:.1f}%)."
                ),
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Available Memory",
                status="✅ PASS",
                reason=(
                    f"Available memory is healthy "
                    f"({available:.1f}%)."
                ),
            )
        )

# ---------------------------------------------------
# Swap Activity
# ---------------------------------------------------
    if memory.swap_total == 0:
        checks.append(
            HealthCheck(
                check="Swap Activity",
                status="✅ PASS",
                reason="No swap Value Availbale on this system.",
            )
        )

    else:
        swap_percent = memory.swap_percent or 0.0
        swap_in = memory.swap_in or 0
        swap_out = memory.swap_out or 0

        if swap_percent >= 50 or swap_in > 0 or swap_out > 0:
            checks.append(
                HealthCheck(
                    check="Swap Activity",
                    status="🔴 CRITICAL",
                    reason=(
                        f"Swap usage is {swap_percent:.1f}% "
                        f"(swap in={swap_in}, swap out={swap_out}). "
                        "The system is actively relying on swap."
                    ),
                )
            )

        elif swap_percent >= 10:
            checks.append(
                HealthCheck(
                    check="Swap Activity",
                    status="⚠️ WARNING",
                    reason=(
                        f"Swap usage is elevated ({swap_percent:.1f}%), "
                        "although no active swapping is currently observed."
                    ),
                )
            )

        else:
            checks.append(
                HealthCheck(
                    check="Swap Activity",
                    status="✅ PASS",
                    reason=(
                        f"Swap usage is low ({swap_percent:.1f}%) "
                        "with no active swap activity."
                    ),
                )
            )


# ---------------------------------------------------
# Memory Pressure (PSI)
# ---------------------------------------------------

    some = memory.psi_some_avg10
    full = memory.psi_full_avg10

    if some is None or full is None:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="✅ PASS",
                reason="Memory Pressure Stall Information (PSI) is unavailable on this system.",
            )
        )

    elif full > 0:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="🔴 CRITICAL",
                reason=(
                    f"Full memory stalls detected "
                    f"(full avg10={full:.2f}). "
                    f"avg60={memory.psi_full_avg60:.2f}, "
                    f"avg300={memory.psi_full_avg300:.2f})."
                    "All runnable tasks were stalled by memory pressure. "
                    "indicating severe memory contention."
                ),
            )
        )
        if (memory.psi_full_avg300 >= 1 and memory.psi_full_avg60 >= 1):
          memory.pressure="Severe"

    elif some >= 10:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="🔴 CRITICAL",
                reason=(
                    f"Memory pressure is very high "
                    f"(some avg10={some:.2f}). "
                    f"avg60={memory.psi_some_avg60:.2f}, "
                    f"avg300={memory.psi_some_avg300:.2f})."
                    "Memory contention is significantly affecting workload execution. "
                    "Atleast, one runnable non-idle task is was stalled"
                ),
            )
        )

        if (memory.psi_some_avg300 >= 5 and memory.psi_some_avg60 >= 5):
          memory.pressure="Serious"

    elif some >= 5:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="⚠️ WARNING",
                reason=(
                    f"Memory pressure is elevated "
                    f"(some avg10={some:.2f})."
                    f"avg60={memory.psi_some_avg60:.2f}, "
                    f"avg300={memory.psi_some_avg300:.2f})."
                ),
            )
        )

        if (memory.psi_some_avg300 >= 2 and memory.psi_some_avg60 >= 2):
          memory.pressure="A little bit"


    else:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="✅ PASS",
                reason=(
                    f"Memory pressure is healthy "
                    f"(some avg10={some:.2f}, full avg10={full:.2f})."
                    f"avg60={memory.psi_some_avg60:.2f}, "
                    f"avg300={memory.psi_some_avg300:.2f})."
                ),
            )
        )

        if not (memory.psi_full_avg300 >= 1  and memory.psi_full_avg60 >= 1):
          memory.pressure="None detected"

# ---------------------------------------------------
# OOM / Allocation Failures
# ---------------------------------------------------

    oom = memory.oom_events
    alloc_failures = memory.allocation_failures
    container_oom = memory.container_oom_events

    if oom is None and alloc_failures is None:
        checks.append(
            HealthCheck(
                check="OOM / Allocation Failures",
                status="✅ PASS",
                reason="OOM and allocation failure statistics are unavailable.",
            )
        )

    elif (oom or 0) > 0:
        checks.append(
            HealthCheck(
                check="OOM / Allocation Failures",
                status="🔴 CRITICAL",
                reason=(
                    f"{oom} Out-Of-Memory event(s) detected. "
                    "The kernel has terminated one or more processes due to memory exhaustion."
                ),
            )
        )
        memory.confidence="Definately a Memory issue"

    elif (alloc_failures or 0) > 0:
        checks.append(
            HealthCheck(
                check="OOM / Allocation Failures",
                status="🔴 CRITICAL",
                reason=(
                    f"{alloc_failures} memory allocation failure(s) detected. "
                    "The kernel was unable to satisfy one or more memory allocation requests."
                ),
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="OOM / Allocation Failures",
                status="✅ PASS",
                reason="No Out-Of-Memory events or allocation failures detected.",
            )
        )

    if container_oom is not None:
      if (container_oom > 0):
        checks.append(
            HealthCheck(
                check="Container OOM Activity",
                status="🔴 CRITICAL",
                reason=(
                    f"Out-Of-Memory event(s) detected. "
                    "The kernel has terminated some processes in this container"
                )
            )
        )
        memory.confidence="Definately a Memory issue"
        memory.comment="See more filtered 'killed process' via dmesg -T or journalctl -k"


# ---------------------------------------------------
# Memory Reclaim
# ---------------------------------------------------

    reclaim = memory.reclaim_activity
    scan = memory.page_scan_rate
    reclaimed = memory.page_reclaim_rate

    if reclaim is None and scan is None and reclaimed is None:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="✅ PASS",
                reason="Memory reclaim statistics are unavailable.",
            )
        )

    elif (scan or 0) > 0 and (reclaimed or 0) == 0:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="🔴 CRITICAL",
                reason=(
                    "The kernel is scanning memory but reclaiming very few pages. "
                    "This indicates severe memory pressure."
                    "Reclaim is better as rates, multiple checks and comparison"
                ),
            )
        )

    elif (reclaim or 0) > 0 or (scan or 0) > 0:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="⚠️ WARNING",
                reason=(
                    "The kernel is actively reclaiming memory. "
                    "Memory pressure may be increasing."
                ),
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Memory Reclaim",
                status="✅ PASS",
                reason="Little or no memory reclaim activity detected.",
            )
        )


# ---------------------------------------------------
# Commit Accounting
# ---------------------------------------------------

    commit = memory.commit_percent

    if commit is None:
        checks.append(
            HealthCheck(
                check="Commit Accounting",
                status="✅ PASS",
                reason="Commit accounting statistics are unavailable.",
            )
        )

    elif commit > 100:
        checks.append(
            HealthCheck(
                check="Commit Accounting",
                status="⚠️  WARNING",
                reason=(
                    f"Committed memory is {commit:.1f}% of the commit limit. "
                    "Processes have committed more memory than the system can safely back."
                    f"Committed memory ({memory.committed_as:,} bytes) "
                    f"exceeds the commit limit ({memory.commit_limit:,} bytes). "
                    f"Commit usage is {commit:.1f}%. "
                    f"Although system could be VERY healthy if most other Major indicators are fine. "
                    f"check overcommit_memory and overcommit_ratio configurations also"
                ),
            )
        )

    elif commit >= 90:
        checks.append(
            HealthCheck(
                check="Commit Accounting",
                status="⚠️  WARNING",
                reason=(
                    f"Committed memory is approaching the commit limit "
                    f"({commit:.1f}%)."
                ),
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Commit Accounting",
                status="✅ PASS",
                reason=(
                    f"Committed memory is within safe limits "
                    f"({commit:.1f}% of commit limit)."
                ),
            )
        )


# ---------------------------------------------------
# Major Page Faults
# ---------------------------------------------------

    faults = memory.major_page_faults

    if faults is None:
        checks.append(
            HealthCheck(
                check="Major Page Faults",
                status="✅ PASS",
                reason="Major page fault statistics are unavailable.",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Major Page Faults",
                status="✅ PASS",
                reason=(
                    f"{faults:,} major page faults have occurred since boot. "
                    "Best intepreted as rates"
                    "Interpret this value alongside page fault rate, memory pressure, and swap activity."
                ),
            )
        )

# ---------------------------------------------------
# Filesystem Cache
# ---------------------------------------------------

    cache = memory.page_cache or memory.cached
    dirty = memory.dirty_pages
    writeback = memory.writeback_pages

    if cache is None:
        checks.append(
            HealthCheck(
                check="Filesystem Cache",
                status="✅ PASS",
                reason="Filesystem cache information is unavailable.",
            )
        )

    elif dirty is not None and writeback is not None:

        if writeback > 100 * 1024 * 1024:
            checks.append(
                HealthCheck(
                    check="Filesystem Cache",
                    status="⚠️ WARNING",
                    reason="Large writeback activity may indicate storage congestion.",
                )
            )

        elif dirty > 500 * 1024 * 1024:
            checks.append(
                HealthCheck(
                    check="Filesystem Cache",
                    status="⚠️ WARNING",
                    reason="Many dirty pages are waiting to be written to disk.",
                )
            )

        else:
            checks.append(
                HealthCheck(
                    check="Filesystem Cache",
                    status="✅ PASS",
                    reason="Filesystem cache is operating normally.",
                )
            )

    else:
        checks.append(
            HealthCheck(
                check="Filesystem Cache",
                status="✅ PASS",
                reason="Filesystem cache is present with no abnormal writeback activity detected.",
            )
        )

    statuses = {check.status for check in checks}

    if any("CRITICAL" in status.upper() or "🔴 " in status for status in statuses):
        verdict = f"Memory remains a primary suspect. Pressure: {memory.pressure}"
        severity = "CRITICAL"
        confidence = "High"
        comments = [
          "Identify the processes or containers with the highest memory usage.",
          "Review recent OOM events, allocation failures, and memory pressure (PSI).",
          "Check for memory leaks or abnormal memory growth over time.",
          "Verify swap activity and page reclaim behavior.",
          "Increase available memory or reduce workload if sustained pressure persists.",
        ]

    elif any("WARNING" in status.upper() or "⚠️ " in status for status in statuses):
        verdict = f"Memory shows warning signs and requires further investigation. Pressure: {memory.pressure}",
        severity = "WARNING"
        confidence = "Medium"
        comments = [
          "Continue monitoring memory utilization and available memory.",
          "Watch for increasing page faults, swap activity, and PSI values.",
          "Look for processes with steadily increasing memory consumption.",
          "Correlate memory metrics with CPU, disk, and application behavior.",
        ]

    else:
        verdict = f"Memory can reasonably be ruled out as the primary cause. Pressure: {memory.pressure}"
        severity = "INFO"
        confidence = "High"
        comments = [
          "Memory appears healthy with no significant pressure detected.",
          "Shift investigation to CPU, disk, network, or application-specific bottlenecks.",
          "Continue routine monitoring for any future changes.",
        ]

    return MemoryAnalysis(
        component="Memory",
        summary=verdict,
        confidence=confidence if confidence else None,
        severity=severity,
        health_checks=checks,
        analyzed_at=timestamp(),
        recommendations=comments,
    )
