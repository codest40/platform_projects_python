from __future__ import annotations

from project.analyzers.processes.users import get_user
from project.analyzers.utils.process_coverage import Coverage
from project.models.processes import (
    ProcessSnapshot,
    ProcessIdentityAnalysis,
    TotalMetrics,
    ObserverState as OB,
)


def analyze_identity(
    process: ProcessSnapshot,
    metrics: TotalMetrics,
) -> ProcessIdentityAnalysis:
    """
    Analyze process identity.

    Answers:
        - What is this process?
        - Who owns it?
        - Where is it running?
        - Is the executable healthy?
    """

    analysis = ProcessIdentityAnalysis(
        pid=process.pid,
        tid=process.tid,
    )

    coverage = Coverage()

    # ---------------------------------------------------------
    # Copy identity information
    # ---------------------------------------------------------

    analysis.name = process.name
    analysis.command = process.command
    analysis.executable_state = process.executable
    analysis.uid = process.uid
    analysis.gid = process.gid
    analysis.container_id = process.container_id
    analysis.cgroup = process.cgroup


    # ---------------------------------------------------------
    # Process Type
    # ---------------------------------------------------------

    coverage.check(
        process.command not in OB.values
        or process.executable not in OB.values
    )

    user = get_user(process.uid) if process.uid not in OB.values else get_user(None)

    kernel_thread = (
        process.command in OB.values
        and process.executable in OB.values
    )

    analysis.signals["is_kernel_thread"] = kernel_thread

    if kernel_thread:

        analysis.process_type = "kernel_thread"
        analysis.classifications.append(
            "kernel_thread"
        )


    elif process.container_id not in OB.values:

        analysis.signals["is_container_process"] = True

        analysis.process_type = "container_process"
        analysis.classifications.append(
            "container_process"
        )


    else:

        analysis.signals["is_host_process"] = True

        analysis.process_type = "host_process"
        analysis.classifications.append(
            "host_process"
        )


    # ---------------------------------------------------------
    # Executable State
    # ---------------------------------------------------------

    coverage.check(
        process.executable not in OB.values
    )

    if process.executable not in OB.values:

        deleted = (
            process.executable.endswith(
                " (deleted)"
            )
        )

        analysis.signals[
            "is_executable_deleted"
        ] = deleted


        if deleted:

            analysis.executable_state = "deleted"

            analysis.classifications.append(
                "deleted_executable"
            )

            analysis.recommendations.append(
                "Investigate why the process is running a deleted executable."
            )


        else:

            analysis.executable_state = "resolved"

            analysis.classifications.append(
                "valid_executable"
            )


    else:

        analysis.signals[
            "is_executable_deleted"
        ] = OB.NA

        analysis.executable_state = "missing"



    # ---------------------------------------------------------
    # Owner
    # ---------------------------------------------------------

    if user is None:

        analysis.signals[
            "is_unknown_owner"
        ] = True

        analysis.owner_type = "unknown"

        analysis.classifications.append(
            "unknown_owner"
        )


    else:

        analysis.signals[
            "is_unknown_owner"
        ] = False


        if user.pw_name == "root":

            analysis.signals[
                "is_root_owned"
            ] = True

            analysis.owner_type = "root"

            analysis.classifications.append(
                "root_owned"
            )


        elif user.pw_shell.endswith(
            "nologin"
        ):

            analysis.signals[
                "is_service_account"
            ] = True

            analysis.owner_type = (
                "service_account"
            )

            analysis.classifications.append(
                "service_process"
            )


        else:

            analysis.signals[
                "is_root_owned"
            ] = False

            analysis.signals[
                "is_service_account"
            ] = False

            analysis.owner_type = (
                "regular_user"
            )



    # ---------------------------------------------------------
    # Interactive Shell
    # ---------------------------------------------------------

    shells = {
        "bash",
        "zsh",
        "fish",
        "sh",
        "dash",
    }

    if process.name not in OB.values:

        interactive = (
            process.name in shells
        )

        analysis.signals[
            "is_interactive_shell"
        ] = interactive


        if interactive:

            analysis.classifications.append(
                "interactive_shell"
            )

    else:

        analysis.signals[
            "is_interactive_shell"
        ] = OB.NA



    # ---------------------------------------------------------
    # System Daemon
    # ---------------------------------------------------------

    if (
        process.ppid is not None
        and process.ppid == 1
        and not kernel_thread
    ):

        analysis.signals[
            "is_system_daemon"
        ] = True

        analysis.classifications.append(
            "system_daemon"
        )

    else:

        analysis.signals[
            "is_system_daemon"
        ] = False



    # ---------------------------------------------------------
    # Process / Thread
    # ---------------------------------------------------------

    if process.tid is not None:

        is_thread = (
            process.tid != process.pid
        )

        analysis.signals[
            "is_thread"
        ] = is_thread


        if is_thread:

            analysis.classifications.append(
                "thread"
            )

        else:

            analysis.classifications.append(
                "process"
            )

    else:

        analysis.signals[
            "is_thread"
        ] = OB.NA



    # ---------------------------------------------------------
    # Facts
    # ---------------------------------------------------------

    if process.name:
        analysis.facts.append(
            f"Process name: {process.name}"
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
            f"Container ID: {process.container_id}"
        )

    if process.cgroup:
        analysis.facts.append(
            f"Cgroup: {process.cgroup}"
        )


    coverage.apply(metrics)
    analysis.coverage = coverage.score(metrics)
    return analysis
