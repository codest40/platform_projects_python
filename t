rules.is_multithreaded(analyses)
rules.is_interactive(analyses)
rules.is_daemon(analyses)
rules.is_container(analyses)
rules.is_blocked(analyses)
rules.is_cpu_bound(analyses)
...



summary.multithreaded = rules.is_multithreaded(results)

summary.interactive = rules.is_interactive(results)

summary.daemon = rules.is_daemon(results)

summary.container = rules.is_container(results)

summary.blocked = rules.is_blocked(results)

summary.cpu_bound = rules.is_cpu_bound(results)

summary.io_bound = rules.is_io_bound(results)

summary.resource_constrained = (
    rules.is_resource_constrained(results)
)

summary.approaching_limits = (
    rules.is_approaching_limits(results)
)

summary.healthy = (
    rules.is_process_healthy(summary)
)
