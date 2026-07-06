# Disk Pipeline

## Purpose

The Disk pipeline evaluates both the capacity and performance of the system's storage subsystem.

A healthy filesystem is more than having free disk space. Applications can experience poor performance even when sufficient storage remains available if the kernel is waiting on storage operations, device queues become saturated, or storage latency begins to increase.

Unlike basic monitoring tools that primarily report disk usage, Observer combines filesystem statistics, Linux kernel I/O metrics, storage pressure, interval-based performance calculations, and workload activity to determine whether storage is genuinely contributing to application slowdowns.

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
Filter Comparison Metrics
      │
      ▼
Load Previous Snapshot
      │
      ▼
Compute Interval Metrics
      │
      ├── Throughput (MB/s)
      ├── IOPS
      ├── Device Utilization
      ├── Queue Depth
      ├── Average Latency
      ├── Flush Rate
      ├── Process IO Rate
      └── Container IO Rate
      │
      ▼
Save Current Snapshot
      │
      ▼
Analyze Disk Health
      │
      ▼
Correlate Storage Evidence
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

The collector gathers raw storage statistics from multiple Linux interfaces.

Many Linux storage counters continually increase from system boot and therefore cannot accurately describe current storage activity on their own. Observer first records these cumulative counters before converting them into interval-based performance metrics during a later stage of the pipeline.

Current data sources include:

* `psutil`
* `/proc/diskstats`
* Linux Pressure Stall Information (PSI)
* Mounted filesystem information
* Filesystem usage statistics
* Linux cgroups (v1 and v2)
* Process I/O statistics

These sources provide information such as:

* Filesystem capacity
* Mounted filesystems
* Read and write operations
* Read and write bytes
* Device busy time
* Outstanding I/O
* Queue time
* Flush operations
* Discard operations
* Storage pressure (PSI)
* Process disk activity
* Container disk activity

The collection stage focuses exclusively on gathering operating system data. No health decisions are made during collection.

---

## Analysis Based on the Most Important Factors

| Priority | Indicator               | Why it matters                                                |
| -------: | ----------------------- | ------------------------------------------------------------- |
|        1 | Filesystem Capacity     | Is the filesystem approaching exhaustion?                     |
|        2 | IO Pressure (PSI)       | Are runnable tasks stalled waiting for storage?               |
|        3 | Device Utilization      | Is the storage device saturated?                              |
|        4 | Queue Depth             | Are IO requests accumulating faster than they complete?       |
|        5 | Read / Write Latency    | Are storage requests taking too long?                         |
|        6 | Throughput (MB/s)       | How much data is moving through the device?                   |
|        7 | IOPS                    | How many IO operations are occurring each second?             |
|        8 | Process Disk Activity   | Is the monitored process generating excessive IO?             |
|        9 | Container Disk Activity | Is container workload contributing to storage pressure?       |
|       10 | Flush Activity          | Is the kernel spending excessive effort flushing dirty pages? |

---

## Stage 2 — Collection Runner

Disk collection executes through Observer's shared collection runner.

The runner provides execution timing, tracing, structured logging, exception handling, and concurrency safeguards so that disk collection behaves consistently with every other resource pipeline.

---

## Stage 3 — Collection Event

After collection completes, Observer records a structured collection event describing both the collected metrics and how the collection executed.

The event contains metadata such as execution duration, status, severity, trace identifiers, and collection details. If collection cannot be completed successfully, an exception event is emitted instead.

---

## Stage 4 — Interval Metric Computation

Most Linux storage statistics are cumulative counters that continually increase throughout system uptime.

To understand current storage behaviour, Observer maintains lightweight comparison snapshots for each resource. By comparing the latest collection with the previous snapshot, it derives interval-based metrics that represent storage activity during the sampling period rather than since system boot.

Current derived metrics include:

* Read throughput (MB/s)
* Write throughput (MB/s)
* Total throughput
* Read IOPS
* Write IOPS
* Total IOPS
* Average read latency
* Average write latency
* Device utilization percentage
* Average queue depth
* Flush rate
* Discard throughput
* Process disk throughput
* Container disk throughput

These comparison snapshots are stored independently from Observer's event log.

* `observer.jsonl` remains the permanent structured event log.
* Resource state files are used only to calculate interval metrics.

---

## Stage 5 — Disk Analysis

The analyzer evaluates both the collected metrics and the derived interval metrics using a series of operational health checks.

Current checks include:

* Filesystem Capacity
* IO Pressure (PSI)
* Device Utilization
* Queue Depth
* IO Latency
* Throughput
* IOPS
* Flush Activity
* Process Disk Activity
* Container Disk Activity

Each health check produces one of three outcomes:

* PASS
* WARNING
* CRITICAL

Rather than relying on a single metric, Observer correlates evidence across multiple independent indicators before reaching a conclusion.

For example:

* High filesystem utilization alone does not necessarily indicate poor storage performance.
* Elevated latency by itself may simply reflect a brief burst of activity.
* Increased throughput is not automatically unhealthy if latency and queue depth remain low.

Storage is considered a likely bottleneck only when several independent indicators begin pointing toward the same conclusion. For example, sustained IO pressure together with high device utilization, increasing queue depth, and elevated latency provides much stronger evidence of storage contention than any individual metric on its own.

---

## Stage 6 — Overall Verdict

After completing every health check, Observer correlates the collected evidence before assigning an overall storage assessment.

Rather than allowing a single abnormal metric to dominate the analysis, multiple independent indicators are evaluated together. This reduces false positives while improving confidence that storage is genuinely responsible for the observed performance degradation.

Depending on the observed conditions, the analysis may conclude that:

* Storage is operating normally.
* Storage requires closer investigation.
* Storage is the most likely source of the observed performance issue.

Recommendations are also included to guide further troubleshooting.

---

## Stage 7 — Analysis Event

The completed assessment is emitted as a structured analysis event.

In addition to the overall verdict, the event records the individual health checks, severity, confidence, recommendations, and trace information. This provides an audit trail explaining why the analyzer reached its conclusion.

---

## Current Scope

The Disk pipeline now derives interval-based performance metrics from cumulative Linux kernel counters, allowing Observer to evaluate current storage behaviour rather than relying solely on values accumulated since system boot.

Current capabilities include:

* Filesystem capacity monitoring
* Storage pressure (PSI)
* Throughput calculation (MB/s)
* IOPS calculation
* Average read and write latency
* Device utilization
* Average queue depth
* Flush rate analysis
* Process storage throughput
* Container storage throughput
* Multi-factor evidence correlation

Future improvements include:

* Filesystem inode utilization
* Per-device analysis
* NVMe-specific performance metrics
* SMART device health integration
* Historical storage trend analysis
* Automatic workload classification
* Predictive storage capacity forecasting

These enhancements will further improve Observer's ability to distinguish brief bursts of activity from sustained storage bottlenecks.

---

## Stage 8 — Response

The Disk pipeline ends after analysis, but its results are designed to be consumed by other parts of Observer.

Depending on the deployment, analysis results can be used to:

* Generate alerts for sustained storage problems.
* Trigger automated remediation workflows.
* Integrate with monitoring or incident management systems.
* Feed dashboards or long-term reporting.
* Invoke custom automation written by the user.

Because these actions are independent of the collection and analysis logic, users are free to extend Observer without changing how storage metrics are collected or evaluated.

