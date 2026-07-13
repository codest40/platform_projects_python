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
    analyses: list,
) -> bool | None:
    """
    Determine whether the process is multithreaded.
    """

    threads = get_analysis(
        analyses,
        ProcessThreadAnalysis,
    )

    if threads is None:
        return None

    if threads.thread_count is None:
        return None

    return threads.thread_count > 1




from project.models.processes import (
    ProcessIdentityAnalysis,
)

def is_interactive(
    analyses: list,
) -> bool | None:
    """
    Determine whether the process is interactive.
    """

    identity = get_analysis(
        analyses,
        ProcessIdentityAnalysis,
    )

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
    analyses: list,
) -> bool | None:
    """
    Determine whether the process is a system daemon.
    """

    identity = get_analysis(
        analyses,
        ProcessIdentityAnalysis,
    )

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
    analyses: list,
) -> bool | None:
    """
    Determine whether the process is running inside
    a container.
    """

    identity = get_analysis(
        analyses,
        ProcessIdentityAnalysis,
    )

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
    analyses: list,
) -> bool | None:
    """
    Determine whether the process is blocked waiting
    for a kernel resource.
    """

    scheduler = get_analysis(
        analyses,
        ProcessSchedulerAnalysis,
    )

    wait = get_analysis(
        analyses,
        ProcessWaitChannelAnalysis,
    )

    if (
        scheduler is None
        and wait is None
    ):
        return None

    # Uninterruptible sleep (D state)
    if (
        scheduler is not None
        and scheduler.state == "D"
    ):
        return True

    # Waiting in the kernel
    if (
        wait is not None
        and has_classification(
            wait,
            "waiting",
        )
    ):
        return True

    return False


from project.models.processes import (
    ProcessMemoryAnalysis,
    ProcessFdAnalysis,
    ProcessLimitsAnalysis,
)


def is_resource_constrained(
    analyses: list,
) -> bool | None:
    """
    Determine whether the process appears to be
    constrained by system resources.
    """

    memory = get_analysis(
        analyses,
        ProcessMemoryAnalysis,
    )

    fd = get_analysis(
        analyses,
        ProcessFdAnalysis,
    )

    limits = get_analysis(
        analyses,
        ProcessLimitsAnalysis,
    )

    if (
        memory is None
        and fd is None
        and limits is None
    ):
        return None

    #
    # High file descriptor utilization
    #

    if (
        fd is not None
        and isinstance(fd.fd_utilization, float)
        and fd.fd_utilization >= 0.90
    ):
        return True

    #
    # Resource limits reached/fixed
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
    analyses: list,
) -> bool | None:
    """
    Determine whether the process is approaching one
    or more configured resource limits.
    """

    fd = get_analysis(
        analyses,
        ProcessFdAnalysis,
    )

    limits = get_analysis(
        analyses,
        ProcessLimitsAnalysis,
    )

    if (
        fd is None
        and limits is None
    ):
        return None

    #
    # File descriptor utilization
    #

    if (
        fd is not None
        and isinstance(fd.fd_utilization, float)
        and fd.fd_utilization >= 0.80
    ):
        return True

    #
    # Future:
    #
    # - Stack utilization
    # - Process count utilization
    # - Address space utilization
    # - Locked memory utilization
    # - CPU time utilization
    #

    return False


from project.models.processes import (
    ProcessIoAnalysis,
)


def is_io_bound(
    analyses: list,
) -> bool | None:
    """
    Determine whether the process is I/O bound.
    """

    io = get_analysis(
        analyses,
        ProcessIoAnalysis,
    )

    if io is None:
        return None

    # Active I/O throughput
    if (
        io.io_bytes_per_sec is not None
        and io.io_bytes_per_sec > 0
    ):
        return True
    # Active I/O syscalls
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
    analyses: list,
) -> bool | None:
    """
    Determine whether the process appears to be
    CPU bound.
    """

    cpu = get_analysis(
        analyses,
        ProcessCpuAnalysis,
    )

    io = get_analysis(
        analyses,
        ProcessIoAnalysis,
    )

    if (
        cpu is None
        and io is None
    ):
        return None

    if (
        cpu is None
        or cpu.cpu_ticks_per_sec is None
        or cpu.cpu_ticks_per_sec <= 0
    ):
        return False

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
    summary,
) -> bool | None:
    """
    Determine the overall health of a process.
    """

    if all(
        value is None
        for value in (
            summary.cpu_bound,
            summary.io_bound,
            summary.blocked,
            summary.resource_constrained,
            summary.approaching_limits,
        )
    ):
        return None

    # Definitely unhealthy
    if summary.blocked:
        return False

    if summary.resource_constrained:
        return False

    # Warning state
    if summary.approaching_limits:
        return True

    return True


def calculate_confidence(
    analyses: list,
) -> str:
    """
    Estimate confidence in the process summary.

    Confidence reflects how much evidence was
    successfully collected and analyzed.
    """

    if not analyses:
        return "LOW"

    score = 0.0

    for analysis in analyses:

        if analysis.coverage == "COMPLETE":
            score += 1.0

        elif analysis.coverage == "PARTIAL":
            score += 0.5

    score /= len(analyses)

    if score >= 0.80:
        return "HIGH"

    if score >= 0.50:
        return "MEDIUM"

    return "LOW"


def calculate_severity(
    summary,
) -> str:
    """
    Determine the overall severity of the process.
    """

    if all(
        value is None
        for value in (
            summary.healthy,
            summary.blocked,
            summary.resource_constrained,
            summary.approaching_limits,
        )
    ):
        return "UNKNOWN"

    #
    # Critical
    #

    if summary.blocked:
        return "CRITICAL"

    if summary.resource_constrained:
        return "CRITICAL"

    #
    # Warning
    #

    if summary.approaching_limits:
        return "WARNING"

    #
    # Healthy
    #

    if summary.healthy:
        return "PASS"

    return "WARNING"
