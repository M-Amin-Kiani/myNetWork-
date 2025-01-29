import psutil
import os
import time
import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 7777  # Port to listen on (non-privileged ports are > 1023)
def alert_cpu_usage(server_ip, server_port):
    """
    Monitors CPU usage and sends a warning message to a server via UDP if usage exceeds the threshold.

    Args:
        server_ip (str): The server's IP address.
        server_port (int): The server's UDP port.
        threshold (int): CPU usage percentage threshold to trigger a warning.
        check_interval (int): Interval (in seconds) to check CPU usage.
    """
    threshold = 2
    check_interval = 1000
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        while True:
            # Get the CPU usage percentage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            if cpu_usage > threshold:
                message = f"Warning: CPU usage is {cpu_usage}%!"
                udp_socket.sendto(message.encode(), (server_ip, server_port))
                print(f"Sent warning: {message}")
            time.sleep(check_interval)

def get_system_usage():
    """Get CPU and memory usage."""
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    return {
        "cpu_percent": cpu_percent,
        "memory_total": memory.total // (1024 * 1024),  # in MB
        "memory_used": memory.used // (1024 * 1024),  # in MB
    }


def get_running_processes_count():
    """Get the number of currently running processes."""
    return len(psutil.pids())


def restart_system():
    """Restart the system."""
    print("Restarting the system...")
    os.system("shutdown /r /t 1" if os.name == "nt" else "sudo reboot")


def monitor_cpu_usage(threshold):
    """Monitor CPU usage and display a warning if it exceeds the threshold."""
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > threshold:
            print(f"WARNING: High CPU usage detected! CPU usage is {cpu_percent}%")
        time.sleep(1)


def tcp_management():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(data)
                    command = data.decode("utf-8")

                    if command == "ram":
                        usage = get_system_usage()
                        tm = (f"Memory Usage: {usage['memory_used']}MB / {usage['memory_total']}MB")
                        print(tm)
                        conn.sendall(bytes(tm, "utf-8"))

                    elif command == "restart":
                        restart_system()

                    elif command == "processes_count":
                        processes_count = get_running_processes_count()
                        tm = (f"Number of running processes: {processes_count}")
                        print(tm)
                        conn.sendall(bytes(tm, "utf-8"))

                    elif command == "cpu_alert":
                        threshold = 80
                        cpu_percent = psutil.cpu_percent(interval=1)
                        if cpu_percent > threshold:
                            warning_message = f"WARNING: High CPU usage detected! CPU usage is {cpu_percent}%"
                            print(warning_message)
                            conn.sendall(bytes(warning_message, "utf-8"))
                        else:
                            normal_message = f"CPU usage is normal: {cpu_percent}%"
                            print(normal_message)
                            conn.sendall(bytes(normal_message, "utf-8"))


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            data = data.decode('utf-8')
            host,port = data.split(':')
            port = int(port)


    monitoring_thread = threading.Thread(
        target=alert_cpu_usage,
        args=(host, port),
        daemon=True
    )
    monitoring_thread.start()
    tcp_management()
