from flask import Flask, jsonify, request, render_template
import time
import platform
import os

# Try to import psutil for real resource monitoring
try:
    import psutil
    # Trigger an initial cpu_percent call to initialize the counter
    psutil.cpu_percent(interval=None)
except ImportError:
    psutil = None

app = Flask(__name__)
START_TIME = time.time()

def fibonacci(n):
    """Tính Fibonacci đệ quy (cố ý không tối ưu) để tạo tải CPU thật.
    n càng lớn thì CPU dùng càng nhiều -> dùng để demo HPA scale."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@app.route("/")
def home():
    # Hỗ trợ cả giao diện HTML đẹp mắt và API JSON (tương thích ngược)
    accept_header = request.headers.get("Accept", "")
    wants_json = (
        "application/json" in accept_header or 
        request.args.get("json", default="false").lower() == "true"
    )
    
    if wants_json:
        return jsonify({
            "message": "Loadtest API đang chạy",
            "endpoints": {
                "/": "Trang chủ (HTML Dashboard hoặc JSON endpoints)",
                "/healthz": "Health check (dùng cho readiness/liveness probe)",
                "/compute?n=30": "Endpoint tốn CPU - dùng để test HPA auto-scaling",
                "/api/metrics": "Lấy thông số tài nguyên CPU và RAM của hệ thống"
            }
        })
    
    return render_template("index.html")


@app.route("/healthz")
def healthz():
    # Endpoint riêng cho readiness/liveness probe - luôn trả lời nhanh,
    # không phụ thuộc vào endpoint /compute đang bận tính toán hay không.
    return jsonify({"status": "ok"}), 200


@app.route("/compute")
def compute():
    """Endpoint tốn CPU thật - dùng k6/Locust/Browser gọi endpoint này để tạo tải,
    quan sát HPA tự động scale số pod."""
    n = request.args.get("n", default=28, type=int)
    n = max(1, min(n, 35))  # giới hạn để tránh treo máy nếu n quá lớn

    start = time.time()
    result = fibonacci(n)
    duration = time.time() - start

    return jsonify({
        "input": n,
        "result": result,
        "duration_seconds": round(duration, 4)
    })


@app.route("/api/metrics")
def metrics():
    """Endpoint trả về chỉ số hệ thống phục vụ cho Dashboard vẽ biểu đồ"""
    uptime_seconds = time.time() - START_TIME
    
    if psutil is not None:
        try:
            # Lấy % CPU sử dụng tại thời điểm hiện tại (non-blocking)
            cpu_percent = psutil.cpu_percent(interval=None)
            
            # Lấy thông số RAM
            svmem = psutil.virtual_memory()
            ram_percent = svmem.percent
            ram_used_gb = svmem.used / (1024 ** 3)
            ram_total_gb = svmem.total / (1024 ** 3)
        except Exception as e:
            cpu_percent = 0.0
            ram_percent = 0.0
            ram_used_gb = 0.0
            ram_total_gb = 0.0
    else:
        # Fallback giả lập nếu chưa cài psutil
        cpu_percent = 12.5
        ram_percent = 45.2
        ram_used_gb = 7.23
        ram_total_gb = 16.0

    os_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
    if psutil is None:
        os_info += " [LƯU Ý: Chạy 'pip install psutil' để lấy thông số thật]"

    return jsonify({
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent,
        "ram_used_gb": round(ram_used_gb, 2),
        "ram_total_gb": round(ram_total_gb, 2),
        "uptime_seconds": round(uptime_seconds, 1),
        "os_info": os_info
    })


if __name__ == "__main__":
    # Chỉ dùng khi chạy nhanh cục bộ (python app.py) để dev.
    # Production luôn chạy qua gunicorn (xem CMD trong Dockerfile).
    app.run(host="0.0.0.0", port=3000)

