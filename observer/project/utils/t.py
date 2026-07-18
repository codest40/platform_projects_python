from project.logging.logger import emit
from project.utils.helpers import timestamp
import platform, psutil
from pathlib import Path
import os
from project.analyzers.processes.users import get_user

print("cwd:", Path.cwd())
print(".env exists:", Path(".env").exists())
print("sender:", os.getenv("EMAIL_SENDER"))

def get_cpu_model():
    with open("/proc/cpuinfo") as f:
        for line in f:
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    return "Not Seen"


print(get_cpu_model())


emit(
    f"[App] App_log",
    f"Testing emit at {timestamp()}",
    collector="App Api",
    comment="Api worked successfullyy",
)

print(f"Timestamp: {timestamp(unix=True)}")

print(psutil.cpu_stats())

print("=================================================")
user = get_user(1000)
print(user)
