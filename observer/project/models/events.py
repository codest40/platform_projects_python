from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import logging
from types import TracebackType

@dataclass(slots=True)
class PlatformEvent:

    event_name: str

    category: str

    collector: str

    operation: str

    summary: str

    severity: str | int = logging.INFO

    event_duration_ms: int | None = None

    cause: str | None = None

    impact: str | None = None

    recommendations: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    tags: list[str] = field(default_factory=list)

    exc_info: tuple[ type[BaseException], BaseException, TracebackType | None,] | None = None

    event_id: str | None = None

    trace_id: str | None = None

    span_id: str | None = None

    parent_span_id: str | None = None



