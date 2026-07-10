from __future__ import annotations
from project.analyzers.processes.users import get_user

from project.models.processes import (
    ProcessSnapshot,
    ProcessIdentityAnalysis,
)


def analyze_identity(
    process: ProcessSnapshot,
) -> ProcessIdentityAnalysis:
    """
    Classify process identity.
    This analyzer performs no health assessment.
    It simply answers:
        • What is this process?
        • Who owns it?
        • Where is it running?
        • Is the executable healthy?
    """

    analysis = ProcessIdentityAnalysis(
        pid=process.pid, tid=process.tid,
    )

    #
    # ---------------------------------------------------------
    # Process type
    # ---------------------------------------------------------
    #

    user = get_user(process.uid)

    if not process.command and process.executable is None:
        analysis.process_type = "kernel_thread"
        analysis.classifications.append("kernel_thread")

    elif process.container_id:
        analysis.process_type = "container_process"
        analysis.classifications.append("container_process")

    else:
        analysis.process_type = "host_process"
        analysis.classifications.append("host_process")

    #
    # ---------------------------------------------------------
    # Executable state
    # ---------------------------------------------------------
    #

    if process.executable:

        if process.executable.endswith(" (deleted)"):
            analysis.executable_state = "deleted"

        else:
            analysis.executable_state = "resolved"

    else:
        analysis.executable_state = "missing"

    #
    # ---------------------------------------------------------
    # Owner classification
    # ---------------------------------------------------------
    #

    if user is None:
        analysis.owner_type = "unknown"

    elif user.pw_name == "root":
        analysis.owner_type = "root"
        analysis.classifications.append("root_owned")

    elif user.pw_shell.endswith("nologin"):
        analysis.owner_type = "service_account"
        analysis.classifications.append("service_process")

    else:
        analysis.owner_type = "regular_user"

    #
    # ---------------------------------------------------------
    # Interactive shell
    # ---------------------------------------------------------
    #

    if process.name:

        if process.name in {
            "bash",
            "zsh",
            "fish",
            "sh",
            "dash",
        }:

            analysis.classifications.append(
                "interactive_shell"
            )

    #
    # ---------------------------------------------------------
    # System daemon
    # ---------------------------------------------------------
    #

    if (
        process.ppid == 1
        and analysis.process_type != "kernel_thread"
    ):
        analysis.classifications.append(
            "system_daemon"
        )

    if process.tid != process.pid:
        analysis.classifications.append("thread")
    else:
        analysis.classifications.append("process")

    #
    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------
    #

    if process.name:
        analysis.facts.append(
            f"Process: {process.name}"
        )

    if process.command:
        analysis.facts.append(
            f"Command: {process.command}"
        )

    if process.executable:
        analysis.facts.append(
            f"Executable: {process.executable}"
        )

    if process.uid is not None:
        analysis.facts.append(
            f"UID: {process.uid}"
        )

    if process.gid is not None:
        analysis.facts.append(
            f"GID: {process.gid}"
        )

    if process.container_id:
        analysis.facts.append(
            "Container ID detected"
        )

    if process.cgroup:
        analysis.facts.append(
            f"Cgroup: {process.cgroup}"
        )

    return analysis
