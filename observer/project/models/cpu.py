from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(slots=True)
class Cpu_Data:
    physical_cores: int
    logical_cores: int

    usage_percent: float
    frequency_mhz: float
    load_average: tuple[float, float, float]
    user_percent: float
    system_percent: float
    idle_percent: float
    iowait_percent: float

    cpu_model: str
    per_core_util: list[float]

    severity: str
    summary: str
    comment: str

@dataclass(slots=True)
class CpuAnalysis:
    health_checks: list[HealthCheck]
    recommendations: list[str] = field(default_factory=list)
    component: str | None=None
    analyzed_at: str | None=None
    summary: str | None=None
    severity: str | None=None
    confidence: str | None=None


