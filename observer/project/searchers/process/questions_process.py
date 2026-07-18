from project.searchers.process.executors import (
    process_by_pid,
    waiting_processes,
    highest_memory_processes,
    root_processes,
)

from .format_process import format_process
from .format_waiting import format_waiting
from .format_high_memory import format_high_memory
from .format_root import format_root


QUESTIONS = {
    "process": {
        "question": "Show everything about a specific PID.",
        "executor": process_by_pid,
        "formatter": format_process,
    },

    "waiting": {
        "question": "Show waiting processes.",
        "executor": waiting_processes,
        "formatter": format_waiting,
    },

    "high_memory": {
        "question": "Show highest memory processes.",
        "executor": highest_memory_processes,
        "formatter": format_high_memory,
    },

    "root": {
        "question": "Show root-owned processes.",
        "executor": root_processes,
        "formatter": format_root,
    },
}
