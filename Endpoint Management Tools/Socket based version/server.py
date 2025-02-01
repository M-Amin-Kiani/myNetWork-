import socket
import threading

# تنظیمات سرور
HOST = "0.0.0.0"  # گوش دادن به تمام اینترفیس‌های شبکه
PORT = 65437  # پورت TCP برای مدیریت کلاینت‌ها
BROADCAST_PORT = 54545  # پورت برای دریافت Broadcast
clients = {}  # ذخیره کلاینت‌های کشف‌شده به صورت {ip: port}

def udp_discovery_listener():
    """
    گوش دادن به پیام‌های UDP broadcast از کلاینت‌ها و ذخیره آدرس‌های آنها
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(("", BROADCAST_PORT))  # گوش دادن به تمام شبکه
        print(f"Listening for client discovery messages on port {BROADCAST_PORT}...")
        
        while True:
            message, addr = udp_socket.recvfrom(1024)
            decoded_msg = message.decode()

            if decoded_msg.startswith("DISCOVER_CLIENT"):
                _, client_ip, client_port = decoded_msg.split(":")
                client_port = int(client_port)  # تبدیل پورت به عدد
                
                if client_ip not in clients:  # بررسی اینکه کلاینت جدید است یا نه
                    clients[client_ip] = client_port
                    print(f"Discovered new client: {client_ip}:{client_port}")

def udp_server_listener():
    """
    گوش دادن به پیام‌های اضطراری کلاینت‌ها از طریق UDP
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((HOST, PORT))
        print(f"Listening for UDP alerts on {HOST}:{PORT}...")
        while True:
            message, addr = udp_socket.recvfrom(1024)
            print(f"\nReceived alert from {addr[0]}:{addr[1]} - {message.decode()}")

def manage_clients():
    """
    نمایش لیست کلاینت‌ها و ارسال دستورات به آن‌ها
    """
    while True:
        if not clients:
            print("No clients discovered yet. Waiting...")
            continue

        print("\nConnected Clients:")
        for i, (ip, port) in enumerate(clients.items()):
            print(f"{i}: {ip}:{port}")

        client_choice = input("Enter client index to manage (or 'exit' to quit): ").strip()
        if client_choice.lower() == "exit":
            break

        try:
            client_choice = int(client_choice)
            ip, port = list(clients.items())[client_choice]
        except (ValueError, IndexError):
            print("Invalid selection. Try again.")
            continue

        main(ip, port)

def main(ip, port):
    """
    ارسال دستورات به کلاینت از طریق TCP
    """
    print("\nClient Management Menu")
    print("1. Check RAM and CPU usage (send 'ram')")
    print("2. Get running processes count (send 'processes_count')")
    print("3. Restart the system (send 'restart')")
    print("4. Get CPU usage alert (send 'cpu_alert')")
    print("5. Exit")

    while True:
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            command = "ram"
        elif choice == "2":
            command = "processes_count"
        elif choice == "3":
            command = "restart"
        elif choice == "4":
            command = "cpu_alert"
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
            continue

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(command.encode())
            data = s.recv(1024)

        print(f"Response from {ip}: {data.decode()}")

# اجرای لیسنر UDP برای کشف کلاینت‌ها
threading.Thread(target=udp_discovery_listener, daemon=True).start()
# اجرای لیسنر UDP برای هشدارهای اضطراری
threading.Thread(target=udp_server_listener, daemon=True).start()
# مدیریت کلاینت‌ها
manage_clients()
