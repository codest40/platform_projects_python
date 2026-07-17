from dataclasses import dataclass, field
from project.models.processes import ProcessSummary


@dataclass(slots=True)
class QueryResult:
    title: str
    processes: list[ProcessSummary] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    description: str = ""
