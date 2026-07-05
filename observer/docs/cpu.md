# CPU Pipeline

## Purpose

The CPU pipeline helps determine whether the CPU is contributing to system performance problems.

Rather than relying on a single metric such as CPU utilization, Observer evaluates multiple CPU health indicators before reaching a conclusion. This approach reduces false positives and provides operators with a more reliable assessment of overall CPU health.

---

## Execution Flow

```text
CPU Pipeline
     │
     ▼
Collect CPU Metrics
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
Analyze CPU Metrics
     │
     ▼
Health Checks
     │
     ├── CPU Utilization
     ├── Idle CPU
     ├── Load Average
     ├── IO Wait
     ├── Core Balance
     └── Kernel Activity
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

The collection stage gathers a snapshot of the system's current CPU state from the operating system.

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

## Stage 4 — CPU Analysis

Once collection is complete, the analyzer evaluates the collected metrics using predefined operational health checks.

Current health checks include:

* CPU utilization
* Idle CPU
* Load average
* IO wait
* Core balance
* Kernel activity

Each health check produces one of three outcomes:

* PASS
* WARNING
* CRITICAL

Instead of relying on a single metric, Observer combines the results of multiple checks before determining whether the CPU is likely contributing to a performance issue.

---

## Stage 5 — Overall Verdict

After all health checks complete, the analyzer produces an overall assessment of CPU health.

Possible outcomes include:

* CPU can reasonably be ruled out as the source of the problem.
* CPU shows warning signs but cannot yet be identified as the primary cause.
* CPU remains a strong candidate for the observed performance issue.

The analyzer also provides recommendations to help guide the next stage of investigation.

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
