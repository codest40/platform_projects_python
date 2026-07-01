"""
Platform Observer Alert Manager

Responsibilities
----------------
- Route alerts to enabled channels
- Supply transport configuration
- Emit success/failure events
- Return delivery results
"""

from __future__ import annotations

from project.alerts.alert import (
    send_email,
    send_slack,
    send_discord,
    send_telegram,
)

from project.models.alert import (
    EmailConfig,
    SlackConfig,
    DiscordConfig,
    TelegramConfig,
    AlertResult,
    AlertBody,
)

from project.logging.logger import emit
from project.utils.helpers import ALERT_CONFIG, log_levels
from project.utils.context import get_caller_context
from project.utils.runner import TraceObserver, EventObserver
from project.utils.decorators import trace
import inspect

# ==========================================================
# EMAIL
# ==========================================================
def get_caller(func):
    caller = get_caller_context(func)
    return caller

@trace("email_alert")
def send_via_email(alert: Alert) -> AlertResult:

      config = ALERT_CONFIG["email"]

      result = send_email(
          config=config,
          alert=alert,
      )

      if result.success:

          emit(
              "alert.email.success",
              f"Email alert delivered via {result.provider}.",
              collector="alert_manager",
              operation="email alert",
              caller = get_caller(send_via_email),
          )

      else:

          emit(
            "alert.email.failed",
            result.reason,
            severity="ERROR",
            collector="alert_manager",
            operation="email alert",
            caller = get_caller(send_via_email),
        )

      return result


# ==========================================================
# SLACK
# ==========================================================

def send_via_slack(alert: SlackConfig) -> AlertResult:

    result = send_slack(
        ALERT_CONFIG["slack"],
        alert,
    )

    if result.success:

        emit(
            "alert.slack.success",
            "Slack alert delivered.",
            collector="alert_manager",
            operation="slack",
        )

    else:

        emit(
            "alert.slack.failed",
            result.message,
            severity="ERROR",
            collector="alert_manager",
            operation="slack",
        )

    return result


# ==========================================================
# DISCORD
# ==========================================================

def send_via_discord(alert: Discordconfig) -> AlertResult:

    result = send_discord(
        ALERT_CONFIG["discord"],
        alert,
    )

    if result.success:

        emit(
            "alert.discord.success",
            "Discord alert delivered.",
            collector="alert_manager",
            operation="discord",
        )

    else:

        emit(
            "alert.discord.failed",
            result.message,
            severity="ERROR",
            collector="alert_manager",
            operation="discord",
        )

    return result


# ==========================================================
# TELEGRAM
# ==========================================================

def send_via_telegram(alert: TelegramConfi) -> AlertResult:

    result = send_telegram(
        ALERT_CONFIG["telegram"],
        alert,
    )

    if result.success:

        emit(
            "alert.telegram.success",
            "Telegram alert delivered.",
            collector="alert_manager",
            operation="telegram",
        )

    else:

        emit(
            "alert.telegram.failed",
            result.message,
            severity="ERROR",
            collector="alert_manager",
            operation="telegram",
        )

    return result


# ==========================================================
# PUBLIC ENTRYPOINT
# ==========================================================
resource="alert"
with TraceObserver(resource):

  @trace("alert")
  def send_alert(
      title: str,
      message: str,
      severity: str = "INFO",
  ) -> list[AlertResult]:
      """
      Send one alert to every enabled notification channel.
      """
      results: list[AlertResult] = []

      #
      # Email
      #

      if ALERT_CONFIG["email"].enabled:

          results.append(

              send_via_email(

                  alert=AlertBody(
                      title=title,
                      message=message,
                      severity=severity,
                  )

              )

          )

        #
        # Slack
        #

      if ALERT_CONFIG["slack"].enabled:

          results.append(

              send_via_slack(

                  AlertBody(
                      title=title,
                      message=message,
                      severity=severity,
                  )

              )

          )

        #
        # Discord
        #

      if ALERT_CONFIG["discord"].enabled:

          results.append(

              send_via_discord(

                  AlertBody(
                      title=title,
                      message=message,
                      severity=severity,
                  )

              )

          )

        #
        # Telegram
        #

      if ALERT_CONFIG["telegram"].enabled:

          results.append(

              send_via_telegram(

                  TelegramAlert(
                      title=title,
                      message=message,
                      severity=severity,
                  )

              )

          )

      return results


#      resource="alert"
#      with TraceObserver(resource):

