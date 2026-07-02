# # Platform Observer


## Current Features
* Structured event model
* Human-readable console logging
* JSON Lines (`.jsonl`) logging for downstream processing
* Automatic trace and span generation
* Parent-child span relationships
* Function tracing decorators
* Runtime caller inspection
* Execution path tracking
* Context-aware event serialization
* Exception reporting with tracebacks
* Collection runner for standardized execution lifecycle
* Runtime metadata (hostname, PID, timestamps, application version)

---

## Project Structure
```
project/
├── collectors/
├── models/
├── utils/
│   ├── context.py
│   ├── decorators.py
│   ├── formatters.py
│   ├── helpers.py
│   ├── logger.py
│   ├── logging_core.py
│   ├── modify.py
│   ├── runner.py
│   └── traces.py
```

Current responsibilities include:

* **Logging Core** – logger configuration and handlers
* **Formatters** – JSON and human-readable output
* **Tracing** – trace/span lifecycle management
* **Context** – caller discovery and runtime metadata
* **Runner** – standardized execution workflow
* **Logger API** – event, exception, and span emission

---

## Logging Outputs

Platform Observer currently writes logs to multiple destinations:

* Console output
* `logs/observer.log` (human-readable)
* `logs/observer.jsonl` (structured JSON)

---

## Planned work includes:
* CPU, memory, disk, and network collectors
* Background job execution
* Metrics aggregation
* OpenTelemetry compatibility
* Exporters
* Alerting support
* Plugin architecture
* Additional output backends

---

