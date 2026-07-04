#

# I collect and analyze based on
```
| Step | Collector         | Why first?                                | Source                 |
| ---- | ----------------- | ----------------------------------------- | ---------------------- |
| 1    | **psutil.py**     | Cross-platform, gives most common metrics | `psutil`               |
| 2    | **diskstats.py**  | Linux kernel IO counters                  | `/proc/diskstats`      |
| 3    | **pressure.py**   | IO Pressure Stall Information             | `/proc/pressure/io`    |
| 4    | **mountinfo.py**  | Mounts, read-only status                  | `/proc/self/mountinfo` |
| 5    | **usage.py**      | Filesystem statistics and utils           | `os.statvfs()`         |
| 6    | **cgroup.py**     | Container IO                              | cgroup v2              |
```

```
| Field                | Why?                               |
| -------------------- | ---------------------------------- |
| `in_flight`          | I/O requests currently in progress |
| `io_ticks`           | Time the device spent doing I/O    |
| `time_in_queue`      | Weighted queue time                |
| `discards_completed` | TRIM/discard operations completed  |
| `sectors_discarded`  | Sectors discarded                  |
| `discard_time_ms`    | Time spent discarding              |
| `flush_completed`    | Cache flush operations completed   |
| `flush_time_ms`      | Time spent flushing                |

```
