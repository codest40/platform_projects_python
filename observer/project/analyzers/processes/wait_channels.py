from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessWaitChannelAnalysis,
    ObserverState as OB,
)

def analyze_wait_channel(
    process: ProcessSnapshot,
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
        analysis.classifications.append("not_waiting")
        analysis.facts.append(
            f"Process is NOT Waiting"
        )
      else:
        analysis.wait_channel = process.wchan
        analysis.facts.append(
            f"Kernel wait channel: {process.wchan}"
        )
        analysis.classifications.append("waiting")

    coverage.apply(process)
    return analysis
