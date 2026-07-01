from project.models.events import PlatformEvent
from dataclasses import asdict, is_dataclass

def safe_event(*args, **kwargs) -> PlatformEvent:
    """
    Positional arguments
    --------------------
    emit()

    emit(summary)

    emit(event_name, summary)

    More than two positional arguments raises ValueError.
    """
    msg = ("emit() accepts at most two positional arguments:\n"
            "    emit(summary)\n"
            "    emit(event_name, summary)")

    if not args and not kwargs:
        raise ValueError("❌ Not Allowed!", msg)

    if len(args) > 2:
        raise ValueError(msg)

    #
    # defaults
    #

    severity = kwargs.pop("severity", kwargs.pop("level", "INFO"))

    event_name = kwargs.pop("event_name", "event")

    summary = kwargs.pop("summary", "")

    #
    # positional parsing
    #

    if len(args) == 1:
        summary = args[0]

    elif len(args) == 2:
        event_name = args[0]
        summary = args[1]

    #
    # known fields
    #

    category = kwargs.pop("category", "system")

    collector = kwargs.pop("collector", "unknown")

    operation = kwargs.pop("operation", "run")

    event_duration_ms = kwargs.pop("duration_ms", None)

    cause = kwargs.pop("cause", None)

    impact = kwargs.pop("impact", None)

    comment = kwargs.pop("comment", None)

    recommendations = kwargs.pop("recommendations", None)

    tags = kwargs.pop("tags", [])

    metadata = kwargs.pop("metadata", {})
    if metadata is None:
        metadata = {}
    elif is_dataclass(metadata):
        metadata = asdict(metadata)
    elif not isinstance(metadata, dict):
        raise TypeError("metadata must be a dataclass, dict, or None")

    exc_info = kwargs.pop("exc_info", None)

    if kwargs:
        metadata.update(kwargs)

    return PlatformEvent(
        severity=severity,
        event_name=event_name,
        category=category,
        collector=collector,
        operation=operation,
        summary=summary,
        event_duration_ms=event_duration_ms,
        cause=cause,
        impact=impact,
        recommendations=(
            recommendations
            if recommendations is not None
            else ([comment] if comment else [])
        ),
        exc_info=exc_info,
        metadata=metadata,
        tags=tags,
    )
