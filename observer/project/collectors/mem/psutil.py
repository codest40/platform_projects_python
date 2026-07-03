from __future__ import annotations
import psutil
from project.models.memory import MemoryData


def collect_psutil_memory(memory: MemoryData) -> None:
    """Populate MemoryData using psutil."""

    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    # ==========================================================
    # Capacity
    # ==========================================================
    memory.total = vm.total
    memory.available = vm.available
    memory.used = vm.used
    memory.free = vm.free

    memory.cached = getattr(vm, "cached", 0)
    memory.buffers = getattr(vm, "buffers", 0)
    memory.shared = getattr(vm, "shared", 0)
    memory.active = getattr(vm, "active", 0)
    memory.inactive = getattr(vm, "inactive", 0)
    memory.wired = getattr(vm, "wired", 0)
    memory.slab = getattr(vm, "slab", 0)

    # ==========================================================
    # Utilization
    # ==========================================================
    memory.percent = vm.percent

    if vm.total:
        memory.available_percent = vm.available / vm.total * 100
        memory.used_percent = vm.used / vm.total * 100
        memory.cache_percent = memory.cached / vm.total * 100
        memory.buffer_percent = memory.buffers / vm.total * 100

    # ==========================================================
    # Swap
    # ==========================================================
    memory.swap_total = swap.total
    memory.swap_used = swap.used
    memory.swap_free = swap.free
    memory.swap_percent = swap.percent

    memory.swap_in = swap.sin
    memory.swap_out = swap.sout
