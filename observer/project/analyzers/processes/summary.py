from __future__ import annotations

from project.models.processes import (
    ProcessSnapshot,
    ProcessSummary,
)


# ==========================================================
# Health
# ==========================================================

def process_health(summary, analyses):
    """
    Overall process health.
    """
    pass


# ==========================================================
# CPU
# ==========================================================

def process_cpu_behavior(summary, analyses):
    """
    Is this process CPU bound?
    """
    pass


# ==========================================================
# I/O
# ==========================================================

def process_io_behavior(summary, analyses):
    """
    Is this process I/O bound?
    """
    pass


# ==========================================================
# Waiting
# ==========================================================

def process_wait_behavior(summary, analyses):
    """
    Is the process blocked?
    """
    pass


# ==========================================================
# Threading
# ==========================================================

def process_threading(summary, analyses):
    """
    Thread topology.
    """
    pass


# ==========================================================
# Identity
# ==========================================================

def process_identity(summary, analyses):
    """
    Container / daemon / shell / kernel thread.
    """
    pass


# ==========================================================
# Resources
# ==========================================================

def process_resources(summary, analyses):
    """
    Memory / FD resource usage.
    """
    pass


# ==========================================================
# Limits
# ==========================================================

def process_limits(summary, analyses):
    """
    Resource limits.
    """
    pass


# ==========================================================
# Coverage
# ==========================================================

def process_coverage(summary, analyses):
    """
    Analyzer coverage.
    """
    pass


def find_analysis(
    analyses: list,
    analysis_type,
):
    """
    Return the first analysis matching a type.
    """

    for analysis in analyses:

        if isinstance(analysis, analysis_type):
            return analysis

    return None

def summarize_process(
    process: ProcessSnapshot,
    analyses: list,
) -> ProcessSummary:
    """
    Produce a high-level diagnosis for a process.

    This answers questions such as:

        Is this process healthy?
        Is it CPU-bound?
        Is it I/O-bound?
        Is it blocked?
        Is it multithreaded?
        Is it interactive?
        Is it a daemon?
        Is it a container process?
        Is it resource constrained?
        Is it approaching limits?
    """

    summary = ProcessSummary(
        pid=process.pid,
        tid=process.tid,
    )

    process_health(summary, analyses)

    process_cpu_behavior(summary, analyses)

    process_io_behavior(summary, analyses)

    process_wait_behavior(summary, analyses)

    process_threading(summary, analyses)

    process_identity(summary, analyses)

    process_resources(summary, analyses)

    process_limits(summary, analyses)

    process_coverage(summary, analyses)

    return summary
