from dataclasses import fields
from project.models.memory import MemoryData, GetMemType
from project.collectors.mem.psutil import collect_psutil_memory
from project.collectors.mem.meminfo import collect_meminfo
from project.collectors.mem.vmstat import collect_vmstat
from project.collectors.mem.pressure import collect_pressure
from project.collectors.mem.cgroup import collect_cgroup
from project.collectors.mem.numa import collect_numa
from project.collectors.mem.process import collect_process_memory
from project.analyzers.mem.mem import analyze_memory_metrics
from project.utils.decorators import trace
from project.utils.pipeline import pipeline_runner
from project.collectors.mem.filter_compute import filter_memory_state, compute_memory_rates

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

@trace("memory")
def collect_memory() -> MemoryData:

    memory = MemoryData()
    collected_total = 0
    collected_successful = 0

    for field in fields(MEMTYPE):

        if not getattr(MEMTYPE, field.name):
            continue

        collected_total += 1
        collector = COLLECTORS.get(field.name)

        if collector is not None:
            try:
                #print(line(f"{collector.__name__}"))
                collector(memory)
                collected_successful += 1
            except Exception as e:
                raise RuntimeError(f"[MEM COLLECTOR] ERROR: {e}")

    memory.collected_total = collected_total
    memory.collected_successful = collected_successful
    return memory


@trace("start_memory_run")
def start_memory_collection():
  result = pipeline_runner(
      resource="memory",
      collect_func=collect_memory,
      analyze_func=analyze_memory_metrics,
      filter_func=filter_memory_state,
      compute_func=compute_memory_rates,
      extra_metadata=None,
  )

  return result

@trace("memory_pipeline")
def memory_pipeline():
    result = start_memory_collection()

memory_pipeline()
