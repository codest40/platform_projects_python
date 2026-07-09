# CPU Pipeline

## Purpose

The CPU pipeline helps determine whether the CPU is contributing to system performance problems.
Observer evaluates raw operating system metrics, computes derived CPU indicators, applies specialized analyzers to each aspect of CPU behavior, normalizes the resulting signals, and finally combines them into a single evidence-based assessment of CPU health.

---

## Execution Flow

```text
CPU Pipeline
     │
     ▼
Collect CPU Metrics
     │
     ├── psutil
     ├── /proc
     ├── cgroups
     ├── PSI
     └── Scheduler
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
     ├── Rates/sec
     ├── Ratios
     ├── Load/Core
     ├── Core Balance
     └── Frequency Ratio
     │
     ▼
Emit Collection Event
     │
     ▼
Run CPU Analyzers
     │
     ├── Utilization
     ├── Idle
     ├── IO Wait
     ├── Load
     ├── Capacity
     ├── Frequency
     ├── Balance
     ├── Kernel
     ├── Steal
     ├── Pressure
     └── Container
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

The CPU collector gathers metrics from multiple operating system interfaces. Each collector is responsible for a specific data source, making the pipeline portable across different Linux distributions and kernel versions.

Current sources include:
* psutil — utilization, CPU times, frequency, load average, core counts
* /proc — processor information, cache size, model information
* cgroups — CPU throttling statistics
* Linux PSI — CPU pressure metrics
* Scheduler — scheduler counters and top CPU-consuming process

The collector records metrics such as:
* CPU utilization
* CPU frequency
* Physical cores
* Logical cores
* Per-core utilization
* Load average
* User CPU time
* System CPU time
* Idle CPU time
* IO wait
* CPU model

At this stage, no health decisions are made. The goal is simply to collect accurate and consistent CPU information.

---
## Stage 2 — Collection Runner

Every collector executes through a common collection runner.

The runner provides shared operational capabilities, including:

* Execution timing
* Structured logging
* Exception handling
* Request tracing
* Thread safety
* Process safety

Using a common runner ensures that every collector behaves consistently and produces a standardized execution record.

---

## Stage 3 — Collection Event

After collection completes, Observer emits a structured collection event.

The event contains information such as:

* Summary
* Severity
* Metadata
* Execution duration
* Trace identifiers
* Caller information

If collection fails, an exception event is emitted instead. This provides a complete audit trail for every collection attempt.

---
## Stage 4 — Derived Metrics

After collection, Observer computes higher-level metrics from the raw operating system counters.

Examples include:

- Context switches per second
- Interrupts per second
- System calls per second
- CPU throttling events per second
- Load normalized per logical core
- Frequency utilization ratio
- Kernel activity ratio
- Core imbalance
- Core spread

Derived metrics provide a stable foundation for health analysis while keeping the collectors responsible only for raw operating system data.

## Stage 5 — CPU Analysis

Once collection is complete, the analyzer evaluates the collected metrics using predefined operational health checks.

Current health checks include:

* CPU utilization
* Idle CPU
* Load average
* IO wait
* Capacity
* Kernel activity
* CPU Frequency
* Core Balance
* CPU Steal Time
* CPU Pressure (PSI)
* Container / cgroup CPU


Each health check produces one of three outcomes:

* PASS
* WARNING
* CRITICAL

Instead of relying on a single metric, Observer combines the results of multiple checks before determining whether the CPU is likely contributing to a performance issue.

---
## Stage 6 — Signal Normalization

Raw metrics are converted into normalized signals used by the summary engine.

Normalization separates metric collection from decision-making, allowing multiple analyzers to contribute evidence without directly determining the final system state.

## Stage 7 — Overall Verdict

After all health checks complete, a summerizer produces an overall assessment of CPU health by combining all analyzer results into a single CPU assessment.

It evaluates:

- Health checks
- Severity
- Confidence score
- Recommendations
- Overall summary

Possible outcomes include:

* CPU can reasonably be ruled out as the source of the problem.
* CPU shows warning signs but cannot yet be identified as the primary cause.
* CPU remains a strong candidate for the observed performance issue.

The analyzers also provides recommendations to help guide the next stage of investigation.

---

## Stage 6 — Analysis Event

The completed analysis is emitted as a structured analysis event.

The event includes:

* Overall verdict
* Severity
* Confidence
* Health check results
* Recommendations
* Trace identifiers

These events create an auditable record explaining how the final assessment was reached.

---
## Collector Architecture

Observer separates CPU collection by operating system source rather than by metric type.

Current collectors include:

```text
collectors/cpu/
├── psutil.py
├── proc.py
├── cgroup.py
├── pressure.py
├── sched.py
├── filter_compute.py
└── cpu.py
```

This modular design improves portability across Linux distributions, simplifies testing, and allows new metric sources to be added without modifying existing collectors.

## Stage 7 — Response

After collection and analysis are complete, Observer can trigger one or more execution layers based on the analysis results.

The execution stage is intentionally separated from collection and analysis, allowing users to integrate their own response mechanisms without modifying the pipeline itself.

Common examples include:

* Alert notifications
* Webhooks
* AWS operations
* Kubernetes actions
* Ticket creation
* Custom automation scripts
* Any other environment-specific workflow

This separation allows the **collection**, **analysis**, and **execution** stages to evolve independently. Users can choose which actions to perform—or whether to perform any actions at all—based on the collected metrics and the resulting analysis.
