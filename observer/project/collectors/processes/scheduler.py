from pathlib import Path

from project.models.processes import ProcessSnapshot


def collect_scheduler(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
) -> ProcessSnapshot:
    """
    Collect scheduler-related process attributes.

    Source:
        /proc/<pid>/stat
    """

    try:

        stat = (proc_dir / "stat").read_text()

        #
        # comm is enclosed in parentheses and may contain spaces.
        # Split after the closing parenthesis.
        #
        _, remainder = stat.rsplit(")", 1)

        fields = remainder.strip().split()

        #
        # Fields after removing:
        # pid (already known)
        # comm (...)
        #

        snapshot.state = fields[0]
        snapshot.ppid = int(fields[1])

        #
        # priority (field 18)
        #
        snapshot.priority = int(fields[15])

        #
        # nice (field 19)
        #
        snapshot.nice = int(fields[16])

        #
        # last CPU the process executed on
        # processor (field 39)
        #
        snapshot.processor = int(fields[36])

    except Exception as e:

        snapshot.collection_errors.append(
            f"scheduler: {e}"
        )

    return snapshot
