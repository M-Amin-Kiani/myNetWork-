import socket
import threading
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65437  # The port used by the server

def udp_server_listener(HOST, PORT):
    """
    Listens for UDP messages on the specified host and port, and displays them along with the sender's IP and port.

    Args:
        host (str): The IP address to bind the server to.
        port (int): The port number to bind the server to.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((HOST, PORT))
        #print(f"Server listening on {HOST}:{PORT+1}...")
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
        # print(f"Received from server: {data.decode('utf-8')}")


if __name__ == "__main__":
    server_thread = threading.Thread(
        target=udp_server_listener,
        args=(HOST, PORT),
        daemon=True
    )
    server_thread.start()
    clients = []
    while True:
        user_input = input("Enter IP and Port (format: IP:Port): done for finish").strip()
        if user_input.lower() == 'done':
            break

        # Parse the input
        ip, port = user_input.split(":")
        port = int(port)  # Ensure the port is an integer

        # Validate IP address format
        socket.inet_aton(ip)  # Will raise an exception if IP is invalid

        # Store the connection details
        clients.append((ip, port))
        print(f'{clients[0][0]} {clients[0][1]}')
    while True:
        print("clients ...")
        i = 0
        for ipx,portx in clients:
            print(f'{i} : {portx} and {ipx} \n')
            port_udp = PORT
            udp_add = f"{HOST}:{port_udp}"
            # Connect to the server and send the selected command
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ipx, portx))
                message = udp_add.encode()
                s.sendall(message)
                data = s.recv(1024)  # Receive the server's response

            i = i + 1
        client_input = int(input("Enter your ip and client for execute command"))
        main(clients[client_input][0], clients[client_input][1])
