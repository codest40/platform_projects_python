// runtime.bpf.c
//
// Observer process runtime event collector.
//
// Kernel -> ring buffer -> userspace
//
// Supported:
//   - open/openat/openat2 FD exhaustion
//   - fatal signals
//   - OOM kills
//

#include "vmlinux.h"

#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>
#include <bpf/bpf_core_read.h>


char LICENSE[] SEC("license") = "GPL";



/*
 * Linux error numbers.
 *
 * eBPF programs do not include libc headers.
 */

#define EMFILE 24
#define ENFILE 23



/*
 * Linux signals.
 */

#define SIGILL   4
#define SIGABRT  6
#define SIGBUS   7
#define SIGFPE   8
#define SIGSEGV 11
#define SIGPIPE 13



/*
 * Event categories
 */

enum event_category {

    EVENT_FD = 1,
    EVENT_MEMORY = 2,
    EVENT_SIGNAL = 3,
};



/*
 * Event codes
 */

enum event_code {

    CODE_EMFILE = 1,
    CODE_ENFILE = 2,

    CODE_OOM_KILL = 100,

    CODE_SIGSEGV = 200,
    CODE_SIGBUS,
    CODE_SIGABRT,
    CODE_SIGILL,
    CODE_SIGFPE,
    CODE_SIGPIPE,
};



/*
 * Shared with userspace.
 */

struct runtime_event {

    __u32 pid;

    __u32 tid;


    __u64 timestamp_ns;


    __u16 category;

    __u16 code;


    __s64 value;
};



/*
 * Ring buffer.
 */

struct {

    __uint(type, BPF_MAP_TYPE_RINGBUF);

    __uint(max_entries, 1 << 20);

} runtime_events SEC(".maps");



/*
 * Emit helper.
 */

static __always_inline void emit_event(
    __u16 category,
    __u16 code,
    __s64 value
)
{

    struct runtime_event *event;


    event = bpf_ringbuf_reserve(
        &runtime_events,
        sizeof(*event),
        0
    );


    if (!event)
        return;



    __u64 id =
        bpf_get_current_pid_tgid();



    event->pid =
        id >> 32;


    event->tid =
        (__u32)id;


    event->timestamp_ns =
        bpf_ktime_get_ns();


    event->category =
        category;


    event->code =
        code;


    event->value =
        value;


    bpf_ringbuf_submit(
        event,
        0
    );
}



/*
 *
 * FD exhaustion
 *
 */


static __always_inline int handle_open_ret(
    long ret
)
{

    if (ret == -EMFILE)
    {

        emit_event(
            EVENT_FD,
            CODE_EMFILE,
            ret
        );

    }
    else if (ret == -ENFILE)
    {

        emit_event(
            EVENT_FD,
            CODE_ENFILE,
            ret
        );

    }


    return 0;
}



SEC("tracepoint/syscalls/sys_exit_open")
int trace_open_exit(
    struct trace_event_raw_sys_exit *ctx
)
{
    return handle_open_ret(ctx->ret);
}



SEC("tracepoint/syscalls/sys_exit_openat")
int trace_openat_exit(
    struct trace_event_raw_sys_exit *ctx
)
{
    return handle_open_ret(ctx->ret);
}



SEC("tracepoint/syscalls/sys_exit_openat2")
int trace_openat2_exit(
    struct trace_event_raw_sys_exit *ctx
)
{
    return handle_open_ret(ctx->ret);
}




/*
 *
 * Signals
 *
 */


SEC("tracepoint/signal/signal_generate")
int trace_signal(
    struct trace_event_raw_signal_generate *ctx
)
{

    switch(ctx->sig)
    {

        case SIGSEGV:

            emit_event(
                EVENT_SIGNAL,
                CODE_SIGSEGV,
                ctx->sig
            );
            break;


        case SIGBUS:

            emit_event(
                EVENT_SIGNAL,
                CODE_SIGBUS,
                ctx->sig
            );
            break;


        case SIGABRT:

            emit_event(
                EVENT_SIGNAL,
                CODE_SIGABRT,
                ctx->sig
            );
            break;


        case SIGILL:

            emit_event(
                EVENT_SIGNAL,
                CODE_SIGILL,
                ctx->sig
            );
            break;


        case SIGFPE:

            emit_event(
                EVENT_SIGNAL,
                CODE_SIGFPE,
                ctx->sig
            );
            break;


        case SIGPIPE:

            emit_event(
                EVENT_SIGNAL,
                CODE_SIGPIPE,
                ctx->sig
            );
            break;

    }


    return 0;
}




/*
 *
 * OOM
 *
 */


/*
 * Your kernel has the tracepoint,
 * but BTF does not expose the struct.
 *
 * Match the tracepoint layout manually.
 */


struct oom_mark_victim_ctx {

    __u64 pad;

    int pid;

    char comm[16];

    unsigned long total_vm;

    unsigned long anon_rss;

    unsigned long file_rss;

    unsigned long shmem_rss;

};



SEC("tracepoint/oom/mark_victim")
int trace_oom(
    struct oom_mark_victim_ctx *ctx
)
{

    emit_event(
        EVENT_MEMORY,
        CODE_OOM_KILL,
        ctx->pid
    );


    return 0;
}
