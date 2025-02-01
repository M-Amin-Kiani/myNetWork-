import requests
import socket
import threading

# 🔑 API Key برای احراز هویت
API_KEY = "AminKiani"

# 📌 دریافت IP محلی کلاینت
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# 📌 پیدا کردن سرورها در شبکه با `Threading` برای افزایش سرعت
def discover_servers():
    print("Discovering servers in the network...")

    discovered_servers = []
    subnet = ".".join(get_local_ip().split(".")[:3])  # بدست آوردن رنج شبکه
    threads = []
    lock = threading.Lock()

    def check_server(ip):
        url = f"http://{ip}:5000/api/clients"
        try:
            headers = {"Authorization": f"Bearer {API_KEY}"}
            response = requests.get(url, headers=headers, timeout=0.5)  # افزایش تایم‌اوت برای دقت بیشتر
            if response.status_code == 200:
                with lock:
                    print(f"Found Server: {ip}")
                    discovered_servers.append(ip)
        except requests.exceptions.RequestException:
            pass  # اگر اتصال برقرار نشد، صرف‌نظر کند

    # ایجاد و اجرای `Thread` برای هر IP
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        thread = threading.Thread(target=check_server, args=(ip,))
        thread.start()
        threads.append(thread)

    # صبر برای تمام شدن تمام `Thread` ها
    for thread in threads:
        thread.join()

    return discovered_servers

# 📌 نمایش لیست سرورهای یافت‌شده و انتخاب یک سرور
def choose_server(servers):
    if not servers:
        print("❌ No servers found in the network.")
        return None

    print("\nAvailable Servers:")
    for idx, server in enumerate(servers):
        print(f"{idx}: {server}")

    while True:
        choice = input("\nEnter the server number to connect: ").strip()
        if choice.isdigit() and 0 <= int(choice) < len(servers):
            return servers[int(choice)]
        print("Invalid choice, please try again.")

# 📌 ارسال درخواست به سرور
def send_data_to_server(server_ip, endpoint):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"http://{server_ip}:5000/api/{endpoint}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"📡 Response ({endpoint}):", response.json())
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error communicating with the server: {e}")

# 📌 منوی اصلی برای انتخاب استعلام دستی
def main(server_ip):
    print("\n🎛️ Client Management Tool")
    print("=======================")
    print("1️⃣  Check RAM and CPU usage (send 'ram')")
    print("2️⃣  Get running processes count (send 'no_process')")
    print("3️⃣  Restart the system (send 'restart')")
    print("4️⃣  Get CPU usage alert (send 'cpu')")
    print("5️⃣  Exit")

    while True:
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            send_data_to_server(server_ip, "ram")
        elif choice == "2":
            send_data_to_server(server_ip, "no_process")
        elif choice == "3":
            send_data_to_server(server_ip, "restart")
        elif choice == "4":
            send_data_to_server(server_ip, "cpu")
        elif choice == "5":
            print("🚪 Exiting...")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# 📌 اجرای کل برنامه
if __name__ == "__main__":
    servers = discover_servers()  # کشف سرورهای موجود در شبکه
    selected_server = choose_server(servers)  # انتخاب یک سرور از لیست
    if selected_server:
        main(selected_server)  # نمایش منو و ارسال درخواست‌های دستی
