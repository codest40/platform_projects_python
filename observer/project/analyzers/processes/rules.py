from __future__ import annotations
from typing import Type
from project.analyzers.processes.data import ANALYZER_SIGNALS
from project.models.processes import (
    ProcessCpuAnalysis,
    ProcessMemoryAnalysis,
    ProcessFdAnalysis,
    ProcessIoAnalysis,
    ProcessSchedulerAnalysis,
    ProcessThreadAnalysis,
    ProcessIdentityAnalysis,
    ProcessWaitChannelAnalysis,
    ProcessLimitsAnalysis,
    ObserverState as OB,
)

CPU = ANALYZER_SIGNALS["analyze_cpu"]
MEM = ANALYZER_SIGNALS["analyze_memory"]
FD = ANALYZER_SIGNALS["analyze_fd"]
IO = ANALYZER_SIGNALS["analyze_io"]
SCHED = ANALYZER_SIGNALS["analyze_scheduler"]
THREAD = ANALYZER_SIGNALS["analyze_threads"]
IDENTITY = ANALYZER_SIGNALS["analyze_identity"]
WAIT = ANALYZER_SIGNALS["analyze_wait_channel"]
LIMIT = ANALYZER_SIGNALS["analyze_limits"]



def get_signal(
    analyses: list,
    analysis_type: Type,
    signal: str,
) -> bool | str | None:

    analysis = get_analysis(
        analyses,
        analysis_type,
    )
    if analysis is None:
        return None
    return analysis.signals.get(signal)

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

def unavailable(*values):
    """
    Collapse unavailable observer states into one.
    """
    if all(value == OB.UNSEEN for value in values):
        return OB.UNSEEN
    if all(value in OB.values for value in values):
        return OB.NA
    return False


def is_multithreaded(
    analyses: list,
) -> bool | str | None:
    """
    Determine whether the process is multithreaded.
    """
    return get_signal(
        analyses,
        ProcessThreadAnalysis,
        THREAD["MULTITHREADED"],
    )


def is_interactive(
    analyses: list,
) -> bool | str | None:
    """
    Determine whether the process is an interactive shell.
    """
    return get_signal(
        analyses,
        ProcessIdentityAnalysis,
        IDENTITY["INTERACTIVE_SHELL"],
    )


def is_daemon(
    analyses: list,
) -> bool | str | None:
    """
    Determine whether the process is a system daemon.
    """
    return get_signal(
        analyses,
        ProcessIdentityAnalysis,
        IDENTITY["SYSTEM_DAEMON"],
    )

def is_container(
    analyses: list,
) -> bool | str | None:
    """
    Determine whether the process is running inside
    a container.
    """
    return get_signal(
        analyses,
        ProcessIdentityAnalysis,
        IDENTITY["CONTAINER_PROCESS"],
    )


def is_blocked(
    analyses: list,
) -> bool | str | None:
    """
    Determine whether the process is blocked
    waiting for a kernel resource.
    """
    scheduler = get_signal(
        analyses,
        ProcessSchedulerAnalysis,
        SCHED["WAITING_ON_IO"],
    )

    wait = get_signal(
        analyses,
        ProcessWaitChannelAnalysis,
        WAIT["WAITING"],
    )
    if scheduler is True:
        return True
    if wait is True:
        return True
    if scheduler in OB.values and wait in OB.values:
        return OB.NA
    return False


def is_cpu_bound(
    analyses: list,
) -> bool | str | None:
    """
    Determine whether the process is CPU-bound.
    """
    return get_signal(
        analyses,
        ProcessCpuAnalysis,
        CPU["CPU_BOUND"],
    )


def is_io_bound(
    analyses: list,
) -> bool | str | None:
    """
    Determine whether the process is I/O-bound.
    """
    return get_signal(
        analyses,
        ProcessIoAnalysis,
        IO["IO_HEAVY"],
    )


def is_resource_constrained(
    analyses: list,
) -> bool | str | None:
    """
    Determine whether the process is constrained by
    one or more system resources.
    """
    signals = (
        get_signal(
            analyses,
            ProcessFdAnalysis,
            FD["FD_LIMIT_REACHED"],
        ),
        get_signal(
            analyses,
            ProcessFdAnalysis,
            FD["FD_EXHAUSTED"],
        ),
        get_signal(
            analyses,
            ProcessFdAnalysis,
            FD["LOW_FD_AVAILABILITY"],
        ),
        get_signal(
            analyses,
            ProcessMemoryAnalysis,
            MEM["MEMORY_FRAGMENTED"],
        ),
        get_signal(
            analyses,
            ProcessCpuAnalysis,
            CPU["CPU_TIME_LIMIT_REACHED"],
        ),
        get_signal(
            analyses,
            ProcessSchedulerAnalysis,
            SCHED["WAITING_ON_IO"],
        ),
    )

    if any(signal is True for signal in signals):
        return True
    unavailable_state = unavailable(*signals)
    if unavailable_state:
        return unavailable_state
    return False


def is_approaching_limits(
    analyses: list,
) -> bool | str | None:
    """
    Determine whether the process is approaching one
    or more configured resource limits.
    """
    signals = (
        get_signal(
            analyses,
            ProcessFdAnalysis,
            FD["NEAR_FD_LIMIT"],
        ),
        get_signal(
            analyses,
            ProcessFdAnalysis,
            FD["LOW_FD_AVAILABILITY"],
        ),
    )
    if any(signal is True for signal in signals):
        return True

    unavailable_state = unavailable(*signals)
    if unavailable_state:
        return unavailable_state
    return False

