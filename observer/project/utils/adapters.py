from dataclasses import asdict, is_dataclass, fields

# Ensure Dict
def model_to_dict(obj):

    if obj is None:
        return {}

    if is_dataclass(obj):
        return {
            f.name: getattr(obj, f.name)
            for f in fields(obj)
        }

    if isinstance(obj, dict):
        return obj.copy()

    return vars(obj).copy()

# ===========================================================
# Adapt Resource Model -> emit()
# ===========================================================

EVENT_FIELDS = {
    "severity",
    "event_name",
    "summary",
    "category",
    "collector",
    "operation",
    "cause",
    "impact",
    "comment",
    "recommendations",
    "tags",
}


def adapt_event_model(
    *,
    resource: str,
    result,
    overrides: dict | None = None,
) -> dict:
    """
    Adapt any resource collection result into kwargs accepted by emit().
    Priority
    --------
    Framework Defaults
        < Resource Model
        < run_collection(success=...) / failure={}
    """

    overrides = overrides or {}

    model = result.data

    # ---------------------------------------------
    # Normalize model
    # ---------------------------------------------
    if model is None:
        data = {}

    data = model_to_dict(model)

    # ---------------------------------------------
    # Framework defaults
    # ---------------------------------------------
    event = {
        "severity": "INFO",
        "event_name": f"{resource.title()}_Collection",
        "summary": f"{resource.title()} collection completed.",
        "category": "system",
        "collector": None,
        "operation": "Collect",
        "cause": None,
        "impact": result.status,
        "comment": None,
        "recommendations": None,
        "tags": [],
    }

    # ---------------------------------------------
    # Promote resource fields
    # ---------------------------------------------
    metadata = {}

    for key, value in data.items():

        if key in EVENT_FIELDS:
            event[key] = value

        else:
            metadata[key] = value

    # ---------------------------------------------
    # Framework overrides always win
    # ---------------------------------------------
    event.update(overrides)

    # ---------------------------------------------
    # Attach metadata
    # ---------------------------------------------
    event["metadata"] = metadata

    # ---------------------------------------------
    # Duration from runner
    # ---------------------------------------------
    event["duration_ms"] = result.duration_ms

    return event



#======================================================
# analysis
#============================================

PROMOTED_ANALYSIS_FIELDS = {
    "component",
    "summary",
    "severity",
    "confidence",
    "health_checks",
    "recommendations",
    "analysis_id",
    "trace_id",
    "span_id",
    "parent_span_id",
    "analyzed_at",
}

def adapt_analysis_model(
    *,
    resource: str,
    analysis,
    overrides: dict | None = None,
) -> dict:

    overrides = overrides or {}

    # -----------------------------
    # Normalize
    # -----------------------------
    if analysis is None:
        data = {}

    data = model_to_dict(analysis)

    # -----------------------------
    # Framework defaults
    # -----------------------------
    event = {
        "component": resource,
        "summary": f"{resource.title()} analysis completed.",
        "severity": "INFO",
        "confidence": None,
        "health_checks": [],
        "recommendations": [],
        "analysis_id": None,
        "trace_id": None,
        "span_id": None,
        "analyzed_at": None,
    }

    metadata = {}

    for key, value in data.items():

        if key in PROMOTED_ANALYSIS_FIELDS:
            event[key] = value
        else:
            metadata[key] = value

    event.update(overrides)

    event["metadata"] = metadata

    return event
