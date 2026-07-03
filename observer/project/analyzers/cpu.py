from project.models.cpu import Cpu_Data, CpuAnalysis
from project.models.events import HealthCheck
from project.utils.runner import get_status
from project.utils.helpers import timestamp


def analyze_cpu_metrics(result) -> CpuAnalysis:

    if result.status != get_status("SUCCESS"):
        raise RuntimeError(
            "❌ [CPU ANALYZER] CPU collection did not complete successfully."
        )

    cpu: Cpu_Data = result.data

    checks: list[HealthCheck] = []

    # ---------------------------------------------------
    # CPU Utilization
    # ---------------------------------------------------

    if cpu.usage_percent >= 90:
        checks.append(
            HealthCheck(
                check="CPU Utilization",
                status="CRITICAL",
                reason=f"CPU utilization is critically high ({cpu.usage_percent:.1f}%).",
            )
        )

    elif cpu.usage_percent >= 70:
        checks.append(
            HealthCheck(
                check="CPU Utilization",
                status="WARNING",
                reason=f"CPU utilization is elevated ({cpu.usage_percent:.1f}%).",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="CPU Utilization",
                status="PASS",
                reason=f"CPU utilization is healthy ({cpu.usage_percent:.1f}%).",
            )
        )

    # ---------------------------------------------------
    # Idle Time
    # ---------------------------------------------------

    if cpu.idle_percent >= 60:
        checks.append(
            HealthCheck(
                check="Idle CPU",
                status="PASS",
                reason=f"Idle CPU time is healthy ({cpu.idle_percent:.1f}%).",
            )
        )

    elif cpu.idle_percent >= 30:
        checks.append(
            HealthCheck(
                check="Idle CPU",
                status="WARNING",
                reason=f"Idle CPU time is becoming low ({cpu.idle_percent:.1f}%).",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Idle CPU",
                status="CRITICAL",
                reason=f"Very little idle CPU remains ({cpu.idle_percent:.1f}%).",
            )
        )

    # ---------------------------------------------------
    # Load Average
    # ---------------------------------------------------

    one_min = cpu.load_average[0]

    if one_min <= cpu.logical_cores:
        checks.append(
            HealthCheck(
                check="Load Average",
                status="PASS",
                reason="Load average is within available CPU capacity.",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Load Average",
                status="CRITICAL",
                reason="Load average exceeds available logical CPU cores.",
            )
        )

    # ---------------------------------------------------
    # IO Wait
    # ---------------------------------------------------

    if cpu.iowait_percent > 20:
        checks.append(
            HealthCheck(
                check="IO Wait",
                status="WARNING",
                reason=f"IO wait is {cpu.iowait_percent:.1f}%; storage may be the bottleneck.",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="IO Wait",
                status="PASS",
                reason="IO wait is within normal limits.",
            )
        )

    # ---------------------------------------------------
    # Per-Core Balance
    # ---------------------------------------------------

    hottest_core = max(cpu.per_core_util)

    if hottest_core >= 95 and cpu.usage_percent < 60:
        checks.append(
            HealthCheck(
                check="Core Balance",
                status="WARNING",
                reason="One CPU core is saturated while overall utilization remains moderate.",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Core Balance",
                status="PASS",
                reason="CPU workload is evenly distributed across cores.",
            )
        )

    # ---------------------------------------------------
    # Kernel Activity
    # ---------------------------------------------------

    if cpu.system_percent > cpu.user_percent:
        checks.append(
            HealthCheck(
                check="Kernel Activity",
                status="WARNING",
                reason="Kernel CPU time exceeds user CPU time.",
            )
        )

    else:
        checks.append(
            HealthCheck(
                check="Kernel Activity",
                status="PASS",
                reason="Kernel CPU activity is within expected limits.",
            )
        )

    # ---------------------------------------------------
    # Overall Verdict
    # ---------------------------------------------------

    statuses = {check.status for check in checks}

    if "CRITICAL" in statuses:
        verdict = "CPU remains a primary suspect."
        severity = "CRITICAL"
        comments = [
          "Inspect top CPU-consuming processes.",
          "Review recent deployment activity.",
        ]

    elif "WARNING" in statuses:
        verdict = "CPU shows warning signs but cannot yet be blamed."
        severity = "WARNING"
        comments = [
          "Check and rechack CPU-consuming processes for leaks.",
          "Scale workload if sustained above 80%.",
        ]

    else:
        verdict = "CPU can reasonably be ruled out."
        severity = "INFO"
        confidence = "Definately high"
        comments = [
          "None",
        ]

    return CpuAnalysis(
        component="cpu",
        summary=verdict,
        confidence=confidence if confidence else None,
        severity=severity,
        health_checks=checks,
        analyzed_at=timestamp(),
        recommendations=comments,
    )
