from pathlib import Path

from project.models.processes import ProcessSnapshot


KB = 1024


def collect_memory(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
) -> ProcessSnapshot:
    """
    Collect lightweight process memory information.
    Source:
        /proc/<pid>/status
    """

    try:

        with (proc_dir / "status").open() as f:

            for line in f:

                if line.startswith("VmRSS:"):

                    snapshot.rss_bytes = (
                        int(line.split()[1]) * KB
                    )

                elif line.startswith("VmSize:"):

                    snapshot.vms_bytes = (
                        int(line.split()[1]) * KB
                    )

                elif line.startswith("Threads:"):

                    snapshot.thread_count = int(
                        line.split()[1]
                    )

    except Exception as e:

        snapshot.collection_errors.append(
            f"memory: {e}"
        )

    return snapshot
