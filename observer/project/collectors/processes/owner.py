from pathlib import Path

from project.models.processes import ProcessSnapshot


def collect_owner(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
) -> ProcessSnapshot:
    """
    Collect process ownership information.

    Source:
        /proc/<pid>/status
    """

    try:

        with (proc_dir / "status").open() as f:

            for line in f:

                if line.startswith("Uid:"):

                    snapshot.uid = int(line.split()[1])

                elif line.startswith("Gid:"):

                    snapshot.gid = int(line.split()[1])

                if (
                    snapshot.uid is not None
                    and snapshot.gid is not None
                ):
                    break

    except Exception as e:

        snapshot.collection_errors.append(
            f"owner: {e}"
        )

    return snapshot
