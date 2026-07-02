"""
Logging Formatters
Provides JSON and human-readable formatters for
Platform Observer log records.
"""

from __future__ import annotations

import json
import logging

from project.models.events import PlatformEvent, AnalysisEvent
from project.utils.context import (
    HOSTNAME, PID,
    timestamp as current_timestamp,
    serialize_event,
    serialize_span,
    serialize_analysis,
)


# =========================================================
# JSON FORMATTER
# =========================================================

class JsonFormatter(logging.Formatter):
    """
    Writes one JSON object per line.
    """

    def format(self, record: logging.LogRecord) -> str:

        if hasattr(record, "platform_event"):
          event: PlatformEvent = record.platform_event
          payload = serialize_event(
              event,
              record.caller,
          )

        elif hasattr(record, "analysis_event"):
          event: AnalysisEvent = record.analysis_event
          payload = serialize_analysis(
              event,
              record.caller,
          )

        elif hasattr(record, "platform_span"):
            span = record.platform_span
            payload = serialize_span(span, record.caller)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(
            payload,
            default=str,
            ensure_ascii=False,
        )


# =========================================================
# PRETTY FORMATTER
# =========================================================

class PrettyFormatter(logging.Formatter):
    """
    Human-friendly log formatter.

    Intended for operators reading logs directly.
    """

    separator = "-" * 80

    def format(self, record: logging.LogRecord) -> str:

        if hasattr(record, "platform_event"):
            return self._format_event(record)

        if hasattr(record, "analysis_event"):
            return self._format_analysis(record)

        if hasattr(record, "platform_span"):
            return self._format_span(record)

        return super().format(record)


    def _format_event(self, record):
        event: PlatformEvent = record.platform_event

        lines = [

            self.separator,

            f"[{event.severity}] {event.event_name}",

            "",

            f"Timestamp      : {current_timestamp()}",

            f"Summary        : {event.summary}",

            f"Category       : {event.category}",

            f"Collector      : {event.collector}",

            f"Operation      : {event.operation}",

            f"Hostname       : {HOSTNAME}",

            f"PID            : {PID}",

        ]

        if event.event_duration_ms is not None:

            lines.append(
                f"Duration       : {event.event_duration_ms} ms"
            )

        if event.cause:

            lines.append(
                f"Cause          : {event.cause}"
            )

        if event.impact:

            lines.append(
                f"Impact         : {event.impact}"
            )

        if event.tags:

            lines.append(
                f"Tags           : {', '.join(event.tags)}"
            )

        if event.event_id:

            lines.append(
                f"Event ID        : {event.event_id}"
            )

        if event.trace_id:

            lines.append(
                f"Trace ID        : {event.trace_id}"
            )

        if event.span_id:

            lines.append(
                f"Span ID        : {event.span_id}"
            )

        if event.parent_span_id:

            lines.append(
                f"Parent ID        : {event.parent_span_id}"
            )

        if event.metadata:

            lines.append("")

            lines.append("Metadata")

            for key, value in event.metadata.items():

                lines.append(
                    f"  • {key:<18} {value}"
                )

        if event.recommendations:

            lines.append("")

            lines.append("Recommendations")

            for item in event.recommendations:

                lines.append(
                    f"  • {item}"
                )


        caller = record.caller
        #print(f"Printing Caller: {caller}")
        if caller:
          lines.extend([
              "",
              "Caller",
              f"  Module        : {caller.get('module', 'N/A')}",
              f"  File          : {caller.get('file', 'N/A')}",
              f"  Function      : {caller.get('function', 'N/A')}",
              f"  Line          : {caller.get('line', 'N/A')}",
          ])

        if record.exc_info:

            lines.extend([
                "",
                "Exception",
                self.formatException(record.exc_info),
            ])

        lines.append(self.separator)

        return "\n".join(lines)


    def _format_span(self, record):

      span = record.platform_span

      lines = [
          self.separator,
          "[SPAN]",
          "",
          f"Name            : {span.name}",
          f"Trace ID        : {span.trace_id}",
          f"Span ID         : {span.span_id}",
          f"Parent Span ID  : {span.parent_span_id}",
          f"Started At      : {span.started_at}",
          f"Finished At     : {span.finished_at}",
          f"Duration        : {span.span_duration_ms} ms",
          "",
          "Caller",
          f"  Module        : {record.caller['module']}",
          f"  File          : {record.caller['file']}",
          f"  Function      : {record.caller['function']}",
          f"  Line          : {record.caller['line']}",
          "",
          "Execution Path: --->",
      ]

      for i, step in enumerate(record.caller["execution"], start=1):
        lines.append(f"  {i}. {step}")

      lines.append(self.separator)

      return "\n".join(lines)



    def _format_analysis(self, record):

        analysis = record.analysis_event
        lines = [
            self.separator,
            "[ANALYSIS]",
            "",
            f"Timestamp      : {analysis.analyzed_at}",
            f"Component      : {analysis.component}",
            f"Summary        : {analysis.summary}",
        ]

        if analysis.confidence is not None:
            lines.append(f"Confidence   : {analysis.confidence}")

        if analysis.recommendations:
            lines.append("Recommendations:")
            for each in analysis.recommendations:
              lines.append(
                f"• {each}"
              )
            lines.append("")

        if analysis.duration_ms is not None:
            lines.append(
                f"Duration       : {analysis.duration_ms:.3f} ms"
            )

        if analysis.analysis_id:
          lines.append(
              f"Analysis ID    : {analysis.analysis_id}"
          )

        if analysis.trace_id:
          lines.append(
              f"Trace ID       : {analysis.trace_id}"
          )

        if analysis.span_id:
          lines.append(
              f"Span ID        : {analysis.span_id}"
          )

        if analysis.health_checks:

          lines.append("")
          lines.append("Health Checks")

          icons = {
              "PASS": "✅",
              "WARNING": "⚠️ ",
              "CRITICAL": "❌ ",
          }

          for check in analysis.health_checks:

              icon = icons.get(check.status, "-")
              lines.append(
                  f"  {icon} [{check.status}] {check.check}"
              )
              lines.append(
                  f"      {check.reason}"
              )

        caller = record.caller
        lines.extend([
            "Caller",
            f"  Module        : {caller['module']}",
            f"  File          : {caller['file']}",
            f"  Function      : {caller['function']}",
            f"  Line          : {caller['line']}",
        ])

        lines.append(self.separator)

        return "\n".join(lines)
