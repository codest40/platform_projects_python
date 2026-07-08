# CPU Metrics Reference

This document explains every CPU metric collected and computed by the Observer platform.

| Metric                      | What it means                                                 | When high / low usually means                                                | Unit   |
| --------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------ |
| `cpu_model`                 | CPU model installed on the system.                            | Used to identify hardware capabilities.                                      | Text   |
| `physical_cores`            | Number of physical CPU cores.                                 | More cores generally provide greater compute capacity.                       | Count  |
| `logical_cores`             | Number of logical CPUs (including Hyper-Threading).           | Used when interpreting CPU load and utilization.                             | Count  |
| `usage_percent`             | Overall CPU currently being used.                             | High → CPU saturation. Low → CPU has spare capacity.                         | %      |
| `per_core_util`             | CPU usage of each logical core.                               | One core much higher than others → single-thread bottleneck or CPU affinity. | %      |
| `user_percent`              | CPU time spent running applications.                          | High → application workload.                                                 | %      |
| `system_percent`            | CPU time spent inside the Linux kernel.                       | High → filesystem, networking, or kernel overhead.                           | %      |
| `idle_percent`              | CPU sitting idle.                                             | Low → CPUs are busy.                                                         | %      |
| `iowait_percent`            | CPU waiting for disk operations to finish.                    | High → storage bottleneck.                                                   | %      |
| `steal_percent`             | Hypervisor stole CPU time from this VM.                       | High → host is oversubscribed.                                               | %      |
| `irq_percent`               | CPU handling hardware interrupts.                             | High → hardware or interrupt-heavy workload.                                 | %      |
| `softirq_percent`           | CPU handling software interrupts.                             | High → heavy network traffic or packet processing.                           | %      |
| `nice_percent`              | CPU used by low-priority processes.                           | High → background jobs consuming CPU.                                        | %      |
| `context_switches`          | Total task switches since boot.                               | Counter only; use the per-second rate for analysis.                          | Count  |
| `interrupts`                | Total hardware interrupts since boot.                         | Counter only; use the per-second rate for analysis.                          | Count  |
| `soft_interrupts`           | Total software interrupts since boot.                         | Counter only; use the per-second rate for analysis.                          | Count  |
| `syscalls`                  | Total system calls since boot.                                | Counter only; use the per-second rate for analysis.                          | Count  |
| `frequency_mhz`             | Current CPU clock speed.                                      | Low under load → power saving or throttling.                                 | MHz    |
| `min_frequency_mhz`         | Lowest supported CPU frequency.                               | Hardware capability.                                                         | MHz    |
| `max_frequency_mhz`         | Highest supported CPU frequency.                              | Hardware capability.                                                         | MHz    |
| `load_average`              | Number of runnable or waiting tasks over 1, 5 and 15 minutes. | Higher than logical cores → CPU contention.                                  | Load   |
| `psi_some_avg10`            | CPU pressure over the last 10 seconds.                        | High → tasks delayed waiting for CPU.                                        | %      |
| `psi_some_avg60`            | CPU pressure over the last 60 seconds.                        | High → sustained scheduler contention.                                       | %      |
| `psi_some_avg300`           | CPU pressure over the last 5 minutes.                         | High → long-term CPU contention.                                             | %      |
| `psi_full_avg10`            | Complete CPU stalls over the last 10 seconds.                 | Should almost always be zero.                                                | %      |
| `psi_full_avg60`            | Complete CPU stalls over the last 60 seconds.                 | High → severe CPU starvation.                                                | %      |
| `psi_full_avg300`           | Complete CPU stalls over the last 5 minutes.                  | High → long-term CPU starvation.                                             | %      |
| `throttled_periods`         | Number of times cgroups throttled CPU usage.                  | High → workload repeatedly hit CPU limits.                                   | Count  |
| `throttled_usec`            | Total CPU time denied by cgroups.                             | High → significant CPU time lost.                                            | μs     |
| `throttle_ratio`            | Relative severity of CPU throttling.                          | High → frequent or severe throttling.                                        | Ratio  |
| `top_process_name`          | Process currently using the most CPU.                         | Identifies the primary CPU consumer.                                         | Text   |
| `top_process_pid`           | PID of the busiest process.                                   | Used for investigation.                                                      | PID    |
| `top_process_cpu_percent`   | CPU consumed by the busiest process.                          | High → possible runaway process.                                             | %      |
| `context_switches_per_sec`  | How often tasks switch each second.                           | Very high → scheduler overhead or many threads.                              | /sec   |
| `interrupts_per_sec`        | Hardware interrupts each second.                              | High → interrupt-heavy workload.                                             | /sec   |
| `soft_interrupts_per_sec`   | Software interrupts each second.                              | High → networking or kernel activity.                                        | /sec   |
| `syscalls_per_sec`          | System calls executed each second.                            | High → heavy kernel interaction.                                             | /sec   |
| `load_per_core_1`           | 1-minute load normalized by CPU count.                        | Above 1 → more work than available CPU.                                      | Ratio  |
| `load_per_core_5`           | 5-minute normalized CPU load.                                 | High → sustained CPU pressure.                                               | Ratio  |
| `load_per_core_15`          | 15-minute normalized CPU load.                                | High → long-term CPU pressure.                                               | Ratio  |
| `highest_core_percent`      | Busiest CPU core.                                             | Near 100% → hotspot.                                                         | %      |
| `lowest_core_percent`       | Least busy CPU core.                                          | Much lower than highest → workload imbalance.                                | %      |
| `average_core_percent`      | Average utilization across all cores.                         | Overall CPU workload.                                                        | %      |
| `core_spread_percent`       | Difference between busiest and least busy core.               | High → uneven scheduling or CPU affinity.                                    | %      |
| `core_imbalance_percent`    | Difference between busiest core and average utilization.      | High → single-thread bottleneck.                                             | %      |
| `frequency_ratio`           | Current CPU speed relative to maximum.                        | Low under load → throttling or power saving.                                 | Ratio  |
| `kernel_ratio`              | Fraction of CPU time spent in kernel mode.                    | High → kernel-heavy workload.                                                | Ratio  |
| `throttled_periods_per_sec` | How often cgroups throttled the workload.                     | High → active CPU limits.                                                    | /sec   |
| `throttled_usec_per_sec`    | How much CPU time was actually denied.                        | High → significant throttling impact.                                        | μs/sec |
