# Disk Uasge helper

| Metric                       | Description                                                          |
| ---------------------------- | -------------------------------------------------------------------- |
| `device`                     | Primary storage device being monitored.                              |
| `primary_partition`          | Main disk partition (e.g. `/dev/sda1`).                              |
| `mount_point`                | Filesystem mount location (e.g. `/`).                                |
| `total`                      | Total filesystem capacity.                                           |
| `used`                       | Disk space currently in use.                                         |
| `free`                       | Disk space currently available.                                      |
| `percent`                    | Percentage of filesystem currently used.                             |
| `read_only`                  | Whether the filesystem is mounted read-only.                         |
| `mounted_fs_total`           | Total capacity across all mounted filesystems.                       |
| `mount_count`                | Number of mounted filesystems.                                       |
| `mounts`                     | Details of mounted devices and mount options.                        |
| `filesystems`                | Information for each mounted filesystem.                             |
| `read_count`                 | Total number of disk read operations performed.                      |
| `write_count`                | Total number of disk write operations performed.                     |
| `read_bytes`                 | Total bytes read from disk.                                          |
| `write_bytes`                | Total bytes written to disk.                                         |
| `read_time_ms`               | Total time spent servicing read requests.                            |
| `write_time_ms`              | Total time spent servicing write requests.                           |
| `io_in_progress`             | Number of IO requests currently being processed.                     |
| `busy_time_ms`               | Time the disk has been busy processing IO.                           |
| `weighted_io_time_ms`        | Weighted IO time used to estimate queue depth.                       |
| `discard_count`              | Number of discard (TRIM) operations performed.                       |
| `discard_bytes`              | Total bytes discarded (TRIM).                                        |
| `discard_time_ms`            | Time spent processing discard requests.                              |
| `flush_count`                | Number of filesystem flush operations.                               |
| `flush_time_ms`              | Time spent flushing cached writes to storage.                        |
| `queue_depth`                | Current number of pending IO requests.                               |
| `average_wait_ms`            | Average time requests waited before service.                         |
| `average_service_time_ms`    | Average time required to complete an IO request.                     |
| `utilization_percent`        | Percentage of time the disk is actively servicing requests.          |
| `dirty_pages`                | Memory pages waiting to be written to disk.                          |
| `writeback_pages`            | Pages currently being written back to storage.                       |
| `psi_some_avg10`             | Percentage of time some tasks waited on storage (10 sec).            |
| `psi_some_avg60`             | Percentage of time some tasks waited on storage (60 sec).            |
| `psi_some_avg300`            | Percentage of time some tasks waited on storage (300 sec).           |
| `psi_full_avg10`             | Percentage of time all tasks were blocked by storage (10 sec).       |
| `psi_full_avg60`             | Percentage of time all tasks were blocked by storage (60 sec).       |
| `psi_full_avg300`            | Percentage of time all tasks were blocked by storage (300 sec).      |
| `process_read_count`         | Number of read operations performed by the monitored process.        |
| `process_write_count`        | Number of write operations performed by the monitored process.       |
| `process_read_bytes`         | Bytes read by the monitored process.                                 |
| `process_write_bytes`        | Bytes written by the monitored process.                              |
| `read_chars`                 | Bytes requested by application read calls (may include cache hits).  |
| `write_chars`                | Bytes requested by application write calls.                          |
| `read_syscalls`              | Number of read system calls executed.                                |
| `write_syscalls`             | Number of write system calls executed.                               |
| `container_read_bytes`       | Total bytes read by container workloads.                             |
| `container_write_bytes`      | Total bytes written by container workloads.                          |
| `container_read_ios`         | Number of read IO operations from containers.                        |
| `container_write_ios`        | Number of write IO operations from containers.                       |
| `container_io_pressure`      | Overall storage pressure experienced by containers.                  |
| `read_mb_per_sec`            | Disk read throughput in MB per second.                               |
| `write_mb_per_sec`           | Disk write throughput in MB per second.                              |
| `total_mb_per_sec`           | Combined disk throughput (read + write).                             |
| `read_iops`                  | Read IO operations performed each second.                            |
| `write_iops`                 | Write IO operations performed each second.                           |
| `total_iops`                 | Total IO operations per second.                                      |
| `average_read_latency_ms`    | Average time required to complete a read request.                    |
| `average_write_latency_ms`   | Average time required to complete a write request.                   |
| `device_utilization_percent` | Percentage of time the device was busy during the sampling interval. |
| `average_queue_depth`        | Average number of requests waiting for the disk.                     |
| `flushes_per_sec`            | Filesystem flush operations performed each second.                   |
| `discard_mb_per_sec`         | Amount of discarded (TRIM) data each second.                         |
| `process_read_mb_per_sec`    | Process read throughput in MB/s.                                     |
| `process_write_mb_per_sec`   | Process write throughput in MB/s.                                    |
| `container_read_mb_per_sec`  | Container read throughput in MB/s.                                   |
| `container_write_mb_per_sec` | Container write throughput in MB/s.                                  |
