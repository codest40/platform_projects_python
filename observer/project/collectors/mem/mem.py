from dataclasses import fields
from project.models.memory import MemoryData, GetMemType
from project.utils.helpers import line
from project.collectors.mem.psutil import collect_psutil_memory
from project.collectors.mem.meminfo import collect_meminfo
from project.collectors.mem.vmstat import collect_vmstat
from project.collectors.mem.pressure import collect_pressure
from project.collectors.mem.cgroup import collect_cgroup
from project.collectors.mem.numa import collect_numa
from project.collectors.mem.process import collect_process_memory
from project.utils.start_event import run_collection, run_analysis


MEMTYPE = GetMemType(
    psutil=True,
    pressure=True,
    meminfo=True,
    vmstat=True,
    cgroup=True,
    numa=True,
    process=True,
)

COLLECTORS = {
    "psutil": collect_psutil_memory,
    "pressure": collect_pressure,
    "meminfo": collect_meminfo,
    "vmstat": collect_vmstat,
    "cgroup": collect_cgroup,
    "numa": collect_numa,
    "process": collect_process_memory,
}


def collect_memory() -> MemoryData:

    memory = MemoryData()

    for field in fields(MEMTYPE):

        if not getattr(MEMTYPE, field.name):
            continue

        collector = COLLECTORS.get(field.name)

        if collector is not None:
            print(line(f"{collector.__name__}"))
            collector(memory)
    return memory


def start_memory_collection():
    result = run_collection(resource="memory", func=collect_memory)
    if result:
      print(result)

start_memory_collection()
