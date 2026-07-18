from __future__ import annotations
from project.extractors.project_root import find_dir
from datetime import datetime
import json
import ast


LOG_DIR = find_dir("logs")
log_path = LOG_DIR / "observer.jsonl"


def read_log_records(x):
    all_data = []
    #print(f"Log Path: {log_path}")
    with open(log_path) as file:
      for line in file:
        data = json.loads(line)
        if data["type"] == x:
            all_data.append(data)
      return all_data



def find_latest_process_analysis(records):
    if not records:
        return None
    return max(
        records,
        key=lambda r: datetime.fromisoformat(r["timestamp"]),
    )


def split_top_level(text: str) -> list[str]:
    fields = []
    current = []

    paren = 0
    bracket = 0
    brace = 0

    quote = None
    escape = False

    for ch in text:
        if escape:
            current.append(ch)
            escape = False
            continue

        if ch == "\\":
            current.append(ch)
            escape = True
            continue

        if quote:
            current.append(ch)
            if ch == quote:
                quote = None
            continue

        if ch in ("'", '"'):
            quote = ch
            current.append(ch)
            continue

        if ch == "(":
            paren += 1
        elif ch == ")":
            paren -= 1
        elif ch == "[":
            bracket += 1
        elif ch == "]":
            bracket -= 1
        elif ch == "{":
            brace += 1
        elif ch == "}":
            brace -= 1

        if (
            ch == ","
            and paren == 0
            and bracket == 0
            and brace == 0
        ):
            field = "".join(current).strip()
            if field:
                fields.append(field)
            current.clear()
            continue
        current.append(ch)
    field = "".join(current).strip()
    if field:
        fields.append(field)
    return fields


def reconstruct_process(process: str) -> dict:
    process = process.removeprefix("ProcessSummary(")
    process = process.removesuffix(")")

    result = {}

    for field in split_top_level(process):
        key, value = field.split("=", 1)

        key = key.strip()
        value = value.strip()

        if key == "analyses":
            result.update(reconstruct_analyses(value))
            continue

        try:
            result[key] = ast.literal_eval(value)
        except Exception:
            result[key] = value
    return result


def reconstruct_analysis(text: str) -> tuple[str, dict]:
    """
    Parse a single Process*Analysis(...) object.
    """
    name, body = text.split("(", 1)
    body = body.removesuffix(")")

    result = {}

    for field in split_top_level(body):
        key, value = field.split("=", 1)

        key = key.strip()
        value = value.strip()

        try:
            result[key] = ast.literal_eval(value)
        except Exception:
            result[key] = value
    return name, result


def reconstruct_analyses(text: str) -> dict:
    """
    Flatten all Process*Analysis objects into a single
    process dictionary.
    """
    result = {}
    signals = {}

    text = text.strip()

    if text == "[]":
        return result

    text = text[1:-1].strip()

    analyses = split_top_level(text)

    ignore = {
        "pid",
        "tid",
        "facts",
        "recommendations",
        "classifications",
        "coverage",
    }

    for analysis in analyses:

        _, fields = reconstruct_analysis(analysis)

        for key, value in fields.items():

            if key in ignore:
                continue
            if key == "signals":
                signals.update(value)
                continue

            result[key] = value
    result["signals"] = signals
    return result


def reconstruct_process_inventory(record: dict) -> dict:
    payload = record["payload"]
    metadata = payload["metadata"]
    inventory = {
        "metadata": {
            "processes": [],
            "analyzed_total": metadata.get("analyzed_total", 0),
            "analyzed_successful": metadata.get(
                "analyzed_successful", 0
            ),
            "analyzed_failed": metadata.get(
                "analyzed_failed", 0
            ),
            "analysis_errors": metadata.get(
                "analysis_errors", []
            ),
            "analyzed_at": payload.get("analyzed_at"),
            "confidence": payload.get("confidence"),
        }
    }
    for process in metadata.get("processes", []):
        inventory["metadata"]["processes"].append(
            reconstruct_process(process)
        )
    return inventory


def load_process_inventory_from_logs(x):

    records = read_log_records(x)

    analysis = find_latest_process_analysis(records)

    inventory = reconstruct_process_inventory(analysis)

    return inventory



