from pathlib import Path

from project.models.processes import ProcessSnapshot


def collect_cpu(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
) -> ProcessSnapshot:
    """
    Collect lightweight CPU accounting information.

    Source:
        /proc/<pid>/stat
    """

    try:

        stat = (proc_dir / "stat").read_text()

        #
        # comm is enclosed in parentheses and may contain spaces.
        #
        _, remainder = stat.rsplit(")", 1)

        fields = remainder.strip().split()

        #
        # utime (field 14)
        #
        snapshot.user_ticks = int(fields[11])

        #
        # stime (field 15)
        #
        snapshot.system_ticks = int(fields[12])

    except Exception as e:

        snapshot.collection_errors.append(
            f"cpu: {e}"
        )

    return snapshot
