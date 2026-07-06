"""
Memory Pressure Analyzer.
Evaluates Linux Pressure Stall Information (PSI)
to determine the severity of memory contention.
"""

from __future__ import annotations

from project.models.memory import MemoryData, HealthCheck
from project.analyzers.mem.data import build_result

def analyze_memory_pressure(
    memory: MemoryData,
) -> build_result(name, state, checks=list[HealthCheck]):

    checks: list[HealthCheck] = []
    some10 = memory.psi_some_avg10
    some60 = memory.psi_some_avg60
    some300 = memory.psi_some_avg300

    full10 = memory.psi_full_avg10
    full60 = memory.psi_full_avg60
    full300 = memory.psi_full_avg300

    # ==========================================================
    # PSI Unsupported
    # ==========================================================

    if some10 is None or full10 is None:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="PASS",
                reason=(
                    "Linux Pressure Stall Information (PSI) "
                    "is unavailable on this system."
                ),
            )
        )
        return build_result(name="pressure", state="UNAVAILABLE", checks)

     result = build_result(name="pressure", state="COMPLETE", checks)
    # ==========================================================
    # Full Stall (Highest Severity)
    # ==========================================================

    if full10 > 0:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="CRITICAL",
                reason=(
                    "Full memory stalls detected. "
                    f"avg10={full10:.2f}, "
                    f"avg60={full60:.2f}, "
                    f"avg300={full300:.2f}. "
                    "All runnable tasks experienced memory stalls."
                ),
            )
        )
        return result

    # ==========================================================
    # Severe Contention
    # ==========================================================

    if some10 >= 10:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="CRITICAL",
                reason=(
                    "Memory pressure is extremely high. "
                    f"avg10={some10:.2f}, "
                    f"avg60={some60:.2f}, "
                    f"avg300={some300:.2f}. "
                    "Processes are spending significant time waiting for memory."
                ),
            )
        )
        return result

    # ==========================================================
    # Elevated Pressure
    # ==========================================================

    if some10 >= 5:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="WARNING",
                reason=(
                    "Memory pressure is elevated. "
                    f"avg10={some10:.2f}, "
                    f"avg60={some60:.2f}, "
                    f"avg300={some300:.2f}."
                ),
            )
        )
        return result

    # ==========================================================
    # Mild Pressure
    # ==========================================================

    if some10 >= 1:
        checks.append(
            HealthCheck(
                check="Memory Pressure",
                status="WARNING",
                reason=(
                    "Light memory pressure detected. "
                    f"avg10={some10:.2f}, "
                    f"avg60={some60:.2f}, "
                    f"avg300={some300:.2f}."
                ),
            )
        )
        return result

    # ==========================================================
    # Healthy
    # ==========================================================

    checks.append(
        HealthCheck(
            check="Memory Pressure",
            status="PASS",
            reason=(
                "No measurable memory pressure detected. "
                f"some={some10:.2f}/{some60:.2f}/{some300:.2f}, "
                f"full={full10:.2f}/{full60:.2f}/{full300:.2f}."
            ),
        )
    )

    return result
