load.py, iowait.py, pressure.py

Phase 1 — Computation
filter_compute.py

This should only:

filter invalid metrics
compute derived metrics
compute rates
compute ratios
mark seen=True

No health decisions here.

Examples:

load_per_core
core_imbalance
cpu_usage_growth
system_user_ratio
effective_busy_percent
frequency_scaling_ratio
Phase 2 — Resource analyzers

Each file owns one concern.

capacity.py
cpu utilization
idle percentage
load.py
load1
load5
load15
load_per_core
iowait.py
iowait
identify storage waiting
balance.py
hottest core
imbalance
uneven scheduling
kernel.py
user/system split
kernel dominance
steal.py
virtualization steal time
container.py
container cpu quota
throttling
cpu limits
pressure.py
CPU PSI
scheduler pressure
frequency.py
frequency scaling
throttling
turbo behaviour
Phase 3 — Normalizer
normalizer.py

Exactly like memory and disk.

Produce standardized signals only.

For example

cpu.total_utilization
cpu.idle_ratio
cpu.user_ratio
cpu.system_ratio
cpu.iowait_ratio

cpu.load.1
cpu.load.5
cpu.load.15
cpu.load_per_core

cpu.core.max
cpu.core.average
cpu.core.imbalance

cpu.frequency.current
cpu.frequency.max
cpu.frequency.ratio

psi.some.10
psi.some.60
psi.some.300
psi.full.10
...

No interpretation.

Phase 4 — Summary

This becomes tiny.

cpu.py

should simply

checks.extend(analyze_capacity(...))
checks.extend(analyze_load(...))
checks.extend(analyze_balance(...))
checks.extend(analyze_kernel(...))
...

then

signals = normalize(cpu)

return summarize_cpu(
    cpu,
    checks,
    signals,
    metadata,
)

Exactly the same flow as memory.

Phase 5 — Summary engine

Eventually I'd rename

cpu.py

to

summary.py

so every resource looks identical.

cpu/
    filter_compute.py
    normalizer.py

    capacity.py
    load.py
    iowait.py
    balance.py
    kernel.py
    steal.py
    pressure.py
    frequency.py
    container.py

    summary.py
    __init__.py

Every resource then has the same structure:

collect
        ↓
filter_compute
        ↓
normalizer
        ↓
resource analyzers
        ↓
