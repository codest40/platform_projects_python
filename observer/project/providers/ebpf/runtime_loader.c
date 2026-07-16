// runtime_loader.c
//
// Userspace loader for Observer runtime eBPF program.
//
// Loads runtime.bpf.o
// Attaches tracepoints
// Reads ring buffer events
//

#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

#include <linux/types.h>

#include <bpf/libbpf.h>
#include <bpf/bpf.h>

#include "runtime.skel.h"


static volatile sig_atomic_t running = 1;



/*
 * Must match runtime.bpf.c exactly
 */

struct runtime_event {

    __u32 pid;

    __u32 tid;


    __u64 timestamp_ns;


    __u16 category;

    __u16 code;


    __s64 value;
};




static void handle_signal(int signo)
{
    running = 0;
}




static int handle_event(
    void *ctx,
    void *data,
    size_t data_sz
)
{

    const struct runtime_event *event = data;


    if (data_sz < sizeof(*event))
        return 0;



    printf(
        "pid=%u tid=%u category=%u code=%u value=%lld\n",
        event->pid,
        event->tid,
        event->category,
        event->code,
        event->value
    );


    return 0;
}





int main(void)
{

    struct runtime_bpf *skel;

    struct ring_buffer *ring_buffer = NULL;

    int err;



    signal(
        SIGINT,
        handle_signal
    );

    signal(
        SIGTERM,
        handle_signal
    );



    libbpf_set_strict_mode(
        LIBBPF_STRICT_ALL
    );



    /*
     * Open skeleton
     */

    skel = runtime_bpf__open();

    if (!skel)
    {
        fprintf(
            stderr,
            "Failed to open skeleton\n"
        );

        return 1;
    }




    /*
     * Load into kernel
     */

    err = runtime_bpf__load(skel);

    if (err)
    {
        fprintf(
            stderr,
            "Failed loading BPF object: %d\n",
            err
        );

        goto cleanup;
    }





    /*
     * Attach tracepoints
     */

    err = runtime_bpf__attach(skel);

    if (err)
    {
        fprintf(
            stderr,
            "Failed attaching BPF programs: %d\n",
            err
        );

        goto cleanup;
    }





    /*
     * Create ring buffer reader
     */

    ring_buffer =
        ring_buffer__new(
            bpf_map__fd(
                skel->maps.runtime_events
            ),
            handle_event,
            NULL,
            NULL
        );


    if (!ring_buffer)
    {
        fprintf(
            stderr,
            "Failed creating ring buffer\n"
        );

        err = -1;

        goto cleanup;
    }




    printf(
        "Observer runtime loader running...\n"
    );




    while (running)
    {

        err =
            ring_buffer__poll(
                ring_buffer,
                100
            );


        if (err == -EINTR)
            break;


        if (err < 0)
        {

            fprintf(
                stderr,
                "Ring buffer error: %d\n",
                err
            );

            break;
        }
    }




cleanup:


    if (ring_buffer)
        ring_buffer__free(
            ring_buffer
        );


    runtime_bpf__destroy(
        skel
    );


    return 0;
}
