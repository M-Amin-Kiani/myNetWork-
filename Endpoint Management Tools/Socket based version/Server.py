import socket
import threading
import sys

# دریافت IP داینامیک کلاینت
HOST = socket.gethostbyname(socket.gethostname())
PORT = 7776  # پورت UDP برای دریافت هشدارها


def udp_server_listener(host, port):
    """لیسنر UDP برای دریافت هشدارهای CPU"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((host, port))
        while True:
            message, addr = udp_socket.recvfrom(1024)
            print(f"\n[UDP] Alert from {addr[0]}:{addr[1]} -> {message.decode()}")


def main(ip, port):
    """مدیریت اتصال به سرور و ارسال دستورات"""
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
            client_info = f"{HOST}:{PORT}"  
            s.sendall(client_info.encode())

            while True:
                choice = input("Enter your choice (1-5): ").strip()
                commands = {"1": "ram", "2": "processes_count", "3": "restart", "4": "cpu_alert"}

                if choice == "5":
                    print("Closing connection...")
                    break

                command = commands.get(choice)
                if not command:
                    print("Invalid choice. Try again.")
                    continue

                s.sendall(command.encode())
                data = s.recv(1024)
                print(f"Received: {data.decode()}")

    except socket.error as e:
        print(f"TCP Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    print(f"Client running on: {HOST}:{PORT}")

    # اجرای UDP لیسنر در ترد جداگانه
    server_thread = threading.Thread(target=udp_server_listener, args=(HOST, PORT), daemon=True)
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
            print(f"Added client: {ip}:{port}")
        except Exception:
            print("Invalid IP or port format. Try again.")

    while True:
        print("\nConnected Clients:")
        for i, (ip, port) in enumerate(clients):
            print(f"{i}: {ip}:{port}")

        client_input = input("Enter client ID to execute command or 'exit' to quit: ").strip()
        if client_input.lower() == 'exit':
            print("Closing client...")
            sys.exit(0)

        if client_input.isdigit() and 0 <= int(client_input) < len(clients):
            main(clients[int(client_input)][0], clients[int(client_input)][1])
        else:
            print("Invalid input. Try again.")
