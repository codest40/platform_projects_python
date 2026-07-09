from pathlib import Path
import os

from project.models.processes import ProcessSnapshot
CLK_TCK = os.sysconf(os.sysconf_names["SC_CLK_TCK"])


def collect_lifecycle(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
) -> ProcessSnapshot:
    """
    Collect process lifetime information.

    Source:
        /proc/<pid>/stat
        /proc/uptime
    """

    try:

        stat = (proc_dir / "stat").read_text()

        #
        # comm is enclosed in parentheses.
        #
        _, remainder = stat.rsplit(")", 1)

        fields = remainder.strip().split()

        #
        # Process start time since boot (clock ticks)
        #
        start_ticks = int(fields[19])

        #
        # System uptime (seconds)
        #
        with open("/proc/uptime") as f:
            uptime_seconds = float(f.readline().split()[0])

        #
        # Convert to seconds since boot.
        #
        snapshot.start_time = start_ticks / CLK_TCK

        #
        # Process runtime.
        #
        snapshot.runtime_seconds = max(
            0.0,
            uptime_seconds - snapshot.start_time,
        )

    except Exception as e:

        snapshot.collection_errors.append(
            f"lifecycle: {e}"
        )

    return snapshot
