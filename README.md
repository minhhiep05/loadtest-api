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
graph TD
    %% Định nghĩa các style màu sắc chuyên nghiệp
    classDef userStyle fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:#fff;
    classDef ingressStyle fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff;
    classDef k8sStyle fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff;
    classDef monitorStyle fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#fff;
    classDef cicdStyle fill:#ec4899,stroke:#be185d,stroke-width:2px,color:#fff;

    %% Các thành phần trong hệ thống
    User([👤 User / Client]):::userStyle
    
    subgraph Ingress Layer ["🌐 Ingress & Security Layer"]
        Cert[Cert-Manager <br/> Let's Encrypt HTTPS]:::ingressStyle
        Ingress[Nginx Ingress Controller]:::ingressStyle
    end

    subgraph K8sCluster ["☸️ Kubernetes Cluster (2 Nodes)"]
        Service[ClusterIP Service]:::k8sStyle
        Pod1[Flask App Pod 1]:::k8sStyle
        Pod2[Flask App Pod 2 ...]:::k8sStyle
        HPA[Horizontal Pod Autoscaler <br/> CPU Utilization > Threshold]:::k8sStyle
    end

    subgraph Monitoring ["📊 Observability Layer"]
        Prometheus[Prometheus <br/> Scrape Metrics]:::monitorStyle
        Grafana[Grafana Dashboard]:::monitorStyle
    end

    subgraph CICD ["🚀 Automation Pipeline"]
        GitLab[GitLab CI/CD]:::cicdStyle
        Registry[(Container Registry)]:::cicdStyle
    end

    %% Luồng đi của dữ liệu và request
    User -->|HTTPS Request| Cert
    Cert --> Ingress
    Ingress -->|Route Traffic| Service
    Service --> Pod1 & Pod2
    
    %% Mối quan hệ HPA và Pod
    HPA -.->|Auto-scale pods| Pod1
    HPA -.->|Auto-scale pods| Pod2

    %% Luồng Monitoring
    Prometheus -->|Collects metrics| Pod1 & Pod2
    Prometheus --> Grafana

    %% Luồng CI/CD
    GitLab -->|Build & Push| Registry
    Registry -->|Deploy updates| K8sCluster

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
