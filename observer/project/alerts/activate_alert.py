from __future__ import annotations

from typing import Any, Callable

from project.alerts.alert_runner import send_alert
from project.logging.logger import emit, emit_exception
from project.models.alert import AlertResult
from project.utils.start_event import compiler


def run_alert(
    *,
    resource: str,
    func: Callable[..., Any],
    args: tuple = (),
    kwargs: dict | None = None,
    **runner_options,
) -> list[AlertResult]:

    obj, caller = compiler(
        resource=resource,
        func=func,
        args=args,
        kwargs=kwargs,
    )

    if obj.exception:

        emit_exception(
            caller=caller,
            category=obj.exc_type.__name__,
            cause=str(obj.exception),
            impact=obj.status,
            exc_info=(
                obj.exc_type,
                obj.exception,
                obj.traceback_obj,
            ),
            event="alert.runner.failed",
            collector="alert_manager",
            operation="alert dispatch",
            level="CRITICAL",
        )

        return []

    results: list[AlertResult] = obj.data

    for alert in results:

        if alert.success:

            emit(
                caller=caller,
                metadata=alert,
                summary=f"Alert delivered via {alert.provider}.",
                comment=alert.reason,
                duration_ms=obj.duration_ms,
                impact=obj.status,
                event=f"alert.{alert.provider}.success",
                collector="alert_manager",
                operation=f"{alert.provider} alert",
            )

        else:

            emit_exception(
                caller=caller,
                category="AlertDeliveryError",
                cause=alert.reason,
                impact=obj.status,
                event=f"alert.{alert.provider}.failed",
                level="ERROR",
                collector="alert_manager",
                operation=f"{alert.provider} alert",
                tags=["alert", alert.provider],
            )

    return results


def activate_run_alert(
    title: str,
    message: str,
    severity: str = "INFO",
) -> list[AlertResult]:

    return run_alert(
        resource="alert",
        func=send_alert,
        kwargs={
            "title": title,
            "message": message,
            "severity": severity,
        },
    )
