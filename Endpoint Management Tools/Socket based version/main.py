import psutil
import os
import time
import socket
import threading

# تنظیمات کلاینت
HOST = socket.gethostbyname(socket.gethostname())  # دریافت IP محلی کلاینت
PORT = 65430  # پورت TCP کلاینت
BROADCAST_PORT = 54545  # پورت ارسال Broadcast
SERVER_IP = "127.0.0.1"  # آدرس IP سرور
SERVER_UDP_PORT = 65437  # پورت UDP سرور برای هشدارها

def alert_cpu_usage():
    """
    مانیتورینگ مصرف CPU و ارسال هشدار به سرور در صورت عبور از حد مجاز
    """
    threshold = 80
    check_interval = 5
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > threshold:
                message = f"Warning: High CPU usage {cpu_usage}%!"
                udp_socket.sendto(message.encode(), (SERVER_IP, SERVER_UDP_PORT))
                print(f"Sent warning: {message}")
            time.sleep(check_interval)

def broadcast_presence():
    """
    ارسال پیام UDP Broadcast برای اعلام حضور در شبکه
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as udp_socket:
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        message = f"DISCOVER_CLIENT:{HOST}:{PORT}"
        while True:
            udp_socket.sendto(message.encode(), ('<broadcast>', BROADCAST_PORT))
            time.sleep(5)  # ارسال هر 5 ثانیه

def get_system_usage():
    """بررسی مصرف RAM و CPU"""
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    return {
        "cpu_percent": cpu_percent,
        "memory_total": memory.total // (1024 * 1024),
        "memory_used": memory.used // (1024 * 1024),
    }

def tcp_management():
    """
    دریافت و پردازش دستورات از سرور
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                command = conn.recv(1024).decode("utf-8")

                if command == "ram":
                    usage = get_system_usage()
                    response = f"Memory Usage: {usage['memory_used']}MB / {usage['memory_total']}MB"
                    conn.sendall(response.encode())

                elif command == "restart":
                    os.system("shutdown /r /t 1" if os.name == "nt" else "sudo reboot")

                elif command == "processes_count":
                    response = f"Running processes: {len(psutil.pids())}"
                    conn.sendall(response.encode())

                elif command == "cpu_alert":
                    cpu_percent = psutil.cpu_percent(interval=1)
                    response = f"CPU Usage: {cpu_percent}%" if cpu_percent > 80 else f"WARNING: High CPU {cpu_percent}%"
                    conn.sendall(response.encode())

# اجرای قابلیت‌های مختلف در Thread های جداگانه
threading.Thread(target=alert_cpu_usage, daemon=True).start()
threading.Thread(target=broadcast_presence, daemon=True).start()
tcp_management()
