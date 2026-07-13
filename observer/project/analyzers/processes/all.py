from project.analyzers.processes.identity import (
    analyze_identity,
)

from project.analyzers.processes.cpu import (
    analyze_cpu,
)
from project.analyzers.processes.mem import (
    analyze_memory,
)
from project.analyzers.processes.io import (
    analyze_io,
)
from project.analyzers.processes.sched import (
    analyze_scheduler,
)
from project.analyzers.processes.threads import (
    analyze_threads,
)
from project.analyzers.processes.fd import (
    analyze_fd,
)
from project.analyzers.processes.limit import (
    analyze_limits,
)
from project.analyzers.processes.wait_channels import (
    analyze_wait_channel,
)


analyses = [
    analyze_identity,
    analyze_cpu,
    analyze_memory,
    analyze_io,
    analyze_scheduler,
    analyze_threads,
    analyze_fd,
    analyze_limits,
    analyze_wait_channel,
]
