import psutil
import os
import time
import socket
import threading

# دریافت IP داینامیک سرور
HOST = socket.gethostbyname(socket.gethostname())
PORT = 7777  # پورت سرور

def alert_cpu_usage(client_ip, client_port):
    """مانیتور کردن استفاده از CPU و ارسال هشدار از طریق UDP"""
    threshold = 80  
    check_interval = 10  
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > threshold:
                message = f"Warning: CPU usage is {cpu_usage}%!"
                udp_socket.sendto(message.encode(), (client_ip, client_port))
                print(f"Sent warning: {message}")
            time.sleep(check_interval)

def get_system_usage():
    """دریافت وضعیت حافظه و پردازنده"""
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    return f"CPU: {cpu_percent}% | RAM: {memory.used // (1024*1024)}MB / {memory.total // (1024*1024)}MB"

def get_running_processes_count():
    """دریافت تعداد پردازش‌های در حال اجرا"""
    return f"Running Processes: {len(psutil.pids())}"

def restart_system():
    """ری‌استارت کردن سیستم"""
    os.system("shutdown /r /t 1" if os.name == "nt" else "sudo reboot")
    return "Restarting system..."

def handle_client(conn, addr):
    """مدیریت هر اتصال به سرور در یک ترد جداگانه"""
    try:
        data = conn.recv(1024).decode().strip()
        print(f"Received client info: {data}")

        if ':' in data:
            client_ip, client_port = data.split(':')
            client_port = int(client_port)
        else:
            print("Invalid client info format!")
            conn.close()
            return

        # شروع ترد هشدار CPU
        monitoring_thread = threading.Thread(target=alert_cpu_usage, args=(client_ip, client_port), daemon=True)
        monitoring_thread.start()

        while True:
            command = conn.recv(1024).decode().strip()
            if not command:
                break

            if command == "ram":
                response = get_system_usage()
            elif command == "processes_count":
                response = get_running_processes_count()
            elif command == "restart":
                response = restart_system()
            elif command == "cpu_alert":
                cpu_percent = psutil.cpu_percent(interval=1)
                response = f"CPU Usage: {cpu_percent}%"
            else:
                response = "Invalid command"

            print(f"Sending response to {addr}: {response}")
            conn.sendall(response.encode())
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()

def tcp_management():
    """مدیریت اتصالات TCP سرور"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT} ...")
        
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()

if __name__ == "__main__":
    print(f"Server running on {HOST}:{PORT}")
    tcp_management()
