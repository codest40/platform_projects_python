

LIMITS = [
    (
        "max_cpu_time",
        "CPU time",
        "max_cpu_time_soft",
        "max_cpu_time_hard",
    ),
    (
        "max_file_size",
        "File size",
        "max_file_size_soft",
        "max_file_size_hard",
    ),
    (
        "max_stack_size",
        "Stack size",
        "max_stack_size_soft",
        "max_stack_size_hard",
    ),
    (
        "max_core_file_size",
        "Core file size",
        "max_core_file_size_soft",
        "max_core_file_size_hard",
    ),
    (
        "max_locked_memory",
        "Locked memory",
        "max_locked_memory_soft",
        "max_locked_memory_hard",
    ),
    (
        "max_processes",
        "Processes",
        "max_processes_soft",
        "max_processes_hard",
    ),
    (
        "max_fds",
        "Open files",
        "max_fds_soft",
        "max_fds_hard",
    ),
    (
        "max_address_space",
        "Address space",
        "max_address_space_soft",
        "max_address_space_hard",
    ),
]



ANALYZER_SIGNALS = {
    "analyze_cpu": {
        "CPU_HIGH": "is_cpu_high",
        "CPU_IDLE": "is_cpu_idle",
        "CPU_RUNNING": "is_cpu_running",
        "CPU_BOUND": "is_cpu_bound",
        "HIGH_PRIORITY": "is_high_priority",
        "REALTIME_PROCESS": "is_realtime_process",
        "CPU_TIME_LIMIT_REACHED": "is_cpu_time_limit_reached",
        "LONG_RUNNING": "is_long_running",
        "USER_CPU_HEAVY": "is_user_cpu_heavy",
        "KERNEL_CPU_HEAVY": "is_kernel_cpu_heavy",
    },

    "analyze_memory": {
        "MEMORY_ALLOCATED": "is_memory_allocated",
        "MEMORY_LARGE": "is_memory_large",
        "VIRTUAL_MEMORY_LARGE": "is_virtual_memory_large",
        "MEMORY_FRAGMENTED": "is_memory_fragmented",
        "MULTITHREADED": "is_multithreaded",
        "SINGLE_THREADED": "is_single_threaded",
    },

    "analyze_fd": {
        "HAS_OPEN_FDS": "has_open_fds",
        "HIGH_FD_USAGE": "is_high_fd_usage",
        "NEAR_FD_LIMIT": "is_near_fd_limit",
        "FD_LIMIT_REACHED": "is_fd_limit_reached",
        "FD_LIMIT_UNLIMITED": "is_fd_limit_unlimited",
        "LOW_FD_AVAILABILITY": "is_low_fd_availability",
        "FD_EXHAUSTED": "is_fd_exhausted",
    },

    "analyze_io": {
        "READ_ACTIVE": "is_read_active",
        "WRITE_ACTIVE": "is_write_active",
        "IO_HEAVY": "is_io_heavy",
        "READ_HEAVY": "is_read_heavy",
        "WRITE_HEAVY": "is_write_heavy",
        "IO_SYSCALL_HEAVY": "is_io_syscall_heavy",
        "CANCELLED_WRITES": "has_cancelled_writes",
        "SMALL_IO_PATTERN": "is_small_io_pattern",
        "LARGE_IO_PATTERN": "is_large_io_pattern",
    },

    "analyze_scheduler": {
        "RUNNING": "is_running",
        "SLEEPING": "is_sleeping",
        "WAITING_ON_IO": "is_waiting_on_io",
        "STOPPED": "is_stopped",
        "ZOMBIE": "is_zombie",
        "HIGH_PRIORITY": "has_high_priority",
        "NEGATIVE_NICE": "has_negative_nice",
        "REALTIME_PROCESS": "is_realtime_process",
        "FIFO": "uses_fifo_scheduler",
        "ROUND_ROBIN": "uses_round_robin_scheduler",
        "DEADLINE": "uses_deadline_scheduler",
        "LONG_RUNNING": "is_long_running",
    },

    "analyze_threads": {
        "MULTITHREADED": "is_multithreaded",
        "SINGLE_THREADED": "is_single_threaded",
        "THREAD_GROUP_LEADER": "is_thread_group_leader",
        "WORKER_THREAD": "is_worker_thread",
        "SESSION_LEADER": "is_session_leader",
        "PROCESS_GROUP_LEADER": "is_process_group_leader",
        "FOREGROUND_PROCESS_GROUP": "is_foreground_process_group",
        "BACKGROUND_PROCESS_GROUP": "is_background_process_group",
        "RUNNING_THREADS": "has_running_threads",
        "SLEEPING_THREADS": "has_sleeping_threads",
        "BLOCKED_THREADS": "has_blocked_threads",
        "ZOMBIE_THREADS": "has_zombie_threads",
        "IDLE_THREADS": "has_idle_threads",
    },

    "analyze_wait_channel": {
        "WAITING": "is_waiting",
    },

    "analyze_identity": {
        "KERNEL_THREAD": "is_kernel_thread",
        "CONTAINER_PROCESS": "is_container_process",
        "HOST_PROCESS": "is_host_process",
        "EXECUTABLE_DELETED": "is_executable_deleted",
        "UNKNOWN_OWNER": "is_unknown_owner",
        "ROOT_OWNED": "is_root_owned",
        "SERVICE_ACCOUNT": "is_service_account",
        "INTERACTIVE_SHELL": "is_interactive_shell",
        "SYSTEM_DAEMON": "is_system_daemon",
        "THREAD": "is_thread",
    },

    "analyze_limits": {
        "SOFT_UNLIMITED": "is_<prefix>_soft_unlimited",
        "HARD_UNLIMITED": "is_<prefix>_hard_unlimited",
        "LOCKED": "is_<prefix>_locked",
        "ADJUSTABLE": "is_<prefix>_adjustable",
    },
}
