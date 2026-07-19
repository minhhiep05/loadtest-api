[![pipeline status](https://gitlab.com/doanhiep169/loadtest-api/badges/main/pipeline.svg)](https://gitlab.com/doanhiep169/loadtest-api/-/commits/main)

<details>
<summary><strong>📑 Mục lục (bấm để xem)</strong></summary>

- [Giới thiệu](#giới-thiệu)
- [Kiến trúc tổng quan](#kiến-trúc-tổng-quan)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Demo Video](#demo-video)
- [1. Cluster 2 node Ready](#1-cluster-2-node-ready)
- [2. HTTPS Certificate hợp lệ](#2-https-certificate-hợp-lệ)
- [3. HPA tự động scale Pod theo tải CPU](#3-hpa-tự-động-scale-pod-theo-tải-cpu)
- [4. GitLab CI/CD Pipeline chạy thành công](#4-gitlab-cicd-pipeline-chạy-thành-công)
- [5. Giám sát bằng Grafana + Prometheus](#5-giám-sát-bằng-grafana--prometheus)
- [6. Giao diện Web Demo trực tiếp](#6-giao-diện-web-demo-trực-tiếp)
- [7. Self-healing khi node gặp sự cố](#7-self-healing-khi-node-gặp-sự-cố)
- [Tác giả](#tác-giả)

</details>
## Giới thiệu

Dự án mô phỏng một hệ thống Kubernetes hoàn chỉnh gồm 2 node (master + worker), triển khai bằng kubeadm, có khả năng **tự động mở rộng (auto-scaling)** theo tải CPU thực tế và **tự phục hồi (self-healing)** khi node gặp sự cố. Toàn bộ quy trình build & deploy được tự động hóa qua GitLab CI/CD, truy cập qua domain riêng với HTTPS, và giám sát real-time bằng Prometheus + Grafana.

## Kiến trúc tổng quan

```
Người dùng
   │
   ▼
HTTPS (nginx-ingress + cert-manager)
   │
   ▼
Service (ClusterIP)
   │
   ▼
Pod (Flask app) ←── HPA tự động scale theo % CPU
   │
   ▼
Prometheus (scrape metrics) ──▶ Grafana (dashboard giám sát)

GitLab CI/CD: push code → build Docker image → push registry → deploy tự động lên cluster
```
## Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Container Orchestration | Kubernetes (kubeadm), Calico (CNI) |
| Containerization | Docker |
| Package Manager | Helm |
| Reverse Proxy / Ingress | nginx-ingress |
| HTTPS tự động | cert-manager + Let's Encrypt |
| Domain / DNS | Domain riêng, trỏ A record |
| Giám sát | Prometheus, Grafana, kube-state-metrics, node-exporter |
| CI/CD | GitLab CI/CD |
| Load Testing | k6 |
| Ứng dụng demo | Python (Flask) |

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

## Tác giả

**Doan Minh Hiep**

- GitHub: [@minhhiep05](https://github.com/minhhiep05)
- GitLab: [@doanhiep169](https://gitlab.com/doanhiep169)
- Email: doanhiep169@gmail.com

