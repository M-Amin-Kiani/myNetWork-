import socket
import threading

def udp_server_listener(host_ip, port):
    """
    Listens for UDP messages on the specified host IP and port, and displays them along with the sender's IP and port.

    Args:
        host_ip (str): The IP address to bind the server to.
        port (int): The port number to bind the server to.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((host_ip, port))
        print(f"Server listening on {host_ip}:{port}...")
        while True:
            message, addr = udp_socket.recvfrom(1024)  # Receive up to 1024 bytes
            print(f"\nReceived message from {addr[0]}:{addr[1]}: {message.decode()}")

def main(ip, port):
    print("Client Management Tool")
    print("=======================")
    print("Options:")
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
            print("Invalid choice. Please try again.")
            continue

        # Connect to the server and send the selected command
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            message = command.encode('utf-8')
            s.sendall(message)
            data = s.recv(1024)  # Receive the server's response

        print(f"Received {data!r}")

def client_management():
    clients = []
    while True:
        user_input = input("Enter IP and Port (format: IP:Port) or type 'done' to finish: ").strip()
        if user_input.lower() == 'done':
            break

        try:
            # Parse the input
            ip, port = user_input.split(":")
            port = int(port)  # Ensure the port is an integer

            # Validate IP address format
            socket.inet_aton(ip)  # Will raise an exception if IP is invalid

            # Store the connection details
            clients.append((ip, port))
            print(f"Added client {ip}:{port}")
        except (ValueError, socket.error):
            print("Invalid input. Please enter in the format IP:Port.")

    return clients

if __name__ == "__main__":
    # Retrieve the local hostname
    hostname = socket.gethostname()
    # Retrieve the IP address associated with the hostname
    host_ip = socket.gethostbyname(hostname)

    # Create a UDP socket and bind to the host IP and a random available port
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
        temp_socket.bind((host_ip, 0))
        # Retrieve the port number assigned by the OS
        assigned_port = temp_socket.getsockname()[1]

    # Start the UDP server listener in a separate thread
    server_thread = threading.Thread(
        target=udp_server_listener,
        args=(host_ip, assigned_port),
        daemon=True
    )
    server_thread.start()

    while True:
        # Enter client management phase
        clients = client_management()

        if not clients:
            print("No clients added.")
            continue

        while True:
            print("\nConnected Clients:")
            for idx, (ip, port) in enumerate(clients):
                print(f"{idx}: {ip}:{port}")

            print("\nOptions:")
            print("1. Select a client to manage")
            print("2. Return to client entry phase")
            print("3. Exit")

            choice = input("Enter your choice (1-3): ").strip()

            if choice == "1":
                try:
                    client_idx = int(input("Enter the client number to manage: ").strip())
                    if 0 <= client_idx < len(clients):
                        ip, port = clients[client_idx]
                        main(ip, port)
                    else:
                        print("Invalid client number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == "2":
                break  # Exit to client entry phase
            elif choice == "3":
                print("Exiting...")
                exit(0)
            else:
                print("Invalid choice. Please try again.")
