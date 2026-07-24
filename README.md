[![pipeline status](https://gitlab.com/doanhiep169/loadtest-api/badges/main/pipeline.svg)](https://gitlab.com/doanhiep169/loadtest-api/-/commits/main)

<details>
<summary><strong>📑 Table of Contents (click to expand)</strong></summary>

- 📌 [Introduction](#introduction)
- 🏗️ [Architecture Overview](#architecture-overview)
- 🛠️ [Technologies Used](#technologies-used)
- 🎬 [Demo Videos](#demo-videos)
- ✅ [1. 2-Node Cluster Ready](#step-1)
- 🔒 [2. Valid HTTPS Certificate](#step-2)
- 📈 [3. HPA Auto-scaling Pods based on CPU Load](#step-3)
- 🚀 [4. Successful GitLab CI/CD Pipeline](#step-4)
- 📊 [5. Monitoring with Grafana + Prometheus](#step-5)
- 🌐 [6. Live Web Demo Interface](#step-6)
- 🔄 [7. Self-healing on Node Failure](#step-7)
- 🔮 [Future Production Improvements](#future-production-improvements)
- 👤 [Author](#author)

</details>

<h2 id="introduction">📌 Introduction</h2>

This project models a complete 2-node Kubernetes cluster (master + worker) deployed using kubeadm. It features **auto-scaling** based on real-time CPU load and **self-healing** capabilities in case of node failures. The entire build & deploy workflow is automated via a GitLab CI/CD pipeline, accessible through a custom domain with HTTPS, and monitored in real-time using Prometheus + Grafana.

<h2 id="architecture-overview">🏗️ Architecture Overview</h2>

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
    CertManager -.->|"issues TLS cert"| Ingress
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
    Pipeline -->|"runs job"| Runner
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


<h2 id="technologies-used">🛠️ Technologies Used</h2>

| Component | Technology |
|---|---|
| Container Orchestration | Kubernetes (kubeadm), Calico (CNI) |
| Containerization | Docker |
| Package Manager | Helm |
| Reverse Proxy / Ingress | nginx-ingress |
| Automatic HTTPS | cert-manager + Let's Encrypt |
| Domain / DNS | Custom Domain, A record routing |
| Monitoring | Prometheus, Grafana, kube-state-metrics, node-exporter |
| CI/CD | GitLab CI/CD |
| Load Testing | k6 |
| Demo Application | Python (Flask) |

<h2 id="demo-videos">🎬 Demo Videos</h2>

- HPA Auto-scaling: https://youtu.be/vFYXPUYhfiA
- Self-healing (cordon/drain): https://youtu.be/7viwdsLyjOA

<h2 id="step-1">✅ 1. 2-Node Cluster Ready</h2>

![Nodes Ready](nodes-ready.png.png)

<h2 id="step-2">🔒 2. Valid HTTPS Certificate</h2>

![Certificate Ready](certificate-ready.png)

<h2 id="step-3">📈 3. HPA Auto-scaling Pods based on CPU Load</h2>

![HPA Scaling](hpa-scaling.png)

<h2 id="step-4">🚀 4. Successful GitLab CI/CD Pipeline</h2>

![Pipeline Passed](pipeline-passed.png)

<h2 id="step-5">📊 5. Monitoring with Grafana + Prometheus</h2>

![Grafana Dashboard](grafana-dashboard.png)

<h2 id="step-6">🌐 6. Live Web Demo Interface</h2>

![Web Demo](web-demo.png)

<h2 id="step-7">🔄 7. Self-healing on Node Failure</h2>

Isolate the worker node (marking it as unschedulable):

![node cordon](node-cordon.png)

Evict all pods from the worker node:

![pod drain](pod-drain.png)

Restore the worker node after the demo:

![node uncordon](node-uncordon.png)

<h2 id="future-production-improvements">🔮 Future Production Improvements</h2>

This project was built for educational and demonstration purposes to showcase the core concepts of Kubernetes (auto-scaling, self-healing, CI/CD, monitoring). If deploying to a production environment, I recognize the need to implement:

- **Control Plane High Availability**: Currently, there is only 1 master node — a multi-master setup is required to avoid a single point of failure.
- **Backup & Disaster Recovery**: Implement periodic backups for etcd.
- **Optimize Resource Requests/Limits**: Adjust CPU/Memory limits closer to actual usage measured via Grafana to avoid resource waste or shortages.
- **Network Policy & RBAC**: Restrict traffic between namespaces and enforce fine-grained access control.
- **Secret Management**: Utilize Vault or Sealed Secrets instead of the default Kubernetes Secrets.
- **Multi-node Worker**: Scale out with more worker nodes to handle higher loads and avoid dependency on a single node.

<h2 id="author">👤 Author</h2>

**Doan Minh Hiep**

- GitHub: [@minhhiep05](https://github.com/minhhiep05)
- GitLab: [@doanhiep169](https://gitlab.com/doanhiep169)
- Email: doanhiep169@gmail.com
