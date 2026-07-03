project/
└── collectors/
    └── memory/
        ├── __init__.py
        ├── memory.py              # Main orchestrator
        ├── psutil.py              # psutil collectors
        ├── meminfo.py             # /proc/meminfo
        ├── vmstat.py              # /proc/vmstat
        ├── pressure.py            # PSI
        ├── cgroup.py             # cgroup v1/v2
        ├── numa.py               # NUMA
        ├── process.py            # current process memory
        └── utils.py              # shared helpers
