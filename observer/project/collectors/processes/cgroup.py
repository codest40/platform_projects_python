from pathlib import Path
import re

from project.models.processes import ProcessSnapshot

CONTAINER_ID = re.compile(r"[a-f0-9]{64}|[a-f0-9]{32}")

def collect_cgroup(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
) -> ProcessSnapshot:
    """
    Collect process cgroup information.

    Source:
        /proc/<pid>/cgroup
    """

    try:

        content = (proc_dir / "cgroup").read_text()

        snapshot.cgroup = content.strip()

        match = CONTAINER_ID.search(content)

        if match:

            snapshot.container_id = match.group(0)

    except Exception as e:

        snapshot.collection_errors.append(
            f"cgroup: {e}"
        )

    return snapshot
