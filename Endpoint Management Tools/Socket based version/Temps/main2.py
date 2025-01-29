import socket
import threading
import psutil
import os
import time
import random

def get_system_usage():
    """Get CPU and memory usage."""
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    return {
        "cpu_percent": cpu_percent,
        "memory_total": memory.total // (1024 * 1024),
        "memory_used": memory.used // (1024 * 1024),
    }

def get_running_processes_count():
    """Get the number of currently running processes."""
    return len(psutil.pids())

def restart_system():
    """Restart the system."""
    print("Restarting the system...")
    os.system("shutdown /r /t 1" if os.name == "nt" else "sudo reboot")

def handle_client(conn):
    """Handles incoming TCP commands from the server."""
    with conn:
        while True:
            command = conn.recv(1024).decode("utf-8")
            if not command:
                break

            if command == "ram":
                usage = get_system_usage()
                response = f"Memory Usage: {usage['memory_used']}MB / {usage['memory_total']}MB"
            elif command == "restart":
                restart_system()
                response = "Restarting system..."
            elif command == "processes_count":
                response = f"Number of running processes: {get_running_processes_count()}"
            elif command == "cpu_alert":
                cpu_percent = psutil.cpu_percent(interval=1)
                response = f"CPU Usage: {cpu_percent}%" if cpu_percent < 80 else f"WARNING: High CPU usage! ({cpu_percent}%)"
            else:
                response = "Invalid command."

            conn.sendall(response.encode("utf-8"))

def client_listener():
    """Listens for connections from the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Get the hostname of the client machine
        hostname = socket.gethostname()
        # Retrieve the IP address associated with the hostname
        host_ip = socket.gethostbyname(hostname)
        
        # Bind to the host IP and a random available port
        server_socket.bind((host_ip, 0))
        # Retrieve the port number assigned by the OS
        assigned_port = server_socket.getsockname()[1]
        
        server_socket.listen()
        print(f"Client listening on {host_ip}:{assigned_port}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Connected to server: {addr}")
            threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    client_listener()
