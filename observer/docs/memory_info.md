# Memory Metrics Reference

## This document explains every memory metric collected and computed by the Observer platform.

| Metric                               | What it means                                     | When high / low usually means                                 | Unit         |
| ------------------------------------ | ------------------------------------------------- | ------------------------------------------------------------- | ------------ |
| `total`                              | Total physical memory installed.                  | System capacity.                                              | Bytes        |
| `available`                          | Memory immediately available for applications.    | Low → memory pressure.                                        | Bytes        |
| `used`                               | Memory currently in use.                          | High alone isn't necessarily bad; check available memory too. | Bytes        |
| `free`                               | Completely unused memory.                         | Linux often keeps this low by using memory for cache.         | Bytes        |
| `cached`                             | Memory used for filesystem cache.                 | High is usually healthy and reclaimable.                      | Bytes        |
| `buffers`                            | Memory used for filesystem metadata buffers.      | High is generally normal.                                     | Bytes        |
| `shared`                             | Memory shared between processes.                  | High → shared memory workloads.                               | Bytes        |
| `active`                             | Recently used memory.                             | High → active workload.                                       | Bytes        |
| `inactive`                           | Less recently used memory.                        | High → reclaimable if needed.                                 | Bytes        |
| `slab`                               | Kernel memory used for caches.                    | High → kernel caching activity.                               | Bytes        |
| `slab_reclaimable`                   | Slab memory that can be reclaimed.                | High → reclaimable kernel cache.                              | Bytes        |
| `slab_unreclaimable`                 | Slab memory that cannot be reclaimed.             | High → potential kernel memory growth.                        | Bytes        |
| `page_tables`                        | Memory used for page tables.                      | High → many mapped pages or processes.                        | Bytes        |
| `kernel_stack`                       | Memory used by kernel stacks.                     | High → many active threads.                                   | Bytes        |
| `wired`                              | Memory locked and cannot be swapped (BSD/macOS).  | High → less reclaimable memory.                               | Bytes        |
| `vmalloc_used`                       | Kernel virtual memory allocation.                 | High → heavy kernel allocations.                              | Bytes        |
| `percent`                            | Overall memory utilization.                       | High → memory becoming exhausted.                             | %            |
| `available_percent`                  | Percentage of memory still available.             | Low → memory pressure.                                        | %            |
| `used_percent`                       | Percentage of memory currently used.              | High → investigate available memory before concluding.        | %            |
| `cache_percent`                      | Memory occupied by cache.                         | High is usually beneficial.                                   | %            |
| `buffer_percent`                     | Memory occupied by buffers.                       | High is generally normal.                                     | %            |
| `swap_total`                         | Total configured swap space.                      | System capacity.                                              | Bytes        |
| `swap_used`                          | Swap currently in use.                            | High → memory shortage or inactive pages swapped out.         | Bytes        |
| `swap_free`                          | Remaining swap space.                             | Low → swap nearing exhaustion.                                | Bytes        |
| `swap_percent`                       | Swap utilization.                                 | High → sustained memory pressure.                             | %            |
| `swap_in`                            | Total data swapped into RAM.                      | Counter only; use rate for analysis.                          | Bytes        |
| `swap_out`                           | Total data swapped to disk.                       | Counter only; use rate for analysis.                          | Bytes        |
| `pages_swapped_in`                   | Pages restored from swap.                         | Counter only; use rate for analysis.                          | Pages        |
| `pages_swapped_out`                  | Pages written to swap.                            | Counter only; use rate for analysis.                          | Pages        |
| `committed_as`                       | Memory promised to applications.                  | High → applications reserving large amounts of memory.        | Bytes        |
| `commit_limit`                       | Maximum memory Linux can commit.                  | System limit.                                                 | Bytes        |
| `commit_percent`                     | Committed memory relative to commit limit.        | High → risk of allocation failures.                           | %            |
| `major_page_faults`                  | Page faults requiring disk access.                | Counter only; use rate for analysis.                          | Count        |
| `minor_page_faults`                  | Page faults served from RAM.                      | Usually normal.                                               | Count        |
| `total_page_faults`                  | Total page faults.                                | Counter only; use rate for analysis.                          | Count        |
| `pages_scanned`                      | Pages scanned by memory reclaim.                  | High → kernel reclaim activity.                               | Pages        |
| `pages_reclaimed`                    | Pages successfully reclaimed.                     | High → reclaim actively freeing memory.                       | Pages        |
| `reclaim_activity`                   | Overall memory reclaim activity.                  | High → sustained memory pressure.                             | Count        |
| `allocation_failures`                | Failed memory allocations.                        | High → memory exhaustion.                                     | Count        |
| `psi_some_avg10`                     | Memory pressure over last 10 seconds.             | High → tasks delayed waiting for memory.                      | %            |
| `psi_some_avg60`                     | Memory pressure over last 60 seconds.             | Sustained memory contention.                                  | %            |
| `psi_some_avg300`                    | Memory pressure over last 5 minutes.              | Long-term memory pressure.                                    | %            |
| `psi_full_avg10`                     | Complete memory stalls over last 10 seconds.      | High → severe memory starvation.                              | %            |
| `psi_full_avg60`                     | Complete memory stalls over last 60 seconds.      | Sustained severe memory pressure.                             | %            |
| `psi_full_avg300`                    | Complete memory stalls over last 5 minutes.       | Long-term memory starvation.                                  | %            |
| `low_memory_events`                  | Number of low-memory events.                      | High → kernel repeatedly under memory pressure.               | Count        |
| `oom_events`                         | Number of Out-Of-Memory events.                   | High → processes killed due to memory exhaustion.             | Count        |
| `huge_pages_total`                   | Configured huge pages.                            | Huge page capacity.                                           | Pages        |
| `huge_pages_free`                    | Available huge pages.                             | Low → huge pages heavily used.                                | Pages        |
| `huge_pages_reserved`                | Huge pages reserved for allocations.              | High → pending huge page usage.                               | Pages        |
| `huge_pages_used`                    | Huge pages currently allocated.                   | High → memory optimized workloads.                            | Pages        |
| `huge_page_size`                     | Size of each huge page.                           | Huge page configuration.                                      | Bytes        |
| `numa_nodes`                         | Number of NUMA nodes.                             | Hardware topology.                                            | Count        |
| `numa_remote_accesses`               | Memory accessed from remote NUMA nodes.           | High → NUMA inefficiency.                                     | Count        |
| `numa_imbalance`                     | Degree of uneven NUMA memory usage.               | High → poor NUMA locality.                                    | Ratio        |
| `rss`                                | Physical memory currently used by the process.    | High → large resident working set.                            | Bytes        |
| `vms`                                | Total virtual memory reserved by the process.     | High → large address space.                                   | Bytes        |
| `uss`                                | Memory used only by this process.                 | High → exclusive process memory.                              | Bytes        |
| `pss`                                | Shared memory fairly distributed among processes. | Better estimate of true process usage.                        | Bytes        |
| `shared_memory`                      | Memory shared with other processes.               | High → shared libraries or IPC.                               | Bytes        |
| `private_memory`                     | Memory used exclusively by the process.           | High → application-owned memory.                              | Bytes        |
| `anonymous_memory`                   | Memory not backed by files.                       | High → heap or stack allocations.                             | Bytes        |
| `file_backed_memory`                 | Memory backed by files.                           | High → mapped files or cache.                                 | Bytes        |
| `process_memory_percent`             | Process share of system memory.                   | High → memory-hungry process.                                 | %            |
| `peak_memory`                        | Highest memory usage reached.                     | Useful for capacity planning.                                 | Bytes        |
| `cgroup_memory_usage`                | Memory used by the current cgroup.                | High → container approaching limits.                          | Bytes        |
| `container_memory_usage`             | Container memory consumption.                     | High → container memory pressure.                             | Bytes        |
| `container_memory_limit`             | Maximum memory available to the container.        | Container capacity.                                           | Bytes        |
| `container_working_set`              | Actively used container memory.                   | High → real workload demand.                                  | Bytes        |
| `container_cache`                    | Cache memory inside the container.                | High is generally reclaimable.                                | Bytes        |
| `container_page_cache`               | Filesystem page cache used by the container.      | High is usually healthy.                                      | Bytes        |
| `container_rss`                      | Physical memory used by the container.            | High → active container memory.                               | Bytes        |
| `container_oom_events`               | OOM events inside the container.                  | High → container exceeded memory limit.                       | Count        |
| `page_cache`                         | Filesystem page cache.                            | High is usually beneficial.                                   | Bytes        |
| `dirty_pages`                        | Pages waiting to be written to disk.              | High → pending disk writes.                                   | Bytes        |
| `writeback_pages`                    | Pages currently being written to disk.            | High → active writeback.                                      | Bytes        |
| `dirty_cache`                        | Dirty filesystem cache.                           | High → write workload.                                        | Bytes        |
| `writeback_cache`                    | Cache currently flushing to storage.              | High → sustained disk writes.                                 | Bytes        |
| `dentry_cache`                       | Cached filesystem directory entries.              | High → filesystem metadata cache.                             | Bytes        |
| `inode_cache`                        | Cached filesystem inodes.                         | High → filesystem metadata cache.                             | Bytes        |
| `page_faults_per_sec`                | Total page faults each second.                    | High → frequent memory access.                                | Faults/sec   |
| `major_page_faults_per_sec`          | Disk-backed page faults each second.              | High → memory pressure or swapping.                           | Faults/sec   |
| `minor_page_faults_per_sec`          | RAM-served page faults each second.               | High → active memory mapping.                                 | Faults/sec   |
| `pages_scanned_per_sec`              | Pages scanned each second for reclaim.            | High → active memory reclaim.                                 | Pages/sec    |
| `pages_reclaimed_per_sec`            | Pages reclaimed each second.                      | High → kernel freeing memory.                                 | Pages/sec    |
| `allocation_failures_per_sec`        | Failed memory allocations each second.            | High → severe memory exhaustion.                              | Failures/sec |
| `swap_in_mb_per_sec`                 | Swap data read into memory each second.           | High → active swapping.                                       | MB/sec       |
| `swap_out_mb_per_sec`                | Swap data written to disk each second.            | High → memory shortage.                                       | MB/sec       |
| `pages_swapped_in_mb_per_sec`        | Swapped pages restored each second.               | High → swap thrashing.                                        | MB/sec       |
| `pages_swapped_out_mb_per_sec`       | Pages moved to swap each second.                  | High → aggressive swapping.                                   | MB/sec       |
| `available_memory_change_mb_per_sec` | Change in available memory each second.           | Large decrease → memory rapidly disappearing.                 | MB/sec       |
| `used_memory_change_mb_per_sec`      | Change in used memory each second.                | Large increase → memory leak or workload growth.              | MB/sec       |
| `dirty_growth_mb_per_sec`            | Growth of dirty pages each second.                | High → writes accumulating faster than flushing.              | MB/sec       |
| `writeback_growth_mb_per_sec`        | Growth of writeback pages each second.            | High → storage actively flushing data.                        | MB/sec       |
| `cache_growth_mb_per_sec`            | Cache growth each second.                         | High → filesystem cache expanding.                            | MB/sec       |
| `buffer_growth_mb_per_sec`           | Buffer growth each second.                        | High → increased filesystem buffering.                        | MB/sec       |
| `process_memory_growth_mb_per_sec`   | Process memory growth each second.                | High → possible memory leak.                                  | MB/sec       |
| `container_memory_growth_mb_per_sec` | Container memory growth each second.              | High → container memory leak or workload expansion.           | MB/sec       |
| `oom_events_per_sec`                 | OOM events occurring each second.                 | High → repeated memory exhaustion.                            | Events/sec   |
| `container_oom_events_per_sec`       | Container OOM events each second.                 | High → container repeatedly exceeding memory limit.           | Events/sec   |
