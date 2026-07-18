from project.executors.query_process import (
    find_by_pid,
    filter_by_signal,
    filter_by_field,
    top,
)

def process_by_pid(inv, pid):
    return find_by_pid(inv, pid)


def waiting_processes(inv):
    return filter_by_signal(
        inv,
        "is_waiting",
    )


def highest_memory_processes(inv):
    return top(
        inv,
        "rss_bytes",
        10,
    )


def root_processes(inv):
    return filter_by_field(
        inv,
        "owner_type",
        "root",
    )
