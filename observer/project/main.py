import argparse
from pathlib import Path
from project.utils.helpers import start_count, get_status
from concurrent.futures import ThreadPoolExecutor, as_completed

def activate_system():
    print("Activating pipeline..")

activate_system()
from project.collectors.cpu.cpu import cpu_pipeline
from project.collectors.mem.mem import memory_pipeline
from project.collectors.disk.disk import disk_pipeline

def start_resource(res, func):
  start = start_count()
  func()
  end = start_count()
  print(f"{res} Pipeline Duration: {end - start}")

# CPU
start_resource("cpu", cpu_pipeline)

#MEM
start_resource("memory", memory_pipeline)

#DISK
start_resource("disk", disk_pipeline)
