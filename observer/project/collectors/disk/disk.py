from dataclasses import fields
from project.models.disk import DiskData, GetDiskType
from project.collectors.disk.psutil import collect_psutil_disk
from project.collectors.disk.diskstat import collect_diskstats
from project.collectors.disk.pressure import collect_pressure
from project.collectors.disk.mount import collect_mounts
from project.collectors.disk.usage import collect_usage
from project.collectors.disk.cgroup import collect_cgroup
from project.collectors.disk.process import collect_process_disk
from project.analyzers.disk import analyze_disk_metrics
from project.alerts.activate_alert import activate_run_alert
from project.utils.decorators import trace
from project.utils.helpers import get_status
from project.utils.start_event import run_collection, run_analysis

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
  result = run_collection(resource="disk", func=collect_disk)
  return result

@trace("disk_pipeline")
def disk_pipeline():
  result = run_collect_disk()
  if result is None:
    print(f"❌ ERROR: Emit() response returned: {result}")
  elif result.status == get_status("FAILED"):
      print("❌ Collecting Disk Metrics Failed")
      activate_run_alert(title="Disk Metrics collection Alert", message=f"❌ Disk Metric Collection Failed: {result}", severity="CRITICAL",)
  elif result.status == get_status("SUCCESS"):
      print("✅ Disk Metrics Collection Passed")
      res = run_analysis(resource="Disk", func=analyze_disk_metrics, result=result)
      if not res:
          print("❌ Disk Analysis Failed")
      print("✅ Disk Metrics Analysis Passed")
  else:
    print(f"❌ ERROR: Emit() response returned: {result.status} \nSomething is very wrong")


#disk_pipeline()

#import reuse_pipeline_runner(kwargs) from start_event
