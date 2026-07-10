# Platform Compatibility

Observer is designed for Linux systems and normalizes metrics collected from multiple Linux interfaces, including:

psutil
/proc
/sys
Linux Pressure Stall Information (PSI)
Linux cgroups (v1 and v2)

Observer has been primarily developed and tested on Ubuntu/Debian systems. While many collectors support other Linux distributions, the availability and naming of kernel metrics can vary depending on:

Linux distribution
Kernel version
cgroup version (v1 or v2)
Container runtime (Docker, Kubernetes, Podman)
Virtualization platform
System permissions

When a metric is unavailable on a particular system, Observer leaves it unset (None) instead of failing the collection pipeline. This allows analysis to continue using the metrics that are available.
