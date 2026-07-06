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
from project.analyzers.mem.data import build_result, analyzers

from project.analyzers.mem.normalizer import normalize
from project.analyzers.mem.summary import summarize_memory
from project.models.memory import Signal, AnalyzerResult
from project.utils.runners import EventRunner
from project.utils.helpers import get_status


def analyze_memory_metrics(result: EventRunner) -> MemoryAnalysis:

    if result.status != get_status("SUCCESS"):
        raise RuntimeError(
            "❌ [MEMORY ANALYZER] Memory collection did not complete successfully"
        )


    memory = result.data
    checks: list[HealthCheck] = []
    metadata: dict = {}

    # ==========================================================
    # 1. Run analyzers (pure detection layer)
    # ==========================================================

    for each in analyzers:
      result = AnalyzerResult(each(memory))
      checks.extend(result.checks)
      metadata[result.name] = {"state": result.state, "total_checks": len(result.checks)}

    # ==========================================================
    # 2. Normalize signals
    # ==========================================================

    signals: list[Signal] = normalize(memory)

    # ==========================================================
    # 3. Summary (final decision engine)
    # ==========================================================

    return summarize_memory(memory, checks, signals, metadata)
