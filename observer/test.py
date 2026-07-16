import subprocess
import time

observer = subprocess.Popen(
    [
        "python3",
        "-m",
        "project.collectors.processes.inventory"
    ]
)

print("Observer PID:", observer.pid)

observer.wait()

print("Done")
