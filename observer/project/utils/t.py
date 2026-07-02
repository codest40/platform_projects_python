from project.logging.logger import emit
from project.utils.helpers import timestamp
import platform

def get_cpu_model():
    with open("/proc/cpuinfo") as f:
        for line in f:
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    return "Unknown"


print(get_cpu_model())

try:
  emit(f"Testing emit at {timestamp()}")
except Exception as e:
  print("Emit() Encountered Issues!")
