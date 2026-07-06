from dataclasses import fields
from project.models.disk import DiskData, GetDiskType
from project.collectors.disk.psutil import collect_psutil_disk
from project.collectors.disk.diskstat import collect_diskstats
from project.collectors.disk.pressure import collect_pressure
from project.collectors.disk.mount import collect_mounts
from project.collectors.disk.usage import collect_usage
from project.collectors.disk.cgroup import collect_cgroup
from project.collectors.disk.process import collect_process_disk
from project.analyzers.disk.disk import analyze_disk_metrics
from project.utils.decorators import trace
from project.utils.pipeline import pipeline_runner
from project.collectors.disk.filter import filter_disk_state, compute_disk_rates

DISKTYPE = GetDiskType(
    psutil=True,
    diskstats=True,
    pressure=True,
    mounts=True,
    filesystems=True,
    process=True,
    cgroup=True,
)


COLLECTORS = {
    "psutil": collect_psutil_disk,
    "diskstats": collect_diskstats,
    "pressure": collect_pressure,
    "mounts": collect_mounts,
    "filesystems": collect_usage,
    "process": collect_process_disk,
    "cgroup": collect_cgroup,
}


@trace("disk")
def collect_disk() -> DiskData:

    disk = DiskData()

    for field in fields(DISKTYPE):

        if not getattr(DISKTYPE, field.name):
            continue

        collector = COLLECTORS.get(field.name)

        if collector is None:
            continue

        collector(disk)

    return disk


@trace("run_disk")
def run_collect_disk():
  result = pipeline_runner(
      resource="disk",
      collect=collect_disk,
      analyze=analyze_disk_metrics,
      filter=filter_disk_state,
      compute=compute_disk_rates,
      extra=run_collect_disk,
  )

  return result

@trace("disk_pipeline")
def disk_pipeline():
  result = run_collect_disk()
  print("DONE")

disk_pipeline()

