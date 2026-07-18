from project.models.query import QueryResult


def _processes(inventory):
    return inventory["metadata"]["processes"]


def find_by_pid(inventory, pid):
    for process in _processes(inventory):
        if process.get("pid") == pid:
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


def filter_by_signal(inventory, signal, value=True):
    result = [
        process
        for process in _processes(inventory)
        if process.get("signals", {}).get(signal) == value
    ]

    return QueryResult(
        title=f"Signal: {signal}",
        description=f"{len(result)} process(es) matched.",
        processes=result,
        warnings=[],
    )


def filter_by_field(inventory, field, value):
    result = [
        process
        for process in _processes(inventory)
        if process.get(field) == value
    ]

    return QueryResult(
        title=f"{field} = {value}",
        description=f"{len(result)} process(es) matched.",
        processes=result,
        warnings=[],
    )


def sort_by(inventory, field, reverse=True):
    result = sorted(
        _processes(inventory),
        key=lambda p: p.get(field) or 0,
        reverse=reverse,
    )

    return QueryResult(
        title=f"Sorted by {field}",
        description=f"{len(result)} process(es).",
        processes=result,
        warnings=[],
    )


def top(inventory, field, limit=10):
    result = sorted(
        _processes(inventory),
        key=lambda p: p.get(field) or 0,
        reverse=True,
    )[:limit]

    return QueryResult(
        title=f"Top {limit} by {field}",
        description=f"{len(result)} process(es).",
        processes=result,
        warnings=[],
    )


def search(inventory, predicate):
    result = [
        process
        for process in _processes(inventory)
        if predicate(process)
    ]
    return QueryResult(
        title="Custom Search",
        description=f"{len(result)} process(es) matched.",
        processes=result,
        warnings=[],
    )

