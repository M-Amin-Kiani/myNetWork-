import requests

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
            command = "noprocess"
        elif choice == "3":
            command = "restart"
        elif choice == "4":
            command = "cpu"
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        base_url = f"http://{ip}:{port}/api/{command}"
        try:
            response = requests.get(base_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print("Response:", response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the client: {e}")

def enter_clients():
    clients = []
    while True:
        user_input = input("Enter IP and Port (format: IP:Port) or type 'done' to finish: ").strip()
        if user_input.lower() == 'done':
            if not clients:
                print("No clients entered. Please add at least one client.")
                continue
            break

        try:
            ip, port = user_input.split(":")
            port = int(port)  # Ensure the port is an integer
            clients.append((ip, port))
        except ValueError:
            print("Invalid format. Please enter in 'IP:Port' format.")
            continue

    return clients

def choose_client(clients):
    while True:
        print("Agents:")
        for index, (ip, port) in enumerate(clients):
            print(f'{index}: {ip}:{port}')

        user_input = input("Enter the agent number to connect or type 'back' to return to client entry: ").strip()
        if user_input.lower() == 'back':
            return False

        try:
            agent_index = int(user_input)
            if 0 <= agent_index < len(clients):
                ip, port = clients[agent_index]
                main(ip, port)
            else:
                print("Invalid agent number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid agent number or 'back' to return.")

def run():
    while True:
        clients = enter_clients()
        if not choose_client(clients):
            continue
        else:
            break

if __name__ == '__main__':
    run()
