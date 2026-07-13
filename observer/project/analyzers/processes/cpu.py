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
    HIGH_CPU = 85.0
    coverage.check(process.cpu_percent not in OB.values)
    coverage.check(process.state not in OB.values)
    if process.cpu_percent not in OB.values:
        analysis.cpu_percent = process.cpu_percent

        analysis.signals["is_cpu_bound"] = (
            process.cpu_percent >= HIGH_CPU
            and process.state == "R"
        )
        if analysis.signals["is_cpu_bound"]:
            analysis.classifications.append("cpu_bound")
            analysis.recommendations.append(
                "Profile the process if sustained."
            )
        else:
            analysis.classifications.append("not_cpu_bound")

    else:
        analysis.signals["is_cpu_bound"] = OB.NA
        analysis.classifications.append("cpu_unknown")

    analysis.append(fact(""))



    coverage.apply(process)
    return analysis
