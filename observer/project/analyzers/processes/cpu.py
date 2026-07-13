from __future__ import annotations
from project.models.processes import (
    ProcessSnapshot,
    ProcessCpuAnalysis,
    ObserverState as OB,
)
from project.analyzers.utils.coverage import Coverage

def analyze_cpu(
    process: ProcessSnapshot,
) -> ProcessCpuAnalysis:
    """
    Analyze CPU behaviour for a single process.
    """

    analysis = ProcessCpuAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    coverage.check(process.cpu_percent not in OB.values)
    if process.cpu_percent not in OB.values:
        analysis.signals["is_cpu_bound"] = (
            process.cpu_percent if process.cpu_percent >= HIGH_CPU
            and process.state == "R" )
        analysis.cpu_percent = process.cpu_percent
        analysis.append(fact(""))
        analysis.append(classifications(""))
    if process.cpu_percent in (OB.NA, OB.NS):
        analysis.append(fact(""))
        analysis.append(classifications(""))





    coverage.apply(process)
    return analysis
