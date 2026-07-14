
EBPF_EVENTS = [
    RuntimeEvent(
        pid=1234,
        timestamp=1720950000.55,
        category="fd",
        code="EMFILE",
    ),

    RuntimeEvent(
        pid=1234,
        timestamp=1720950010.20,
        category="signal",
        code="SIGSEGV",
    ),

    RuntimeEvent(
        pid=5678,
        timestamp=1720950020.10,
        category="memory",
        code="OOM_KILL",
    ),
]
