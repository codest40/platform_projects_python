from typing import Literal
from project.models.memory import AnalyzerResult, HealthCheck

AnalyzerState = Literal["COMPLETE", "PARTIAL", "UNAVAILABLE"]


def build_result(
    name: str,
    state: AnalyzerState,
    checks: list[HealthCheck],
) -> AnalyzerResult:

    if not isinstance(name, str):
        raise TypeError("[MEM ANALYZER DATA] name must be a str")

    if state not in ("COMPLETE", "PARTIAL", "UNAVAILABLE"):
        raise ValueError(
            f"[MEM ANALYZER DATA] Invalid analyzer state: {state}"
        )

    return AnalyzerResult(
        name=name,
        state=state,
        checks=checks,
    )



analyzers = [
    analyze_cache,
    analyze_capacity,
    analyze_memory_growth,
    analyze_commit,
    analyze_container,
    analyze_oom,
    analyze_memory_pressure,
    analyze_memory_paging,
    analyze_memory_reclaim,
    analyze_swap,
    analyze_process,
]
