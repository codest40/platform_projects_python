"""
Memory Pipeline Orchestrator.

This is the ONLY entry point for memory analysis.
It wires all layers together:
- analyzers
- normalizer
- summary engine
"""

from __future__ import annotations
from project.models.memory import MemoryData, MemoryAnalysis, HealthCheck

from project.analyzers.mem.cache import analyze_cache
from project.analyzers.mem.capacity import analyze_capacity
from project.analyzers.mem.growth import analyze_memory_growth
from project.analyzers.mem.commit import analyze_commit
from project.analyzers.mem.container import analyze_container
from project.analyzers.mem.oom import analyze_oom
from project.analyzers.mem.pressure import analyze_memory_pressure
from project.analyzers.mem.paging import analyze_memory_paging
from project.analyzers.mem.reclaim import analyze_memory_reclaim
from project.analyzers.mem.swap import analyze_swap
from project.analyzers.mem.process import analyze_process

from project.analyzers.mem.normalizer import normalize
from project.analyzers.mem.summary import summarize_memory
from project.models.memory import Signal
from project.utils.runners import EventRunner
from project.utils.helpers import get_status


def analyze_memory_metrics(result: EventRunner) -> MemoryAnalysis:

    if result.status != get_status("SUCCESS"):
        raise RuntimeError(
            "❌ [MEMORY ANALYZER] Memory collection did not complete successfully"
        )


    memory = result.data
    checks: list[HealthCheck] = []

    # ==========================================================
    # 1. Run analyzers (pure detection layer)
    # ==========================================================

    checks.extend(analyze_cache(memory))
    checks.extend(analyze_capacity(memory))

    checks.extend(analyze_memory_growth(memory))
    checks.extend(analyze_commit(memory))

    checks.extend(analyze_container(memory))
    checks.extend(analyze_oom(memory))

    checks.extend(analyze_memory_pressure(memory))
    checks.extend(analyze_memory_paging(memory))
    checks.extend(analyze_memory_reclaim(memory))

    checks.extend(analyze_swap(memory))
    checks.extend(analyze_process(memory))

    # ==========================================================
    # 2. Normalize signals
    # ==========================================================

    signals: list[Signal] = normalize(memory)

    # ==========================================================
    # 3. Summary (final decision engine)
    # ==========================================================

    return summarize_memory(memory, checks, signals)
