"""
Platform Observer Logging Core

Creates and configures the application's logging infrastructure,
including log directories, handlers, and the shared logger instance.
"""

from __future__ import annotations
import logging
from pathlib import Path
from project.logging.formatters import (
    JsonFormatter,
    PrettyFormatter,
)


# =========================================================
# LOG DIRECTORIES
# =========================================================

LOG_DIR = Path("logs")

LOG_DIR.mkdir(parents=True, exist_ok=True)

JSON_LOG = LOG_DIR / "observer.jsonl"

TEXT_LOG = LOG_DIR / "observer.log"


# =========================================================
# LOGGER
# =========================================================

LOGGER_NAME = "platform_observer"

logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.DEBUG)

logger.propagate = False


# =========================================================
# HANDLER FACTORY
# =========================================================

def create_handler(
    handler: logging.Handler,
    formatter: logging.Formatter,
    level: int = logging.DEBUG,
) -> logging.Handler:

    handler.setLevel(level)

    handler.setFormatter(formatter)

    return handler


# =========================================================
# FILE HANDLERS
# =========================================================

json_handler = create_handler(
    logging.FileHandler(
        JSON_LOG,
        encoding="utf-8",
    ),
    JsonFormatter(),
)

pretty_handler = create_handler(
    logging.FileHandler(
        TEXT_LOG,
        encoding="utf-8",
    ),
    PrettyFormatter(),
)


# =========================================================
# CONSOLE HANDLER
# =========================================================

console_handler = create_handler(
    logging.StreamHandler(),
    PrettyFormatter(),
)


# =========================================================
# REGISTER HANDLERS
# =========================================================

if not logger.handlers:

    logger.addHandler(json_handler)

    logger.addHandler(pretty_handler)

    logger.addHandler(console_handler)
