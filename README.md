[![pipeline status](https://gitlab.com/doanhiep169/loadtest-api/badges/main/pipeline.svg)](https://gitlab.com/doanhiep169/loadtest-api/-/commits/main)

## Demo Video
- HPA Auto-scaling: https://youtu.be/vFYXPUYhfiA
- Self-healing (cordon/drain): https://youtu.be/7viwdsLyjOA

### 1. Cluster 2 node Ready
![Nodes Ready](nodes-ready.png.png)

### 2. HTTPS Certificate hợp lệ
![Certificate Ready](certificate-ready.png)

### 3. HPA tự động scale Pod theo tải CPU
![HPA Scaling](hpa-scaling.png)

### 4. GitLab CI/CD Pipeline chạy thành công
![Pipeline Passed](pipeline-passed.png)

### 5. Giám sát bằng Grafana + Prometheus
![Grafana Dashboard](grafana-dashboard.png)

### 6. Giao diện Web Demo trực tiếp
![Web Demo](web-demo.png)

## 7. Self-healing khi node gặp sự cố

Cô lập node worker (đánh dấu không nhận pod mới):

![node cordon](node-cordon.png)

Trục xuất toàn bộ pod ra khỏi worker:

![pod drain](pod-drain.png)

Khôi phục lại worker sau khi demo xong:

![node uncordon](node-uncordon.png)
