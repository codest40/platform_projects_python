from __future__ import annotations
from typing import Type


# ==========================================================
# Analysis Lookup
# ==========================================================

def get_analysis(
    analyses: list,
    analysis_type: Type,
):
    """
    Return the requested analysis object.
    """

    for analysis in analyses:

        if isinstance(
            analysis,
            analysis_type,
        ):
            return analysis

    return None


# ==========================================================
# Classification Helpers
# ==========================================================

def has_classification(
    analysis,
    classification: str,
) -> bool:
    """
    Return True if an analysis contains a classification.
    """

    if analysis is None:
        return False

    return (
        classification
        in analysis.classifications
    )


# ==========================================================
# Fact Helpers
# ==========================================================

def has_fact(
    analysis,
    text: str,
) -> bool:
    """
    Return True if an analysis contains a fact.
    """

    if analysis is None:
        return False

    return any(
        text in fact
        for fact in analysis.facts
    )


# ==========================================================
# Coverage
# ==========================================================

def coverage_percent(
    analysis,
) -> float | None:
    """
    Percentage of metrics successfully analyzed.
    """

    if analysis is None:
        return None

    expected = analysis.metrics_expected
    available = analysis.metrics_available

    if (
        expected is None
        or available is None
        or expected == 0
    ):
        return None

    return (
        available / expected
    ) * 100


from project.models.processes import (
    ProcessThreadAnalysis,
)


def is_multithreaded(
    threads: ProcessThreadAnalysis | None,
) -> bool | None:
    """
    Determine whether the process is multithreaded.
    """

    if threads is None:
        return None

    if threads.thread_count is None:
        return None

    return threads.thread_count > 1



from project.models.processes import (
    ProcessIdentityAnalysis,
)


def is_interactive(
    identity: ProcessIdentityAnalysis | None,
) -> bool | None:
    """
    Determine whether the process is interactive.
    """

    if identity is None:
        return None

    return has_classification(
        identity,
        "interactive_shell",
    )


from project.models.processes import (
    ProcessIdentityAnalysis,
)


def is_daemon(
    identity: ProcessIdentityAnalysis | None,
) -> bool | None:
    """
    Determine whether the process is a system daemon.
    """

    if identity is None:
        return None

    return has_classification(
        identity,
        "system_daemon",
    )



from project.models.processes import (
    ProcessIdentityAnalysis,
)


def is_container(
    identity: ProcessIdentityAnalysis | None,
) -> bool | None:
    """
    Determine whether the process is running inside a container.
    """

    if identity is None:
        return None

    return has_classification(
        identity,
        "container_process",
    )


from project.models.processes import (
    ProcessSchedulerAnalysis,
    ProcessWaitChannelAnalysis,
)


def is_blocked(
    scheduler: ProcessSchedulerAnalysis | None,
    wait: ProcessWaitChannelAnalysis | None,
) -> bool | None:
    """
    Determine whether the process is blocked waiting
    for a kernel resource.
    """

    if scheduler is None and wait is None:
        return None

    #
    # Uninterruptible sleep
    #

    if (
        scheduler is not None
        and scheduler.state == "D"
    ):
        return True

    #
    # Waiting in kernel
    #

    if (
        wait is not None
        and "waiting" in wait.classifications
    ):
        return True

    return False


from project.models.processes import (
    ProcessMemoryAnalysis,
    ProcessFdAnalysis,
    ProcessLimitsAnalysis,
)


def is_resource_constrained(
    memory: ProcessMemoryAnalysis | None,
    fd: ProcessFdAnalysis | None,
    limits: ProcessLimitsAnalysis | None,
) -> bool | None:
    """
    Determine whether the process appears to be
    constrained by system resources.
    """

    if (
        memory is None
        and fd is None
        and limits is None
    ):
        return None

    #
    # High FD usage
    #

    if (
        fd is not None
        and fd.fd_utilization is not None
        and fd.fd_utilization != "N/A"
        and fd.fd_utilization >= 0.90
    ):
        return True

    #
    # Finite resource limits
    #

    if limits is not None:

        for classification in limits.classifications:

            if classification.endswith("_fixed"):
                return True

    return False


