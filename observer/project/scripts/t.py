
"""
Test script for Platform Observer logger.
"""

from project.models.summary import PlatformEvent
from project.utils.logger import emit, emit_all


emit("Platform Observer started.")

emit(
    "disk_check",
    "Disk usage is high.",
    level="WARNING",
    category="storage",
    collector="disk",
    operation="scan",
    tags=["disk", "warning"],
    comment="Investigate disk usage if it remains above 90%.",
    filesystem="/var",
    used_percent=94,
)


def cpu_check():
    emit(
        "cpu_check",
        "CPU usage collected.",
        cpu=37,
        memory=58,
    )


# ==========================================================
# Nested function
# ==========================================================

def collect():

    def read_cpu():
        emit(
            "cpu_read",
            "Reading CPU statistics."
        )

    read_cpu()


cpu_check()

collect()


# emit_all
event = PlatformEvent(
    severity="ERROR",
    event_name="database_failure",
    category="database",
    collector="postgres",
    operation="connect",
    summary="Unable to connect to PostgreSQL.",

    duration_ms=1250,
    cause="Connection timeout",
    impact="Database unavailable",

    recommendations=[
        "Verify PostgreSQL service.",
        "Check firewall rules.",
    ],

    metadata={
        "host": "db01",
        "port": 5432,
        "retry": 3,
    },

    tags=["database", "critical"],
)

emit_all(event)
