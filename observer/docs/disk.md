# Disk Pipeline

## Purpose

The Disk pipeline evaluates both the capacity and performance of the system's storage subsystem.

A healthy filesystem is more than having free disk space. Applications can experience poor performance even when plenty of storage remains available if the kernel is waiting on disk operations or storage devices become saturated.

Observer combines filesystem information with Linux I/O metrics to determine whether storage is likely contributing to performance problems.

---

## Execution Flow

```text
Disk Pipeline
      │
      ▼
Collect Disk Metrics
      │
      ▼
Run Collection
      │
      ├── Trace
      ├── Timer
      ├── Thread Lock
      ├── Process Lock
      └── Exception Handling
      │
      ▼
Emit Collection Event (log)
      │
      ▼
Analyze Disk Metrics
      │
      ▼
Health Checks
      │
      ├── Filesystem Utilization
      ├── IO Pressure (PSI)
      ├── Outstanding IO
      ├── IO Latency
      ├── Writeback Activity
      ├── Process Disk IO
      └── Flush Activity
      │
      ▼
Generate Analysis
      │
      ▼
Emit Analysis Event (log)
      │
      ▼
Executors / Alerts / Automation
```

---

## Stage 1 — Metric Collection

The collector gathers storage information from multiple Linux interfaces to provide both filesystem and I/O visibility.

Current data sources include:

* `psutil`
* `/proc/diskstats`
* Linux Pressure Stall Information (PSI)
* Mounted filesystem information
* Linux cgroups
* Process I/O statistics

These sources provide information such as:

* Filesystem capacity
* Disk utilization
* Mounted filesystems
* Read and write operations
* Read and write bytes
* Outstanding I/O requests
* Device busy time
* Queue time
* Flush activity
* Storage pressure (PSI)
* Container disk I/O
* Process disk I/O

The collection stage records storage activity exactly as reported by the operating system. No conclusions are drawn during collection.

---

## Primary Health Indicators

Not every storage metric contributes equally to diagnosing a disk problem. Observer prioritizes indicators that provide the strongest evidence of storage contention.

| Priority | Check                  | Why it matters                                       |
| -------: | ---------------------- | ---------------------------------------------------- |
|        1 | Filesystem utilization | Is the filesystem approaching capacity?              |
|        2 | IO Pressure (PSI)      | Are runnable tasks waiting for storage resources?    |
|        3 | Outstanding IO         | Is the device developing an IO queue?                |
|        4 | IO latency             | Are storage requests taking too long to complete?    |
|        5 | Writeback activity     | Is the kernel struggling to flush dirty pages?       |
|        6 | Process Disk IO        | Is an application generating excessive disk traffic? |
|        7 | Flush activity         | Are flush operations behaving normally?              |

---

## Stage 2 — Collection Runner

Disk collection executes through Observer's shared collection runner.

The runner provides execution timing, structured logging, tracing, exception handling, and concurrency protection so that disk collection behaves consistently with every other resource pipeline.

---

## Stage 3 — Collection Event

Once collection completes, Observer emits a structured collection event describing the execution.

The event records information such as execution duration, status, metadata, severity, trace identifiers, and collection details. If collection cannot be completed successfully, an exception event is emitted instead.

---

## Stage 4 — Disk Analysis

The analyzer evaluates the collected metrics using a series of storage health checks.

Current checks include:

* Filesystem Utilization
* IO Pressure (PSI)
* Outstanding IO
* IO Latency
* Writeback Activity
* Process Disk IO
* Flush Activity

Each health check produces one of three outcomes:

* PASS
* WARNING
* CRITICAL

The analyzer evaluates storage from both a **capacity** and **performance** perspective.

For example:

* A filesystem may have plenty of free space but still experience high I/O pressure.
* High storage utilization does not necessarily indicate poor performance if I/O latency remains low.
* Elevated latency combined with outstanding I/O requests often provides stronger evidence of storage contention than utilization alone.

---

## Stage 5 — Overall Verdict

After completing all health checks, Observer combines the results into an overall storage assessment.

The analysis may conclude that:

* Storage is operating normally.
* Storage shows early warning signs.
* Storage remains the primary suspect for the observed performance issue.

Recommendations are included to guide the next stage of investigation.

---

## Stage 6 — Analysis Event

The completed assessment is emitted as a structured analysis event.

The event contains the overall verdict, severity, confidence, health check results, recommendations, and trace information, providing a complete explanation of the analyzer's decision.

---

## Current Scope

The Disk pipeline currently focuses on identifying storage capacity issues and signs of I/O contention.

Some Linux kernel counters are presently evaluated as cumulative values rather than rates over time. Future releases will expand the analysis to include more time-based performance measurements.

Planned improvements include:

* Read and write throughput (MB/s)
* Read and write IOPS
* Average queue depth over time
* Device utilization percentage
* Read and write latency trends
* Flush rate analysis
* Filesystem inode utilization
* Per-device comparisons
* SMART device health integration
* Historical storage trend analysis

These enhancements will improve the analyzer's ability to distinguish brief bursts of activity from sustained storage bottlenecks.

---

## Stage 7 — Response

The Disk pipeline produces a structured assessment that can be consumed by other components within Observer.

Depending on the deployment, the results may be used to:

* Generate storage alerts.
* Trigger automated remediation workflows.
* Notify monitoring or incident management systems.
* Feed dashboards and long-term reporting.
* Execute custom automation based on storage conditions.

By keeping response mechanisms separate from collection and analysis, Observer allows storage diagnostics to remain independent while giving users the flexibility to integrate their own operational workflows.


| Step | Collector         | Why first?                                | Source                 |
| ---- | ----------------- | ----------------------------------------- | ---------------------- |
| 1    | **psutil.py**     | Cross-platform, gives most common metrics | `psutil`               |
| 2    | **diskstats.py**  | Linux kernel IO counters                  | `/proc/diskstats`      |
| 3    | **pressure.py**   | IO Pressure Stall Information             | `/proc/pressure/io`    |
| 4    | **mountinfo.py**  | Mounts, read-only status                  | `/proc/self/mountinfo` |
| 5    | **usage.py**      | Filesystem statistics and utils           | `os.statvfs()`         |
| 6    | **cgroup.py**     | Container IO                              | cgroup v2              |

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

