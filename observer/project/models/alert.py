from __future__ import annotations
from dataclasses import dataclass

# ==========================================================
# EMAIL CONFIG
# ==========================================================

@dataclass(slots=True)
class EmailConfig:
    smtp_server: str

    smtp_port: int

    sender: str

    receiver: str

    username: str

    password: str

    use_tls: bool = True

    timeout: int = 10

    enabled: bool = True


# ==========================================================
# SLACK CONFIG
# ==========================================================

@dataclass(slots=True)
class SlackConfig:

    webhook_url: str

    timeout: int = 10

    enabled: bool = False

# ==========================================================
# DISCORD CONFIG
# ==========================================================

@dataclass(slots=True)
class DiscordConfig:

    webhook_url: str

    timeout: int = 10

    enabled: bool = False

# ==========================================================
# TELEGRAM CONFIG
# ==========================================================

@dataclass(slots=True)
class TelegramConfig:
    bot_token: str

    chat_id: str

    timeout: int = 10
    enabled: bool = False


# ALERT RESULT
@dataclass(slots=True)
class AlertResult:

    provider: str

    success: bool

    reason: str


@dataclass(slots=True)
class AlertBody:
    title: str
    message: str
    severity: str = "INFO"

