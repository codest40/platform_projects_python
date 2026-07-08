"""
Entry point for CPU analysis.

Pipeline:
1. Run analyzers
2. Normalize signals
3. Build final summary
"""

from __future__ import annotations
from project.models.cpu import (
    CpuAnalysis,
    HealthCheck,
    Signal,
    AnalyzerResult,
)

from project.analyzers.cpu.capacity import analyze_capacity
from project.analyzers.cpu.load import analyze_load
from project.analyzers.cpu.iowait import analyze_iowait
from project.analyzers.cpu.balance import analyze_balance
from project.analyzers.cpu.kernel import analyze_kernel
from project.analyzers.cpu.steal import analyze_steal
from project.analyzers.cpu.container import analyze_container
from project.analyzers.cpu.pressure import analyze_pressure
from project.analyzers.cpu.frequency import analyze_frequency

from project.analyzers.cpu.normalizer import normalize
from project.analyzers.cpu.summary import summarize_cpu


# ==========================================================
# Registered CPU analyzers
# ==========================================================

analyzers = [
    analyze_capacity,
    analyze_load,
    analyze_iowait,
    analyze_balance,
    analyze_kernel,
    analyze_steal,
    analyze_container,
    analyze_pressure,
    analyze_frequency,
]


# ==========================================================
# CPU Analysis Pipeline
# ==========================================================

def analyze_cpu_metrics(
    result: Cpu_Data,
) -> CpuAnalysis:

    cpu = result
    if not cpu.seen:
        raise RuntimeError(
            "❌ [CPU ANALYZER] CPU Pipeline did NOT reach Computation stage!"
        )

    checks: list[HealthCheck] = []
    metadata: dict = {}

    # ======================================================
    # 1. Run analyzers
    # ======================================================

    for analyzer in analyzers:

        analyzer_result: AnalyzerResult = analyzer(cpu)

        checks.extend(analyzer_result.checks)

        metadata[analyzer_result.name] = {
            "state": analyzer_result.state,
            "total_checks": len(analyzer_result.checks),
        }

    # ======================================================
    # 2. Normalize Signals
    # ======================================================

    signals: list[Signal] = normalize(cpu)

    # ======================================================
    # 3. Build Final Summary
    # ======================================================

    return summarize_cpu(
        cpu=cpu,
        checks=checks,
        signals=signals,
        metadata=metadata,
    )
