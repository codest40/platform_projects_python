from project.models.query import QueryResult
from project.models.processes import ObserverState as OB


def get_process_by_pid(inventory, pid):
    """
    Return information about a single process.
    """
    for process in inventory.processes:
        if process.pid == pid:
            return QueryResult(
                title=f"Process {pid}",
                description="Process found.",
                processes=[process],
                warnings=[],
            )

    return QueryResult(
        title=f"Process {pid}",
        description="Process not found.",
        processes=[],
        warnings=[f"PID {pid} does not exist."],
    )


def get_waiting_processes(inventory):
    """
    Return all processes currently waiting.
    """
    waiting = [
        process
        for process in inventory.processes
        if process.wait_channel_analysis
        and process.wait_channel_analysis.signals.get("is_waiting")
    ]

    return QueryResult(
        title="Waiting Processes",
        description=f"{len(waiting)} waiting process(es) found.",
        processes=waiting,
        warnings=[],
    )


def get_high_memory_processes(inventory, limit=10):
    """
    Return processes using the most resident memory.
    """
    processes = sorted(
        inventory.processes,
        key=lambda p: p.rss_bytes or 0,
        reverse=True,
    )[:limit]

    return QueryResult(
        title="Highest Memory Processes",
        description=f"Top {len(processes)} memory consumers.",
        processes=processes,
        warnings=[],
    )
