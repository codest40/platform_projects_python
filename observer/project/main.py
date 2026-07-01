import argparse
from pathlib import Path

def activate_system():
    print("Activating pipeline..")

activate_system()
from project.collectors.sys.cpu import collect_cpu_metrics
from project.utils.runner import get_status
from project.alerts.alert_runner import send_alert

result = collect_cpu_metrics()

if result.status == get_status("FAILED"):
    print("Collecting Cpu Metrics Failed")
    send_alert(
      title="Testing alert",
      message="❌ Cpu Metric Collection Failed",
      severity="CRITICAL",
    )

elif result.status == get_status("SUCCESS"):
    print("Collecting Cpu Metrics Passed")
    send_alert(title="Testing alert", message="Cpu Metric Collection Passed")

else:
    print(f"❌ ERROR: Emit() response returned: {result.status} \nSomething is very wrong")
