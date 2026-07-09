#  Memory Pipeline

## Purpose

Observer evaluates memory health using multiple independent data sources, derived metrics, and specialized analyzers rather than relying solely on memory utilization. By combining kernel pressure information, paging behavior, reclaim activity, swap usage, commit accounting, container statistics, and process memory usage.
Unlike simple monitoring tools that focus primarily on memory utilization, Observer examines several kernel-level indicators to distinguish between normal memory usage and genuine memory pressure. This helps operators identify situations where memory is becoming a bottleneck before they result in service failures.
---

## Execution Flow

```text
Memory Pipeline
      │
      ▼
Collect Memory Metrics
      │
      ├── psutil
      ├── /proc
      ├── vmstat
      ├── PSI
      ├── cgroups
      ├── NUMA
      └── Processes
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
Compute Derived Metrics
      │
      ├── Growth Rates
      ├── Paging Rates
      ├── Reclaim Rates
      ├── Commit Ratio
      ├── Cache Ratios
      └── Memory Pressure Ratios
      │
      ▼
Emit Collection Event
      │
      ▼
Run Memory Analyzers
      │
      ├── Capacity
      ├── Growth
      ├── Swap
      ├── Pressure
      ├── Reclaim
      ├── Paging
      ├── OOM
      ├── Commit
      ├── Cache
      ├── Container
      └── Process
      │
      ▼
Normalize Signals
      │
      ▼
Summary Engine
      │
      ▼
Emit Analysis Event
      │
      ▼
Executors / Alerts / Automation
```

---

## Stage 1 — Metric Collection

The collector gathers memory information from multiple Linux interfaces to build a detailed view of the system's memory state.
collectors/mem/

```
├── psutil.py
├── proc.py
├── vmstat.py
├── pressure.py
├── cgroup.py
├── numa.py
├── process.py
├── filter_compute.py
└── mem.py
```

Current data sources include:

* `psutil`
* `/proc/meminfo`
* `/proc/vmstat`
* Linux Pressure Stall Information (PSI)
* Linux cgroups (v1 and v2)
* NUMA statistics
* Process memory statistics

These sources provide information such as:

* Memory capacity and utilization
* Available memory
* Cached and buffered memory
* Swap usage
* Memory pressure (PSI)
* OOM events
* Allocation failures
* Memory reclaim activity
* Commit accounting
* Filesystem cache
* Container memory usage
* NUMA memory access
* Process memory usage

The collection stage focuses only on gathering data. It does not determine whether the system is healthy or unhealthy.

---

## Stage 2 — Collection Runner

Memory collection executes through Observer's shared collection runner.

The runner handles execution timing, tracing, structured logging, exception handling, and concurrency safeguards so that memory collection behaves consistently with every other resource collector.

---

## Stage 3 — Collection Event

After collection completes, Observer records a structured collection event describing what was collected and how the collection executed.

The event contains metadata such as execution duration, status, severity, trace identifiers, and collection details. If collection cannot be completed successfully, an exception event is emitted instead.

---

## Stage 4 — Memory Analysis

The analyzer evaluates the collected metrics using a series of operational health checks.

Current checks include:

* Available Memory
* Swap Activity
* Memory Pressure (PSI)
* OOM / Allocation Failures
* Memory Reclaim
* Commit Accounting
* Major Page Faults
* Filesystem Cache

## Analysis Priorities
| Priority | Check                       | Why it matters                                                    |
| -------: | --------------------------- | ----------------------------------------------------------------- |
|        1 | Available memory            | Is the machine actually running out of usable RAM?                |
|        2 | Swap activity               | Is the kernel compensating by swapping?                           |
|        3 | PSI memory pressure         | Are tasks stalling because of memory pressure?                    |
|        4 | OOM / allocation failures   | Has memory exhaustion already occurred?                           |
|        5 | Page reclaim / scanning     | Is the kernel working hard to reclaim memory?                     |
|        6 | Commit ratio                | Has memory been overcommitted?                                    |
|        7 | Major page faults           | Is disk-backed paging hurting performance?                        |
|        8 | Cache vs application memory | Is high usage just filesystem cache or real application pressure? |


Each check produces one of three outcomes:

* PASS
* WARNING
* CRITICAL

Rather than treating high memory utilization as a problem on its own, Observer considers multiple indicators together. For example, a system using most of its memory may still be perfectly healthy if there is little memory pressure, no swap activity, and no allocation failures.

Likewise, relatively low memory utilization does not always indicate a healthy system if sustained pressure, reclaim activity, or OOM events are present.

---

## Stage 5 — Overall Verdict

The Summary Engine combines analyzer results, normalized signals, collection coverage, and analyzer completion status into a single evidence-based assessment of overall memory health. It determines:

- overall severity
- confidence
- recommendations
- health summary
- final analysis object

Depending on the observed conditions, the analysis may conclude that:

* Memory is operating normally.
* Memory requires closer investigation.
* Memory is the most likely source of the observed performance issue.

Recommendations are also included to help guide further troubleshooting.

---

## Stage 6 — Analysis Event

The completed assessment is emitted as a structured analysis event.

In addition to the overall verdict, the event records the individual health checks, severity, confidence, recommendations, and trace information. This provides an audit trail explaining why the analyzer reached its conclusion.

---
## Stage 7 — Response

The Memory pipeline ends after analysis, but its results are designed to be consumed by other parts of Observer.

Depending on the deployment, analysis results can be used to:

* Generate alerts for sustained memory pressure.
* Trigger automated remediation workflows.
* Integrate with monitoring or incident management systems.
* Feed dashboards or long-term reporting.
* Invoke custom automation written by the user.

Because these actions are independent of the collection and analysis logic, users are free to extend Observer without changing how memory metrics are collected or evaluated.





