from project.models.processes import (
    ProcessSnapshot,
    ProcessCache,
    CollectorFailure,
)


def collect_io(
    snapshot: ProcessSnapshot,
    cache: ProcessCache,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect process I/O accounting.
    Source:
        /proc/<pid>/io
    """

    try:

        if cache.io is None:
            raise RuntimeError("/proc/<pid>/io unavailable")

        for line in cache.io.splitlines():

            key, value = line.split(":")

            value = int(value.strip())

            match key.strip():

                case "rchar":
                    snapshot.read_chars = value

                case "wchar":
                    snapshot.write_chars = value

                case "syscr":
                    snapshot.read_syscalls = value

                case "syscw":
                    snapshot.write_syscalls = value

                case "read_bytes":
                    snapshot.read_bytes = value

                case "write_bytes":
                    snapshot.write_bytes = value

                case "cancelled_write_bytes":
                    snapshot.cancelled_write_bytes = value

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_io: {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_io",
                field="io",
                reason=str(e),
            )
        )

    return snapshot
