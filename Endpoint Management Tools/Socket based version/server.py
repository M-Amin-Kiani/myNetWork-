import socket
import threading
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')  # برای پشتیبانی از Unicode

HOST = socket.gethostbyname(socket.gethostname())
PORT = 0  # مقدار 0 یعنی سیستم خودش پورت آزاد را انتخاب کند

def udp_server_listener():
    """لیسنر UDP برای دریافت هشدارهای CPU"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((HOST, PORT))
        actual_port = udp_socket.getsockname()[1]
        print(f"[INFO] Listening for UDP alerts on {HOST}:{actual_port} ...")

        while True:
            message, addr = udp_socket.recvfrom(1024)
            print(f"\n⚠️ [UDP] Alert from {addr[0]}:{addr[1]} -> {message.decode()}")

def get_udp_alert():
    """دریافت هشدارهای UDP"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((HOST, 0))
        udp_socket.settimeout(2)  # برای جلوگیری از انتظار بی‌پایان
        try:
            message, addr = udp_socket.recvfrom(1024)
            return message.decode()
        except socket.timeout:
            return None

def main(ip, port, udp_port):
    """اتصال به سرور و ارسال دستورات"""
    print("\nClient Management Tool")
    print("=======================")
    print("1. Check RAM and CPU usage (send 'ram')")
    print("2. Get running processes count (send 'processes_count')")
    print("3. Restart the system (send 'restart')")
    print("4. Get CPU usage alert (send 'cpu_alert')")
    print("5. Exit")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            client_info = f"{HOST}:{udp_port}"
            s.sendall(client_info.encode())

            while True:
                choice = input("Enter your choice (1-5): ").strip()
                commands = {"1": "ram", "2": "processes_count", "3": "restart", "4": "cpu_alert"}

                if choice == "5":
                    print("[INFO] Closing connection...")
                    break

                command = commands.get(choice)
                if not command:
                    print("[ERROR] Invalid choice. Try again.")
                    continue

                s.sendall(command.encode())
                data = s.recv(1024).decode()

                # نمایش هشدار در صورت بالا بودن CPU
                if "⚠️ Warning" in data:
                    print(f"\n⚠️ [ALERT] {data}")
                else:
                    print(f"[TCP] Response: {data}")

                # اضافه کردن هشدارهای UDP
                time.sleep(1)  # برای اطمینان از اینکه UDP پیام‌ها را دریافت می‌کنیم
                udp_data = get_udp_alert()
                if udp_data:
                    print(f"⚠️ {udp_data}")

    except socket.error as e:
        print(f"[ERROR] TCP Error: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected Error: {e}")

if __name__ == "__main__":
    print("[INFO] Starting client...")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
        temp_socket.bind((HOST, 0))
        UDP_PORT = temp_socket.getsockname()[1]

    print(f"[INFO] Client running on: {HOST}:{UDP_PORT}")

    server_thread = threading.Thread(target=udp_server_listener, daemon=True)
    server_thread.start()

    clients = []
    while True:
        user_input = input("Enter IP and Port (format: IP:Port) or type 'done' to finish: ").strip()
        if user_input.lower() == 'done':
            break

        try:
            ip, port = user_input.split(":")
            port = int(port)
            socket.inet_aton(ip)
            clients.append((ip, port))
            print(f"[INFO] Added client: {ip}:{port}")
        except Exception:
            print("[ERROR] Invalid IP or port format. Try again.")

    while True:
        for i, (ip, port) in enumerate(clients):
            print(f"{i}: {ip}:{port}")

        client_input = input("Enter client ID or 'exit' to quit: ").strip()
        if client_input.lower() == 'exit':
            print("[INFO] Closing client...")
            sys.exit(0)

        if client_input.isdigit() and 0 <= int(client_input) < len(clients):
            main(clients[int(client_input)][0], clients[int(client_input)][1], UDP_PORT)
        else:
            print("[ERROR] Invalid input. Try again.")
