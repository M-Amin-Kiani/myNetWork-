from flask import Flask, jsonify
import psutil
import os
import socket

app = Flask(__name__)

# Manager code starts here
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

def cpu_usage(threshold=2):
    """Monitor CPU usage and display a warning if it exceeds the threshold."""
    return psutil.cpu_percent(interval=1)
# Manager code ends here

@app.route('/api/ram', methods=['GET'])
def ram_usage():
    usage = get_system_usage()
    tm = f"Memory Usage: {usage['memory_used']}MB / {usage['memory_total']}MB"
    print(tm)
    return jsonify({"ram_usage": tm})

@app.route('/api/cpu', methods=['GET'])
def cpu_usage_route():
    cpu_percent = cpu_usage()
    return jsonify({"cpu": cpu_percent})

@app.route('/api/noprocess', methods=['GET'])
def no_process():
    no_p = get_running_processes_count()
    return jsonify({"no_process": no_p})

@app.route('/api/restart', methods=['GET'])
def restart():
    restart_system()
    return jsonify({"message": "success"})

def get_host_ip():
    """Get the local machine's IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external IP address to determine the local IP
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_free_port():
    """Find an available port by binding to port 0."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

if __name__ == '__main__':
    host_ip = get_host_ip()
    port = get_free_port()
    print(f"Starting Flask app on {host_ip}:{port}")
    app.run(host=host_ip, port=port, debug=True)
