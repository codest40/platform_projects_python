from __future__ import annotations

from project.analyzers.utils.coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessWaitChannelAnalysis,
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

      if process.wchan == "-":
        analysis.wait_channel = "N/A"
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

    analysis.metrics_available = coverage.available
    analysis.metrics_expected = coverage.expected

    return analysis
