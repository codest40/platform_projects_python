import argparse
from pathlib import Path

def activate_system():
    print("Activating pipeline..")

activate_system()
from project.collectors.cpu import collect_cpu_metrics
from project.utils.runner import get_status
from project.alerts.activate_alert import activate_run_alert

# CPU
result = collect_cpu_metrics()

if result is None:
  print(f"❌ ERROR: Emit() response returned: {result}")
elif result.status == get_status("FAILED"):
    print("Collecting Cpu Metrics Failed")
    activate_run_alert(title="Testing alert", message="❌ Cpu Metric Collection Failed", severity="CRITICAL",)
elif result.status == get_status("SUCCESS"):
    print("Collecting Cpu Metrics Passed")
    activate_run_alert(title="Testing alert", message="Cpu Metric Collection Passed")
else:
  print(f"❌ ERROR: Emit() response returned: {result.status} \nSomething is very wrong")
#MEM

