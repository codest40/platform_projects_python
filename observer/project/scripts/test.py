
"""
Test script for Platform Observer logger.
"""

from project.models.events import PlatformEvent
from project.utils.logger import emit, emit_all
from project.utils.decorators import trace


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


# ==========================================================
# Nested function
# ==========================================================

@trace()
def collect():

    def read_cpu():
        emit(
            "cpu_read",
            "Reading CPU statistics."
        )

    read_cpu()


collect()


