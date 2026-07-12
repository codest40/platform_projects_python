
def analyze_process_metrics(**kwargs):
  print("DONE")
  return {}

def analyze_process(process):

    analyses = []

    analyses.append(
        analyze_identity(process)
    )

    analyses.append(
        analyze_cpu(process)
    )

    analyses.append(
        analyze_memory(process)
    )

    analyses.append(
        analyze_io(process)
    )

    analyses.append(
        analyze_scheduler(process)
    )

    analyses.append(
        analyze_threads(process)
    )

    analyses.append(
        analyze_fd(process)
    )

    analyses.append(
        analyze_limits(process)
    )

    analyses.append(
        analyze_wait_channel(process)
    )

    return summarize_process(
        process,
        analyses,
    )
