[![pipeline status](https://gitlab.com/doanhiep169/loadtest-api/badges/main/pipeline.svg)](https://gitlab.com/doanhiep169/loadtest-api/-/commits/main)

<details>
<summary><strong>📑 Mục lục (bấm để xem)</strong></summary>

- 📌 [Giới thiệu](#gioi-thieu)
- 🏗️ [Kiến trúc tổng quan](#kien-truc-tong-quan)
- 🛠️ [Công nghệ sử dụng](#cong-nghe-su-dung)
- 🎬 [Demo Video](#demo-video)
- ✅ [1. Cluster 2 node Ready](#buoc-1)
- 🔒 [2. HTTPS Certificate hợp lệ](#buoc-2)
- 📈 [3. HPA tự động scale Pod theo tải CPU](#buoc-3)
- 🚀 [4. GitLab CI/CD Pipeline chạy thành công](#buoc-4)
- 📊 [5. Giám sát bằng Grafana + Prometheus](#buoc-5)
- 🌐 [6. Giao diện Web Demo trực tiếp](#buoc-6)
- 🔄 [7. Self-healing khi node gặp sự cố](#buoc-7)
- 🔮 [Định hướng cải thiện nếu triển khai Production](#dinh-huong-cai-thien)
- 👤 [Tác giả](#tac-gia)

</details>

<h2 id="gioi-thieu">📌 Giới thiệu</h2>

Dự án mô phỏng một hệ thống Kubernetes hoàn chỉnh gồm 2 node (master + worker), triển khai bằng kubeadm, có khả năng **tự động mở rộng (auto-scaling)** theo tải CPU thực tế và **tự phục hồi (self-healing)** khi node gặp sự cố. Toàn bộ quy trình build & deploy được tự động hóa qua GitLab CI/CD, truy cập qua domain riêng với HTTPS và giám sát real-time bằng Prometheus + Grafana.

<h2 id="kien-truc-tong-quan">🏗️ Kiến trúc tổng quan</h2>

```mermaid
flowchart TB
    User(["👤 Users"])
    Developer(["👨‍💻 Developer"])

    subgraph K8s["☸️ Kubernetes Cluster (kubeadm — 2 nodes: Master + Worker)"]
        direction TB

        subgraph IngressLayer["🌐 Ingress Layer"]
            Ingress["NGINX Ingress Controller
            (hostPort 80/443)"]
            CertManager["cert-manager
            + Let's Encrypt"]
        end

        Service["ClusterIP Service"]

        subgraph Deployment["📦 Deployment"]
            Pod1["Flask Pod"]
            Pod2["Flask Pod"]
            Pod3["Flask Pod"]
        end

        HPA["⚖️ Horizontal Pod
        Autoscaler"]
        MetricsServer["📊 metrics-server"]

        subgraph Monitoring["📈 Monitoring Stack"]
            Prom["Prometheus"]
            Grafana["Grafana"]
        end

        Runner["🏃 GitLab Runner
        (shell executor)"]
    end

    GitLab["📁 GitLab Repository"]
    Pipeline["🔄 GitLab CI/CD
    Pipeline (.gitlab-ci.yml)"]
    Registry["🐳 Container Registry"]

    User -->|"HTTPS
    app.domain.com"| Ingress
    CertManager -.->|"cấp TLS cert"| Ingress
    Ingress --> Service
    Service --> Pod1
    Service --> Pod2
    Service --> Pod3

    MetricsServer -.->|"CPU/Memory"| HPA
    HPA -.->|"scale 1↔5"| Deployment

    Pod1 & Pod2 & Pod3 --> Prom
    Prom --> Grafana

    Developer -->|"git push"| GitLab
    GitLab -->|"trigger"| Pipeline
    Pipeline -->|"chạy job"| Runner
    Runner -->|"1. build & push"| Registry
    Runner -->|"2. kubectl set image
    (manual approve)"| Deployment
    Deployment -->|"pull image"| Registry

    classDef userStyle fill:#FFE0B2,stroke:#E65100,stroke-width:2px,color:#000,font-weight:bold
    classDef trafficStyle fill:#BBDEFB,stroke:#1565C0,stroke-width:2px,color:#000
    classDef podStyle fill:#C8E6C9,stroke:#2E7D32,stroke-width:2px,color:#000
    classDef controlStyle fill:#E1BEE7,stroke:#6A1B9A,stroke-width:2px,color:#000
    classDef monitorStyle fill:#FFF9C4,stroke:#F57F17,stroke-width:2px,color:#000
    classDef cicdStyle fill:#FFCCBC,stroke:#BF360C,stroke-width:2px,color:#000
    classDef runnerStyle fill:#F8BBD0,stroke:#AD1457,stroke-width:2px,color:#000

    class User,Developer userStyle
    class Ingress,CertManager,Service trafficStyle
    class Pod1,Pod2,Pod3 podStyle
    class HPA,MetricsServer controlStyle
    class Prom,Grafana monitorStyle
    class GitLab,Pipeline,Registry cicdStyle
    class Runner runnerStyle

    style K8s fill:#F1F8E9,stroke:#558B2F,stroke-width:3px
    style IngressLayer fill:#E3F2FD,stroke:#1976D2,stroke-width:1.5px
    style Deployment fill:#E8F5E9,stroke:#43A047,stroke-width:1.5px
    style Monitoring fill:#FFFDE7,stroke:#FBC02D,stroke-width:1.5px
```


<h2 id="cong-nghe-su-dung">🛠️ Công nghệ sử dụng</h2>

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

<h2 id="demo-video">🎬 Demo Video</h2>

- HPA Auto-scaling: https://youtu.be/vFYXPUYhfiA
- Self-healing (cordon/drain): https://youtu.be/7viwdsLyjOA

<h2 id="buoc-1">✅ 1. Cluster 2 node Ready</h2>

![Nodes Ready](nodes-ready.png.png)

<h2 id="buoc-2">🔒 2. HTTPS Certificate hợp lệ</h2>

![Certificate Ready](certificate-ready.png)

<h2 id="buoc-3">📈 3. HPA tự động scale Pod theo tải CPU</h2>

![HPA Scaling](hpa-scaling.png)

<h2 id="buoc-4">🚀 4. GitLab CI/CD Pipeline chạy thành công</h2>

![Pipeline Passed](pipeline-passed.png)

<h2 id="buoc-5">📊 5. Giám sát bằng Grafana + Prometheus</h2>

![Grafana Dashboard](grafana-dashboard.png)

<h2 id="buoc-6">🌐 6. Giao diện Web Demo trực tiếp</h2>

![Web Demo](web-demo.png)

<h2 id="buoc-7">🔄 7. Self-healing khi node gặp sự cố</h2>

Cô lập node worker (đánh dấu không nhận pod mới):

![node cordon](node-cordon.png)

Trục xuất toàn bộ pod ra khỏi worker:

![pod drain](pod-drain.png)

Khôi phục lại worker sau khi demo xong:

![node uncordon](node-uncordon.png)

<h2 id="dinh-huong-cai-thien">🔮 Định hướng cải thiện nếu triển khai Production</h2>

Dự án này được xây dựng với mục đích học tập và demo các khái niệm cốt lõi của Kubernetes (auto-scaling, self-healing, CI/CD, giám sát). Nếu triển khai cho môi trường production thực tế, tôi nhận thấy cần bổ sung thêm:

- **High Availability cho Control Plane**: hiện tại chỉ có 1 master node — cần multi-master để tránh single point of failure
- **Backup & Disaster Recovery**: thêm cơ chế backup định kỳ cho etcd
- **Tối ưu Resource Requests/Limits**: điều chỉnh lại giới hạn CPU/Memory sát với mức sử dụng thực tế đo được qua Grafana, tránh lãng phí hoặc thiếu hụt tài nguyên
- **Network Policy & RBAC**: giới hạn traffic giữa các namespace, phân quyền truy cập chi tiết hơn
- **Secret Management**: dùng Vault hoặc Sealed Secrets thay vì Kubernetes Secret mặc định
- **Multi-node Worker**: mở rộng thêm worker node để chịu tải cao hơn và tránh phụ thuộc vào 1 node duy nhất

<h2 id="tac-gia">👤 Tác giả</h2>

**Doan Minh Hiep**

- GitHub: [@minhhiep05](https://github.com/minhhiep05)
- GitLab: [@doanhiep169](https://gitlab.com/doanhiep169)
- Email: doanhiep169@gmail.com
