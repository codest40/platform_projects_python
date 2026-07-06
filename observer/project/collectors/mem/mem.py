from dataclasses import fields
from project.models.memory import MemoryData, GetMemType
from project.utils.helpers import line, get_status
from project.collectors.mem.psutil import collect_psutil_memory
from project.collectors.mem.meminfo import collect_meminfo
from project.collectors.mem.vmstat import collect_vmstat
from project.collectors.mem.pressure import collect_pressure
from project.collectors.mem.cgroup import collect_cgroup
from project.collectors.mem.numa import collect_numa
from project.collectors.mem.process import collect_process_memory
from project.analyzers.mem.mem import analyze_memory_metrics
from project.utils.start_event import run_collection, run_analysis
from project.alerts.activate_alert import activate_run_alert

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
    collectors_total = 0
    collectors_successful = 0

    for field in fields(MEMTYPE):

        if not getattr(MEMTYPE, field.name):
            continue

        collectors_total += 1
        collector = COLLECTORS.get(field.name)

        if collector is not None:
            try:
                #print(line(f"{collector.__name__}"))
                collector(memory)
                collectors_successful += 1
            except Exception as e:
                raise RuntimeError(f"[MEM COLLECTOR] ERROR: {e}")

        memory.collectors_total = collectors_total
        memory.collectors_successful = collectors_successful
    return memory


def start_memory_collection():
    result = run_collection(resource="memory", func=collect_memory)
    return result

def memory_pipeline():
  result = start_memory_collection()
  if result is None:
    print(f"❌ ERROR: Emit() response returned: {result}")
  elif result.status == get_status("FAILED"):
      print("❌ Collecting memory Metrics Failed")
      activate_run_alert(title="Memory Metrics collection Alert", message=f"❌ Memory Metrics Collection Failed: {result}", severity="CRITICAL",)
  elif result.status == get_status("SUCCESS"):
      print("✅ Memory Metrics Collection Passed")
      res = run_analysis(resource="memory", func=analyze_memory_metrics, result=result)
      if not res:
          print("❌ Memory Analysis Failed")
          print(f"Result: {res}")
      else:
          print("✅ Memory Metrics Analysis Passed")
  else:
    print(f"❌ ERROR: Emit() response returned: {result.status} \nSomething is veru wrong.. Check codes")

memory_pipeline()
