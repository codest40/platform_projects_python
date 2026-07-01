"""
Platform Observer Alert Transporters
- Send Email
- Send Slack
- Send Discord
- Send Telegram
"""

from __future__ import annotations

import smtplib
from email.message import EmailMessage

import requests
from project.utils.helpers import timestamp
from project.models.alert import (
    EmailConfig,
    SlackConfig,
    DiscordConfig,
    TelegramConfig,
    AlertResult,
)


# ==========================================================
# EMAIL
# ==========================================================
def send_email(
    config,
    alert: AlertBody,
) -> bool:
    """
    Send an email using any supplied SMTP provider.
    """
    def get_provider(email):
        return email.split("@", 1)[1].split(".", 1)[0]

    provider=get_provider(config.username)
    result=AlertResult(success=False, provider=provider, reason="")

    try:

        message = EmailMessage()
        message["From"] = config.sender
        message["To"] = config.receiver
        message["Subject"] = alert.title
        body = f"""
Severity : {alert.severity} || Date: {timestamp(format=False).strftime('%Y-%m-%d_%H-%M-%S')}

{alert.message}
"""

        message.set_content(body)

        with smtplib.SMTP(
            config.smtp_server,
            config.smtp_port,
            timeout=config.timeout,
        ) as smtp:

            if config.use_tls:
                smtp.starttls()

            smtp.login(
                config.username,
                config.password,
            )

            smtp.send_message(message)
            result.success=True
        return result

    except Exception as e:
        result.reason=e
        return result


# ==========================================================
# SLACK
# ==========================================================

def send_slack(
    config,
    alert: AlertSlack,
) -> bool:

    payload = {
        "text": f"*{alert.severity}*\n\n{alert.title}\n\n{alert.message}"
    }

    try:

        response = requests.post(
            config.webhook_url,
            json=payload,
            timeout=config.timeout,
        )

        return response.status_code == 200

    except Exception:

        return False


# ==========================================================
# DISCORD
# ==========================================================

def send_discord(
    config,
    alert: AlertDiscord,
) -> bool:

    payload = {
        "content": (
            f"**{alert.severity}**\n\n"
            f"**{alert.title}**\n\n"
            f"{alert.message}"
        )
    }

    try:

        response = requests.post(
            config.webhook_url,
            json=payload,
            timeout=config.timeout,
        )

        return response.status_code in (200, 204)

    except Exception:

        return False


# ==========================================================
# TELEGRAM
# ==========================================================

def send_telegram(
    config,
    alert: AlertTelegram,
) -> bool:

    url = (
        f"https://api.telegram.org/bot"
        f"{config.bot_token}/sendMessage"
    )

    payload = {
        "chat_id": config.chat_id,
        "text": (
            f"{alert.severity}\n\n"
            f"{alert.title}\n\n"
            f"{alert.message}"
        ),
    }

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=config.timeout,
        )

        return response.status_code == 200

    except Exception:

        return False
