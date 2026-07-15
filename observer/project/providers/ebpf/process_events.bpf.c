// process_events.bpf.c

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>

char LICENSE[] SEC("license") = "GPL";

/*
 * Called whenever a process executes
 * (execve family of syscalls).
 */

SEC("tracepoint/sched/sched_process_exec")
int process_exec(void *ctx)
{
    bpf_printk("Observer: process executed\n");
    return 0;
}
