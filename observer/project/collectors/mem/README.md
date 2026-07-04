# Collector	Source	Purpose
```
psutil.py	psutil	Cross-platform memory and swap metrics
meminfo.py	/proc/meminfo	Kernel memory, cache, commit, huge pages
vmstat.py	/proc/vmstat	Page faults, reclaim activity, swap, OOM
pressure.py	/proc/pressure/memory	Memory pressure (PSI)
cgroup.py	/sys/fs/cgroup	Container memory usage, limits, working set
numa.py	/sys/devices/system/node	NUMA topology and remote memory accesses
process.py	psutil.Process()	Observer process RSS, USS, PSS, VMS
```
