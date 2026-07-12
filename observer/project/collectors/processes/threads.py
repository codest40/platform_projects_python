from pathlib import Path

from project.models.processes import (
    ProcessSnapshot,
    ThreadSnapshot,
    CollectorFailure,
)


def collect_threads(
    snapshot: ProcessSnapshot,
    proc_dir: Path,
    collector_failures: list[CollectorFailure],
) -> ProcessSnapshot:
    """
    Collect thread inventory.
    Sources
        /proc/<pid>/task/<tid>/stat
        /proc/<pid>/task/<tid>/status
        /proc/<pid>/task/<tid>/wchan
    """

    try:

        task_dir = proc_dir / "task"

        snapshot.threads = []

        for thread_dir in sorted(
            task_dir.iterdir(),  key=lambda p: int(p.name),
        ):
            if not thread_dir.name.isdigit():
                continue

            tid = int(thread_dir.name)

            thread = ThreadSnapshot(
                tid=tid,
            )

            # -------------------------
            # stat
            # -------------------------

            try:

                stat = (
                    thread_dir / "stat"
                ).read_text()

                fields = stat.split()
                right = stat.rfind(")")
                rest = stat[right + 2:].split()
                thread.state = rest[0]
                thread.user_ticks = int(rest[11])
                thread.system_ticks = int(rest[12])
                thread.priority = int(rest[15])
                thread.nice = int(rest[16])
                thread.start_time = int(rest[19])
                thread.processor = int(rest[36])
                thread.rt_priority = int(rest[37])
                thread.policy = int(rest[38])

            except Exception:
                pass

            # -------------------------
            # status
            # -------------------------
            try:

                status = (
                    thread_dir / "status"
                ).read_text()

                for line in status.splitlines():

                    if line.startswith("Name:"):
                        thread.name = line.split()[1]

                    elif line.startswith("Uid:"):
                        thread.uid = int(
                            line.split()[1]
                        )
                    elif line.startswith("voluntary_ctxt_switches:"):
                        thread.voluntary_context_switches = int(line.split()[1])

                    elif line.startswith("nonvoluntary_ctxt_switches:"):
                        thread.involuntary_context_switches = int(line.split()[1])

            except Exception:
                pass

            # -------------------------
            # wchan
            # -------------------------
            try:

                wchan = (
                    thread_dir / "wchan"
                ).read_text().strip()

                thread.wchan = wchan

            except Exception:
                pass

            snapshot.threads.append(thread)

        snapshot.thread_count = len(
            snapshot.threads
        )

    except Exception as e:

        snapshot.collection_errors.append(
            f"ps_threads: {e}"
        )

        collector_failures.append(
            CollectorFailure(
                pid=snapshot.pid,
                collector="ps_threads",
                field="task",
                reason=str(e),
            )
        )

    if (
        snapshot.thread_count is not None
        and snapshot.threads is not None
    ):
      if snapshot.thread_count != len(snapshot.threads):
          snapshot.collection_errors.append("ERROR: Thread count mismatch")

      snapshot.running_threads = sum(t.state == "R" for t in snapshot.threads)
      snapshot.sleeping_threads = sum(t.state == "S" for t in snapshot.threads)
      snapshot.uninterruptible_threads = sum(t.state == "D" for t in snapshot.threads)
      snapshot.idle_threads = sum(t.state == "I" for t in snapshot.threads)
      snapshot.zombie_threads = sum(t.state == "Z" for t in snapshot.threads)

    return snapshot
