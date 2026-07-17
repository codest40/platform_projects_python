# Adapting the Observer eBPF Program to Your Kernel

The Observer eBPF runtime uses Linux tracepoints.

Different kernel versions may expose different tracepoints or
different event argument layouts. Before modifying or extending
the Observer eBPF program, inspect the tracepoints available on
your own system.

--------------------------------------------------------------
1. Verify available syscall tracepoints
--------------------------------------------------------------

sudo bpftrace -l 'tracepoint:syscalls:*open*'

Examples:

tracepoint:syscalls:sys_enter_open
tracepoint:syscalls:sys_exit_open
tracepoint:syscalls:sys_enter_openat
tracepoint:syscalls:sys_exit_openat
tracepoint:syscalls:sys_enter_openat2
tracepoint:syscalls:sys_exit_openat2

--------------------------------------------------------------
2. Inspect tracepoint argument layouts
--------------------------------------------------------------

View every field exposed by a tracepoint.

Example:

sudo bpftrace -lv tracepoint:syscalls:sys_exit_openat

Also inspect newer variants:

sudo bpftrace -lv tracepoint:syscalls:sys_exit_openat2

Use these field names inside your eBPF program.

--------------------------------------------------------------
3. List OOM tracepoints
--------------------------------------------------------------

sudo bpftrace -l 'tracepoint:oom:*'

Inspect one:

sudo bpftrace -lv tracepoint:oom:oom_kill

--------------------------------------------------------------
4. List signal tracepoints
--------------------------------------------------------------

sudo bpftrace -l 'tracepoint:signal:*'

Inspect one:

sudo bpftrace -lv tracepoint:signal:signal_generate

--------------------------------------------------------------
5. List scheduler tracepoints
--------------------------------------------------------------

sudo bpftrace -l 'tracepoint:sched:*'

Examples:

sched_process_exit
sched_process_exec
sched_process_fork
sched_switch

Inspect one:

sudo bpftrace -lv tracepoint:sched:sched_process_exit

--------------------------------------------------------------
6. List all available tracepoint categories
--------------------------------------------------------------

sudo bpftrace -l 'tracepoint:*'

This helps discover kernel features that may not exist on
another distribution or kernel version.

--------------------------------------------------------------
7. Verify BTF support
--------------------------------------------------------------

ls /sys/kernel/btf/vmlinux

If present, your kernel exposes BTF information, allowing
CO-RE (Compile Once, Run Everywhere) eBPF programs.

--------------------------------------------------------------
8. Generate vmlinux.h (if needed)
--------------------------------------------------------------

bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h

--------------------------------------------------------------
9. Rebuild the Observer eBPF program
--------------------------------------------------------------

After changing tracepoints or event structures:

clang -O2 -g \
    -target bpf \
    -D__TARGET_ARCH_x86 \
    -c runtime.bpf.c \
    -o runtime.bpf.o

--------------------------------------------------------------
10. Test the generated events
--------------------------------------------------------------

sudo ./runtime_loader

Trigger the event (open files, OOM, signals, etc.) and verify
that runtime events are printed correctly.
