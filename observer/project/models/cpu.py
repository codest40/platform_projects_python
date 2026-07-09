from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

@dataclass(slots=True)
class CpuData:

    # ======================================================
    # CPU Information
    # ======================================================

    cpu_model: str | None=None
    cache_size: str | None=None

    physical_cores: int | None=None
    logical_cores: int | None=None

    # ======================================================
    # CPU Utilization
    # ======================================================

    usage_percent: float | None=None
    per_core_util: list[float] | None=None

    # ======================================================
    # CPU Time Breakdown
    # ======================================================

    user_percent: float | None=None
    system_percent: float | None=None
    idle_percent: float | None=None

    iowait_percent: float | None=None
    steal_percent: float | None=None
    irq_percent: float | None=None
    softirq_percent: float | None=None
    nice_percent: float | None=None

    # ======================================================
    # Scheduler Statistics
    # ======================================================

    context_switches: int | None=None
    interrupts: int | None=None
    soft_interrupts: int | None=None
    syscalls: int | None=None

    # ======================================================
    # Frequency
    # ======================================================

    frequency_mhz: float | None=None
    min_frequency_mhz: float | None=None
    max_frequency_mhz: float | None=None

    # ======================================================
    # Load
    # ======================================================

    load_average: tuple[float, float, float] | None=None

    # ======================================================
    # Linux PSI (optional)
    # ======================================================

    psi_some_avg10: float | None = None
    psi_some_avg60: float | None = None
    psi_some_avg300: float | None = None
    psi_full_avg10: float | None = None
    psi_full_avg60: float | None = None
    psi_full_avg300: float | None = None
    # ======================================================
    # CPU Throttling (cgroups)
    # ======================================================

    cpu_throttled_periods: int | None = None
    cpu_throttle_periods: int | None = None
    cpu_throttled_usec: int | None = None
    cpu_throttle_ratio: float | None = None
    # ======================================================
    # Top CPU Process
    # ======================================================

    top_process_name: str | None = None
    top_process_pid: int | None = None
    top_process_cpu_percent: float | None = None

    # ======================================================
    # Computed Rates
    # ======================================================

    context_switches_per_sec: float | None = None
    interrupts_per_sec: float | None = None
    soft_interrupts_per_sec: float | None = None
    syscalls_per_sec: float | None = None

    # ======================================================
    # Computed Ratios / Derived Metrics
    # ======================================================

    load_per_core_1: float | None = None
    load_per_core_5: float | None = None
    load_per_core_15: float | None = None

    highest_core_percent: float | None = None
    average_core_percent: float | None = None
    core_imbalance_percent: float | None = None
    lowest_core_percent: float | None = None
    core_spread_percent: float | None = None

    frequency_ratio: float | None = None
    kernel_ratio: float | None = None

    cpu_throttled_periods_per_sec: float | None = None
    cpu_throttled_usec_per_sec: float | None = None
    cpu_throttle_event_ratio: float | None=None
    # ======================================================
    # Collection Metadata
    # ======================================================

    severity: str | None = None
    summary: str | None = None
    comment: str | None = None

    collected_at: float | None = None
    collected_total: int = 0
    collected_successful: int = 0
    signals_expected: int = 0
    signals_created: int = 0

    seen: bool = False

@dataclass
class Signal:
    name: str
    value: float
    domain: str
    type: str
    unit: str | None = None

@dataclass
class AnalyzerResult:
    name: str
    state: str
    checks: list[HealthCheck]
    evidence: list[str] | None=None
    completed: bool | None=None

@dataclass(slots=True)
class HealthCheck:
    check: str
    reason: str
    status: Literal["PASS", "WARNING", "CRITICAL"] = "PASS"
    category: str | None=None

@dataclass(slots=True)
class Confidence:
    result: str
    reasons: list[str] = field(default_factory=list)

@dataclass(slots=True)
class CpuAnalysis:

    health_checks: list[HealthCheck]
    recommendations: list[str] = field(default_factory=list)
    severity: Literal["INFO", "WARNING", "CRITICAL"] = "INFO"

    component: str | None=None
    analyzed_at: str | None=None
    summary: str | None=None
    confidence: Confidence | None = None
