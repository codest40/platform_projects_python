#

# 1. Verify available syscall tracepoints
sudo bpftrace -l 'tracepoint:syscalls:*open*'

# 2. Inspect sys_exit_openat arguments
sudo bpftrace -lv tracepoint:syscalls:sys_exit_openat

# 3. Inspect sys_exit_openat2 arguments
sudo bpftrace -lv tracepoint:syscalls:sys_exit_openat2

# 4. List OOM tracepoints
sudo bpftrace -l 'tracepoint:oom:*'

# 5. List signal tracepoints
sudo bpftrace -l 'tracepoint:signal:*'

# 6. List scheduler tracepoints
sudo bpftrace -l 'tracepoint:sched:*'
