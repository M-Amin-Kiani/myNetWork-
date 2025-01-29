# This is a sample Python script.
import requests

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


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
        response = requests.get(base_url)
        print("Response:", response.json())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    clients = []
    while True:
        user_input = input("Enter IP and Port (format: IP:Port): done for finish").strip()
        if user_input.lower() == 'done':
            break

        # Parse the input
        ip, port = user_input.split(":")
        port = int(port)  # Ensure the port is an integer

        # Store the connection details
        clients.append((ip, port))
    i = 0
    while True:
        print("Agents...")
        for ipx, portx in clients:
            print(f'{i} : {ipx} and {portx} \n')
            i = i + 1

        agent = int(input("please enter your agent"))
        main(clients[agent][0], clients[agent][1])