from project.models.processes import (
    ProcessFdAnalysis,
    ProcessLimitsAnalysis,
)


def is_approaching_limits(
    fd: ProcessFdAnalysis | None,
    limits: ProcessLimitsAnalysis | None,
) -> bool | None:
    """
    Determine whether the process is approaching one
    or more configured resource limits.
    """

    if (
        fd is None
        and limits is None
    ):
        return None

    #
    # File descriptors
    #

    if (
        fd is not None
        and isinstance(fd.fd_utilization, float)
        and fd.fd_utilization >= 0.80
    ):
        return True

    return False

from project.models.processes import (
    ProcessIoAnalysis,
)


def is_io_bound(
    io: ProcessIoAnalysis | None,
) -> bool | None:
    """
    Determine whether the process is I/O bound.
    """

    if io is None:
        return None

    #
    # Active I/O
    #

    if (
        io.io_bytes_per_sec is not None
        and io.io_bytes_per_sec > 0
    ):
        return True

    if (
        io.io_syscalls_per_sec is not None
        and io.io_syscalls_per_sec > 0
    ):
        return True

    return False


from project.models.processes import (
    ProcessCpuAnalysis,
    ProcessIoAnalysis,
)


def is_cpu_bound(
    cpu: ProcessCpuAnalysis | None,
    io: ProcessIoAnalysis | None,
) -> bool | None:
    """
    Determine whether the process appears to be
    CPU bound.
    """

    if cpu is None and io is None:
        return None

    #
    # No CPU activity
    #

    if (
        cpu is None
        or cpu.cpu_ticks_per_sec is None
        or cpu.cpu_ticks_per_sec <= 0
    ):
        return False

    #
    # Significant I/O means it is probably
    # not CPU-bound.
    #

    if io is not None:

        if (
            io.io_bytes_per_sec is not None
            and io.io_bytes_per_sec > 0
        ):
            return False

        if (
            io.io_syscalls_per_sec is not None
            and io.io_syscalls_per_sec > 0
        ):
            return False

    return True



def is_process_healthy(
    *,
    cpu_bound: bool | None,
    io_bound: bool | None,
    blocked: bool | None,
    resource_constrained: bool | None,
    approaching_limits: bool | None,
) -> bool | None:
    """
    Determine the overall health of a process.
    """

    if all(
        value is None
        for value in (
            cpu_bound,
            io_bound,
            blocked,
            resource_constrained,
            approaching_limits,
        )
    ):
        return None

    #
    # Definitely unhealthy
    #

    if blocked:
        return False

    if resource_constrained:
        return False

    #
    # Warning state
    #

    if approaching_limits:
        return True

    return True


def calculate_confidence(
    analyses: list,
) -> str:
    """
    Estimate confidence in the process summary.

    Confidence reflects how much evidence was available,
    not whether the process is healthy.
    """

    if not analyses:
        return "LOW"

    total = len(analyses)

    complete = 0.0

    for analysis in analyses:

        coverage = getattr(
            analysis,
            "coverage",
            None,
        )

        if coverage == "COMPLETE":
            complete += 1.0

        elif coverage == "PARTIAL":
            complete += 0.5

    score = complete / total

    if score >= 0.80:
        return "HIGH"

    if score >= 0.50:
        return "MEDIUM"

    return "LOW"


def calculate_severity(
    *,
    healthy: bool | None,
    blocked: bool | None,
    resource_constrained: bool | None,
    approaching_limits: bool | None,
) -> str:
    """
    Determine the overall process severity.
    """

    if all(
        value is None
        for value in (
            healthy,
            blocked,
            resource_constrained,
            approaching_limits,
        )
    ):
        return "UNKNOWN"

    #
    # Critical
    #

    if blocked:
        return "CRITICAL"

    if resource_constrained:
        return "CRITICAL"

    #
    # Warning
    #

    if approaching_limits:
        return "WARNING"

    #
    # Healthy
    #

    if healthy:
        return "PASS"

    return "WARNING"


