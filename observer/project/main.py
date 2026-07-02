import argparse
from pathlib import Path
from project.utils.helpers import start_count
from concurrent.futures import ThreadPoolExecutor


def activate_system():
    print("Activating pipeline..")

activate_system()
from project.collectors.cpu import collect_cpu_metrics
from project.utils.runner import get_status

def start_resource(res, func):
  start = start_count()
  func()
  end = start_count()
  print(f"{res} Pipeline Duration: {end - start}")

# CPU
start_resource("cpu", collect_cpu_metrics)

#MEM
#start_resource("mem", collect_mem_metrics)
