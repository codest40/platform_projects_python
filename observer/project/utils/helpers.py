from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from datetime import datetime
from zoneinfo import ZoneInfo
from time import perf_counter
import traceback as tb
import logging

#===================================================================
# Time Manager
UTC = ZoneInfo("UTC")
LOCAL_TZ = ZoneInfo("Europe/London")

def utc_now():
    return datetime.now(UTC)

def utc_local():
    return datetime.now(LOCAL_TZ)

def timestamp(local: bool = False, format: bool = True) -> str:
    if local:
        return utc_local()
    if not format:
      return utc_now()

    return utc_now().isoformat()


def start_count():
    return perf_counter()


#==================================================
VALID_STATUS = frozenset({"PENDING", "RUNNING", "SUCCESS", "FAILED", "LOCKED"})
def get_status(status: str) -> str:
    if status not in VALID_STATUS:
        raise ValueError(f"Invalid status: {status}")
    return status


#==================================================================
DEFAULT_WIDTH = 80
DEFAULT_FILL = "="
DEFAULT_TITLE = "[RUNNER] Script Running"

def line(
    title: str = DEFAULT_TITLE,
    width: int = DEFAULT_WIDTH,
    fill: str = DEFAULT_FILL,
) -> str:
    return f" {title} ".center(width, fill)


#================================================================
# LOG LEVLE
from project.models.context import LogLevels
def log_levels():
  return LogLevels(
        log_levels={
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        },
    )


#=====================================================
# Context buid helpers

from project.models.context import ContextHelpers

def context_helpers() -> ContextHelpers:

    return ContextHelpers(

        project_root=(
            "project",
        ),

        span_prefix=(
            "project.",
        ),

        app_name="Platform Observer",

        app_version="1.0.0",

        schema_version="1.0",

    )


# ==========================
# ALERT CONFIG
# ==========================================================
from project.models.alert import (
    EmailConfig,
    SlackConfig,
    DiscordConfig,
    TelegramConfig,
)

ALERT_CONFIG = {
    "email": EmailConfig(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        sender="paragoninfonet@gmail.com",
        receiver="rundailytest@gmail.com",
        username="paragoninfonet@gmail.com",
        password="ijiegyoumcquwzpw",
        use_tls=True,
        timeout=10,
    ),

    "slack": SlackConfig(
        webhook_url="",
        timeout=10,
    ),

    "discord": DiscordConfig(
        webhook_url="",
        timeout=10,
    ),

    "telegram": TelegramConfig(
        bot_token="",
        chat_id="",
        timeout=10,
    ),
}


#=============================================
# Resource Options
#===============================================
