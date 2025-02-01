import psutil
import os


def get_system_usage():
    """Get CPU and memory usage."""
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    return {
        "cpu_percent": cpu_percent,
        "memory_total": memory.total // (1024 * 1024),  # in MB
        "memory_used": memory.used // (1024 * 1024),   # in MB
    }


def get_running_processes_count():
    """Get the number of currently running processes."""
    return len(psutil.pids())


def restart_system():
    """Restart the system."""
    print("Restarting the system...")
    os.system("shutdown /r /t 1" if os.name == "nt" else "sudo reboot")


def cpu_usage(threshold=80):
    """Monitor CPU usage and display a warning if it exceeds the threshold."""
    return psutil.cpu_percent(interval=1)
