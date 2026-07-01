# Logger system flow

```
User Script
     │
     ▼
emit(...)
(logger.py)
     │
     │  Parses user call
     ▼
safe_event(...)
(modify.py)
     │
     │  Creates PlatformEvent
     ▼
PlatformEvent(...)
(models/summary.py)
     │
     │  Returns event object
     ▼
logger.log(...)
(logger.py)
     │
     │  Uses configured logger
     ▼
platform_observer logger
(logging_core.py)
     │
     │
     ├────────────► JSON Handler
     │                 │
     │                 ▼
     │          JsonFormatter
     │          (formatters.py)
     │                 │
     │                 ▼
     │        serialize_event()
     │        (context.py)
     │                 │
     │                 ├─ current_timestamp()
     │                 ├─ get_system_context()
     │                 ├─ attach(event)
     │                 │      │
     │                 │      ▼
     │                 │  traces.py
     │                 │
     │                 ▼
     │           observer.jsonl
     │
     │
     ├────────────► Pretty Handler
     │                 │
     │                 ▼
     │         PrettyFormatter
     │         (formatters.py)
     │                 │
     │                 ▼
     │           observer.log
     │
     │
     └────────────► Console Handler
                       │
                       ▼
                   Terminal
