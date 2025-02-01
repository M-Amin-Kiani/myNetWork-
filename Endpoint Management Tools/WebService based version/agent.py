from flask import Flask, jsonify, request
import psutil
import os
import socket
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# GET /api/ram HTTP/1.1
# Host: 192.168.1.106:5000
# Authorization: Bearer your_secure_api_key  ==> ارسال نشود یا اشتباه باشد، سرور کد نامعتبر میفرستد 401  

app = Flask(__name__)
# امنیت بالا از طریق احراز هویت و محدودسازی درخواست‌ها (Rate Limiting)
# 🔑 API Key که کلاینت‌ها باید برای احراز هویت از آن استفاده کنند
# برنامه به‌صورت امن اجرا شده و فقط از طریق کلید ای پی ای به سرور متصل می‌شود.
API_KEY = "AminKiani"

# 🛡️ اعمال Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"],  # افزایش محدودیت به 20 درخواست در دقیقه
    storage_uri="memory://",
)

# 📌 احراز هویت
def authenticate_request():
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        return False
    return True

# 📌 مسیر برای بررسی وجود سرور در شبکه (برای کشف سرورها)
@app.route('/api/clients', methods=['GET'])
def get_clients():
    return jsonify({"message": "Server is up and running"}), 200

# 📌 بررسی میزان رم
@app.route('/api/ram', methods=['GET'])
@limiter.limit("10 per minute")
def ram_usage():
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401
    usage = get_system_usage()
    return jsonify({"ram_usage": f"{usage['memory_used']}MB / {usage['memory_total']}MB"})

# 📌 بررسی میزان استفاده CPU
@app.route('/api/cpu', methods=['GET'])
@limiter.limit("10 per minute")
def cpu_usage_route():
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401
    cpu_percent = cpu_usage()
    return jsonify({"cpu": cpu_percent})

# 📌 دریافت تعداد پردازش‌های فعال
@app.route('/api/no_process', methods=['GET'])
def no_process():
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401
    no_p = len(psutil.pids())
    return jsonify({"no_process": no_p})

# 📌 دریافت اطلاعات سیستم
def get_system_usage():
    memory = psutil.virtual_memory()
    return {
        "memory_total": memory.total // (1024 * 1024),
        "memory_used": memory.used // (1024 * 1024),
    }

# 📌 دریافت میزان استفاده از CPU
def cpu_usage():
    return psutil.cpu_percent(interval=1)

# 📌 دریافت IP محلی دستگاه
def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    host_ip = get_host_ip()
    port = 5000
    print(f"Starting Flask app on {host_ip}:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)  # تغییر host به 0.0.0.0
