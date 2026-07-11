from pathlib import Path
from project.models.processes import (
    ProcessSnapshot,
    CollectorFailure,
)

from project.collectors.processes.data import LIMIT_FIELDS


def _parse_limit(value: str) -> int | None:
    """
    Convert a limit value from /proc/<pid>/limits.

    unlimited -> unlimited
    numeric   -> int
    None   -> None
    """

    if value == "unlimited":
        return "unlimited"

    try:
        return int(value)
    except ValueError:
        return None


def collect_limits(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process resource limits.

    Source:
        /proc/<pid>/limits
    """

    try:

        limits_file = proc_dir / "limits"

        with limits_file.open() as f:

            # Skip header

            next(f, None)

            for line in f:

                line = line.rstrip()
                for resource, (
                    soft_attr,
                    hard_attr,
                ) in LIMIT_FIELDS.items():

                    if not line.startswith(resource):
                        continue

                    # Example:
                    # Max open files            1024    4096    files

                    values = (
                        line[len(resource):]
                        .split()
                    )

                    if len(values) < 2:
                        break

                    setattr(
                        snapshot,
                        soft_attr,
                        _parse_limit(values[0]),
                    )

                    setattr(
                        snapshot,
                        hard_attr,
                        _parse_limit(values[1]),
                    )

                    break

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_limits: {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_limits",
                field="limits",
                reason=str(e),
            )
        )

    return snapshot
