from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class ContextHelpers:

    project_root: tuple[str, ...]
    span_prefix: tuple[str, ...]

    app_name: str
    app_version: str
    schema_version: str


@dataclass(frozen=True, slots=True)
class LogLevels:
    log_levels: dict[str, int]
