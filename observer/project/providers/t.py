# t.py

import time

files = []

try:
    while True:
        files.append(open("/dev/null"))
except OSError as e:
    print(e)
    print(f"PID = {__import__('os').getpid()}")
    print("Sleeping for 10 seconds...")
    time.sleep(10)
