from pathlib import Path

from project.models.processes import ProcessSnapshot
from pathlib import Path

def collect_identity(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
) -> None:
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

        with (proc_dir / "status").open() as f:

            for line in f:

                if line.startswith("Name:"):

                    snapshot.name = line.split(":", 1)[1].strip()

                    break

    except Exception as e:

        snapshot.collection_errors.append(
            f"identity(name): {e}"
        )

    #
    # ---------------------------------------------------------
    # Command line
    # ---------------------------------------------------------
    #

    try:

        cmdline = (
            proc_dir / "cmdline"
        ).read_bytes()

        snapshot.command = cmdline.replace(
            b"\x00",
            b" "
        ).decode(
            errors="replace"
        ).strip()

    except Exception as e:

        snapshot.collection_errors.append(
            f"identity(cmdline): {e}"
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

    except Exception as e:

        snapshot.collection_errors.append(
            f"identity(exe): {e}"
        )

    return snapshot

