# Platform Compatibility
Observer is a Linux-first observability framework that collects metrics from multiple Linux interfaces and normalizes them into a consistent internal data model for analysis.

## Supported Metric Sources
Observer currently targets:

- Linux kernels with `/proc` and `/sys`
- Python 3.12+
- Read access to standard kernel interfaces
- Optional support for Linux PSI and cgroups when available

Observer collects metrics from:

* `psutil`
* `/proc`
* `/sys`
* Linux Pressure Stall Information (PSI)
* Linux cgroups (v1 and v2)

---

## Current Platform Support

Observer has been primarily developed and validated on:

* Ubuntu
* Debian

Many collectors also work on other Linux distributions. However, the availability, naming, and behavior of kernel metrics may differ depending on the system configuration.
Different Linux distributions, kernel versions, and runtime environments may expose different files, counters, or kernel features. As a result, some metrics may be unavailable on certain systems.
Factors that can affect metric availability include:

* Linux distribution
* Kernel version
* cgroup version (v1 or v2)
* Container runtime (Docker, Kubernetes, Podman, etc.)
* Virtualization platform
* System permissions and capabilities

---

## Compatibility Philosophy

Observer is designed to be resilient across different Linux environments.

> **Missing metrics are not treated as collection failures.**

If a metric is unavailable on a particular system, Observer records it as `None` and continues the collection pipeline. This allows analyzers to operate using the metrics that are available instead of failing because a platform-specific interface is missing.

As support for additional Linux environments expands, collectors will continue to recognize platform-specific metric sources while presenting a consistent internal data model to the analysis engine.

---

## Compatibility Roadmap

Future releases will expand testing and validation across:

### Linux Distributions

* RHEL
* Rocky Linux
* AlmaLinux
* Fedora
* Arch Linux
* Amazon Linux
* SUSE Linux Enterprise

### Container Platforms

* Docker
* Kubernetes
* Podman

### Cloud Platforms

* Amazon Web Services (AWS)
* Microsoft Azure
* Google Cloud Platform (GCP)
