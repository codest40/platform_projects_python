from typing import Literal
from project.models.cpu import AnalyzerResult, HealthCheck

AnalyzerState = Literal["COMPLETE", "PARTIAL", "UNAVAILABLE"]


def build_result(
    *,
    name: str,
    state: AnalyzerState,
    checks: list[HealthCheck],
) -> AnalyzerResult:

    if not isinstance(name, str):
        raise TypeError("[CPU DATA ANALYZER DATA] name must be a str")

    if state not in ("COMPLETE", "PARTIAL", "UNAVAILABLE"):
        raise ValueError(
            f"[CPU DATA ANALYZER] Invalid analyzer state: {state}"
        )

    return AnalyzerResult(
        name=name,
        state=state,
        checks=checks,
    )



