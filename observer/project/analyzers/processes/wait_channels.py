from __future__ import annotations
from project.analyzers.utils.process_coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessWaitChannelAnalysis,
    TotalMetrics,
    ObserverState as OB,
)

def analyze_wait_channel(
    process: ProcessSnapshot,
    metrics: TotalMetrics,
) -> ProcessWaitChannelAnalysis:

    analysis = ProcessWaitChannelAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    coverage.check(process.wchan is not None)

    if process.wchan is not None:

      if process.wchan in (None, "-", "0", "0000000000000000"):
        analysis.wait_channel = OB.NA
        analysis.signals["is_waiting"] = False
        analysis.classifications.append("not_waiting")
        analysis.facts.append("Process is not blocked in a kernel wait channel.")
      else:
        analysis.wait_channel = process.wchan
        analysis.signals["is_waiting"] = True
        analysis.facts.append(
            f"Kernel wait channel: {process.wchan}"
        )
        analysis.classifications.append("waiting")
    coverage.apply(metrics)
    analysis.coverage = coverage.score(metrics)
    return analysis

