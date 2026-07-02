# CPU Pipeline

- The CPU pipeline is responsible for determining whether the CPU is likely contributing to system performance problems.

- Rather than relying solely on CPU utilization, the pipeline evaluates several strong indicators before reaching a conclusion.

## Execution Flow
```
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
Executors / Alerts etc
```

## Stage 1 — Metric Collection

The collector gathers raw CPU metrics from the operating system using psutil.

Current metrics include:

- CPU utilization
- CPU frequency
- Physical cores
- Logical cores
- Per-core utilization
- Load average
- User CPU time
- System CPU time
- Idle CPU time
- IO wait
- CPU model

The collector does not determine system health.
Its responsibility is only to produce an accurate snapshot of the CPU.



## Stage 2 — Collection Runner

Every collector executes through the common runner.

The runner provides:

- execution timing
- structured logging
- exception capture
- tracing
- thread safety
- process safety

This allows every collector to behave consistently.


## Stage 3 — Collection Event

After successful collection an event is emitted containing:

- summary
- severity
- metadata
- execution duration
- trace identifiers
- caller information

If collection fails, an exception event is emitted instead.


## Stage 4 — CPU Analysis

The analyzer evaluates the collected metrics using predefined operational rules.

Current health checks include:

- CPU utilization
- Idle CPU
- Load average
- IO wait
- Core balance
- Kernel activity

Each check produces one of three outcomes:
- PASS
- WARNING
- CRITICAL

For easy readabiltyi

## Stage 5 — Overall Verdict

After every health check completes, the analyzer determines an overall CPU assessment.

Possible outcomes include:

- CPU can reasonably be ruled out.
- CPU shows warning signs but cannot yet be blamed.
- CPU remains a primary suspect.

The analyzer also recommends next steps for the operator.


## Stage 6 — Analysis Event

The completed analysis is emitted as a structured event containing:

- overall verdict
- severity
- confidence
- health checks
- recommendations
- trace identifiers

This creates an audit trail explaining why a conclusion was reached.


## Stage 7 — Response

After collection and analysis complete, Observer can trigger one or more execution layers based on the results.
The framework is intentionally designed to be extensible, allowing users to integrate their own response mechanisms without modifying the collection or analysis pipeline.

Examples include:

* Alert notifications
* Webhooks
* AWS operations
* Kubernetes actions
* Ticket creation
* Custom automation scripts
* Any other execution workflow appropriate for the environment

This separation allows the **collection**, **analysis**, and **execution** stages to evolve independently. Users can choose which actions to perform—or whether to perform any actions at all—based on the collected metrics and the analysis outcome.


