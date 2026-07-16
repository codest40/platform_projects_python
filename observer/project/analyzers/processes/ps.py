from __future__ import annotations
from project.models.processes import (
    ProcessSnapshot,
    ProcessSummary,
    ProcessSummaryInventory,
    ObserverState as OB,
)
import traceback
from project.utils.helpers import timestamp
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
            tb = traceback.extract_tb(e.__traceback__)
            frame = tb[-1]
            result.analyzed_failed += 1
            result.analysis_errors.append(
                f"PID {process.pid}: {type(e).__name__}: {e} | "
                f"module={frame.filename} | "
                f"function={frame.name} | "
                f"line={frame.lineno}"
            )
        #fd = next(x for x in summary.analyses
        #   if type(x).__name__ == "ProcessFdAnalysis")
        #if fd:
        #  print(fd.signals)


    result.analyzed_total = len(inventory.processes)
    result.analyzed_at = timestamp()
    result.confidence = OB.DF
    return result

def analyze_process_metrics(result):
  r = analyze_processes(result)
  #print("Recieved By analyzer!")
  return r

