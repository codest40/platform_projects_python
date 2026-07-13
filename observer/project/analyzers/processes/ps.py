from __future__ import annotations
from project.models.processes import (
    ProcessSnapshot,
    ProcessSummary,
    ProcessSummaryInventory,
)

from project.analyzers.processes.summary import (
    summarize_process,
)


def analyze_processes(
    inventory: ProcessInventory,
) -> ProcessAnalysis:

    result = ProcessSummaryInventory()
    for process in inventory.processes:

        try:
            summary = summarize_process(process)
            result.processes.append(summary)
            result.analyzed_successful += 1
        except Exception as e:
            result.analyzed_failed += 1
            result.analysis_errors.append(
                f"PID {process.pid}: {type(e).__name__}: {e}"
            )
    result.analyzed_total = len(inventory.processes)
    return result

def analyze_process_metrics(result):
  r = analyze_processes(result)
  #print(f"PRINITNG FINAL ANALYSIS DATA:\n {r}")
  #print("Recieved By analyzer!")
  return r

