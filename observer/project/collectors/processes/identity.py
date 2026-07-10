from pathlib import Path
from project.models.processes import ProcessSnapshot, CollectorFailure, ProcessCache


def collect_identity(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
    cache: ProcessCache,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Populate process identity fields.
    Reads inexpensive identity information that uniquely identifies
    the process.
    """

    #
    # ---------------------------------------------------------
    # Process name
    # ---------------------------------------------------------
    #

    try:
        if cache.status is None:
            raise RuntimeError("/proc/<pid>/status unavailable")

        status = cache.status.splitlines()
        for line in status:

                if line.startswith("Name:"):

                    snapshot.name = line.split(":", 1)[1].strip()
                    break

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_identity(name): {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_identity",
                field="statue[name]",
                reason=str(e),
            )
        )

    #
    # ---------------------------------------------------------
    # Command line
    # ---------------------------------------------------------
    #

    try:
        if cache.cmdline is None:
            raise RuntimeError("/proc/<pid>/cmdline unavailable")

        cmdline = cache.cmdline

        snapshot.command = (
            cmdline
            .replace(b"\x00", b" ")
            .decode(errors="replace")
            .strip()
        )

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_identity(cmdline): {e}"
        )
        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_identity",
                field="cmdline",
                reason=str(e),
            )
        )

    #
    # ---------------------------------------------------------
    # Executable
    # ---------------------------------------------------------
    #

    try:

        snapshot.executable = (
            proc_dir / "exe"
        ).resolve().as_posix()

    #
    # Expected on many Linux systems.
    #
    except (PermissionError, FileNotFoundError) as e:
      if isinstance(e, PermissionError):
             reason="permission denied"
      else:
             reason="File Not Found"

      collector_failures.append(
            CollectorFailure(
              pid=snapshot.pid,
              collector="ps_identity",
              field="executable",
              reason=reason,
            )
      )

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_identity(exe): {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_identity",
                field="executable",
                reason=str(e),
            )
        )

    return snapshot
