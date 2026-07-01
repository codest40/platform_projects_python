"""
Platform Observer Alert Manager

Responsibilities
----------------
- Route alerts to enabled channels
- Supply transport configuration
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

from project.utils.helpers import ALERT_CONFIG, log_levels
from project.utils.decorators import trace

# ==========================================================
# EMAIL
# ==========================================================

def send_via_email(alert: Alert) -> AlertResult:

      config = ALERT_CONFIG["email"]

      result = send_email(
          config=config,
          alert=alert,
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

    return result


# ==========================================================
# DISCORD
# ==========================================================

def send_via_discord(alert: Discordconfig) -> AlertResult:

    result = send_discord(
        ALERT_CONFIG["discord"],
        alert,
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

    return result


# ==========================================================
# PUBLIC ENTRYPOINT
# ==========================================================
def send_alert(
      title: str,
      message: str,
      severity: str = "INFO",
  ) -> list[AlertResult]:
      """
      Send one alert to every enabled notification channel.
      """
      results: list[AlertResult] = []

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


