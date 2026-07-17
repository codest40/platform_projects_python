from project.executors.query_process import (
    get_process_by_pid,
    get_waiting_processes,
    get_high_memory_processes,
)

QUESTIONS = {
    "process": {
        "question": "Show everything about a specific PID.",
        "executor": get_process_by_pid,
    },
    "waiting": {
        "question": "Show processes currently waiting.",
        "executor": get_waiting_processes,
    },
    "high_memory": {
        "question": "Show processes using the most memory.",
        "executor": get_high_memory_processes,
    },
}
